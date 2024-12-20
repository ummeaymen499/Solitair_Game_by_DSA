# Import necessary modules
import tkinter as tk
from game import SolitaireGame
from tkinter import messagebox

# Initialize Tkinter root
root = tk.Tk()
root.title("Solitaire")
root.geometry("1600x800")
root.configure(bg='#004000') 

selected_card = None
selected_column = None
selected_sequence = []

# Dictionary to store drag data
drag_data = {"x": 0, "y": 0, "item": None, "from_waste": False}

# Initialize game
game = SolitaireGame()

# Timer variables
timer_label = None
timer_seconds = 0

# Move counter variable
move_counter = 0
move_counter_label = None

# Score counter variable
score = 0
score_label = None

# Timer update function
def update_timer():
    global timer_seconds
    timer_seconds += 1
    minutes, seconds = divmod(timer_seconds, 60)
    timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
    root.after(1000, update_timer)

# Move counter update function
def update_move_counter():
    global move_counter, score
    move_counter += 1
    move_counter_label.config(text=f"Moves: {move_counter}")
    score -= 1  # Deduct 1 point per move
    update_score()
    print(f"Move Counter: {move_counter}, Score: {score}")

# Score update function
def update_score():
    global score
    score_label.config(text=f"Score: {score}")
    print(f"Score updated: {score}")  

# Add score function
def add_score(points):
    global score
    score += points
    update_score()
    print(f"Added {points} points. New score: {score}") 

# Function to display a card on the UI
def display_card(card, x, y, column, is_foundation=False, from_waste=False):
    if card is None:
        print(f"Attempted to display a None card at column {column}")
        return
    card_label = tk.Label(root, image=card.image, bg='#006400')  
    card_label.image = card.image 
    card_label.place(x=x, y=y)
    
    if not is_foundation:
        bind_card_events(card_label, card, column, from_waste)

# Function to bind events to a card
def bind_card_events(card_label, card, column, from_waste):
    # Bind mouse press event
    card_label.bind("<ButtonPress-1>", lambda event: on_card_press(event, card, column, from_waste))
    # Bind mouse motion event
    card_label.bind("<B1-Motion>", on_card_motion)
    # Bind mouse release event
    card_label.bind("<ButtonRelease-1>", on_card_release)

# Handle card press event
def on_card_press(event, card, column, from_waste):
    print("Card press event")
    global selected_card, selected_column, selected_sequence, drag_data
    widget = event.widget
    drag_data["item"] = widget
    drag_data["x"] = event.x
    drag_data["y"] = event.y
    print(f"Card press event: {widget}")

    print(f"Card clicked: {card} in column {column}")
    if selected_card is None:
        for foundation_pile in range(4):
            print("Checking foundation")
            if game.is_valid_move_to_foundation(card, foundation_pile):
                
                if from_waste:
                    game.move_card_from_waste_to_foundation(foundation_pile)
                    print("Valid move to foundation from waste")
                else:
                    print("Valid move to foundation from tabulaeu")
                    game.move_card(column, foundation_pile, to_foundation=True)
                update_move_counter()
                add_score(10)  
                arrange_cards() 
                return 
            else:
                print("Invalid move to foundation")


        selected_card = card
        selected_column = column
        drag_data["from_waste"] = from_waste

    
        if column is not None:
            selected_sequence = game.get_face_up_sequence(column, card)
        else:
            selected_sequence = [card]
        print(f"Selected card sequence: {selected_sequence}")
    else:
      
        if game.is_valid_move_sequence(selected_sequence, column):
            print(f"Moving card sequence: {selected_sequence} to column {column}")
            game.move_pile(selected_column, column, selected_card)
            update_move_counter()
            add_score(5) 
            arrange_cards()
        else:
            print(f"Invalid move for sequence: {selected_sequence}")
        
      
        selected_card = None
        selected_column = None
        selected_sequence = []
        drag_data["from_waste"] = False

def on_card_motion(event):
    global drag_data
    widget = drag_data.get("item")

    if widget is None:
        print("Error: widget is None in on_card_motion")
        return

 
    if not widget.winfo_exists():
        print("Error: widget no longer exists")
        return

    try:
       
        if widget is not None:
            x = widget.winfo_x() - drag_data["x"] + event.x
            y = widget.winfo_y() - drag_data["y"] + event.y
            widget.place(x=x, y=y)
        else:
            print("Error: widget is None when calculating position")
    except tk.TclError as e:
        print(f"An error occurred while updating position: {e}")
        return

# Handle card release event
def on_card_release(event):
    print("Card release event")
    global drag_data, selected_card, selected_column, selected_sequence
    widget = event.widget
    if widget is None or not widget.winfo_exists():
        print("Error: widget is None or does not exist in on_card_release")
        return

    x = widget.winfo_x()
    y = widget.winfo_y()
    column = (x + 50) // 120  # Calculate the column based on x position

    if column < 7:  # It's a tableau column
        if drag_data["from_waste"]:
            # Case 1: Waste to Tableau
            if game.is_valid_move(selected_card, column):
                game.move_card_from_waste(column)
                update_move_counter()  
                add_score(5)  
                arrange_cards()
            else:
                print("Invalid move from Waste to Tableau")
                arrange_cards() 
        elif selected_sequence:
            print("Case 2: Tableau to Tableau with sequence")
            if column != selected_column and game.is_valid_move_sequence(selected_sequence, column):
                game.move_pile(selected_column, column, selected_card)
                update_move_counter()
                add_score(5) 
                arrange_cards()
            else:
                print("Invalid move for sequence from Tableau to Tableau")
                arrange_cards()
        elif selected_card:
            print("Case 3: Tableau to Tableau with single card")
            single_card_sequence = [selected_card]  # Wrap in list for compatibility
            if column != selected_column and game.is_valid_move_sequence(single_card_sequence, column):
                game.move_card(selected_column, column)
                update_move_counter()
                add_score(5)  
                arrange_cards()
            else:
                print("Invalid move for single card from Tableau to Tableau")
                arrange_cards()

    # Reset drag data and selected state
    drag_data = {"x": 0, "y": 0, "item": None, "from_waste": False}
    selected_card = None
    selected_column = None
    selected_sequence = []

# Handle stockpile click event
def on_stock_click(event):
    
        game.draw_from_stock()
        update_move_counter()
        arrange_cards()
   

# Handle foundation click event
def on_foundation_click(event, foundation_pile):
    global selected_card, selected_column
 
    if selected_card and game.is_valid_move_to_foundation(selected_card, foundation_pile):
        if drag_data["from_waste"]:
            game.move_card_from_waste_to_foundation(foundation_pile)
        else:
            game.move_card(selected_column, foundation_pile, to_foundation=True)
        update_move_counter()
        add_score(10)  
        arrange_cards()
        selected_card = None
        selected_column = None

def on_auto_complete_click(event):
    try:
        moves_made = game.auto_complete()
        if not moves_made:
            messagebox.showinfo("Auto-Complete", "No more moves possible. Auto-complete could not proceed.")
    except Exception as e:
        messagebox.showerror("Error", f"Error during auto-complete: {e}")
    arrange_cards()

# Handle undo click event
def on_undo_click(event):
    global score
    game.undo()
    score -= 5  
    update_score()
    arrange_cards()

# Handle redo click event
def on_redo_click(event):
    game.redo()
    arrange_cards()

# Handle restart click event
def on_restart_click(event):
    global game, selected_card, selected_column, selected_sequence, drag_data, timer_seconds, move_counter, score
    game = SolitaireGame()  # Reinitialize the game
    selected_card = None
    selected_column = None
    selected_sequence = []
    drag_data = {"x": 0, "y": 0, "item": None, "from_waste": False}
    timer_seconds = 0
    move_counter = 0
    score = 0
    update_labels() 
    arrange_cards()

def update_labels():
    global move_counter, score
    move_counter_label.config(text=f"Moves: {move_counter}")
    score_label.config(text=f"Score: {score}")
    print(f"Move Counter: {move_counter}, Score: {score}")  # Debugging output

def arrange_cards():
    for widget in root.winfo_children():
        widget.destroy()

    x_offset = 50
    y_offset = 210
    for i in range(7):
        for j, card in enumerate(game.tableau.columns[i].to_list()):
            display_card(card, x_offset + i * 120, y_offset + j * 30, i)
       
        top_card = game.tableau.get_top_card(i)
        print(f"Top card of column {i}: {top_card}")

  
    foundation_x = 410
    foundation_y = 25
    for i in range(4):
        card = game.foundation.get_top_card(i)
        if card:
            display_card(card, foundation_x + i * 120, foundation_y, column=None, is_foundation=True)
        foundation_label = tk.Label(root, text=f"Foundation {i+1}", bg='#004000', fg='white')
        foundation_label.place(x=foundation_x + i * 120, y=foundation_y)
        foundation_label.bind("<Button-1>", lambda event, pile=i: on_foundation_click(event, pile))

    
    if not game.stock.is_empty():
        stock_card = game.stock.queue[game.stock.front]
        stock_label = tk.Label(root, image=stock_card.image, bg='#006400')
        stock_label.image = stock_card.image
        stock_label.place(x=50, y=25)
        stock_label.bind("<Button-1>", lambda event: on_stock_click(event))  # Draw 3 cards on click
    else:
        stock_label = tk.Label(root, text="Empty Stock", bg='#006400', fg='white')
        stock_label.place(x=50, y=25)
        stock_label.bind("<Button-1>", lambda event: on_stock_click(event))  # Draw 3 cards on click

  
    for i in range(len(game.waste)):
        card = game.waste[i]
        display_card(card, 170, 25, None, from_waste=True)

    
   
    auto_complete_button = tk.Button(
        root,
        text="Auto-Complete",
        command=lambda: on_auto_complete_click(None),
        bg="#FFFACD",         # Solitaire-like green background color
        fg="#808080",             # White text color
        font=("Helvetica", 14, "bold"),  # Bold text with larger font size
        padx=5,                # Increase padding for a bigger button
        pady=5,
        relief="solid",            # Solid border for more defined shape
        bd=2, 
        highlightbackground="#004000", # Border color to match background
        highlightthickness=2    
    )
    auto_complete_button.place(x=1000, y=25)
    # Add undo button
    undo_button = tk.Button(root, text="Undo", command=lambda: on_undo_click(None),
        bg="#FFFACD",        
        fg="#808080",             
        font=("Helvetica", 12, "bold"), 
        relief="solid",     
        padx=5,                
        # pady=5,
        bd=2, 
        highlightbackground="#004000", 
        highlightthickness=2)
    undo_button.place(x=1000, y=150)

    # Add redo button
    redo_button = tk.Button(root, text="Redo", command=lambda: on_redo_click(None),
     bg="#FFFACD",       
        fg="#808080",             
        font=("Helvetica", 12, "bold"),  
        relief="solid",     
        padx=5,                
        bd=2, 
        highlightbackground="#004000",
        highlightthickness=2)
    redo_button.place(x=1000, y=200)

    # Add restart button
    restart_button = tk.Button(root, text="Restart", command=lambda: on_restart_click(None),
     bg="#FFFACD",         
        fg="#808080",             
        font=("Helvetica", 12, "bold"),  
        relief="solid",     
        padx=5,               
        bd=2, 
        highlightbackground="#004000", 
        highlightthickness=2)
    restart_button.place(x=1000, y=250)

    # Add timer label
    global timer_label
    timer_label = tk.Label(root, text="Time: 00:00", bg='#004000', fg='white', font=("Helvetica", 12, "bold"),padx=10, pady=5)
    timer_label.place(x=900, y=600)

    # Add move counter label
    global move_counter_label
    move_counter_label = tk.Label(root, text=f"Moves: {move_counter}", bg='#004000', fg='white',font=("Helvetica", 12, "bold"),padx=10, pady=5)
    move_counter_label.place(x=1020, y=600)

    # Add score label
    global score_label
    score_label = tk.Label(root, text=f"Score: {score}", bg='#004000', fg='white',font=("Helvetica", 12, "bold"),padx=10, pady=5)
    score_label.place(x=1150, y=600)

    # Check for victory
    if game.check_victory():
        add_score(500)  # Add 500 points for winning the game
        messagebox.showinfo("Victory", f"Congratulations! You have won the game!\nFinal Score: {score}")
        root.destroy()  # End the game by closing the window

arrange_cards()

update_timer()

root.mainloop()