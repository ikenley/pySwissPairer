from typing import List

from algorithm.Pairing import Pairing
from algorithm.Player import Player


class Round:
    def __init__(self) -> None:
        self.mPlayers: List[Player] = []
        self.mPairings: List[Pairing] = []
        self.mPairingsCommitted: bool = False

    def __str__(self) -> str:
        return "{{\"mPlayers\": {}, \"mPairings\": {}, \"mPairingsCommitted\": {} }}" \
            .format(str(self.mPlayers), str(self.mPairings), self.mPairingsCommitted)

    def __repr__(self) -> str:
        return self.__str__()

    def addPlayer(self, player: Player) -> None:
        self.mPlayers.append(player)

    def getPlayer(self, idx: int) -> Player:
        return self.mPlayers[idx]

    def removePlayer(self, idx: int) -> None:
        self.mPlayers.pop(idx)

    def removePlayer(self, player: Player) -> None:
        self.mPlayers.remove(player)

    def containsPlayer(self, player: Player) -> bool:
        return player in self.mPlayers

    def getPlayersSize(self) -> int:
        return len(self.mPlayers)

    def getPairing(self, idx: int) -> Pairing:
        return self.mPairings[idx]

    def addPairings(self, pairings: List[Pairing]) -> None:
        self.mPairings.extend(pairings)

    def getPlayers(self) -> List[Player]:
        return self.mPlayers

    def getPairings(self) -> List[Pairing]:
        return self.mPairings

    def allMatchesReported(self) -> bool:
        for pairing in self.mPairings:
            if not pairing.isReported():
                return False
        return True

    def commitAllPairings(self) -> None:
        if False == self.mPairingsCommitted:
            for pairing in self.mPairings:
                pairing.commitMatchesToPlayers()
            self.mPairingsCommitted = True

    def uncommitAllPairings(self, players: List[Player]) -> None:
        if True == self.mPairingsCommitted:
            pairing: Pairing
            for pairing in self.mPairings:
                pairing.uncommitMatchesToPlayers()

                # Replace old player objects with new ones
                players.remove(pairing.getPlayer_0())
                players.add(pairing.getPlayer_0())
                players.remove(pairing.getPlayer_1())
                players.add(pairing.getPlayer_1())

            self.mPairingsCommitted = False
