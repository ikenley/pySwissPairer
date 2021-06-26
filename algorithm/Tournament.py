from typing import List
import jsonpickle

from algorithm.Player import Player
from algorithm.Round import Round
from algorithm.SwissPairings import SwissPairings
from algorithm.Pairing import Pairing


class Tournament:
    def __init__(self) -> None:
        self.__Name: str = ""
        self.__MaxRounds: int = 0
        self.__Rounds: List[Round] = []
        self.__Players: List[Player] = []

    def __str__(self) -> str:
        return jsonpickle.encode(self, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def setName(self, name: str) -> None:
        self.__Name = name

    def setMaxRounds(self, maxRounds: int) -> None:
        self.__MaxRounds = maxRounds

    def addRound(self) -> Round:
        newRound: Round = Round(len(self.__Rounds) + 1)
        if len(self.__Rounds) > 0:
            lastRound: Round = self.__Rounds[len(self.__Rounds) - 1]
            newRound.addPlayerIds(lastRound.getPlayerIds())
        else:
            player: Player
            for player in self.__Players:
                newRound.addPlayerId(player.getId())
        self.__Rounds.append(newRound)
        return newRound

    def pairRound(self, printGraphviz: bool = False) -> List[Pairing]:
        if len(self.__Rounds) == self.__MaxRounds:
            return None
        roundToPair: Round = self.__Rounds[len(self.__Rounds) - 1]
        if len(self.__Rounds) <= 1:
            roundToPair.addPairings(
                SwissPairings.pairRoundOne(
                    self.getPlayersFromIds(roundToPair.getPlayerIds()),
                    printGraphviz=printGraphviz,
                )
            )
        else:
            roundToPair.addPairings(
                SwissPairings.pairTree(
                    self.getPlayersFromIds(roundToPair.getPlayerIds()),
                    roundToPair.getRoundNum(),
                    printGraphviz=printGraphviz,
                )
            )
        return roundToPair.getPairings()

    def commitRound(self) -> None:
        roundToCommit: Round = self.__Rounds[len(self.__Rounds) - 1]
        if roundToCommit.allMatchesReported:
            roundToCommit.commitAllPairings()

    def uncommitRound(self) -> None:
        roundToUncommit: Round = self.__Rounds[len(self.__Rounds) - 1]
        if roundToUncommit.allMatchesReported:
            roundToUncommit.uncommitAllPairings()

    def getName(self) -> str:
        return self.__Name

    def addPlayer(self, player: Player) -> None:
        self.__Players.append(player)

    def getPlayersFromIds(self, playerIds: List[int]) -> List[Player]:
        playerList: List[Player] = []
        id: int
        for id in playerIds:
            player: Player
            for player in self.__Players:
                if id == player.getId():
                    playerList.append(player)
                    break
        return playerList
