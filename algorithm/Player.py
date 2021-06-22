import uuid
from typing import List
import json

from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class Player:
    def __init__(self, name: str, isBye: bool) -> None:
        self.mUuid: int = uuid.uuid4().int
        self.mName: str = name
        self.mMatchWins: int = 0
        self.mMatchLosses: int = 0
        self.mMatchDraws: int = 0

        self.mPlayedAgainst: List[int] = []
        self.mIsBye: bool = isBye

    # Win modifiers

    def addWin(self, other: "Player") -> None:
        self.mMatchWins = self.mMatchWins + 1
        if other.mUuid not in self.mPlayedAgainst:
            self.mPlayedAgainst.append(other.mUuid)

    def addDraw(self, other: "Player") -> None:
        self.mMatchDraws = self.mMatchDraws + 1
        if other.mUuid not in self.mPlayedAgainst:
            self.mPlayedAgainst.append(other.mUuid)

    def addLoss(self, other: "Player") -> None:
        self.mMatchLosses = self.mMatchLosses + 1
        if other.mUuid not in self.mPlayedAgainst:
            self.mPlayedAgainst.append(other.mUuid)

    def removeWin(self, other: "Player") -> None:
        self.mMatchWins = self.mMatchWins - 1
        if other.mUuid in self.mPlayedAgainst:
            self.mPlayedAgainst.remove(other.mUuid)

    def removeDraw(self, other: "Player") -> None:
        self.mMatchDraws = self.mMatchDraws - 1
        if other.mUuid in self.mPlayedAgainst:
            self.mPlayedAgainst.remove(other.mUuid)

    def removeLoss(self, other: "Player") -> None:
        self.mMatchLosses = self.mMatchLosses - 1
        if other.mUuid in self.mPlayedAgainst:
            self.mPlayedAgainst.remove(other.mUuid)

    # Getters

    def getPoints(self) -> int:
        return (self.mMatchWins * 3) + self.mMatchDraws

    def canPairAgainst(self, other: "Player") -> None:
        return (self.mUuid != other.mUuid) and (
            other.mUuid not in self.mPlayedAgainst
        )

    def isBye(self) -> bool:
        return self.mIsBye

    def getName(self) -> str:
        return self.mName

    def getStandingsString(self) -> str:
        return "{} [{}-{}-{}]".format(
            self.mName, self.mMatchWins, self.mMatchLosses, self.mMatchDraws
        )

    def __str__(self) -> str:
        return json.dumps(self.__dict__, cls=pySwissJsonEncoder, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def setName(self, name: str) -> None:
        self.mName = name

    def getId(self) -> int:
        return self.mUuid

    # Rich comparison methods

    def __lt__(self, other: "Player") -> bool:
        return self.getPoints() < other.getPoints()

    def __le__(self, other: "Player") -> bool:
        return self.getPoints() <= other.getPoints()

    def __ge__(self, other: "Player") -> bool:
        return self.getPoints() >= other.getPoints()

    def __gt__(self, other: "Player") -> bool:
        return self.getPoints() > other.getPoints()

    def __eq__(self, other: "Player") -> bool:
        # Old overrided equals() compared team and name
        return self.mUuid == other.mUuid

    def __ne__(self, other: "Player") -> bool:
        return self.mUuid != other.mUuid
