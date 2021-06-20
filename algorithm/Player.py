import uuid
from typing import List


class Player:

    def __init__(self, name: str = "", isBye: bool = False, other: "Player" = None) -> None:
        if other is not None:
            self.mUuid: int = other.mUuid
            self.mName: str = other.mName
            self.mWins: int = other.mWins
            self.mLosses: int = other.mLosses
            self.mDraws: int = other.mDraws

            self.mPlayedAgainst: List[int] = []
            self.mPlayedAgainst.extend(other.mPlayedAgainst)
            self.mIsBye: bool = other.mIsBye
        else:
            self.mUuid: int = uuid.uuid4().int
            self.mName: str = name
            self.mWins: int = 0
            self.mLosses: int = 0
            self.mDraws: int = 0

            self.mPlayedAgainst: List[int] = []
            self.mIsBye: bool = isBye

# Win modifiers

    def addWin(self, other: "Player") -> None:
        self.mWins = self.mWins + 1
        if other.mUuid not in self.mPlayedAgainst:
            self.mPlayedAgainst.append(other.mUuid)

    def addDraw(self, other: "Player") -> None:
        self.mDraws = self.mDraws + 1
        if other.mUuid not in self.mPlayedAgainst:
            self.mPlayedAgainst.append(other.mUuid)

    def addLoss(self, other: "Player") -> None:
        self.mLosses = self.mLosses + 1
        if other.mUuid not in self.mPlayedAgainst:
            self.mPlayedAgainst.append(other.mUuid)

    def removeWin(self, other: "Player") -> None:
        self.mWins = self.mWins - 1
        if other.mUuid in self.mPlayedAgainst:
            self.mPlayedAgainst.remove(other.mUuid)

    def removeDraw(self, other: "Player") -> None:
        self.mDraws = self.mDraws - 1
        if other.mUuid in self.mPlayedAgainst:
            self.mPlayedAgainst.remove(other.mUuid)

    def removeLoss(self, other: "Player") -> None:
        self.mLosses = self.mLosses - 1
        if other.mUuid in self.mPlayedAgainst:
            self.mPlayedAgainst.remove(other.mUuid)

# Getters

    def getPoints(self) -> int:
        return (self.mWins * 3) + self.mDraws

    def canPairAgainst(self, other: "Player") -> None:
        return (self.mUuid != other.mUuid) and (other.mUuid not in self.mPlayedAgainst)

    def isBye(self) -> bool:
        return self.mIsBye

    def getName(self) -> str:
        return self.mName

    def getStandingsString(self) -> str:
        return "{} [{}-{}-{}]".format(self.mName, self.mWins, self.mLosses, self.mDraws)

    def __str__(self) -> str:
        return self.mName

    def __repr__(self) -> str:
        return self.__str__()

    def setName(self, name: str) -> None:
        self.mName = name

    def getRecordString(self) -> str:
        return int(self.mWins) + "-" + int(self.mLosses) + "-" + int(self.mDraws) + "(" + self.getPoints() + ")"

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
