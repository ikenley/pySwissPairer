from typing import List
import json

from algorithm.Pairing import Pairing
from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class Round:
    def __init__(self, roundNum: int) -> None:
        self.__PlayerIds: List[int] = []
        self.__Pairings: List[Pairing] = []
        self.__PairingsCommitted: bool = False
        self.__RoundNum = roundNum

    def __str__(self) -> str:
        return json.dumps(self.__dict__, cls=pySwissJsonEncoder, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def addPlayerId(self, playerId: int) -> None:
        self.__PlayerIds.append(playerId)

    def addPlayerIds(self, playerIds: List[int]) -> None:
        self.__PlayerIds.extend(playerIds)

    def getPlayerIds(self) -> List[int]:
        return self.__PlayerIds

    def addPairings(self, pairings: List[Pairing]) -> None:
        self.__Pairings.extend(pairings)

    def getPairing(self, idx: int) -> Pairing:
        return self.__Pairings[idx]

    def getPairings(self) -> List[Pairing]:
        return self.__Pairings

    def getRoundNum(self) -> int:
        return self.__RoundNum

    def allMatchesReported(self) -> bool:
        for pairing in self.__Pairings:
            if not pairing.isReported():
                return False
        return True

    def commitAllPairings(self) -> None:
        if not self.__PairingsCommitted:
            for pairing in self.__Pairings:
                pairing.commitMatchesToPlayers()
            self.__PairingsCommitted = True

    def uncommitAllPairings(self) -> None:
        if self.__PairingsCommitted:
            pairing: Pairing
            for pairing in self.__Pairings:
                pairing.uncommitMatchesToPlayers()
            self.__PairingsCommitted = False
