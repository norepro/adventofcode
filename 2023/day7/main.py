#!/usr/bin/python3

from collections import defaultdict

VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "*": 1,
}

JOKER_CARDS = "AKQJT98765432"


def get_type(hand):
    rank = defaultdict(int)
    for c in hand:
        rank[c] += 1
    match len(rank):
        case 1:
            return 6  # Five of a kind
        case 2:
            # Four of a kind or full house
            return 5 if max(rank.values()) == 4 else 4
        case 3:
            # Three of a kind or two pair
            return 3 if max(rank.values()) == 3 else 2
        case 4:
            return 1  # One pair
        case _:
            return 0  # High card


def get_type_with_jokers(hand, replace=True, max_type=-1):
    if replace:
        hand = hand.replace("J", "")
    if len(hand) == 5:
        return get_type(hand)
    for c in JOKER_CARDS:
        type = get_type_with_jokers(hand + c, False, max_type)
        max_type = max(max_type, type)
        if max_type == 6:
            break
    return max_type


def get_score(hand, with_jokers):
    # V1122334455
    value_hand = hand.replace("J", "*") if with_jokers else hand
    type = get_type_with_jokers(hand) if with_jokers else get_type(hand)
    return (
        type * 10000000000
        + VALUES[value_hand[0]] * 100000000
        + VALUES[value_hand[1]] * 1000000
        + VALUES[value_hand[2]] * 10000
        + VALUES[value_hand[3]] * 100
        + VALUES[value_hand[4]]
    )


with open("input.txt", "r") as f:
    hand_bids = []
    for line in f:
        hand, bid = line.split()
        hand_bids.append((hand, int(bid)))
hand_bids.sort(key=lambda x: get_score(x[0], False))
total_winnings = sum([(i + 1) * x[1] for i, x in enumerate(hand_bids)])
print(f"Part 1: {total_winnings}")

hand_bids.sort(key=lambda x: get_score(x[0], True))
total_winnings = sum([(i + 1) * x[1] for i, x in enumerate(hand_bids)])
print(f"Part 2: {total_winnings}")
