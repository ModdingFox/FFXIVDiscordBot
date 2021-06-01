using Dalamud.Game.Command;
using Dalamud.Plugin;
using System;
using System.Net;

using System.Threading.Tasks;
using Dalamud.Game.ClientState.Actors;
using System.Threading;
using System.Collections;

using Newtonsoft.Json;
using System.Net.Http;

namespace ClubSpectrumRadar
{
    public class Plugin : IDalamudPlugin
    {
        public string Name => "Club Spectrum Radar";

        private const string commandName = "/csRadar";

        private DalamudPluginInterface pi;
        private Configuration configuration;
        private PluginUI ui;

        public string AssemblyLocation { get => assemblyLocation; set => assemblyLocation = value; }
        private string assemblyLocation = System.Reflection.Assembly.GetExecutingAssembly().Location;

        private Task getPlayersTask;
        private CancellationTokenSource getPlayersCancellationTokenSource;

        private ArrayList playerLastSeenList = new ArrayList();

        private class playerPayloadObject
        {
            public long timeStamp;
            public ArrayList addPlayers;
            public ArrayList removePlayers;

            public playerPayloadObject()
            {
                TimeSpan t = DateTime.UtcNow - new DateTime(1970, 1, 1);
                timeStamp = (long)t.TotalSeconds;
                addPlayers = new ArrayList();
                removePlayers = new ArrayList();
            }
        }

        public void Initialize(DalamudPluginInterface pluginInterface)
        {
            this.pi = pluginInterface;

            this.configuration = this.pi.GetPluginConfig() as Configuration ?? new Configuration();
            this.configuration.Initialize(this.pi);

            this.ui = new PluginUI(this.configuration);

            this.pi.CommandManager.AddHandler(commandName, new CommandInfo(OnCommand)
            {
                HelpMessage = "Config options for the Club Spectrum Radar"
            });

            getPlayersCancellationTokenSource = new CancellationTokenSource();
            getPlayersTask = Task.Run(getPlayersTaskAction);

            this.pi.UiBuilder.OnBuildUi += DrawUI;
            this.pi.UiBuilder.OnOpenConfigUi += (sender, args) => DrawConfigUI();
        }

        public void Dispose()
        {
            this.ui.Dispose();

            getPlayersCancellationTokenSource?.Cancel();
            while (getPlayersTask != null && !getPlayersTask.IsCompleted)
            {
                Thread.Sleep(1);
            }

            getPlayersTask?.Dispose();
            getPlayersCancellationTokenSource?.Dispose();
            this.pi.CommandManager.RemoveHandler(commandName);
            this.pi.Dispose();
        }

        private void OnCommand(string command, string args)
        {
            this.ui.Visible = true;
        }

        private void DrawUI()
        {
            this.ui.Draw();
        }

        private void DrawConfigUI()
        {
            this.ui.SettingsVisible = true;
        }

        private void getPlayersTaskAction()
        {
            while (!getPlayersCancellationTokenSource.IsCancellationRequested)
            {
                if (this.configuration.RadarScanEnabled)
                {
                    var localPlayer = this.pi.ClientState.LocalPlayer;
                    if (localPlayer == null)
                    {
                        continue;
                    }

                    ArrayList foundUsers = new ArrayList();
                    playerPayloadObject playerPayload = new playerPayloadObject();

                    for (var i = 0; i < this.pi.ClientState.Actors.Length; i++)
                    {
                        var actor = this.pi.ClientState.Actors[i];
                        if (actor != null && actor.ObjectKind == ObjectKind.Player)
                        {
                            PluginLog.Information("Seen: " + actor.Name);
                            foundUsers.Add(actor.Name);
                        }
                    }

                    foreach (string currentUser in foundUsers)
                    {
                        if (!playerLastSeenList.Contains(currentUser)) { playerPayload.addPlayers.Add(currentUser); }
                    }

                    foreach (string currentUser in playerLastSeenList)
                    {
                        if (!foundUsers.Contains(currentUser)) { playerPayload.removePlayers.Add(currentUser); }
                    }

                    if (playerPayload.addPlayers.Count > 0 || playerPayload.removePlayers.Count > 0)
                    {
                        string payloadString = JsonConvert.SerializeObject(playerPayload);
                        PluginLog.Information(payloadString);

                        HttpClient http = new HttpClient();
                        HttpResponseMessage response = http.PostAsync(this.configuration.UploadTo, new StringContent(payloadString)).Result;

                        if (response.StatusCode == HttpStatusCode.OK)
                        {
                            playerLastSeenList = foundUsers;

                            PluginLog.Information(response.Content.ReadAsStringAsync().Result);
                            PluginLog.Information("Payload sent");
                        }
                        else { PluginLog.Error("Error: Could not contact the server to update list"); }
                    }
                }
                else
                {
                    Thread.Sleep(1000);
                }
                getPlayersCancellationTokenSource.Token.WaitHandle.WaitOne(1000);
            }
        }
    }
}
