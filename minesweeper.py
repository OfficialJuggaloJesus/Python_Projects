import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGUI:
    def __init__(self, size=10, bombs=10):
        self.size = size
        self.bombs = bombs
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.hidden_board = [[0 for _ in range(size)] for _ in range(size)]
        self.generate_bombs()

        self.window = tk.Tk()
        self.window.title("Minesweeper")
        
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.create_board()

    def generate_bombs(self):
        bombs_placed = 0
        while bombs_placed < self.bombs:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.hidden_board[x][y] != -1:
                self.hidden_board[x][y] = -1
                bombs_placed += 1
                self.update_neighbors(x, y)

    def update_neighbors(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < self.size and 0 <= y + j < self.size:
                    if self.hidden_board[x + i][y + j] != -1:
                        self.hidden_board[x + i][y + j] += 1

    def create_board(self):
        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(self.window, width=2, height=1, 
                                   command=lambda x=i, y=j: self.click(x, y))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def click(self, x, y):
        if self.hidden_board[x][y] == -1:
            self.buttons[x][y].config(text="*", state=tk.DISABLED)
            messagebox.showinfo("Game Over", "You hit a bomb! Game Over.")
            self.reveal_board()
        else:
            self.board[x][y] = str(self.hidden_board[x][y])
            self.buttons[x][y].config(text=self.board[x][y], state=tk.DISABLED)
            if self.check_win():
                messagebox.showinfo("Congratulations!", "You win! Congratulations.")
                self.reveal_board()

    def check_win(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def reveal_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.hidden_board[i][j] == -1:
                    self.buttons[i][j].config(text="*", state=tk.DISABLED)
                else:
                    self.buttons[i][j].config(text=str(self.hidden_board[i][j]), state=tk.DISABLED)

    def play(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = MinesweeperGUI()
    game.play()
