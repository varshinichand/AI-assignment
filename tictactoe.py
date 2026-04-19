"""
AI-Based Tic-Tac-Toe Game using Minimax Algorithm with Alpha-Beta Pruning
A complete Tkinter GUI implementation of Tic-Tac-Toe with an unbeatable AI opponent.

Author: AI Assistant
Date: 2026
Purpose: College AI Mini Project - Demonstrates Minimax and Alpha-Beta Pruning algorithms
"""

import tkinter as tk
from tkinter import messagebox
import time
from typing import List, Tuple, Optional


class TicTacToe:
    """
    Main Tic-Tac-Toe game class implementing Minimax algorithm with Alpha-Beta Pruning.
    
    This class manages:
    - Game state and board management
    - AI logic using Minimax with Alpha-Beta pruning
    - Game rules (winner detection, draw detection)
    - GUI interactions
    """
    
    def __init__(self):
        """Initialize game variables and setup GUI."""
        # Game board: 3x3 grid represented as a list of 9 elements (0-8)
        # 0 = empty, 1 = human (X), 2 = AI (O)
        self.board: List[int] = [0] * 9
        
        # Game state variables
        self.human_player: int = 1  # Human plays as X
        self.ai_player: int = 2     # AI plays as O
        self.current_turn: int = self.human_player  # Human starts first
        self.game_over: bool = False
        self.ai_is_thinking: bool = False  # Flag to prevent user input during AI move
        
        # Setup Tkinter GUI
        self.setup_gui()
    
    def setup_gui(self) -> None:
        """
        Setup the Tkinter GUI window and create game board buttons.
        
        Creates a 3x3 grid of buttons with proper layout and styling.
        """
        # Main window setup
        self.root = tk.Tk()
        self.root.title("AI Tic-Tac-Toe - Minimax with Alpha-Beta Pruning")
        self.root.geometry("500x600")
        self.root.config(bg="#2c3e50")
        
        # Title Label
        title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe: AI vs Human",
            font=("Arial", 20, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Status Label (to show whose turn it is)
        self.status_label = tk.Label(
            self.root,
            text="Your Turn (X)",
            font=("Arial", 14),
            fg="#3498db",
            bg="#2c3e50"
        )
        self.status_label.pack(pady=5)
        
        # Game Board Frame
        board_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        board_frame.pack(pady=10)
        
        # Create 3x3 grid of buttons
        self.buttons: List[tk.Button] = []
        for i in range(9):
            # Calculate row and column from button index
            row = i // 3
            col = i % 3
            
            # Create button for each cell
            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 24, "bold"),
                width=6,
                height=3,
                bg="#ecf0f1",
                fg="black",
                activebackground="#95a5a6",
                command=lambda idx=i: self.on_button_click(idx),
                relief="raised",
                bd=3
            )
            
            # Position button in grid
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.pack(pady=10)
        
        # Restart button
        restart_btn = tk.Button(
            control_frame,
            text="Restart Game",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            command=self.restart_game,
            activebackground="#229954"
        )
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        exit_btn = tk.Button(
            control_frame,
            text="Exit",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            command=self.root.quit,
            activebackground="#c0392b"
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # Info Label
        info_label = tk.Label(
            self.root,
            text="Human: X  |  AI: O",
            font=("Arial", 10),
            fg="#95a5a6",
            bg="#2c3e50"
        )
        info_label.pack(pady=5)
    
    def on_button_click(self, index: int) -> None:
        """
        Handle human player's move when a button is clicked.
        
        Args:
            index: Position on the board (0-8)
        """
        # Prevent move if:
        # 1. Game is already over
        # 2. Cell is already occupied
        # 3. AI is currently thinking
        if self.game_over or self.board[index] != 0 or self.ai_is_thinking:
            return
        
        # Place human's move on the board
        self.board[index] = self.human_player
        self.update_button_display(index)
        
        # Check if human won
        winner = self.check_winner(self.board)
        if winner == self.human_player:
            self.game_over = True
            messagebox.showinfo("Game Over", "Congratulations! You Win! 🎉")
            return
        
        # Check if it's a draw
        if self.is_draw(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a Draw! 🤝")
            return
        
        # Now it's AI's turn
        self.current_turn = self.ai_player
        self.status_label.config(text="AI is thinking... (O)", fg="#e74c3c")
        self.ai_is_thinking = True
        self.root.update()
        
        # Add delay for realism (0.5 seconds)
        time.sleep(0.5)
        
        # AI makes its move
        self.ai_move()
    
    def ai_move(self) -> None:
        """
        Execute the AI's move using Minimax algorithm with Alpha-Beta Pruning.
        
        The best move is found and executed on the board.
        """
        # Find the best move for AI using minimax with alpha-beta pruning
        best_score = float('-inf')
        best_move = None
        
        # Iterate through all empty cells
        for i in range(9):
            if self.board[i] == 0:  # Empty cell
                # Try placing AI's move
                self.board[i] = self.ai_player
                
                # Calculate score using minimax with alpha-beta pruning
                # Alpha = worst score for maximizer, Beta = worst score for minimizer
                score = self.minimax(
                    self.board,
                    depth=0,
                    is_maximizing=False,  # After AI's move, it's human's turn (minimizing)
                    alpha=float('-inf'),
                    beta=float('inf')
                )
                
                # Undo the move
                self.board[i] = 0
                
                # Track the best move
                if score > best_score:
                    best_score = score
                    best_move = i
        
        # Make the best move
        if best_move is not None:
            self.board[best_move] = self.ai_player
            self.update_button_display(best_move)
            
            # Check if AI won
            winner = self.check_winner(self.board)
            if winner == self.ai_player:
                self.game_over = True
                messagebox.showinfo("Game Over", "AI Wins! Better luck next time! 🤖")
                self.ai_is_thinking = False
                return
            
            # Check if it's a draw
            if self.is_draw(self.board):
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a Draw! 🤝")
                self.ai_is_thinking = False
                return
        
        # Back to human's turn
        self.current_turn = self.human_player
        self.status_label.config(text="Your Turn (X)", fg="#3498db")
        self.ai_is_thinking = False
    
    def minimax(
        self,
        board: List[int],
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float
    ) -> int:
        """
        Minimax algorithm with Alpha-Beta Pruning.
        
        This is the core AI logic. It recursively explores all possible game states
        and returns the best score for the current position.
        
        Minimax works by:
        1. Maximizing player (AI) tries to maximize the score
        2. Minimizing player (Human) tries to minimize the score
        3. Alpha-Beta Pruning cuts off branches that won't affect the final decision
        
        Args:
            board: Current state of the game board
            depth: Current depth in the game tree (used for move prioritization)
            is_maximizing: True if it's AI's turn (maximizing), False if human's turn (minimizing)
            alpha: Best score the maximizer can guarantee (used in pruning)
            beta: Best score the minimizer can guarantee (used in pruning)
        
        Returns:
            The best score for the current position
        """
        # Check terminal states (base cases of recursion)
        winner = self.check_winner(board)
        
        if winner == self.ai_player:
            # AI won - return positive score
            # Add depth penalty to prefer faster wins
            return 10 - depth
        
        if winner == self.human_player:
            # Human won - return negative score
            # Subtract depth penalty to prefer winning later over losing sooner
            return depth - 10
        
        if self.is_draw(board):
            # Draw state - return neutral score
            return 0
        
        # Recursive case: explore possible moves
        if is_maximizing:
            # AI's turn - try to maximize the score
            max_score = float('-inf')
            
            for i in range(9):
                if board[i] == 0:  # Empty cell
                    # Try placing AI's move
                    board[i] = self.ai_player
                    
                    # Recursively evaluate this move (now it's human's turn)
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    
                    # Undo the move
                    board[i] = 0
                    
                    # Update max score
                    max_score = max(score, max_score)
                    
                    # Alpha-Beta Pruning: cut off if we found a move that's too good
                    # (the minimizer won't allow us to reach this branch)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break  # Prune remaining branches
            
            return max_score
        
        else:
            # Human's turn - try to minimize the score
            min_score = float('inf')
            
            for i in range(9):
                if board[i] == 0:  # Empty cell
                    # Try placing human's move
                    board[i] = self.human_player
                    
                    # Recursively evaluate this move (now it's AI's turn)
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    
                    # Undo the move
                    board[i] = 0
                    
                    # Update min score
                    min_score = min(score, min_score)
                    
                    # Alpha-Beta Pruning: cut off if we found a move that's too bad
                    # (the maximizer won't allow us to reach this branch)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break  # Prune remaining branches
            
            return min_score
    
    def check_winner(self, board: List[int]) -> Optional[int]:
        """
        Check if there's a winner on the board.
        
        Args:
            board: Current state of the game board
        
        Returns:
            1 if human won, 2 if AI won, None if no winner yet
        """
        # All possible winning combinations (rows, columns, diagonals)
        winning_combinations = [
            # Rows
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            # Columns
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            # Diagonals
            [0, 4, 8],
            [2, 4, 6]
        ]
        
        # Check each winning combination
        for combination in winning_combinations:
            pos1, pos2, pos3 = combination
            
            # If all three positions have the same player's mark, that player won
            if (board[pos1] != 0 and
                board[pos1] == board[pos2] == board[pos3]):
                return board[pos1]
        
        # No winner found
        return None
    
    def is_draw(self, board: List[int]) -> bool:
        """
        Check if the game is a draw (board is full and no winner).
        
        Args:
            board: Current state of the game board
        
        Returns:
            True if the board is full (all cells occupied) and no winner, False otherwise
        """
        # Check if all cells are occupied (no empty cells)
        return 0 not in board and self.check_winner(board) is None
    
    def update_button_display(self, index: int) -> None:
        """
        Update the GUI button to show the current move.
        
        Args:
            index: Position on the board (0-8)
        """
        player_symbol = "X" if self.board[index] == self.human_player else "O"
        player_color = "#2c3e50" if self.board[index] == self.human_player else "#e74c3c"
        
        self.buttons[index].config(
            text=player_symbol,
            fg=player_color,
            state="disabled",
            disabledforeground=player_color
        )
    
    def restart_game(self) -> None:
        """
        Reset the game to its initial state and allow a new game to be played.
        """
        # Reset board
        self.board = [0] * 9
        
        # Reset game state
        self.current_turn = self.human_player
        self.game_over = False
        self.ai_is_thinking = False
        
        # Reset all buttons
        for i in range(9):
            self.buttons[i].config(text="", state="normal", bg="#ecf0f1")
        
        # Update status
        self.status_label.config(text="Your Turn (X)", fg="#3498db")
    
    def run(self) -> None:
        """
        Start the game by launching the Tkinter event loop.
        
        This method is called to display the GUI and start playing the game.
        """
        self.root.mainloop()


def main() -> None:
    """
    Main entry point for the Tic-Tac-Toe game.
    
    Creates a game instance and starts the application.
    """
    game = TicTacToe()
    game.run()


if __name__ == "__main__":
    """
    Entry point when the script is run directly.
    """
    main()
