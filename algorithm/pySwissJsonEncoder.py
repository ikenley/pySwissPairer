from json import JSONEncoder
from typing import Any, Dict, List


class pySwissJsonEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        from algorithm.Player import Player
        from algorithm.Tournament import Tournament

        if isinstance(o, Tournament):
            playerDicts: List[Dict] = []
            player: Player
            for player in o.__Players:
                playerDicts.append(player.__dict__)
            tourneyDict: Dict = {}
            tourneyDict["mPlayers"] = playerDicts
            tourneyDict["mMaxRounds"] = o.__MaxRounds
            tourneyDict["mName"] = o.__Name
            tourneyDict["mRounds"] = o.__Rounds
            return tourneyDict
        if isinstance(o, Player):
            return o.getId()
        else:
            return o.__dict__
