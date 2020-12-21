#! /usrbin/python
"""
CLI Driver for the CardDeck module.
"""
import argparse
import sys
from .deck import Deck, ShuffleStrategy

NUMBER_OF_CARDS = 3


def parse_arguments(args):
    help_str = (
        "2-Player card game where each player is given %d cards. The card"
        " values are then summed. The player with the higher score"
        " wins!" % (NUMBER_OF_CARDS, ))
    parser = argparse.ArgumentParser(description=help_str)
    parser.add_argument("-v",
                        "--verbose",
                        help="Enable verbose output",
                        action="store_const",
                        const=True,
                        default=False)
    parser.add_argument("-s",
                        "--shuffle-strategy",
                        help=("Shuffle strategy to be used. Valid options are"
                              " RANDOM,RIFFLE,CUT"),
                        default="RANDOM")
    parser.add_argument("-r",
                        "--shuffle-rounds",
                        help="Number of times the deck should be shuffled",
                        type=int,
                        default=1)
    return vars(parser.parse_args(args))


def play_game(args):
    deck = Deck.standard_deck()
    for _ in range(args["shuffle_rounds"]):
        try:
            deck.shuffle(ShuffleStrategy[args["shuffle_strategy"]])
        except KeyError:
            print("Invalid shuffle strategy provided.")
            sys.exit(1)
        if args["verbose"]:
            print(str(deck))
    player1_score = 0
    player2_score = 0
    print("\tPlayer 1\t\t\tPlayer 2")
    for _ in range(NUMBER_OF_CARDS):
        player1_card = deck.pop()
        player2_card = deck.pop()
        player1_score += player1_card.get_value()
        player2_score += player2_card.get_value()
        print("\t%s (%d)\t\t\t\t%s (%d)" %
              (str(player1_card), player1_card.get_value(), str(player2_card),
               player2_card.get_value()))
    print("TOTAL:      %d\t\t\t\t    %d" % (
        player1_score,
        player2_score,
    ))
    if player1_score == player2_score:
        print("It's a draw!")
    else:
        winning_player = "1" if player1_score > player2_score else "2"
        print("Player %s is the winner!" % (winning_player, ))


if __name__ == "__main__":
    module_args = parse_arguments(sys.argv[1:])
    play_game(module_args)
