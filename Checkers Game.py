#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk

class CheckerPiece():
    def __init__(self, color, row, col, is_king = False):
        self.color = color
        self.is_king = is_king
        self.row = row
        self.col = col

class CheckerBoard():
    def __init__(self):
        self.board = self.create_initial_board()
        
    def create_initial_board(self):
        board = [[None] * 8 for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = CheckerPiece('white', row, col)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = CheckerPiece('red', row, col)
        return board
        
    def move_piece(self, piece: CheckerPiece, destination):
        startRow = piece.row
        startCol = piece.col
        endRow, endCol = destination
        self.board[startRow][startCol] = None
        self.board[endRow][endCol] = piece
        if (piece.color == 'red' and endRow == 0) or (piece.color == 'white' and endRow == 7):
            piece.is_king = True
        piece.row = endRow
        piece.col = endCol 
         # 
        
    def is_valid_move(self, piece, end): #
        rowStart = piece.row
        colStart = piece.col 
        rowEnd, colEnd = end # (x, y)
        rowDiff = rowEnd - rowStart
        colDiff = colEnd - colStart
        if self.board[rowEnd][colEnd] is None: 
            # check invalid cases first -- when abs(row_diff) != abs(col_dff) or abs(row_diff) > 2 or abs(row_diff) == 0 --> return (false, none)
            # captured case --> is abs(row_diff) == 2: --> valid_capture 
            # king logic --> if it's a king then return (True, None)
            # else: return (self.is_forward_move(piece, row_diff))
            if abs(rowDiff) != abs(colDiff) or abs(rowDiff) > 2 or rowDiff == 0:
                print("Invalid Move")
                return (False, None)
            if abs(rowDiff) == 2:
                return self.is_valid_capture(piece, end)
            if piece.is_king:
                return (True, None)
            else:
                return (self.is_forward_move(piece, rowDiff), None)
            # self.board[rowEnd][colEnd].move_piece()
        return (False, None)
            
    def is_forward_move(self, piece, rowDiff):
        if piece.color == 'white' and rowDiff > 0:
            return True
        if piece.color == 'red' and rowDiff < 0:
            return True
        return False
    
    def is_valid_capture(self, piece, end):
        rowEnd, colEnd = end 
        row_diff = rowEnd - piece.row
        
        if self.board[rowEnd][colEnd] == None:
            midptX = (piece.row + rowEnd) // 2
            midptY = (piece.col + colEnd) // 2
            if self.board[midptX][midptY] and self.board[midptX][midptY].color != piece.color:
                return (True, self.board[midptX][midptY])
            else:
                print('Cannot Jump')
                return (self.is_forward_move(piece, row_diff), self.board[midptX][midptY])
        
    def remove_piece(self, piece):
        row = piece.row 
        col = piece.col 
        self.board[row][col] = None
        
class CheckerGame():
    def __init__(self, master):
        self.master = master
        self.selectedPiece = None
        self.current_turn_color = 'white'
        self.master.title("Checkers")
        self.checkerboard = CheckerBoard()
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='blanched almond')
        self.canvas.pack()
        self.status_var = tk.StringVar()  # Variable to hold status updates
        self.status_label = tk.Label(self.master, textvariable=self.status_var, font=('Arial', 14))
        self.status_label.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.game_over = False
        self.locked = False
        self.draw_board()
        self.update_status()
    
    def draw_board(self):
        self.canvas.delete('all')
        for r in range(8):
            for c in range(8):
                x1, y1 = c * 50, r * 50
                x2, y2 = x1 + 50, y1 + 50
                fill = 'dark green' if (r + c) % 2 else 'blanched almond'
                squareOutline = ''
                if self.selectedPiece:
                    selected_piece_row = self.selectedPiece.row
                    selected_piece_col = self.selectedPiece.col
                    if r == selected_piece_row and c == selected_piece_col:
                        squareOutline = 'black'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, tags = 'square', outline = squareOutline, width = 5)
                piece = self.checkerboard.board[r][c]
                if piece:
                    self.draw_piece(piece)
                    
    def draw_piece(self, piece):
        x1, y1 = piece.col * 50 + 10, piece.row * 50 + 10
        x2, y2 = x1 + 30, y1 + 30
        self.canvas.create_oval(x1, y1, x2, y2, fill=piece.color, outline="")
        if piece.is_king:
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="*", font=("Arial", 20), fill="gold")
            
    def handle_click(self, event):
        # if game over, end
        # calculate board coord by set col, row = event.x // 50, event.y // 50
        # if self.selectedPiece != None
        # check if valid move by unpacking tuple
        # if valid, do stuff
        # else draw board again
        if self.game_over:
            return
        col, row = event.x // 50, event.y // 50
        destination = (row, col)
        print("clicked on ", destination)
        if self.selectedPiece:
            # see if the move is valid 
            is_valid, captured_piece = self.checkerboard.is_valid_move(self.selectedPiece, destination)
            if is_valid: 
                self.checkerboard.move_piece(self.selectedPiece, destination)
                if captured_piece:
                    self.checkerboard.remove_piece(captured_piece)
                else:
                    self.selectedPiece = None
                    self.switch_turns()
                self.draw_board()
                self.update_status()
                
            else:
                print("Invalid option")
                self.selectedPiece = None
                self.draw_board()
        else: 
            piece = self.checkerboard.board[row][col]
            if piece and piece.color == self.current_turn_color:
                self.selectedPiece = piece 
                self.draw_board()
            
        
    def switch_turns(self):
        self.current_turn_color = "red" if self.current_turn_color == "white" else "white"      
        
    def update_status(self):
        if self.game_over:
            self.status_var.set(f"Game over! ", self.current_turn_color, "wins!")
        else:
            self.status_var.set(f"It is {self.current_turn_color}'s turn!")
            
def main():
    root = tk.Tk()
    game = CheckerGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:




