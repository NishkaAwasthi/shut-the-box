import tkinter as tk
import random
from itertools import combinations

class ShutTheBox:
    def __init__(self, master):
        self.master = master
        self.master.title("Shut the Box Game")
        self.master.config(bg="#87CEEB")  # Sky blue background
        
        self.numbers = list(range(1, 13))
        self.selected_numbers = []
        
        self.setup_styles()  # Call this first to set up styles
        self.create_board()
        self.create_dice_button()
        self.create_status_label()
        self.create_reset_button()  # Create reset button but keep it hidden

        self.current_sum = 0  # Store the current sum of the rolled dice

    def setup_styles(self):
        self.button_style = {
            "font": ("Comic Sans MS", 24),
            "bg": "#ffcc00",  # Bright yellow background for buttons
            "fg": "black",  # Change text color to black
            "activebackground": "#ffa500",  # Darker orange on click
            "relief": "raised",
            "width": 5,
            "height": 2
        }
        
        self.status_label_style = {
            "font": ("Comic Sans MS", 20),
            "bg": "#87CEEB",
            "fg": "#333333",  # Darker text for status label
            "padx": 10,
            "pady": 10
        }

        self.dice_button_style = {
            "font": ("Comic Sans MS", 24),
            "bg": "#4caf50",  # Green background for dice button
            "fg": "#000000",  # White text
            "activebackground": "#388e3c",  # Darker green on click
            "relief": "raised",
            "padx": 20,
            "pady": 10
        }

        self.reset_button_style = {
            "font": ("Comic Sans MS", 24),
            "bg": "#e74c3c",  # Red background for reset button
            "fg": "#000000",  # Change text color to black
            "activebackground": "#c0392b",  # Darker red on click
            "relief": "raised",
            "padx": 20,
            "pady": 10
        }

    def create_board(self):
        self.buttons = {}
        for i, number in enumerate(self.numbers):
            button = tk.Button(self.master, text=str(number), command=lambda n=number: self.eliminate_number(n), **self.button_style)
            row = i // 4  # Calculate row for 3x4 grid
            col = i % 4   # Calculate column for 3x4 grid
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.buttons[number] = button
        
        # Make buttons expand evenly
        for i in range(4):
            self.master.grid_columnconfigure(i, weight=1)

    def create_dice_button(self):
        self.dice_button = tk.Button(self.master, text="Roll Dice", command=self.roll_dice, **self.dice_button_style)
        self.dice_button.grid(row=3, columnspan=4, padx=5, pady=10)

    def create_reset_button(self):
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_game, **self.reset_button_style)
        self.reset_button.grid(row=4, columnspan=4, padx=5, pady=10)  # Reset button below Roll Dice button
        self.reset_button.grid_remove()  # Initially hide the reset button

    def create_status_label(self):
        self.status_label = tk.Label(self.master, text="", **self.status_label_style)
        self.status_label.grid(row=5, columnspan=4, pady=10)

    def roll_dice(self):
        # Show "Rolling..." for 2 seconds before revealing the roll
        self.update_status("Rolling...")
        self.master.after(2000, self.do_roll)

    def do_roll(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        self.current_sum = self.dice1 + self.dice2
        self.update_status(f"Rolled: {self.dice1} + {self.dice2} = {self.current_sum}")

        # Clear previous selections
        self.selected_numbers.clear()
        for button in self.buttons.values():
            button.config(bg='#ffcc00')  # Reset button colors to default

        # Check if the player can make a move
        if not self.can_make_move():
            self.update_status(f"No valid moves left that sum to {self.current_sum}! You lose!")  # Updated message
            self.dice_button.config(state='disabled')  # Disable the roll button
            self.reset_button.grid()  # Show reset button
            return

        # Disable the Roll Dice button until the player eliminates numbers
        self.dice_button.config(state='disabled')

    def eliminate_number(self, number):
        if number in self.buttons and self.buttons[number]['state'] == 'normal':
            self.selected_numbers.append(number)
            self.buttons[number].config(state='disabled', bg='lightgray')  # Disable the button
            self.update_status(f"Eliminated: {number}")

            # Check for win condition
            if all(self.buttons[n]['state'] == 'disabled' for n in self.numbers):
                self.update_status("You win!")
                self.reset_button.grid()  # Show reset button
                return
            
            # Check if the current sum matches the rolled sum
            if sum(self.selected_numbers) == self.current_sum:
                self.dice_button.config(state='normal')  # Enable roll again
                self.update_status("You can roll again!")
            else:
                self.update_status("You can keep eliminating numbers!")

            # Check for loss condition again after elimination
            if not self.can_make_move():
                self.update_status(f"No valid moves left that sum to {self.current_sum}! You lose!")  # Updated message
                self.dice_button.config(state='disabled')  # Disable the roll button
                self.reset_button.grid()  # Show reset button
        else:
            self.update_status("Invalid elimination! Cannot eliminate this number.")


    def can_make_move(self):
        # Get available numbers based on button state
        available_numbers = [n for n in self.numbers if self.buttons[n]['state'] == 'normal']

        # Check if any combination of available_numbers sums to current_sum
        if not available_numbers:  # If there are no available numbers
            return False

        for r in range(1, len(available_numbers) + 1):
            for combo in combinations(available_numbers, r):
                if sum(combo) == self.current_sum:
                    return True

        return False

    def reset_game(self):
        self.selected_numbers.clear()
        for number in self.numbers:
            self.buttons[number].config(state='normal', bg='#ffcc00')  # Reset button colors
        self.update_status("")
        self.dice_button.config(state='normal')  # Enable the Roll Dice button again
        self.reset_button.grid_remove()  # Hide the reset button after resetting

    def update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    game = ShutTheBox(root)
    root.mainloop()
