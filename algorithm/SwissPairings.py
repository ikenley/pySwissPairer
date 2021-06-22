import random
from typing import List

from algorithm.Player import Player
from algorithm.Pairing import Pairing
from algorithm.PairingTreeNode import PairingTreeNode


class SwissPairings:
    def pairRoundOne(players: List[Player]) -> List[Pairing]:
        """[summary]

        Args:
            players (List[Player]): [description]

        Returns:
            List[Pairing]: [description]
        """
        pairings: List[Pairing] = []
        # Shuffle players, then pair across the table
        random.shuffle(players)
        for i in range(int(len(players) / 2)):
            pairings.append(
                Pairing(
                    players[i],
                    players[int(i + (len(players) / 2)) % len(players)],
                )
            )
        return pairings

    def pairTree(players: List[Player]) -> List[Pairing]:
        """
        Given a list of players, use Swiss Pairing to pair them off, starting
        with the player with the most points and working down recursively.
        This does it's best to pair high ranking players with other high
        ranking players. It will not pair players on the same team against each
        other, nor will it pair players that have already played.

        Args:
            players (List[Player]): A list of players to pair

        Returns:
            List[Pairing]: A list of pairings
        """

        # Randomize the player order for pairing
        random.shuffle(players)

        # Make a root node for the search tree
        pairings: List[Pairing] = []
        root: PairingTreeNode = PairingTreeNode(None, None)
        root.setNumPlayers(len(players))

        # Recursively search for the best pairing
        SwissPairings.recursivelyFindPairings(root, players, pairings)

        return pairings

    def recursivelyFindPairings(
        parent: PairingTreeNode, players: List[Player], pairings: List[Pairing]
    ) -> bool:
        """
        For a PairingTreeNode, find all possible child pairs for the player
        with the most points who is unpaired. Then, if there are still unpaired
        players, continue recursively finding pairs for that PairingTreeNode.

        Eventually there will be no more unpaired players, i.e. it's at the
        bottom of the search tree. When it first hit bottom, that path down the
        tree is the round's pairings. Because it always pairs starting with the
        player with the most points, and picks the pair with the smallest
        points delta, the pairings should be optimal by Wizard's rules.

        Args:
            parent (PairingTreeNode): The parent node for this node. It knows
                         what players have already been paired down this branch
            players (List[Player]): All of the players in the tournament
            pairings (List[Pairing]): The pairings for the round are placed in
                         this ArrayList for returning once they are found
        Returns:
            bool: true if the search is over, false if it must continue
        """

        # Find the unpaired player with the most points
        maxPoints: int = -1
        maxPointPlayer: Player = None
        player: Player
        for player in players:
            if (
                player.getPoints() > maxPoints
                and parent.isNotPaired(player)
                and not player.isBye()
            ):
                maxPointPlayer = player
                maxPoints = player.getPoints()

        if maxPointPlayer is None:
            # Something failed horribly
            return False

        # Find all potential matches for that player
        tmpPairings: List[Pairing] = []
        for player in players:
            if player.canPairAgainst(maxPointPlayer) and parent.isNotPaired(
                player
            ):
                tmpPairings.append(Pairing(maxPointPlayer, player))
                # print(Pairing(maxPointPlayer, player))

        numPairings: int = len(tmpPairings)
        if 0 == numPairings:
            # No pairings, stop searching
            return False
        elif 1 < numPairings:
            # More than one pairing, Sort the pairings by how closely the
            # player's points match
            tmpPairings.sort()

        # Add all pairings to the search tree
        pairing: Pairing
        for pairing in tmpPairings:
            # Add the pair to the search tree
            child: PairingTreeNode = PairingTreeNode(parent, pairing)

            # Check if the search can continue
            if not child.canHaveChildren():
                # There are no more players to pair, so we're done
                # Start exiting from the recursion, adding to the list of
                # pairs at each level
                pairings.insert(0, child.getPairing())
                return True
            else:
                # If there are more players to pair, recurse and find the pairs
                if SwissPairings.recursivelyFindPairings(
                    child, players, pairings
                ):
                    # Add this pair to the pairings and keep exiting from the
                    # recursion
                    pairings.insert(0, child.getPairing())
                    return True

        # This branch of the search can't pair all players, so return false
        return False
