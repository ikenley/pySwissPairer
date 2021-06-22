from typing import List
import json

from algorithm.Pairing import Pairing
from algorithm.Player import Player
from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class Round:
    def __init__(self) -> None:
        self.mPlayerIds: List[int] = []
        self.mPairings: List[Pairing] = []
        self.mPairingsCommitted: bool = False

    def __str__(self) -> str:
        return json.dumps(self.__dict__, cls=pySwissJsonEncoder, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def addPlayerId(self, playerId: int) -> None:
        self.mPlayerIds.append(playerId)

    def removePlayerId(self, playerId: int) -> None:
        self.mPlayerIds.remove(playerId)

    def getPlayerId(self, idx: int) -> int:
        return self.mPlayerIds[idx]

    def addPlayerIds(self, playerIds: List[int]) -> None:
        self.mPlayerIds.extend(playerIds)

    def getPlayerIds(self) -> List[int]:
        return self.mPlayerIds

    def containsPlayerId(self, playerId: int) -> bool:
        return playerId in self.mPlayerIds

    def getPlayersSize(self) -> int:
        return len(self.mPlayerIds)

    def addPairings(self, pairings: List[Pairing]) -> None:
        self.mPairings.extend(pairings)

    def getPairing(self, idx: int) -> Pairing:
        return self.mPairings[idx]

    def getPairings(self) -> List[Pairing]:
        return self.mPairings

    def allMatchesReported(self) -> bool:
        for pairing in self.mPairings:
            if not pairing.isReported():
                return False
        return True

    def commitAllPairings(self) -> None:
        if not self.mPairingsCommitted:
            for pairing in self.mPairings:
                pairing.commitMatchesToPlayers()
            self.mPairingsCommitted = True

    def uncommitAllPairings(self, players: List[Player]) -> None:
        if self.mPairingsCommitted:
            pairing: Pairing
            for pairing in self.mPairings:
                pairing.uncommitMatchesToPlayers()

                # Replace old player objects with new ones
                players.remove(pairing.getPlayer_0())
                players.add(pairing.getPlayer_0())
                players.remove(pairing.getPlayer_1())
                players.add(pairing.getPlayer_1())

            self.mPairingsCommitted = False
