import random
from typing import List

from algorithm.Tournament import Tournament
from algorithm.Player import Player
from algorithm.Round import Round
from algorithm.Pairing import Pairing


class SwissPairingsTest:

    def randomlyAssignWinners(pairings: List[Pairing]) -> None:
        """This simulates a round where each pairing is assigned either a winner/loser, or a draw

        Args:
            pairings (List[Pairing]): The pairings to simulate a round for
        """
        pairing: Pairing
        for pairing in pairings:
            if pairing.getPlayer_0().isBye():
                pairing.getPlayer_0().addLoss(pairing.getPlayer_1())
                pairing.getPlayer_1().addWin(pairing.getPlayer_0())
            elif pairing.getPlayer_1().isBye():
                pairing.getPlayer_0().addWin(pairing.getPlayer_1())
                pairing.getPlayer_1().addLoss(pairing.getPlayer_0())
            else:
                outcome: int = random.randint(0, 2)
                if 0 == outcome:
                    pairing.reportMatch(1, 0, 0)
                elif 1 == outcome:
                    pairing.reportMatch(0, 1, 0)
                else:
                    pairing.reportMatch(0, 0, 1)

    def printStandings(players: List[Player]) -> None:
        players.sort(reverse=True)
        print("Standings")
        print("---------")
        player: Player
        for player in players:
            print(player.getStandingsString())

    def printPairing(pairings: List[Pairing]) -> None:
        print("Pairings")
        print("--------")
        pairing: Pairing
        for pairing in pairings:
            print(pairing.getPairingString())
        print("")


if __name__ == "__main__":

    for j in range(1):

        maxRounds: int = 3

        tourney: Tournament = Tournament()
        tourney.setName("Test {}".format(j))
        tourney.setMaxRounds(maxRounds)
        tourney.addPlayer(Player("Adam   ", False))
        tourney.addPlayer(Player("Bob    ", False))
        tourney.addPlayer(Player("Charlie", False))
        tourney.addPlayer(Player("Dan    ", False))
        tourney.addPlayer(Player("Edward ", False))
        tourney.addPlayer(Player("Frank  ", False))
        tourney.addPlayer(Player("George ", False))
        tourney.addPlayer(Player("Henry  ", False))

        print("Test " + str(j))
        print("------\n")

        # For each round
        for i in range(maxRounds):
            print("Round " + str(i+1))
            print("-------\n")

            # Create and pair the round
            round: Round = tourney.addRound()
            pairings: List[Pairing] = tourney.pairRound()

            # Print the pairings
            SwissPairingsTest.printPairing(pairings)

            # Simulate the round
            SwissPairingsTest.randomlyAssignWinners(pairings)
            tourney.commitRound()

            # Print the standings after the simulated round
            SwissPairingsTest.printStandings(round.getPlayers())

            print("\n=========================================================\n")
