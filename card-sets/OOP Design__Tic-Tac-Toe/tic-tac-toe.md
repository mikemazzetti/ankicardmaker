---
deck: "OOP Design::Tic-Tac-Toe"
topic: "Tic-Tac-Toe"
tags: [ankicardmaker, ood-tic-tac-toe]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Tic-Tac-Toe — OOP Design

Source of truth for the `OOP Design::Tic-Tac-Toe` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What's the core scope of a "Design Tic-Tac-Toe" OOD problem?
   **A:** An NxN board (usually 3x3) where two players alternate placing X/O; after each move, detect a win or draw; reject invalid moves (occupied cell, out-of-bounds, wrong turn, game already over).

2. **Q:** What does the Board class own?
   **A:** A 2D grid of Cell (or PieceType) values, plus methods to place a piece at a position and query the current state of any cell.

3. **Q:** Cell *(reversed — both ways)*
   **A:** A single position on the Board holding a PieceType (EMPTY by default) and its own (row, col) coordinates.

4. **Q:** What relationship does Game have with Board and Player, and why doesn't Board know about Player?
   **A:** Game composes one Board and a list of Players, coordinating whose turn it is; Board stays unaware of Player so it remains a simple, reusable grid abstraction.

5. **Q:** Why is the Strategy pattern a good fit for win detection in Tic-Tac-Toe?
   **A:** Win conditions vary (3-in-a-row on 3x3, k-in-a-row on an NxN board, diagonals-only variants); a WinningStrategy interface with checkWinner(Board, lastMove) lets you swap rules without touching Game or Board.

6. **Q:** Which design pattern fits notifying a UI/console/logger whenever a move is made or the game ends?
   **A:** Observer pattern — Game publishes state-change events to registered GameObservers instead of calling UI code directly.

7. **Q:** What's an efficient way to check for a win after each move, instead of rescanning the whole board?
   **A:** Track running sums/counts per row, column, and both diagonals; update only the row/col/diagonal touched by the last move, and check if any count reaches the winning length — O(1) per move instead of O(N^2).

8. **Q:** What must Game.makeMove(Player, row, col) validate before applying the move?
   **A:** That the game isn't already over, that it's this player's turn, and that the target cell is in bounds and currently EMPTY.

9. **Q:** Tricky edge case: what should happen if a player attempts a move after the game already has a winner?
   **A:** makeMove() should reject it (return failure or throw) rather than mutating the board further — Game must check its status before applying any move.

10. **Q:** How would you generalize the design from 3x3 Tic-Tac-Toe to an NxN board with a k-in-a-row win condition?
   **A:** Parameterize Board with size N and Game/WinningStrategy with a target k, and generalize the row/col/diagonal running counters so a win is "k of the same symbol in a line," not necessarily the full board dimension.

11. **Q:** Why keep PieceType/Symbol as an enum rather than a raw char or boolean?
   **A:** Type safety and extensibility (e.g. more than 2 symbols) plus an explicit EMPTY value that's clearer than overloading null or '\0'.

12. **Q:** Java: implement a Board with a 2D grid and a placeMark(row, col, mark) method that validates bounds and occupancy.
   **A:** <pre><code>public class Board {
    private final PieceType[][] grid;
    private final int size;

    public Board(int size) {
        this.size = size;
        this.grid = new PieceType[size][size];
        for (PieceType[] row : grid) {
            Arrays.fill(row, PieceType.EMPTY);
        }
    }

    public boolean placeMark(int row, int col, PieceType mark) {
        if (row &lt; 0 || row &gt;= size || col &lt; 0 || col &gt;= size) {
            throw new IllegalArgumentException("Cell out of bounds");
        }
        if (grid[row][col] != PieceType.EMPTY) {
            return false;
        }
        grid[row][col] = mark;
        return true;
    }

    public PieceType getCell(int row, int col) {
        return grid[row][col];
    }
}</code></pre>

13. **Q:** Python: implement a WinChecker that uses running row/column/diagonal counts to detect a win in O(1) per move.
   **A:** <pre><code>from enum import Enum

class Piece(Enum):
    EMPTY = 0
    X = 1
    O = -1

class WinChecker:
    def __init__(self, size: int) -&gt; None:
        self.size = size
        self.rows = [0] * size
        self.cols = [0] * size
        self.diag = 0
        self.anti_diag = 0

    def record_move(self, row: int, col: int, piece: Piece) -&gt; bool:
        value = piece.value
        self.rows[row] += value
        self.cols[col] += value
        if row == col:
            self.diag += value
        if row + col == self.size - 1:
            self.anti_diag += value

        target = self.size * value
        return target in (self.rows[row], self.cols[col], self.diag, self.anti_diag)</code></pre>

14. **Q:** Java: implement Game.makeMove(row, col) combining board placement, win/draw check, and turn advancement.
   **A:** <pre><code>public boolean makeMove(int row, int col) {
    if (status != GameStatus.IN_PROGRESS) {
        throw new IllegalStateException("Game already over");
    }
    Player current = players.get(currentPlayerIndex);
    if (!board.placeMark(row, col, current.getSymbol())) {
        return false;
    }
    if (checkWinner(row, col, current.getSymbol())) {
        status = GameStatus.WIN;
    } else if (isBoardFull()) {
        status = GameStatus.DRAW;
    } else {
        currentPlayerIndex = (currentPlayerIndex + 1) % players.size();
    }
    return true;
}</code></pre>

15. **Q:** Python: implement a Player dataclass and a Game class that alternates turns.
   **A:** <pre><code>from dataclasses import dataclass

@dataclass
class Player:
    name: str
    symbol: "Piece"

class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_index = 0

    def current_player(self):
        return self.players[self.current_index]

    def advance_turn(self):
        self.current_index = (self.current_index + 1) % len(self.players)</code></pre>

## Cloze cards

- {{c1::Board}}, {{c2::Cell}}, {{c3::Player}}, and {{c4::Game}} are the core classes in a Tic-Tac-Toe design.
- The {{c1::PieceType}} (or Symbol) enum typically has values {{c2::X, O, EMPTY}} representing what occupies a cell.
- A draw is declared when {{c1::the board is completely full and no win condition has been met}}.
- Game typically tracks {{c1::whose turn it is}} via a currentPlayerIndex (or similar reference), advanced only after a move is successfully applied.
