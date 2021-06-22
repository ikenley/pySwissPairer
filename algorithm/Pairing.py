import sys
import json

from algorithm.Player import Player
from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class Pairing:
    def __init__(self, player_0: Player, player_1: Player) -> None:
        self.mPlayer_0: Player = player_0
        self.mPlayer_1: Player = player_1
        self.mReported: bool = False
        self.mPlayer_0_gameWins: int = 0
        self.mPlayer_1_gameWins: int = 0
        self.mGameDraws: int = 0

    def getPlayer_0(self) -> Player:
        return self.mPlayer_0

    def getPlayer_1(self) -> Player:
        return self.mPlayer_1

    def getDelta(self) -> int:
        if self.getPlayer_0().isBye() or self.getPlayer_1().isBye():
            return sys.maxsize

        return abs(self.getPlayer_0().getPoints() - self.getPlayer_1().getPoints())

    def getPairingString(self) -> str:
        return self.getPlayer_0().getName() + " vs " + self.getPlayer_1().getName()

    def __str__(self) -> str:
        return json.dumps(self.__dict__, cls=pySwissJsonEncoder, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def isReported(self) -> bool:
        return self.mReported

    def reportMatch(self, player_0_wins: int, player_1_wins: int, draws: int) -> None:
        self.mPlayer_0_gameWins = player_0_wins
        self.mPlayer_1_gameWins = player_1_wins
        self.mGameDraws = draws

        self.mReported = (
            self.mPlayer_0_gameWins > 0
            or self.mPlayer_1_gameWins > 0
            or self.mGameDraws > 0
        )

    def commitMatchesToPlayers(self) -> None:
        if self.mPlayer_0_gameWins > self.mPlayer_1_gameWins:
            self.getPlayer_0().addWin(self.getPlayer_1())
            self.getPlayer_1().addLoss(self.getPlayer_0())
        elif self.mPlayer_1_gameWins > self.mPlayer_0_gameWins:
            self.getPlayer_0().addLoss(self.getPlayer_1())
            self.getPlayer_1().addWin(self.getPlayer_0())
        else:
            self.getPlayer_0().addDraw(self.getPlayer_1())
            self.getPlayer_1().addDraw(self.getPlayer_0())

    def uncommitMatchesToPlayers(self) -> None:
        if self.mPlayer_0_gameWins > self.mPlayer_1_gameWins:
            self.getPlayer_0().removeWin(self.getPlayer_1())
            self.getPlayer_1().removeLoss(self.getPlayer_0())
        elif self.mPlayer_1_gameWins > self.mPlayer_0_gameWins:
            self.getPlayer_0().removeLoss(self.getPlayer_1())
            self.getPlayer_1().removeWin(self.getPlayer_0())
        else:
            self.getPlayer_0().removeDraw(self.getPlayer_1())
            self.getPlayer_1().removeDraw(self.getPlayer_0())

    def player_0_won(self) -> bool:
        return self.mReported and self.mPlayer_0_gameWins > self.mPlayer_1_gameWins

    def player_1_won(self) -> bool:
        return self.mReported and self.mPlayer_1_gameWins > self.mPlayer_0_gameWins

    def getPlayer_0_wins(self) -> int:
        return self.mPlayer_0_gameWins

    def getPlayer_1_wins(self) -> int:
        return self.mPlayer_1_gameWins

    def getDraws(self) -> int:
        return self.mGameDraws

    def __lt__(self, other: "Pairing") -> bool:
        return self.getDelta() < other.getDelta()

    def __le__(self, other: "Pairing") -> bool:
        return self.getDelta() <= other.getDelta()

    def __eq__(self, other: "Pairing") -> bool:
        return self.getDelta() == other.getDelta()

    def __ne__(self, other: "Pairing") -> bool:
        return self.getDelta() != other.getDelta()

    def __ge__(self, other: "Pairing") -> bool:
        return self.getDelta() >= other.getDelta()

    def __gt__(self, other: "Pairing") -> bool:
        return self.getDelta() > other.getDelta()
