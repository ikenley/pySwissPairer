from json import JSONEncoder
from typing import Any, Dict, List


class pySwissJsonEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        from algorithm.Player import Player
        from algorithm.Tournament import Tournament

        if isinstance(o, Tournament):
            playerDicts: List[Dict] = []
            player: Player
            for player in o.mPlayers:
                playerDicts.append(player.__dict__)
            tourneyDict: Dict = {}
            tourneyDict["mPlayers"] = playerDicts
            tourneyDict["mMaxRounds"] = o.mMaxRounds
            tourneyDict["mName"] = o.mName
            tourneyDict["mRounds"] = o.mRounds
            return tourneyDict
        if isinstance(o, Player):
            return o.getId()
        else:
            return o.__dict__
