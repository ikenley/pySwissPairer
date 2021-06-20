import random
from typing import List

from algorithm.Player import Player
from algorithm.Round import Round
from algorithm.SwissPairings import SwissPairings
from algorithm.Pairing import Pairing


class Tournament:
    def __init__(self) -> None:
        self.mName: str = ""
        self.mMaxRounds: int = 0
        self.mRounds: List[Round] = []
        self.mPlayers: List[Player] = []

    def __str__(self) -> str:
        return "{{\"mName\": {}, \"mPlayers\": {}, \"mMaxRounds\": {}, \"mRounds\": {} }}" \
            .format(self.mName, str(self.mPlayers), self.mMaxRounds, str(self.mRounds))

    def __repr__(self) -> str:
        return self.__str__()

    def setName(self, name: str) -> None:
        self.mName = name

    def setMaxRounds(self, maxRounds: int) -> None:
        self.mMaxRounds = maxRounds

    def randomizePlayers(self) -> None:
        random.shuffle(self.mPlayers)

    def getRounds(self) -> List[Round]:
        return self.mRounds

    def addRound(self) -> Round:
        newRound: Round = Round()
        if len(self.mRounds) > 0:
            lastRound: Round = self.mRounds[len(self.mRounds) - 1]
            player: Player
            for player in lastRound.getPlayers():
                newRound.addPlayer(Player(other=player))
        else:
            player: Player
            for player in self.mPlayers:
                newRound.addPlayer(Player(other=player))
        self.mRounds.append(newRound)
        return newRound

    def pairRound(self) -> List[Pairing]:
        roundToPair: Round = self.mRounds[len(self.mRounds) - 1]
        if len(self.mRounds) <= 1:
            roundToPair.addPairings(
                SwissPairings.pairRoundOne(roundToPair.getPlayers()))
        else:
            roundToPair.addPairings(
                SwissPairings.pairTree(roundToPair.getPlayers()))
        return roundToPair.getPairings()

    def commitRound(self) -> None:
        roundToCommit: Round = self.mRounds[len(self.mRounds) - 1]
        roundToCommit.commitAllPairings()

    def getRounds(self) -> List[Round]:
        return self.mRounds

    def getMaxRounds(self) -> int:
        return self.mMaxRounds

    def getName(self) -> str:
        return self.mName

    def addPlayer(self, player: Player) -> None:
        self.mPlayers.append(player)
