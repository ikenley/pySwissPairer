
import sys
from typing import List

from algorithm.Player import Player


class Pairing:

    def __init__(self, player_0: Player, player_1: Player) -> None:
        self.mPlayer_0: Player = player_0
        self.mPlayer_1: Player = player_1
        self.mReported: bool = False
        self.mPlayer_0_wins: int = 0
        self.mPlayer_1_wins: int = 0
        self.mDraws: int = 0

    def getPlayer_0(self) -> Player:
        return self.mPlayer_0

    def getPlayer_1(self) -> Player:
        return self.mPlayer_1

    def getDelta(self) -> int:
        if (self.mPlayer_0.isBye() or self.mPlayer_1.isBye()):
            return sys.maxsize

        return abs(self.mPlayer_0.getPoints() - self.mPlayer_1.getPoints())

    def getPairingString(self) -> str:
        return self.getPlayer_0().getName() + " vs " + self.getPlayer_1().getName()

    def __str__(self) -> str:
        return "{{ \"mPlayer_0\": {}, \"mPlayer_1\": {}, \"mReported\": {}, \"mPlayer_0_wins\": {}, \"mPlayer_1_wins\": {}, \"mDraws\": {} }}" \
            .format(str(self.mPlayer_0), str(self.mPlayer_1), self.mReported, self.mPlayer_0_wins, self.mPlayer_1_wins, self.mDraws)

    def __repr__(self) -> str:
        return self.__str__()

    def isReported(self) -> bool:
        return self.mReported

    def reportMatch(self, player_0_wins: int, player_1_wins: int, draws: int) -> None:
        self.mPlayer_0_wins = player_0_wins
        self.mPlayer_1_wins = player_1_wins
        self.mDraws = draws

        self.mReported = (self.mPlayer_0_wins >
                          0 or self.mPlayer_1_wins > 0 or self.mDraws > 0)

    def commitMatchesToPlayers(self) -> None:
        if (self.mPlayer_0_wins > self.mPlayer_1_wins):
            self.getPlayer_0().addWin(self.getPlayer_1())
            self.getPlayer_1().addLoss(self.getPlayer_0())
        elif (self.mPlayer_1_wins > self.mPlayer_0_wins):
            self.getPlayer_0().addLoss(self.getPlayer_1())
            self.getPlayer_1().addWin(self.getPlayer_0())
        else:
            self.getPlayer_0().addDraw(self.getPlayer_1())
            self.getPlayer_1().addDraw(self.getPlayer_0())

    def uncommitMatchesToPlayers(self) -> None:
        if (self.mPlayer_0_wins > self.mPlayer_1_wins):
            self.getPlayer_0().removeWin(self.getPlayer_1())
            self.getPlayer_1().removeLoss(self.getPlayer_0())
        elif (self.mPlayer_1_wins > self.mPlayer_0_wins):
            self.getPlayer_0().removeLoss(self.getPlayer_1())
            self.getPlayer_1().removeWin(self.getPlayer_0())
        else:
            self.getPlayer_0().removeDraw(self.getPlayer_1())
            self.getPlayer_1().removeDraw(self.getPlayer_0())

    def player_0_won(self) -> bool:
        return self.mReported and self.mPlayer_0_wins > self.mPlayer_1_wins

    def player_1_won(self) -> bool:
        return self.mReported and self.mPlayer_1_wins > self.mPlayer_0_wins

    def getPlayer_0_wins(self) -> int:
        return self.mPlayer_0_wins

    def getPlayer_1_wins(self) -> int:
        return self.mPlayer_1_wins

    def getDraws(self) -> int:
        return self.mDraws

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
