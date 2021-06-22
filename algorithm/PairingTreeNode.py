from typing import List
import json

from algorithm.Player import Player
from algorithm.Pairing import Pairing
from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class PairingTreeNode:
    def __init__(self, parent: "PairingTreeNode", pairing: Pairing) -> None:
        self.mPairing: Pairing = pairing
        self.mPairedPlayers: List[Player] = []
        self.mNumPlayers: int = 0

        if pairing is not None:
            self.mPairing = pairing
            self.mPairedPlayers.append(pairing.getPlayer_0())
            self.mPairedPlayers.append(pairing.getPlayer_1())

        # Link the parent and copy in the parent's paired players
        if parent is not None:
            self.mNumPlayers = parent.mNumPlayers
            self.mPairedPlayers.extend(parent.mPairedPlayers)

    def __str__(self) -> str:
        return json.dumps(self.__dict__, cls=pySwissJsonEncoder, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def isNotPaired(self, player: Player) -> bool:
        return player not in self.mPairedPlayers

    def canHaveChildren(self) -> bool:
        return len(self.mPairedPlayers) != self.mNumPlayers

    def setNumPlayers(self, numPlayers: int) -> None:
        self.mNumPlayers = numPlayers

    def getPairing(self) -> Pairing:
        return self.mPairing
