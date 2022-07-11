using System;
using System.Collections;

namespace ClubSpectrumRadar
{
    internal class playerPayloadObject
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
}