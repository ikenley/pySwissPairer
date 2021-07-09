import uuid
from typing import List

import jsonpickle


class Player:
    def __init__(self, name: str, isBye: bool) -> None:
        self.__Uuid: int = uuid.uuid4().int
        self.__Name: str = name
        self.__MatchWins: int = 0
        self.__MatchLosses: int = 0
        self.__MatchDraws: int = 0

        self.__PlayedAgainst: List[int] = []
        self.__IsBye: bool = isBye

    # Win modifiers

    def addWin(self, other: "Player") -> None:
        self.__MatchWins = self.__MatchWins + 1
        if other.getId() not in self.__PlayedAgainst:
            self.__PlayedAgainst.append(other.getId())

    def addDraw(self, other: "Player") -> None:
        self.__MatchDraws = self.__MatchDraws + 1
        if other.getId() not in self.__PlayedAgainst:
            self.__PlayedAgainst.append(other.getId())

    def addLoss(self, other: "Player") -> None:
        self.__MatchLosses = self.__MatchLosses + 1
        if other.getId() not in self.__PlayedAgainst:
            self.__PlayedAgainst.append(other.getId())

    def removeWin(self, other: "Player") -> None:
        self.__MatchWins = self.__MatchWins - 1
        if other.getId() in self.__PlayedAgainst:
            self.__PlayedAgainst.remove(other.getId())

    def removeDraw(self, other: "Player") -> None:
        self.__MatchDraws = self.__MatchDraws - 1
        if other.getId() in self.__PlayedAgainst:
            self.__PlayedAgainst.remove(other.getId())

    def removeLoss(self, other: "Player") -> None:
        self.__MatchLosses = self.__MatchLosses - 1
        if other.getId() in self.__PlayedAgainst:
            self.__PlayedAgainst.remove(other.getId())

    # Getters

    def getPoints(self) -> int:
        return (self.__MatchWins * 3) + self.__MatchDraws

    def canPairAgainst(self, other: "Player") -> None:
        return (self.__Uuid != other.getId()) and (
            other.getId() not in self.__PlayedAgainst
        )

    def isBye(self) -> bool:
        return self.__IsBye

    def getName(self) -> str:
        return self.__Name

    def getStandingsString(self) -> str:
        return "{} [{}-{}-{}]".format(
            self.__Name,
            self.__MatchWins,
            self.__MatchLosses,
            self.__MatchDraws,
        )

    def __str__(self) -> str:
        return jsonpickle.encode(self, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def setName(self, name: str) -> None:
        self.__Name = name

    def getId(self) -> int:
        return self.__Uuid

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
        return self.__Uuid == other.getId()

    def __ne__(self, other: "Player") -> bool:
        return self.__Uuid != other.getId()
