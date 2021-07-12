# pySwissPairer

Swiss Pairing Algorithm written in Python

## Algorithm Overview

The goal is to create pairings for each round of a tournament such that players with more points are paired against other players with more points, and no one is paired against someone they've been paired against previously.

This algorithm performs a depth-first search on a tree of potential pairings. Each node in the tree contains a pairing of two players, and a list of players that have been paired up until that point.

1. Start by creating the root `PairingTreeNode`, which has a empty pairing and an empty list of paired players.
1. Sort this `PairingTreeNode`'s list of unpaired players by points, high to low.

- If there are no players to pair, then all pairings have been found and the pairings are returned.

1. Choose the player with the highest point total.
1. Make a list of players which the chosen player has not been paired against yet (potential pairings), and sort that list by points, high to low.

- If there are no valid pairings, this is an invalid branch of the tree. Return back up the tree and try the next potential pairing.

1. Iterate over the list of potential pairings and for each pairing:
1. Create a `Pairing` between those two players, add it to a `PairingTreeNode` and add the node to the tree as a child of the current `PairingTreeNode`.
1. Move to the newly created `PairingTreeNode` and recurse to step 2 to find that node's children. This makes the search depth-first.

Byes ares supported by adding a dummy 'bye' `Player` object to the list of players

## General Usage

A simple example can be found in `SwissPairingsTest.py`. Printing standings and pairings

1. Create a `Tournament` object
1. Set the tournament's name with `Tournament.setName()`
1. Set the number of rounds with `Tournament.setMaxRounds()`
1. Add players with `Tournament.addPlayer()`
1. Call `Tournament.addRound()` to add a round to the tournament
1. Call `Tournament.pairRound()` to pair all the players in that round
1. For each `Pairing`, call `Pairing.reportMatch()`
1. When all matches have been reported, call the `Tournament.commitRound()`
1. Loop back to step 2 until the tournament is done

## Shortcomings

- Players cannot be added or removed once the tournament starts.
- Tiebreaker metrics are not calculated (opponent match win percentage, game win percentage, etc.)

## Object Overview

### Tournament

The `Tournament` class encapsulates all data necessary for a tournament. It contains

- The name of the tournament
- The number of rounds for this tournament
- A list of `Round` objects
- A list of `Player` objects

### Round

The `Round` class contains

- A list of Player UUIDs which are participating in this round
- A list of `Pairing` objects describing the pairings for this round
- A boolean indicating this round's data has been committed to the Player objects
- The round number

### Pairing

The `Pairing` class contains

- Two `Player` objects which are paired together
- A boolean indicating if this match data was reported yet
- The number of wins for each player and the number of draws

### Player

The `Player` class contains

- A UUID
- The player's name
- The number of match wins, losses, and draws
- A list of player UUIDs which this player has already been paired against
- A boolean indicating whether or not this player is a bye

## References

- [Scorekeeping By Hand](https://web.archive.org/web/20170411120229/http://wiki.magicjudges.org/en/w/Scorekeeping_By_Hand)
- [How does the Swiss pairing system work (programmatically)?](https://www.reddit.com/r/magicTCG/comments/34kk0p/request_how_does_the_swiss_pairing_system_work/cqvmuym/)
- [Magic: the Gathering Tournament Rules](https://media.wpn.wizards.com/attachements/mtg_mtr_23apr21_en_0.pdf)

---

## Getting Started

1. Install Python 3

```
# Create virtual environment
python -m venv env
. ./env/Scripts/activate

# Install packages
pip install -r requirements.txt

# Run local test
python SwissPairingsTest.py
```

---

## Deploying

- This app uses the SAM CLI to package the application as a Lambda function

```
sam build --use-container
sam deploy --profile terraform-dev --region us-east-1 --stack-name swiss-pair-app-api --s3-bucket 924586450630-artifacts --s3-prefix swiss-pair-app-api
```

- [Git bash will not resolve “sam” command](https://stackoverflow.com/questions/62986561/git-bash-will-not-resolve-sam-command)
