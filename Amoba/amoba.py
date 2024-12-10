import tkinter as tk
import random
from typing import List, Optional

# Ablak létrehozása
root = tk.Tk()
root.title("Amőba játék")

# Globális változók a játékhoz
board: List[List[str]] = [["" for _ in range(3)] for _ in range(3)]  # 3x3 tábla létrehozása
current_player = "X"  # A játékos mindig 'X'
game_over = False

# Gombok tárolása (kezdetben üres, később `Button` objektumok lesznek)
buttons: List[List[Optional[tk.Button]]] = [[None for _ in range(3)] for _ in range(3)]


# Ellenőrzi, hogy van-e győztes
def check_winner() -> Optional[str]:
    global game_over
    # Sorok, oszlopok és átlók ellenőrzése
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    for col_index in range(3):
        if board[0][col_index] == board[1][col_index] == board[2][col_index] != "":
            return board[0][col_index]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    # Döntetlen ellenőrzése
    if all(board[row_index][col_index] != "" for row_index in range(3) for col_index in range(3)):
        game_over = True
        return "Draw"
    return None


# AI logika (egyszerű véletlenszerű lépés)
def ai_move():
    global game_over
    if game_over:
        return
    empty_cells = [(row_index, col_index) for row_index in range(3) for col_index in range(3) if board[row_index][col_index] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)  # Véletlenszerű üres mezőt választ
        board[row][col] = "O"
        if buttons[row][col]:  # Ellenőrzés, hogy a gomb létezik
            buttons[row][col].config(text="O", state="disabled")
        winner = check_winner()
        if winner:
            end_game(winner)


# Játék vége üzenet
def end_game(winner: str):
    global game_over
    game_over = True
    if winner == "Draw":
        result_label.config(text="Döntetlen!")
    else:
        result_label.config(text=f"{winner} nyert!")


# Gomb lenyomása a játékos részéről
def button_click(row_index: int, col_index: int):
    global current_player, game_over
    if not game_over and board[row_index][col_index] == "":
        board[row_index][col_index] = current_player
        if buttons[row_index][col_index]:  # Ellenőrzés, hogy a gomb létezik
            buttons[row_index][col_index].config(text=current_player, state="disabled")
        winner = check_winner()
        if winner:
            end_game(winner)
        else:
            # Ha nincs győztes, az AI következik
            ai_move()


# Grafikus tábla létrehozása
for row_idx in range(3):
    for col_idx in range(3):
        btn = tk.Button(root, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda r=row_idx, c=col_idx: button_click(r, c))
        btn.grid(row=row_idx, column=col_idx)
        buttons[row_idx][col_idx] = btn

# Eredmény kijelző
result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.grid(row=3, column=0, columnspan=3)

# Fő ciklus futtatása
root.mainloop()
