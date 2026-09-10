---
deck: "OOP Design::Chess"
topic: "Chess"
tags: [ankicardmaker, ood-chess]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Chess — OOP Design

Source of truth for the `OOP Design::Chess` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What's the core scope of a "Design Chess" OOD problem?
   **A:** Model an 8x8 board with the standard piece set and legal-move rules, alternate turns between two players, detect check/checkmate/stalemate, and optionally support special moves (castling, en passant, pawn promotion).

2. **Q:** Why make Piece an abstract class/interface rather than one class with a type field, and what pattern name does this correspond to?
   **A:** Each piece type has fundamentally different movement rules, so polymorphism lets each concrete subclass (Knight, Bishop, ...) implement its own getValidMoves()/canMove() instead of one giant switch — this is effectively the Strategy pattern, with the piece's own class selecting the algorithm.

3. **Q:** Which pattern fits representing a single Move, with support for undo/redo and move history?
   **A:** Command pattern — a Move object encapsulates the source/destination Square, the piece moved, any captured piece, and an undo() that restores the prior board state.

4. **Q:** Which pattern fits notifying a UI/logger when the game enters check or ends?
   **A:** Observer pattern — Game publishes events (CHECK, CHECKMATE, STALEMATE) to registered listeners rather than calling UI/log code directly.

5. **Q:** Square *(reversed — both ways)*
   **A:** A single position on the 8x8 Board, identified by (row, col) or algebraic notation like e4, optionally holding a Piece.

6. **Q:** What does Game.makeMove(Move) need to validate before applying it?
   **A:** That the move is legal for that piece type, that it's the correct player's turn, that the destination isn't occupied by the mover's own piece, and that applying it would not leave the mover's own King in check.

7. **Q:** What's the difference between checkmate and stalemate?
   **A:** Checkmate: the King is in check with no legal moves available (a loss). Stalemate: the King is NOT in check, but the player has no legal moves at all (a draw).

8. **Q:** Tricky edge case: how do you prevent a player from making a move that leaves their own King in check (e.g. moving a pinned piece)?
   **A:** Tentatively apply the move on a scratch copy of the board, then re-run check-detection for the mover's own King; if it's still (or newly) in check, reject the move as illegal before committing it.

9. **Q:** How is castling modeled, given it moves two pieces (King + Rook) in a single turn?
   **A:** As its own special Move type (or flag) that atomically updates both King and Rook positions, gated by preconditions: neither piece has moved before, the squares between them are empty, and the King doesn't pass through or land in check.

10. **Q:** How is en passant modeled, given the captured pawn isn't on the destination square?
   **A:** The Move needs an explicit "captured piece location" separate from its destination Square, set only when the precondition holds (an adjacent enemy pawn just advanced two squares on the immediately preceding turn).

11. **Q:** How is pawn promotion handled in the design?
   **A:** When a Pawn reaches the farthest rank, Game/Move triggers a replace-piece step that swaps the Pawn for a new Piece (usually Queen, or player-chosen) on that Square — often built via a PieceFactory.

12. **Q:** Java: implement an abstract Piece with getValidMoves(Board, Square), and a concrete Knight subclass.
   **A:** <pre><code>public abstract class Piece {
    protected final Color color;

    protected Piece(Color color) {
        this.color = color;
    }

    public Color getColor() { return color; }

    public abstract List&lt;Square&gt; getValidMoves(Board board, Square current);
}

public class Knight extends Piece {
    private static final int[][] OFFSETS = {
        {1, 2}, {2, 1}, {-1, 2}, {-2, 1},
        {1, -2}, {2, -1}, {-1, -2}, {-2, -1}
    };

    public Knight(Color color) { super(color); }

    @Override
    public List&lt;Square&gt; getValidMoves(Board board, Square current) {
        List&lt;Square&gt; moves = new ArrayList&lt;&gt;();
        for (int[] offset : OFFSETS) {
            int row = current.getRow() + offset[0];
            int col = current.getCol() + offset[1];
            if (board.isOnBoard(row, col)) {
                Piece occupant = board.getPieceAt(row, col);
                if (occupant == null || occupant.getColor() != color) {
                    moves.add(board.getSquare(row, col));
                }
            }
        }
        return moves;
    }
}</code></pre>

13. **Q:** Python: implement is_in_check(board, color) by scanning the opposing pieces' valid moves for the king's square.
   **A:** <pre><code>def is_in_check(board, color):
    king_square = board.find_king(color)
    opponent = Color.BLACK if color == Color.WHITE else Color.WHITE

    for square in board.squares_with_color(opponent):
        piece = board.get_piece_at(square)
        if king_square in piece.get_valid_moves(board, square):
            return True
    return False</code></pre>

14. **Q:** Java: implement a Move class encapsulating from/to/captured piece with apply() and undo().
   **A:** <pre><code>public class Move {
    private final Square from;
    private final Square to;
    private final Piece movedPiece;
    private final Piece capturedPiece;

    public Move(Square from, Square to, Piece movedPiece, Piece capturedPiece) {
        this.from = from;
        this.to = to;
        this.movedPiece = movedPiece;
        this.capturedPiece = capturedPiece;
    }

    public void apply(Board board) {
        board.setPieceAt(to, movedPiece);
        board.setPieceAt(from, null);
    }

    public void undo(Board board) {
        board.setPieceAt(from, movedPiece);
        board.setPieceAt(to, capturedPiece);
    }
}</code></pre>

15. **Q:** Python: implement a minimal Board class with an 8x8 grid, get_piece_at, set_piece_at, and is_on_board.
   **A:** <pre><code>class Board:
    def __init__(self):
        self._grid = [[None for _ in range(8)] for _ in range(8)]

    def get_piece_at(self, row, col):
        return self._grid[row][col]

    def set_piece_at(self, row, col, piece):
        self._grid[row][col] = piece

    def is_on_board(self, row, col):
        return 0 &lt;= row &lt; 8 and 0 &lt;= col &lt; 8</code></pre>

## Cloze cards

- {{c1::Board}}, {{c2::Square}}, {{c3::Piece}} (abstract), and {{c4::Game}} are core classes; concrete pieces like {{c5::King, Queen, Rook, Bishop, Knight, Pawn}} extend Piece.
- The {{c1::Color}} enum has two values, {{c2::WHITE and BLACK}}, used for both pieces and for tracking whose turn it is.
- A player is in {{c1::check}} when their King is under attack by at least one opposing piece given the current board state.
- {{c1::Checkmate}} occurs when a player is in check and has no legal move that removes the check — no move escapes, blocks, or captures the attacker.
