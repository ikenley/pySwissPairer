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
        tourney.randomizePlayers()

        print("Test " + str(j))

        for i in range(maxRounds):
            print("Round " + str(i+1))

            round: Round = tourney.addRound()
            pairings: List[Pairing] = tourney.pairRound()

            SwissPairingsTest.printPairing(pairings)

            SwissPairingsTest.randomlyAssignWinners(pairings)

            tourney.commitRound()

            SwissPairingsTest.printStandings(round.getPlayers())

            print("\n=========================================================\n")

        # pairingList: List[Pairing] = []

        # for i in range(5):
        #     print("Round " + str(i+1))
        #     print("")
        #     players.sort()
        #     SwissPairingsTest.printStandings(players)
        #     print("")

        #     if 0 == i:
        #         pairingList = SwissPairings.pairRoundOne(players)
        #     else:
        #         pairingList = SwissPairings.pairTree(players)
        #     SwissPairingsTest.printPairing(pairingList)
        #     SwissPairingsTest.randomlyAssignWinners(pairingList)

        #     print("\n=========================================================\n")

        # print("Final")
        # players.sort
        # SwissPairingsTest.printStandings(players)
