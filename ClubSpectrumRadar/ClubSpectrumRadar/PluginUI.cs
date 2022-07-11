using ImGuiNET;
using System;
using System.Numerics;

namespace ClubSpectrumRadar
{
    class PluginUI : IDisposable
    {
        private Configuration configuration;

        private bool visible = false;
        public bool Visible
        {
            get { return this.visible; }
            set { this.visible = value; }
        }

        private bool settingsVisible = false;
        public bool SettingsVisible
        {
            get { return this.settingsVisible; }
            set { this.settingsVisible = value; }
        }

        public PluginUI(Configuration configuration)
        {
            this.configuration = configuration;
        }

        public void Dispose()
        {

        }

        public void Draw()
        {
            DrawMainWindow();
            DrawSettingsWindow();
        }

        public void DrawMainWindow()
        {
            if (!Visible)
            {
                return;
            }

            ImGui.SetNextWindowSize(new Vector2(225, 175), ImGuiCond.Always);
            ImGui.SetNextWindowSizeConstraints(new Vector2(225, 175), new Vector2(float.MaxValue, float.MaxValue));
            if (ImGui.Begin("Club Spectrum Radar - Status", ref this.visible, ImGuiWindowFlags.NoResize | ImGuiWindowFlags.NoScrollbar | ImGuiWindowFlags.NoScrollWithMouse))
            {
                ImGui.Text("Radar Scan Enabled: " + ((this.configuration.RadarScanEnabled) ? ("Running") : ("Stopped")));
                ImGui.Text("Say Chat Scan Enabled: " + ((this.configuration.SayChatScanEnabled) ? ("Running") : ("Stopped")));
                ImGui.Text("Shout Chat Scan Enabled: " + ((this.configuration.ShoutChatScanEnabled) ? ("Running") : ("Stopped")));
                ImGui.Text("Yell Chat Scan Enabled: " + ((this.configuration.YellChatScanEnabled) ? ("Running") : ("Stopped")));
                ImGui.Text($"Upload To: {this.configuration.UploadTo}");

                ImGui.Spacing();
                ImGui.Separator();
                ImGui.Spacing();

                if (ImGui.Button("Show Settings"))
                {
                    SettingsVisible = true;
                }
            }
            ImGui.End();
        }

        public void DrawSettingsWindow()
        {
            if (!SettingsVisible)
            {
                return;
            }

            ImGui.SetNextWindowSize(new Vector2(250, 175), ImGuiCond.Always);
            ImGui.SetNextWindowSizeConstraints(new Vector2(250, 175), new Vector2(float.MaxValue, float.MaxValue));
            if (ImGui.Begin("Club Spectrum Radar - Config", ref this.settingsVisible,
                ImGuiWindowFlags.NoResize | ImGuiWindowFlags.NoScrollbar | ImGuiWindowFlags.NoScrollWithMouse))
            {
                var RadarScanEnabledValue = this.configuration.RadarScanEnabled;
                if (ImGui.Checkbox("Radar Scan", ref RadarScanEnabledValue))
                {
                    this.configuration.RadarScanEnabled = RadarScanEnabledValue;
                    this.configuration.Save();
                }

                var SayChatScanEnabledValue = this.configuration.SayChatScanEnabled;
                if (ImGui.Checkbox("Say Chat Scan", ref SayChatScanEnabledValue))
                {
                    this.configuration.SayChatScanEnabled = SayChatScanEnabledValue;
                    this.configuration.Save();
                }

                var ShoutChatScanEnabledValue = this.configuration.ShoutChatScanEnabled;
                if (ImGui.Checkbox("Shout Chat Scan", ref ShoutChatScanEnabledValue))
                {
                    this.configuration.ShoutChatScanEnabled = ShoutChatScanEnabledValue;
                    this.configuration.Save();
                }

                var YellChatScanEnabledValue = this.configuration.YellChatScanEnabled;
                if (ImGui.Checkbox("Yell Chat Scan", ref YellChatScanEnabledValue))
                {
                    this.configuration.YellChatScanEnabled = YellChatScanEnabledValue;
                    this.configuration.Save();
                }

                var UploadToValue = this.configuration.UploadTo;
                uint bufferSize = 512;
                byte[] buff = new byte[bufferSize];
                byte[] uploadOriginalBytes = System.Text.Encoding.UTF8.GetBytes(UploadToValue);
                for (int i = 0; i < bufferSize; i++) { buff[i] = 0x00; }
                for (int i = 0; i < bufferSize && i < uploadOriginalBytes.Length; i++) { buff[i] = uploadOriginalBytes[i]; }

                if (ImGui.InputText("Upload To", buff, bufferSize))
                {
                    string newData = System.Text.Encoding.UTF8.GetString(buff);
                    newData = newData.Trim('\0');
                    this.configuration.UploadTo = newData;
                    this.configuration.Save();
                }
            }
            ImGui.End();
        }
    }
}