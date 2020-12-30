import os
import time
from dataclasses import dataclass
from typing import List, Optional

infile = "input"
path = os.path.dirname(os.path.realpath(__file__))


@dataclass
class Deck:
    size: int
    s1: list[int]
    s2: list[int]


class Node:
    def __init__(self, card, n=None, p=None):
        self.value = card
        self.next = n
        self.prev = p

    def __repr__(self):
        return f"{self.value}"


@dataclass
class DeckT:
    size: int
    head: Optional[Node]
    tail: Optional[Node]

    def to_list(self):
        cards, curr = [], self.head
        while curr is not None:
            cards.append(curr.value)
            curr = curr.next
        return cards

    def add_card(self, val):
        card = Node(card=val)
        card.prev = self.tail
        if self.size == 0:
            self.tail = card
            self.head = card
        else:
            self.tail.next = card
            self.tail = card
        self.size += 1

    def take_card(self):
        card = self.head
        if self.size > 1:
            next_card = self.head.next
            next_card.prev = None
            self.head = next_card
        else:
            self.head = None
            self.tail = None
        self.size -= 1
        return card.value

    def clone(self, sz):
        head = Node(card=self.head.value)
        curr = head
        old = self.head.next
        num = 1
        while num < sz and old is not None:
            node = Node(card=old.value)
            node.prev = curr
            curr.next = node
            curr = node
            old = old.next
            num += 1
        tail = curr
        return DeckT(size=sz, head=head, tail=tail)

    def __repr__(self):
        return f"{self.to_list()}"


def parse_line(line, decks, player):
    if not line:
        return player
    if "Player 1" in line:
        return 1
    if "Player 2" in line:
        return 2
    if player == 1:
        decks[0].append(int(line))
        return 1
    if player == 2:
        decks[1].append(int(line))
        return 2


def copy(deck):
    return Deck(size=deck.size, s1=deck.s1.copy(), s2=deck.s2.copy())


def build_deck(deck):
    deck.reverse()
    head = Node(card=deck[0])
    curr = head
    for i in range(1, len(deck)):
        node = Node(card=deck[i])
        curr.next = node
        node.prev = curr
        curr = node
    tail = curr
    return DeckT(head=head, tail=tail, size=len(deck))


def make_key(d1, d2):
    return f"{d1}:{d2}"


def game(d1, d2):
    rounds = set()
    while d1.size > 0 and d2.size > 0:
        curr = make_key(d1, d2)
        if curr in rounds:
            return d1, d2
        rounds.add(curr)
        c1, c2 = d1.take_card(), d2.take_card()
        if d1.size >= c1 and d2.size >= c2:
            d1_copy, d2_copy = d1.clone(c1), d2.clone(c2)
            winner, _loser = game(d1_copy, d2_copy)
            if winner == d1_copy:
                winner = d1
            else:
                winner = d2
        else:
            if c1 > c2:
                winner = d1
            else:
                winner = d2
        if winner == d1:
            d1.add_card(c1)
            d1.add_card(c2)
        else:
            d2.add_card(c2)
            d2.add_card(c1)
    if d1.size == 0:
        return d2, d1
    return d1, d2


def calculate_winner(d):
    cards = []
    while len(d.s1) > 0:
        cards.append(d.s1.pop())
    while len(d.s2) > 0:
        d.s1.append(d.s2.pop())
    while len(d.s1) > 0:
        cards.append(d.s1.pop())
    print("deck 1")
    result, p = 0, 1
    while len(cards) > 0:
        result += cards.pop() * p
        p += 1
    return result


def part_2(d1, d2):
    deck_1 = build_deck(d1)
    deck_2 = build_deck(d2)
    winner, loser = game(deck_1, deck_2)
    result = 0
    p = 1
    cards = winner.to_list()
    while len(cards) > 0:
        result += cards.pop() * p
        p += 1
    return result
    # print(calculate_winner(winner))


def part_1(d1, d2):
    while d1.size != 0 and d2.size != 0:
        c1 = d1.s1.pop()
        c2 = d2.s1.pop()
        if c1 > c2:
            d1.s2.append(c1)
            d1.s2.append(c2)
            d1.size += 1
            d2.size -= 1
        else:
            d2.s2.append(c2)
            d2.s2.append(c1)
            d2.size += 1
            d1.size -= 1
        if len(d1.s1) == 0:
            while len(d1.s2) > 0:
                d1.s1.append(d1.s2.pop())
        if len(d2.s1) == 0:
            while len(d2.s2) > 0:
                d2.s1.append(d2.s2.pop())
    cards = []
    if d1.size != 0:
        while len(d1.s1) > 0:
            cards.append(d1.s1.pop())
        while len(d1.s2) > 0:
            d1.s1.append(d1.s2.pop())
        while len(d1.s1) > 0:
            cards.append(d1.s1.pop())
        print("deck 1")
    else:
        while len(d2.s1) > 0:
            cards.append(d2.s1.pop())
        while len(d2.s2) > 0:
            d2.s1.append(d2.s2.pop())
        while len(d2.s1) > 0:
            cards.append(d2.s1.pop())
        print("deck 2")
    result, p = 0, 1
    while len(cards) > 0:
        result += cards.pop() * p
        p += 1
    return result


def main(infile=infile):
    input_file = f"{path}/resources/{infile}"
    decks = ([], [])
    player = 1
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            player = parse_line(line, decks, player)
    decks[0].reverse()
    decks[1].reverse()
    d1 = Deck(size=len(decks[0]), s1=decks[0].copy(), s2=[])
    d2 = Deck(size=len(decks[1]), s1=decks[1].copy(), s2=[])
    start = time.monotonic()
    result_1 = part_1(d1, d2)
    result_2 = part_2(decks[0], decks[1])
    end = time.monotonic()
    return result_1, result_2, end - start


def display(a1, a2, elapsed_time):
    print(f"answer 1: {a1}")
    print(f"answer 2: {a2}")
    print(f"elapsed time: {elapsed_time}")


if __name__ == '__main__':
    answer_1, answer_2, elapsed_time = main()
    display(answer_1, answer_2, elapsed_time)
