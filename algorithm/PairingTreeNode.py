from typing import List
import jsonpickle

from algorithm.Player import Player
from algorithm.Pairing import Pairing


class PairingTreeNode:
    def __init__(
        self,
        parent: "PairingTreeNode",
        pairing: Pairing,
        roundNum: int,
        printGraphviz: bool = False,
    ) -> None:
        self.__Pairing: Pairing = pairing
        self.__PairedPlayers: List[Player] = []
        self.__NumPlayers: int = 0

        if pairing is not None:
            self.__Pairing = pairing
            self.__PairedPlayers.append(pairing.getPlayer_0())
            self.__PairedPlayers.append(pairing.getPlayer_1())

        # Link the parent and copy in the parent's paired players
        if parent is not None:
            self.__NumPlayers = parent.getNumPlayers()
            self.__PairedPlayers.extend(parent.getPairedPlayers())

        if printGraphviz:
            gvFile = open("gv.txt", "a")  # append mode

            graphvizStr: str = '    {}[label="'.format(
                self.getNodeLabel(roundNum)
            )
            if pairing is not None:
                graphvizStr = graphvizStr + "{} ({}) vs {} ({})".format(
                    self.__Pairing.getPlayer_0().getName(),
                    self.__Pairing.getPlayer_0().getPoints(),
                    self.__Pairing.getPlayer_1().getName(),
                    self.__Pairing.getPlayer_1().getPoints(),
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
        if self.__Pairing is not None:
            nodeHash: int = 0
            paired: Player
            for paired in self.__PairedPlayers:
                nodeHash = (nodeHash << 5) ^ paired.getId()
                nodeHash = (nodeHash << 5) ^ paired.getPoints()

            nodeHash = (nodeHash << 5) ^ self.__Pairing.getPlayer_0().getId()
            nodeHash = (
                nodeHash << 5
            ) ^ self.__Pairing.getPlayer_0().getPoints()
            nodeHash = (nodeHash << 5) ^ self.__Pairing.getPlayer_1().getId()
            nodeHash = (
                nodeHash << 5
            ) ^ self.__Pairing.getPlayer_1().getPoints()

            return "_{}".format(nodeHash)
        return "_{}".format(roundNum)

    def __str__(self) -> str:
        return jsonpickle.encode(self, indent=2)

    def __repr__(self) -> str:
        return self.__str__()

    def isNotPaired(self, player: Player) -> bool:
        return player not in self.__PairedPlayers

    def canHaveChildren(self) -> bool:
        return len(self.__PairedPlayers) != self.__NumPlayers

    def setNumPlayers(self, numPlayers: int) -> None:
        self.__NumPlayers = numPlayers

    def getPairing(self) -> Pairing:
        return self.__Pairing

    def getNumPlayers(self) -> int:
        return self.__NumPlayers

    def getPairedPlayers(self) -> int:
        return self.__PairedPlayers
