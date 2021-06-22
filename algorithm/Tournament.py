from typing import List
import json

from algorithm.Player import Player
from algorithm.Round import Round
from algorithm.SwissPairings import SwissPairings
from algorithm.Pairing import Pairing
from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class Tournament:
    def __init__(self) -> None:
        self.mName: str = ""
        self.mMaxRounds: int = 0
        self.mRounds: List[Round] = []
        self.mPlayers: List[Player] = []

    def __str__(self) -> str:
        return json.dumps(self, cls=pySwissJsonEncoder, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def setName(self, name: str) -> None:
        self.mName = name

    def setMaxRounds(self, maxRounds: int) -> None:
        self.mMaxRounds = maxRounds

    def getRounds(self) -> List[Round]:
        return self.mRounds

    def addRound(self) -> Round:
        newRound: Round = Round()
        if len(self.mRounds) > 0:
            lastRound: Round = self.mRounds[len(self.mRounds) - 1]
            newRound.addPlayerIds(lastRound.getPlayerIds())
        else:
            player: Player
            for player in self.mPlayers:
                newRound.addPlayerId(player.getId())
        self.mRounds.append(newRound)
        return newRound

    def pairRound(self) -> List[Pairing]:
        roundToPair: Round = self.mRounds[len(self.mRounds) - 1]
        if len(self.mRounds) <= 1:
            roundToPair.addPairings(
                SwissPairings.pairRoundOne(
                    self.getPlayersFromIds(roundToPair.getPlayerIds())
                )
            )
        else:
            roundToPair.addPairings(
                SwissPairings.pairTree(
                    self.getPlayersFromIds(roundToPair.getPlayerIds())
                )
            )
        return roundToPair.getPairings()

    def commitRound(self) -> None:
        roundToCommit: Round = self.mRounds[len(self.mRounds) - 1]
        roundToCommit.commitAllPairings()

    def getMaxRounds(self) -> int:
        return self.mMaxRounds

    def getName(self) -> str:
        return self.mName

    def addPlayer(self, player: Player) -> None:
        self.mPlayers.append(player)

    def getPlayersFromIds(self, playerIds: List[int]) -> List[Player]:
        playerList: List[Player] = []
        id: int
        for id in playerIds:
            player: Player
            for player in self.mPlayers:
                if id == player.getId():
                    playerList.append(player)
                    break
        return playerList
