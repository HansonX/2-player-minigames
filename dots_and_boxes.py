class DotsAndBoxes:
    def __init__(self, p1, p2, rows, cols):
        if rows < 1 or cols < 1:
            raise ValueError("rows and cols must be >= 1.")
        self.players = [p1, p2]
        self.r, self.c = rows - 1, cols - 1
        self.horiz = [[False] * cols for _ in range(rows + 1)]
        self.vert  = [[False] * (cols + 1) for _ in range(rows)]
        self.boxes  = [[None] * cols for _ in range(rows)]
        self.scores = {p1: 0, p2: 0}
        self.turn = 1

    def _current_player(self):
        return self.players[(self.turn - 1) % 2]

    def _count_filled_boxes(self):
        filled = 0
        for i in range(self.r):
            for j in range(self.c):
                if self.boxes[i][j] is not None:
                    filled += 1
        return filled

    def gameOver(self):
        return self._count_filled_boxes() == self.r * self.c

    def _complete_boxes_from_edge(self, i, j, orient):
        curr = self._current_player()
        gained = 0
        if orient == 'h':
            if i > 0 and self.boxes[i-1][j] is None:
                if self.horiz[i-1][j] and self.vert[i-1][j] and self.vert[i-1][j+1] and self.horiz[i][j]:
                    self.boxes[i-1][j] = curr
                    self.scores[curr] += 1
                    gained += 1
            if i < self.r and self.boxes[i][j] is None:
                if self.horiz[i+1][j] and self.vert[i][j] and self.vert[i][j+1] and self.horiz[i][j]:
                    self.boxes[i][j] = curr
                    self.scores[curr] += 1
                    gained += 1
        else:
            if j > 0 and self.boxes[i][j-1] is None:
                if self.vert[i][j-1] and self.horiz[i][j-1] and self.horiz[i+1][j-1] and self.vert[i][j]:
                    self.boxes[i][j-1] = curr
                    self.scores[curr] += 1
                    gained += 1
            if j < self.c and self.boxes[i][j] is None:
                if self.vert[i][j+1] and self.horiz[i][j] and self.horiz[i+1][j] and self.vert[i][j]:
                    self.boxes[i][j] = curr
                    self.scores[curr] += 1
                    gained += 1
        return gained

    def _translate_move(self, r_in, c_in):
        max_row = self.r * 2 + 1
        max_col = self.c * 2 + 1
        if not (1 <= r_in <= max_row and 1 <= c_in <= max_col):
            raise ValueError(f"Coordinates out of range. Row must be in [1..{max_row}], Col in [1..{max_col}].")
        if r_in % 2 == 1 and c_in % 2 == 0:
            i = r_in // 2
            j = c_in // 2 - 1
            if not (0 <= i < len(self.horiz) and 0 <= j < len(self.horiz[0])):
                raise ValueError("That horizontal edge is out of bounds.")
            return ('h', i, j)
        if r_in % 2 == 0 and c_in % 2 == 1:
            i = r_in // 2 - 1
            j = c_in // 2
            if not (0 <= i < len(self.vert) and 0 <= j < len(self.vert[0])):
                raise ValueError("That vertical edge is out of bounds.")
            return ('v', i, j)
        raise ValueError("Invalid position. Choose an edge (between two dots), not a dot or box interior.")

    def move(self, r_in, c_in):
        try:
            orient, i, j = self._translate_move(r_in, c_in)
        except ValueError as e:
            print(f"[Invalid move] {e}")
            return False
        if orient == 'h':
            if self.horiz[i][j]:
                print("[Invalid move] That horizontal edge is already taken.")
                return False
            self.horiz[i][j] = True
        else:
            if self.vert[i][j]:
                print("[Invalid move] That vertical edge is already taken.")
                return False
            self.vert[i][j] = True
        gained = self._complete_boxes_from_edge(i, j, orient)
        if gained == 0:
            self.turn += 1
        return True

    def render(self):
        lines = []
        header = [" "]
        for col in range(self.c * 2 + 1):
            header.append(str(col + 1))
        lines.append(" ".join(header))
        for i in range(self.r):
            row = [str(i * 2 + 1)]
            for cc in range(self.c):
                row.append("•")
                row.append('-' if self.horiz[i][cc] else ' ')
            row.append("•")
            lines.append(" ".join(row))
            row2 = [str(i * 2 + 2)]
            for cc in range(self.c + 1):
                row2.append('|' if self.vert[i][cc] else ' ')
                if cc < self.c:
                    row2.append(self.boxes[i][cc][1] if self.boxes[i][cc] else ' ')
            lines.append(" ".join(row2))
        row = [str(self.r * 2 + 1)]
        for cc in range(self.c):
            row.append("•")
            row.append('-' if self.horiz[self.r][cc] else ' ')
        row.append("•")
        lines.append(" ".join(row))
        return "\n".join(lines)


def _prompt_move_input(max_r, max_c):
    raw = input(f"Move (row col) between 1..{max_r} and 1..{max_c} or 'q' to quit: ").strip()
    if raw.lower() in ("q", "quit", "exit"):
        return None
    parts = raw.replace(",", " ").split()
    if len(parts) != 2:
        print("[Input error] Please enter exactly two numbers: row col")
        return _prompt_move_input(max_r, max_c)
    try:
        r = int(parts[0])
        c = int(parts[1])
    except ValueError:
        print("[Input error] Row and col must be integers.")
        return _prompt_move_input(max_r, max_c)
    if not (1 <= r <= max_r and 1 <= c <= max_c):
        print(f"[Input error] Out of range. Row must be 1..{max_r}, Col 1..{max_c}.")
        return _prompt_move_input(max_r, max_c)
    return (r, c)


if __name__ == '__main__':
    game = DotsAndBoxes("p1", "p2", 4, 4)
    max_r = game.r * 2 + 1
    max_c = game.c * 2 + 1
    print("Welcome to Dots & Boxes!")
    print("Enter moves by specifying the grid coordinates (row col) printed along the edges.")
    print("Pick a coordinate that lies on an edge (between two dots), not a dot or inside a box.")
    print("You get another turn if your move completes a box. Type 'q' to quit.\n")
    while not game.gameOver():
        print(game.render())
        print()
        print(f"Scores — {game.players[0]}: {game.scores[game.players[0]]} | {game.players[1]}: {game.scores[game.players[1]]}")
        print(f"Turn {game.turn}: {game._current_player()}")
        move = _prompt_move_input(max_r, max_c)
        if move is None:
            print("\nYou quit the game.")
            break
        applied = game.move(move[0], move[1])
        if not applied:
            print()
            continue
        print()
    print(game.render())
    print()
    print(f"Final Scores: {game.players[0]} : {game.scores[game.players[0]]}, "
          f"{game.players[1]} : {game.scores[game.players[1]]}")
    total_boxes = game.r * game.c
    filled = game.scores[game.players[0]] + game.scores[game.players[1]]
    if filled == total_boxes:
        p0, p1 = game.players
        if game.scores[p0] > game.scores[p1]:
            print(f"Winner: {p0} 🏆")
        elif game.scores[p1] > game.scores[p0]:
            print(f"Winner: {p1} 🏆")
        else:
            print("It's a tie!")
