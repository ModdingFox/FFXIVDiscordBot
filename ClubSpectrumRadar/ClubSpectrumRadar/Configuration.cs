using Dalamud.Configuration;
using Dalamud.Plugin;
using System;

namespace ClubSpectrumRadar
{
    [Serializable]
    public class Configuration : IPluginConfiguration
    {
        public int Version { get; set; } = 0;

        public bool RadarScanEnabled { get; set; } = false;
        public bool SayChatScanEnabled { get; set; } = false;
        public bool ShoutChatScanEnabled { get; set; } = false;
        public bool YellChatScanEnabled { get; set; } = false;
        public string UploadTo { get; set; } = "";
        
        [NonSerialized]
        private DalamudPluginInterface pluginInterface;

        public void Initialize(DalamudPluginInterface pluginInterface)
        {
            this.pluginInterface = pluginInterface;
        }

        public void Save()
        {
            this.pluginInterface.SavePluginConfig(this);
        }
    }
}
