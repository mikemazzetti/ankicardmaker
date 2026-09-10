---
deck: "OOP Design::Snake and Ladder"
topic: "Snake and Ladder"
tags: [ankicardmaker, ood-snake-and-ladder]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Snake and Ladder — OOP Design

Source of truth for the `OOP Design::Snake and Ladder` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What's the core scope of a "Design Snake and Ladder" OOD problem?
   **A:** Model an NxN board (typically 100 cells) where players take turns rolling dice and moving; some cells are snake heads (move the player down) or ladder bottoms (move the player up); the first player to land exactly on the final cell wins.

2. **Q:** How are Snake and Ladder modeled relative to Board cells?
   **A:** Both are simple (start, end) pairs: a Snake's start > end (head to tail, moves the player down), a Ladder's start < end (bottom to top, moves the player up). Board typically merges both into one Map<Integer,Integer> of "cell -> jump destination" for O(1) lookup.

3. **Q:** What's the relationship between Board, Player, and Dice within Game?
   **A:** Game composes one Board, a list of Players (each tracking its own current position), and a Dice; Board and Dice stay unaware of Player/Game, keeping them reusable and decoupled.

4. **Q:** Which pattern fits supporting different dice configurations (a single 6-sided die, two dice, a weighted/loaded die)?
   **A:** Strategy pattern — a Dice interface with roll() lets Game accept any implementation without changing its own logic.

5. **Q:** Which pattern fits notifying observers (e.g. a console UI) of each turn's roll, move, and any snake/ladder jump?
   **A:** Observer pattern — Game publishes turn events to registered listeners after each move is applied.

6. **Q:** Snake (in Snake and Ladder) *(reversed — both ways)*
   **A:** A board element with a head cell (higher number) and a tail cell (lower number); landing on the head moves the player down to the tail.

7. **Q:** Ladder (in Snake and Ladder) *(reversed — both ways)*
   **A:** A board element with a bottom cell (lower number) and a top cell (higher number); landing on the bottom moves the player up to the top.

8. **Q:** In order, what is Game.playTurn() responsible for?
   **A:** Roll the dice for the current player, compute the tentative new position, apply the overshoot rule if needed, apply any snake/ladder jump at the landing cell, check for a win, then advance to the next player.

9. **Q:** Why store snake and ladder jumps in a single unified Map<Integer,Integer> on Board rather than two separate lists?
   **A:** A move only needs one O(1) lookup — "does my landing cell have a jump destination?" — regardless of whether it's a snake or ladder, which simplifies Game's per-turn logic.

10. **Q:** Tricky edge case: what must Board validation prevent when constructing Snakes/Ladders?
   **A:** A cell can't be both a snake head and a ladder bottom at once (an ambiguous jump), and a Snake's/Ladder's start and end cells can't be the same.

11. **Q:** Tricky edge case: should landing on a jump destination that is itself another jump's start cell cascade automatically?
   **A:** Most implementations apply only the single jump-map lookup for the landing cell (no automatic chaining), treating a board where one snake's tail sits on another snake's head as an invalid/unexpected configuration to reject at setup.

12. **Q:** Tricky edge case: how is a win detected, given the overshoot rule?
   **A:** After applying the roll (and any jump), check if the player's position equals exactly the final cell — since overshooting rolls are rejected outright, reaching the win condition always means landing exactly on it.

13. **Q:** What does Dice.roll() return, and why keep Dice as an interface rather than a concrete class Game calls directly?
   **A:** An int between 1 and the die's number of faces; keeping it an interface (Strategy) lets tests inject a deterministic/mock Dice instead of depending on real randomness.

14. **Q:** Java: implement Board with a jump-table Map<Integer,Integer> for snakes/ladders and a resolveLanding method.
   **A:** <pre><code>public class Board {
    private final int size;
    private final Map&lt;Integer, Integer&gt; jumps = new HashMap&lt;&gt;();

    public Board(int size) {
        this.size = size;
    }

    public void addSnake(int head, int tail) {
        if (head &lt;= tail) {
            throw new IllegalArgumentException("Snake head must be greater than tail");
        }
        jumps.put(head, tail);
    }

    public void addLadder(int bottom, int top) {
        if (bottom &gt;= top) {
            throw new IllegalArgumentException("Ladder bottom must be less than top");
        }
        jumps.put(bottom, top);
    }

    public int resolveLanding(int position) {
        return jumps.getOrDefault(position, position);
    }

    public int getSize() { return size; }
}</code></pre>

15. **Q:** Python: implement a Dice protocol/ABC with a SingleDie and a WeightedDie implementation.
   **A:** <pre><code>from abc import ABC, abstractmethod
import random

class Dice(ABC):
    @abstractmethod
    def roll(self) -&gt; int:
        ...

class SingleDie(Dice):
    def __init__(self, faces: int = 6) -&gt; None:
        self.faces = faces

    def roll(self) -&gt; int:
        return random.randint(1, self.faces)

class WeightedDie(Dice):
    def __init__(self, weights: dict) -&gt; None:
        self.faces = list(weights.keys())
        self.weights = list(weights.values())

    def roll(self) -&gt; int:
        return random.choices(self.faces, weights=self.weights, k=1)[0]</code></pre>

16. **Q:** Java: implement Game.playTurn() applying the roll, overshoot rule, jump resolution, and win check.
   **A:** <pre><code>public void playTurn() {
    if (winner != null) {
        throw new IllegalStateException("Game already has a winner");
    }
    Player player = players.get(currentPlayerIndex);
    int roll = dice.roll();
    int tentative = player.getPosition() + roll;

    if (tentative &lt;= board.getSize()) {
        int landing = board.resolveLanding(tentative);
        player.setPosition(landing);
        if (landing == board.getSize()) {
            winner = player;
        }
    }
    currentPlayerIndex = (currentPlayerIndex + 1) % players.size();
}</code></pre>

17. **Q:** Python: implement a Player class and a simulate_game loop that returns the winner.
   **A:** <pre><code>class Player:
    def __init__(self, name: str) -&gt; None:
        self.name = name
        self.position = 0

def simulate_game(game, max_turns: int = 1000):
    for _ in range(max_turns):
        game.play_turn()
        if game.winner is not None:
            return game.winner
    return None</code></pre>

## Cloze cards

- {{c1::Board}}, {{c2::Player}}, {{c3::Dice}}, and {{c4::Game}} are core classes, with {{c5::Snake}} and {{c6::Ladder}} modeling the board's jump cells.
- If a player's roll would move them past the final cell (e.g. position 97 + a roll of 6 on a 100-cell board), the standard rule is {{c1::the move is not applied at all — the player stays in place and must roll the exact number needed}}.
