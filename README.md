Solitaire Game (Klondike)

Overview:
This project is a Python-based implementation of the Solitaire game, adhering to the Klondike rules. The game is designed to replicate the classic Solitaire gameplay, where the goal is to move all the cards into the foundation piles, sorted in increasing order from Ace to King, by suit. This version features a well-structured user interface (GUI) and an in-depth game engine that handles the initialization, shuffling, card movements, undo/redo functionality, and win conditions. It provides an interactive, enjoyable experience for users to play the game in a terminal or GUI-based environment.

The game supports common Solitaire features such as:

Card Moves: Moving cards between tableau piles, foundation piles, and drawing cards from the stockpile.
Undo/Redo: Keeping track of moves for undo and redo functionality.
Legal Moves: Ensuring valid moves according to the game rules.
Timer and Scoring: A timer tracks the game’s duration, and the scoring system reflects the player’s performance.
Features
Card Representation: Each card has attributes like suit, rank, and face-up/down status. The deck is shuffled and dealt to the tableau piles.
Tableau and Foundation: Cards are arranged into tableau piles, where the goal is to eventually move all cards to the foundation piles, following the correct order.
Valid Moves: Moves are only allowed if they follow the rules: alternating colors, sequential ranks in tableau piles, and building foundation piles from Ace to King by suit.
Undo/Redo: Tracks moves made by the player and allows reversing actions (undo) or redoing them (redo).
Timer and Scoring: A timer runs from the start to the end of the game, while the score updates as the player progresses through the game.
Win Condition: The game ends when all cards are moved to the foundation piles in the correct order.
Technologies Used
Python 3.x: Core programming language.
Tkinter: For creating a graphical user interface (GUI), if used.
Collections (Queue, Stack): Python’s collections module is used to implement the game mechanics such as tableau piles, foundation piles, and stockpile.
List/Array: Used to represent the deck of cards and to manage the cards in different piles.
Project Structure
card.py: Contains the Card class, which represents each card with attributes like rank, suit, and face-up/down status.
deck.py: Manages the deck of cards, shuffling, and dealing to tableau piles.
game.py: Implements core game logic, including the movement of cards between tableau piles, foundation piles, stockpile drawing, win condition checks, and the undo/redo functionality.
ui.py: (Optional) Contains code to create the graphical user interface (GUI) using Tkinter for player interaction.
main.py: The entry point of the program. This file runs the game, initializes the deck, shuffles it, and starts the gameplay.
How to Run the Game
To run the Solitaire game on your local machine, follow these steps:

Clone the repository:

bash
Copy code
git clone <https://gitlab.com/ummeaymen499/CSC200M24PID112>
Navigate to the project folder:

bash
Copy code
cd solitaire-game
Install any required dependencies (if using GUI or other external libraries):

bash
Copy code
pip install -r requirements.txt
Run the game:

bash
Copy code
python main.py
This will start the Solitaire game, where you can interact with the game using the terminal or the GUI if implemented.

Game Design
Card Class
The Card class represents each card in the deck. Each card has the following attributes:

Rank: The rank of the card (Ace, 2, 3,..., Queen, King).
Suit: The suit of the card (Hearts, Diamonds, Clubs, Spades).
Face-Up/Face-Down: Whether the card is visible or hidden.
The __str__ method displays the card as <rank> of <suit> if the card is face-up, or as Card is face down if the card is face-down.

Deck Class
The deck is represented as an array of 52 cards, and it is shuffled at the beginning of the game. Seven tableau piles are created with the appropriate number of cards dealt (increasing from 1 to 7 cards), where only the top card of each pile is face-up.

Game Logic
The game is initialized by shuffling the deck and dealing the cards into seven tableau piles. The game loop ensures that valid moves are made by the player. The foundation piles are built from Ace to King, following suit, and the player can draw cards from the stockpile to help build the tableau and foundation piles.

Undo/Redo System
An undo/redo system is implemented using stacks to keep track of all moves made. The player can revert to a previous state (undo) or redo a previously undone action.

Timer and Scoring
The game includes a timer that starts when the game begins and stops when the game ends. The score updates each time a card is moved from a tableau pile to the foundation, reflecting the player's progress.

Testing
The project uses a variety of tests to ensure that all game functionalities work as expected. Here are some key test cases:

1. Card Initialization Test
Objective: Ensure each card is correctly initialized with suit, rank, and face-up/down status.
Test Steps:
Create a Card object with a specific suit and rank.
Verify the card's attributes.
Verify the face-up status is False initially.
Expected Result: The Card object should be correctly initialized with the specified suit, rank, and face-down status.
2. Deck Shuffling Test
Objective: Ensure the deck is shuffled correctly and contains exactly 52 cards.
Test Steps:
Create a deck and shuffle it.
Verify that the deck contains 52 cards.
Verify that the shuffled deck contains no duplicate cards.
Expected Result: The deck should contain 52 unique cards, and the order should be randomized.
3. Valid Move Test
Objective: Ensure that valid moves are properly implemented (e.g., alternating colors and sequential ranks).
Test Steps:
Move a red 7 onto a black 8.
Attempt to move a red 7 onto a red 6.
Expected Result: The first move should be allowed, and the second move should be rejected.
4. Undo/Redo Test
Objective: Ensure that the undo and redo functionality works correctly.
Test Steps:
Make a series of moves in the game.
Undo the last move and verify the game state reverts.
Redo the undone move and verify the game state restores.
Expected Result: The undo/redo functionality should work as expected.
5. Win Condition Test
Objective: Ensure the game correctly detects the win condition when all cards are in the foundation piles.
Test Steps:
Move all cards to the foundation piles in correct order.
Verify the win condition triggers and the game ends.
Expected Result: The game should declare victory when all cards are placed in the foundation piles.
6. Timer and Scoring Test
Objective: Verify that the timer starts, stops, and the score updates as the player moves cards.
Test Steps:
Start the game and check that the timer begins.
Move cards to the foundation piles and verify the score increases.
End the game and verify the timer stops.
Expected Result: The timer should function correctly, and the score should update as the game progresses.


Test Cases
Testing the Solitaire game is crucial to ensure that all features work as expected. Below are the detailed test cases for verifying the key functionalities of the game.

1. Card Initialization Test
Objective: Ensure that each card is correctly initialized with the proper suit, rank, and face-up/down status.

Test Steps:

Create a Card object with the suit "Hearts" and rank "Ace".
Verify that the card's suit is "Hearts".
Verify that the card's rank is "Ace".
Verify that the card's face-up status is False initially (as cards are face-down when first dealt).
Expected Result:

The card should have the correct suit ("Hearts").
The card should have the correct rank ("Ace").
The card should be face-down (False).
Test Code Example:

python
Copy code
card = Card('Hearts', 'Ace')
assert card.suit == 'Hearts', "Suit should be Hearts"
assert card.rank == 'Ace', "Rank should be Ace"
assert not card.face_up, "Card should be face down initially"
2. Deck Shuffling Test
Objective: Ensure the deck is shuffled correctly and contains exactly 52 unique cards.

Test Steps:

Create a deck and shuffle it.
Check if the deck contains exactly 52 cards.
Check that all cards in the shuffled deck are unique (no duplicates).
Ensure the deck is shuffled by verifying that the order of cards is different from an ordered deck.
Expected Result:

The deck should contain exactly 52 unique cards.
The deck should be shuffled, meaning the order of cards should not be the same as the initial order.
Test Code Example:

python
Copy code
deck = Deck()
deck.shuffle()
assert len(deck.cards) == 52, "Deck should contain 52 cards"
assert len(set(deck.cards)) == 52, "Deck should not contain duplicates"
3. Valid Move Test
Objective: Ensure that valid moves are implemented correctly according to the Solitaire rules.

Test Steps:

Create a tableau with a red 7 (Hearts) on top of a black 8 (Spades).
Attempt to move the red 7 onto the black 8. This should be a valid move.
Attempt to move a red 7 onto a red 6 (Diamonds). This should be an invalid move.
Expected Result:

The first move (red 7 onto black 8) should succeed.
The second move (red 7 onto red 6) should fail and not be allowed.
Test Code Example:

python
Copy code
# Assuming tableau_pile[0] is the tableau with a red 7 on top of black 8
assert valid_move(tableau_pile[0], 'red 7', 'black 8'), "Move should be valid"
assert not valid_move(tableau_pile[1], 'red 7', 'red 6'), "Move should be invalid"
4. Undo/Redo Functionality Test
Objective: Ensure that the undo and redo functionality works as expected.

Test Steps:

Make a few moves in the game (e.g., moving cards from the tableau to the foundation).
Call the undo method to reverse the last move and verify that the game state is reverted.
Call the redo method to restore the last undone move and verify that the game state is restored.
Expected Result:

The undo functionality should correctly revert the last move.
The redo functionality should restore the previously undone move.
Test Code Example:

python
Copy code
game = Game()
game.make_move('move1')
game.make_move('move2')

# Check if undo works
game.undo()
assert game.current_state == 'move1', "Undo did not revert to the correct state"

# Check if redo works
game.redo()
assert game.current_state == 'move2', "Redo did not restore the correct state"
5. Win Condition Test
Objective: Ensure the game correctly detects the win condition when all cards are moved to the foundation piles.

Test Steps:

Simulate moving all cards from the tableau to the foundation piles.
Verify that the game recognizes this as a win condition and terminates the game.
Expected Result:

The game should detect the win condition when all cards are placed in the foundation piles in the correct order (Ace to King, sorted by suit).
The game should notify the player of the victory.
Test Code Example:

python
Copy code
game = Game()
# Simulate moving cards to foundation piles
game.move_to_foundation('Hearts', 'Ace')
game.move_to_foundation('Hearts', '2')
# Repeat for all suits and ranks

assert game.check_win(), "Game should end when all cards are in foundation piles"
6. Timer and Scoring Test
Objective: Verify that the timer and scoring mechanisms work correctly.

Test Steps:

Start the game and ensure the timer starts.
Make a few valid moves (e.g., move cards to foundation piles).
Verify that the timer has incremented and is running.
Verify that the score updates correctly with each move.
Expected Result:

The timer should increment over time, reflecting the duration of the game.
The score should increase as the player moves cards to the foundation piles.
The game should stop the timer when the player wins.
Test Code Example:

python
Copy code
game = Game()
game.start_timer()
# Make some moves
game.move_to_foundation('Clubs', 'Ace')
game.move_to_foundation('Diamonds', '2')

# Check if the timer is running
assert game.timer > 0, "Timer should be running during the game"
assert game.score > 0, "Score should increase as cards are moved"
7. Invalid Card Placement Test
Objective: Ensure that invalid card placements (e.g., moving cards to incorrect piles) are properly handled.

Test Steps:

Attempt to place a King on an empty tableau pile (which is not allowed).
Attempt to place a red card on a red card in the tableau pile (which is not allowed).
Expected Result:

The first test should fail as Kings can only be placed on empty tableau piles or other Kings.
The second test should fail as only alternating colors are allowed in tableau piles.
Test Code Example:

python
Copy code
assert not valid_move(tableau_pile[0], 'King', 'empty'), "Kings cannot be placed on empty tableau pile"
assert not valid_move(tableau_pile[1], 'red 3', 'red 5'), "Red cards cannot be placed on other red cards"


Conclusion: 
This project implements a fully functional Solitaire game with a well-defined set of rules and features. The game allows players to interact with the tableau piles, foundation piles, and stockpile, using valid moves to complete the game. It supports advanced features like undo/redo functionality, a timer, and scoring. The code is modular and easy to maintain, with clear documentation and test cases for ensuring the functionality works as expected.




























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































