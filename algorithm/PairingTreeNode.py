from typing import List
import json

from algorithm.Player import Player
from algorithm.Pairing import Pairing
from algorithm.pySwissJsonEncoder import pySwissJsonEncoder


class PairingTreeNode:
    def __init__(
        self,
        parent: "PairingTreeNode",
        pairing: Pairing,
        roundNum: int,
        printGraphviz: bool = False,
    ) -> None:
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

        if printGraphviz:
            gvFile = open("gv.txt", "a")  # append mode

            graphvizStr: str = '    {}[label="'.format(
                self.getNodeLabel(roundNum)
            )
            if pairing is not None:
                graphvizStr = graphvizStr + "{} ({}) vs {} ({})".format(
                    self.mPairing.getPlayer_0().getName(),
                    self.mPairing.getPlayer_0().getPoints(),
                    self.mPairing.getPlayer_1().getName(),
                    self.mPairing.getPlayer_1().getPoints(),
                )
            else:
                graphvizStr = graphvizStr + "Round " + str(roundNum)
            graphvizStr = graphvizStr + '"]\n'
            gvFile.write(graphvizStr)

            if parent is not None:
                gvFile.write(
                    "    {} -> {}\n".format(
                        parent.getNodeLabel(roundNum),
                        self.getNodeLabel(roundNum),
                    )
                )

            gvFile.close()

    def getNodeLabel(self, roundNum: int) -> str:
        if self.mPairing is not None:
            nodeHash: int = 0
            paired: Player
            for paired in self.mPairedPlayers:
                nodeHash = (nodeHash << 5) ^ paired.getId()
                nodeHash = (nodeHash << 5) ^ paired.getPoints()

            nodeHash = (nodeHash << 5) ^ self.mPairing.getPlayer_0().getId()
            nodeHash = (
                nodeHash << 5
            ) ^ self.mPairing.getPlayer_0().getPoints()
            nodeHash = (nodeHash << 5) ^ self.mPairing.getPlayer_1().getId()
            nodeHash = (
                nodeHash << 5
            ) ^ self.mPairing.getPlayer_1().getPoints()

            return "_{}".format(nodeHash)
        return "_{}".format(roundNum)

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
