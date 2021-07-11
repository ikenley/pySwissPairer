import random
from typing import List

from api.algorithm.Tournament import Tournament
from api.algorithm.Player import Player
from api.algorithm.Round import Round
from api.algorithm.Pairing import Pairing


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
                for _ in range(3):
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

        maxRounds: int = 3
        maxPlayers: int = 8

        tourney: Tournament = Tournament()
        tourney.setName("Test {}".format(j))
        tourney.setMaxRounds(maxRounds)
        for i in range(maxPlayers):
            tourney.addPlayer(Player("Player {}".format(i), False))

        print("Test " + str(j))
        print("------\n")

        printGraphviz: bool = True

        if printGraphviz:
            gvFile = open("gv.txt", "w")  # write mode
            gvFile.write("digraph tourney {\n\n")
            gvFile.close()

        # For each round
        for i in range(maxRounds):
            print("Round " + str(i + 1))
            print("-------\n")

            # Create and pair the round
            round: Round = tourney.addRound()
            pairings: List[Pairing] = tourney.pairRound(
                printGraphviz=printGraphviz
            )

            # Print the pairings
            SwissPairingsTest.printPairing(pairings)

            # Simulate the round
            SwissPairingsTest.randomlyAssignWinners(pairings)
            tourney.commitRound()
            tourney.uncommitRound()
            tourney.commitRound()

            # Print the standings after the simulated round
            SwissPairingsTest.printStandings(
                tourney.getPlayersFromIds(round.getPlayerIds())
            )

            print("\n======================================================\n")

        json_file = open("tourney_json.txt", "wt")
        json_file.write(str(tourney))
        json_file.close()

        if printGraphviz:
            gvFile = open("gv.txt", "a")  # append mode
            gvFile.write("}")
            gvFile.close()
