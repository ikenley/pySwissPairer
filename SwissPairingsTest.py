import random
from typing import List

from algorithm.Tournament import Tournament
from algorithm.Player import Player
from algorithm.Round import Round
from algorithm.Pairing import Pairing


class SwissPairingsTest:
    def randomlyAssignWinners(pairings: List[Pairing]) -> None:
        """This simulates a round where each pairing is assigned either a
           winner/loser, or a draw

        Args:
            pairings (List[Pairing]): The pairings to simulate a round for
        """
        pairing: Pairing
        for pairing in pairings:
            if pairing.getPlayer_0().isBye():
                pairing.reportMatch(0, 2, 0)
            elif pairing.getPlayer_1().isBye():
                pairing.reportMatch(2, 0, 0)
            else:
                win: int = 0
                loss: int = 0
                draw: int = 0
                for game in range(3):
                    outcome: int = random.randint(0, 2)
                    if 0 == outcome:
                        win = win + 1
                    elif 1 == outcome:
                        loss = loss + 1
                    else:
                        draw = draw + 1

                    if 2 == win or 2 == loss:
                        break
                pairing.reportMatch(win, loss, draw)

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

        maxRounds: int = 5

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

        gvFile = open("gv.txt", "w")  # write mode
        gvFile.write("digraph tourney {\n\n")
        gvFile.close()

        # For each round
        for i in range(maxRounds):
            print("Round " + str(i + 1))
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
            SwissPairingsTest.printStandings(
                tourney.getPlayersFromIds(round.getPlayerIds())
            )

            print("\n======================================================\n")

        # print(tourney)
        gvFile = open("gv.txt", "a")  # append mode
        gvFile.write("}")
        gvFile.close()
