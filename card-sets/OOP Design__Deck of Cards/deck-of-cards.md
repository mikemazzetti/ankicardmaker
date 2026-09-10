---
deck: "OOP Design::Deck of Cards"
topic: "Deck of Cards"
tags: [ankicardmaker, ood-deck-of-cards]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Deck of Cards — OOP Design

Source of truth for the `OOP Design::Deck of Cards` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what's the core scope of a "Design a Deck of Cards" system, before layering a specific game on top?
   **A:** Model a standard 52-card deck: represent individual cards (suit + rank), build/reset a full deck, shuffle it, and deal cards to players/hands — general enough that specific games (Poker, Blackjack, ...) can be built on top.

2. **Q:** What single responsibility does the Card class have?
   **A:** Hold an immutable pair of (Suit, Rank) and expose read-only accessors — it does not know about decks, hands, or games.

3. **Q:** Deck (class) *(reversed — both ways)*
   **A:** A collection of 52 unique Card objects, responsible for building a full set, shuffling it, and dealing cards from the top.

4. **Q:** Why make Card immutable (no setters)?
   **A:** A Card's identity never changes after creation, so immutability lets it be shared safely across Deck/Hand/discard-pile collections without defensive copying, and keeps equals()/hashCode() simple to reason about.

5. **Q:** What kind of relationship does Deck have with Card?
   **A:** Composition — Deck owns a List<Card>; cards are created once (typically by a factory) and moved between Deck/Hand/discard collections rather than duplicated.

6. **Q:** Which design pattern fits letting Deck use different shuffling algorithms (Fisher-Yates, seeded-for-tests, etc.)?
   **A:** Strategy pattern: define a ShuffleStrategy interface with shuffle(List<Card>), and inject a concrete strategy into Deck instead of hardcoding one algorithm.

7. **Q:** Which pattern fits creating a full standard 52-card deck (and variants like a 24-card Euchre deck)?
   **A:** Factory Method — a static DeckFactory.createStandardDeck() (or createEuchreDeck()) builds and returns a populated Deck, isolating construction logic from the Deck class itself.

8. **Q:** Since Ace can rank high or low depending on the game, how should card comparison be designed?
   **A:** Pull ordering out of Card into an injectable Comparator<Card> (or Strategy) supplied per game, rather than hardcoding one ranking inside Card itself.

9. **Q:** What does Deck.deal(int n) do, and what state does it mutate?
   **A:** Removes and returns the top n Cards as a List<Card>, shrinking the Deck's internal remaining-cards collection (mutates Deck state).

10. **Q:** Beyond storing cards, what should a Hand class expose?
   **A:** addCard(Card), removeCard(Card), and ways to inspect the hand (getCards(), size()) — game-specific scoring/evaluation belongs in a separate evaluator, not in Hand itself.

11. **Q:** Why does Card need a correct equals()/hashCode() implementation?
   **A:** So game logic (detecting duplicate cards dealt, matching pairs in a hand) can rely on value equality of (suit, rank) instead of reference equality.

12. **Q:** How would you extend this design to support Jokers?
   **A:** Add a JOKER rank (or a dedicated subtype) whose suit may be null/absent, and make sure comparison/equality logic and any Strategy/Comparator handle that case explicitly rather than assuming every card has a real suit.

13. **Q:** Java: implement an immutable Card class with Suit/Rank fields, value equality, and natural ordering by rank.
   **A:** <pre><code>public final class Card implements Comparable&lt;Card&gt; {
    private final Suit suit;
    private final Rank rank;

    public Card(Suit suit, Rank rank) {
        this.suit = suit;
        this.rank = rank;
    }

    public Suit getSuit() { return suit; }
    public Rank getRank() { return rank; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Card)) return false;
        Card other = (Card) o;
        return suit == other.suit &amp;&amp; rank == other.rank;
    }

    @Override
    public int hashCode() {
        return Objects.hash(suit, rank);
    }

    @Override
    public int compareTo(Card other) {
        return this.rank.compareTo(other.rank);
    }

    @Override
    public String toString() {
        return rank + " of " + suit;
    }
}</code></pre>

14. **Q:** Python: implement Suit/Rank enums, an immutable Card dataclass, and a build_standard_deck() factory.
   **A:** <pre><code>from dataclasses import dataclass
from enum import Enum
from typing import List

class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"

class Rank(Enum):
    TWO, THREE, FOUR, FIVE = 2, 3, 4, 5
    SIX, SEVEN, EIGHT, NINE = 6, 7, 8, 9
    TEN, JACK, QUEEN, KING, ACE = 10, 11, 12, 13, 14

@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

def build_standard_deck() -&gt; List[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]</code></pre>

15. **Q:** Java: implement Deck.shuffle() and Deck.deal(int n) using a backing Deque<Card>, rejecting a deal that exceeds what remains.
   **A:** <pre><code>public class Deck {
    private final Deque&lt;Card&gt; cards = new ArrayDeque&lt;&gt;();

    public Deck(List&lt;Card&gt; initialCards) {
        cards.addAll(initialCards);
    }

    public void shuffle() {
        List&lt;Card&gt; temp = new ArrayList&lt;&gt;(cards);
        Collections.shuffle(temp);
        cards.clear();
        cards.addAll(temp);
    }

    public List&lt;Card&gt; deal(int n) {
        if (n &gt; cards.size()) {
            throw new IllegalStateException("Not enough cards remaining to deal " + n);
        }
        List&lt;Card&gt; dealt = new ArrayList&lt;&gt;();
        for (int i = 0; i &lt; n; i++) {
            dealt.add(cards.pollFirst());
        }
        return dealt;
    }

    public int remaining() {
        return cards.size();
    }
}</code></pre>

16. **Q:** Python: implement a Hand class with add_card, remove_card, size, and a readable repr.
   **A:** <pre><code>from typing import List

class Hand:
    def __init__(self) -&gt; None:
        self._cards: List["Card"] = []

    def add_card(self, card: "Card") -&gt; None:
        self._cards.append(card)

    def remove_card(self, card: "Card") -&gt; None:
        self._cards.remove(card)

    def size(self) -&gt; int:
        return len(self._cards)

    def __repr__(self) -&gt; str:
        return f"Hand({self._cards!r})"</code></pre>

## Cloze cards

- A generic Deck of Cards design typically has core classes {{c1::Card}}, {{c2::Deck}}, {{c3::Hand}}, and {{c4::Player}}.
- The {{c1::Suit}} enum has exactly four constant values: {{c2::CLUBS, DIAMONDS, HEARTS, SPADES}}.
- The {{c1::Rank}} enum has 13 values, {{c2::TWO through ACE}}, and Ace's numeric value may need to flex between high (14) and low (1) depending on the game.
- If deal(n) is called with fewer than n cards remaining, the Deck should {{c1::throw an exception (e.g. IllegalStateException/EmptyDeckException) rather than silently returning a short list}}, so callers can't mistake a short hand for a full one.
