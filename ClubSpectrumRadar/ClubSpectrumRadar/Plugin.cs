using Dalamud.Game.ClientState;
using Dalamud.Game.ClientState.Objects;
using Dalamud.Game.ClientState.Objects.Enums;
using Dalamud.Game.Command;
using Dalamud.IoC;
using Dalamud.Logging;
using Dalamud.Plugin;

using Newtonsoft.Json;

using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using System.Threading;
using System.Collections;

namespace ClubSpectrumRadar
{
    public sealed class Plugin : IDalamudPlugin
    {
        public string Name => "ClubSpectrumRadar";

        private const string commandName = "/csRadar";

        private Task getPlayersTask;
        private CancellationTokenSource getPlayersCancellationTokenSource;
        private ArrayList playerLastSeenList = new ArrayList();


        private DalamudPluginInterface PluginInterface { get; init; }
        private ClientState ClientState { get; init; }
        private CommandManager CommandManager { get; init; }
        private Configuration Configuration { get; init; }
        private ObjectTable ObjectTable { get; init; }
        private PluginUI PluginUi { get; init; }

        private void getPlayersTaskAction()
        {
            while (!getPlayersCancellationTokenSource.IsCancellationRequested)
            {
                if (this.Configuration.RadarScanEnabled)
                {
                    var localPlayer = this.ClientState.LocalPlayer;
                    if (localPlayer == null)
                    {
                        continue;
                    }

                    ArrayList foundUsers = new ArrayList();
                    playerPayloadObject playerPayload = new playerPayloadObject();

                    for (var i = 0; i < this.ObjectTable.Length; i++)
                    {
                        var actor = this.ObjectTable[i];
                        if (actor != null && actor.ObjectKind == ObjectKind.Player)
                        {
                            PluginLog.Information("Seen: " + actor.Name);
                            foundUsers.Add(actor.Name.ToString());
                        }
                    }

                    foreach (string currentUser in foundUsers)
                    {
                        if (!this.playerLastSeenList.Contains(currentUser)) { playerPayload.addPlayers.Add(currentUser); }
                    }

                    foreach (string currentUser in this.playerLastSeenList)
                    {
                        if (!foundUsers.Contains(currentUser)) { playerPayload.removePlayers.Add(currentUser); }
                    }

                    if (playerPayload.addPlayers.Count > 0 || playerPayload.removePlayers.Count > 0)
                    {
                        string payloadString = JsonConvert.SerializeObject(playerPayload);
                        PluginLog.Information(payloadString);

                        HttpClient http = new HttpClient();
                        HttpResponseMessage response = http.PostAsync(this.Configuration.UploadTo, new StringContent(payloadString)).Result;

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

        public Plugin(
            [RequiredVersion("1.0")] DalamudPluginInterface pluginInterface,
            [RequiredVersion("1.0")] CommandManager commandManager,
            [RequiredVersion("1.0")] ClientState clientState,
            [RequiredVersion("1.0")] ObjectTable objectTable)
        {
            this.PluginInterface = pluginInterface;
            this.ClientState = clientState;
            this.CommandManager = commandManager;
           
            this.Configuration = this.PluginInterface.GetPluginConfig() as Configuration ?? new Configuration();
            this.Configuration.Initialize(this.PluginInterface);

            this.ObjectTable = objectTable;

            this.PluginUi = new PluginUI(this.Configuration);

            this.CommandManager.AddHandler(commandName, new CommandInfo(OnCommand) { HelpMessage = "Config options for the Club Spectrum Radar" });

            getPlayersCancellationTokenSource = new CancellationTokenSource();
            getPlayersTask = Task.Run(getPlayersTaskAction);

            this.PluginInterface.UiBuilder.Draw += DrawUI;
            this.PluginInterface.UiBuilder.OpenConfigUi += DrawConfigUI;
        }

        public void Dispose()
        {
            this.PluginUi.Dispose();
            this.CommandManager.RemoveHandler(commandName);
        }

        private void OnCommand(string command, string args) { this.PluginUi.Visible = true; }

        private void DrawUI() { this.PluginUi.Draw(); }

        private void DrawConfigUI() { this.PluginUi.SettingsVisible = true; }
    }
}
