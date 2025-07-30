import itertools
from collections import Counter

# Hand rank values: higher is better
HAND_RANKS = {
    'high_card': 0,
    'pair': 1,
    'two_pair': 2,
    'three_of_a_kind': 3,
    'straight': 4,
    'flush': 5,
    'full_house': 6,
    'four_of_a_kind': 7,
    'straight_flush': 8,
}

RANK_ORDER = '23456789TJQKA'
RANK_VALUES = {r: i for i, r in enumerate(RANK_ORDER, start=2)}

def card_to_tuple(card):
    """Convert 'As' -> ('A', 's')"""
    return card[0], card[1]

def get_rank_counts(cards):
    ranks = [card[0] for card in cards]
    return Counter(ranks)

def get_suit_counts(cards):
    suits = [card[1] for card in cards]
    return Counter(suits)

def is_flush(cards):
    suit_counts = get_suit_counts(cards)
    return any(v >= 5 for v in suit_counts.values())

def is_straight(ranks):
    unique_ranks = sorted(set(ranks), reverse=True)
    for i in range(len(unique_ranks) - 4):
        if unique_ranks[i] - unique_ranks[i + 4] == 4:
            return unique_ranks[i]
    # Special case: A-2-3-4-5 straight
    if set([14, 2, 3, 4, 5]).issubset(set(ranks)):
        return 5
    return None

def hand_score(cards):
    """
    Given 5 cards, return a score tuple:
    (rank_category, [tiebreakers])
    Higher tuples beat lower ones.
    """
    cards = [card_to_tuple(c) for c in cards]
    ranks = sorted([RANK_VALUES[r] for r, s in cards], reverse=True)
    suits = [s for r, s in cards]
    rank_counts = Counter(ranks)
    rank_freq = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))
    is_flush_hand = is_flush(cards)
    straight_high = is_straight(ranks)

    # Straight flush
    if is_flush_hand and straight_high:
        return (HAND_RANKS['straight_flush'], [straight_high])

    # Four of a kind
    if rank_freq[0][1] == 4:
        kicker = [r for r in ranks if r != rank_freq[0][0]][0]
        return (HAND_RANKS['four_of_a_kind'], [rank_freq[0][0], kicker])

    # Full house
    if rank_freq[0][1] == 3 and rank_freq[1][1] >= 2:
        return (HAND_RANKS['full_house'], [rank_freq[0][0], rank_freq[1][0]])

    # Flush
    if is_flush_hand:
        flush_cards = [RANK_VALUES[r] for r, s in cards if suits.count(s) >= 5]
        flush_cards = sorted(flush_cards, reverse=True)[:5]
        return (HAND_RANKS['flush'], flush_cards)

    # Straight
    if straight_high:
        return (HAND_RANKS['straight'], [straight_high])

    # Three of a kind
    if rank_freq[0][1] == 3:
        kickers = [r for r in ranks if r != rank_freq[0][0]][:2]
        return (HAND_RANKS['three_of_a_kind'], [rank_freq[0][0]] + kickers)

    # Two pair
    if rank_freq[0][1] == 2 and rank_freq[1][1] == 2:
        kicker = [r for r in ranks if r != rank_freq[0][0] and r != rank_freq[1][0]][0]
        top2 = sorted([rank_freq[0][0], rank_freq[1][0]], reverse=True)
        return (HAND_RANKS['two_pair'], top2 + [kicker])

    # One pair
    if rank_freq[0][1] == 2:
        kickers = [r for r in ranks if r != rank_freq[0][0]][:3]
        return (HAND_RANKS['pair'], [rank_freq[0][0]] + kickers)

    # High card
    return (HAND_RANKS['high_card'], ranks[:5])

def best_hand(seven_cards):
    best = None
    best_score = (-1, [])
    for five in itertools.combinations(seven_cards, 5):
        score = hand_score(list(five))
        if score > best_score:
            best_score = score
            best = five
    return best_score

def compare_hands(you, opponent, board):
    """
    Given your hand, opponent's hand, and 5-card board,
    return 1 (win), 0.5 (tie), or 0 (loss).
    """
    you_score = best_hand(you + board)
    opp_score = best_hand(opponent + board)
    if you_score > opp_score:
        return 1.0
    elif you_score < opp_score:
        return 0.0
    else:
        return 0.5
