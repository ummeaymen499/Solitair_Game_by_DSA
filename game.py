from card import Deck
from tableau import Tableau
from foundation import Foundation
from circular_queue import CircularQueue
from stack import Stack

class SolitaireGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.tableau = Tableau()
        self.foundation = Foundation()
        self.stock = CircularQueue(24)  # FIFO queue for stockpile
        self.waste = []  # List to act as an array for waste pile
        self.undo_stack = Stack()
        self.redo_stack = Stack()

        self.deal_cards()

        # Initialize the stockpile with the remaining 24 cards
        while not self.stock.is_full():
            card = self.deck.draw_card()
            if card:
                self.stock.enqueue(card)

    def deal_cards(self):
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.draw_card()
                if j == i:
                    card.flip()
                self.tableau.add_card(i, card)

    def draw_from_stock(self):
        # Step 1: Refill stock from waste if stock is empty
        if self.stock.is_empty() and self.waste:
            for _ in range(len(self.waste)): 
                card = self.waste.pop(0)  
                card.flip() 
                self.stock.enqueue(card)
            print(f"Recycled waste pile into stockpile, stock size: {self.stock.size()}")  # Debugging output    
        
    
        drawn_cards = []
        if not self.stock.is_empty():
            card = self.stock.dequeue()  
            card.flip() 
            self.waste.append(card)  
            drawn_cards.append(card)
            print(f"Drew card: {card}, stock size: {self.stock.size()}, waste size: {len(self.waste)}")  # Debugging output
        
        # Step 3: Undo and Redo stacks
        if drawn_cards:
            self.undo_stack.push(('draw', drawn_cards))  
            self.redo_stack.clear()  
        
        return drawn_cards


    def move_card(self, from_column, to_column, to_foundation=False):
        card = self.tableau.get_top_card(from_column)
        if card and not card.face_up:
            card.flip()  
        
        if to_foundation:
            if card and self.is_valid_move_to_foundation(card, to_column):
                self.foundation.add_card(to_column, card)
                self.tableau.remove_card(from_column)
                self.undo_stack.push(('move', from_column, to_column, card, to_foundation))
                self.redo_stack.clear()  
                next_card = self.tableau.get_top_card(from_column)
                if next_card and not next_card.face_up:
                    next_card.flip()
            else:
                print(f"Move to foundation is invalid for card {card}")
        else:
            if card and self.is_valid_move(card, to_column):
                self.tableau.remove_card(from_column)
                self.tableau.add_card(to_column, card)
                self.undo_stack.push(('move', from_column, to_column, card, to_foundation))
                self.redo_stack.clear()  
                next_card = self.tableau.get_top_card(from_column)
                if next_card and not next_card.face_up:
                    next_card.flip()
            else:
                print(f"Move is invalid for card {card} to column {to_column}")

    def move_pile(self, from_column, to_column, start_card):
        sequence = self.get_face_up_sequence(from_column, start_card)
        if not sequence:
            return

    
        if not self.is_valid_move_sequence(sequence, to_column):
            return

        
        for card in sequence:
            self.tableau.remove_card(from_column)
            self.tableau.add_card(to_column, card)
        self.undo_stack.push(('move_pile', from_column, to_column, sequence))
        self.redo_stack.clear() 

        next_card = self.tableau.get_top_card(from_column)
        if next_card and not next_card.face_up:
            next_card.flip()

    def move_card_from_waste(self, to_column):
        if self.waste:
            card = self.waste[-1]
            if self.is_valid_move(card, to_column):
                self.tableau.add_card(to_column, card)
                self.waste.pop()
                self.undo_stack.push(('move_to_tableau', 'waste', to_column, card))
                self.redo_stack.clear() 
            else:
                print(f"Move from waste to tableau is invalid for card {card} to column {to_column}")

    def move_card_from_waste_to_foundation(self, foundation_pile):
        if self.waste:
            card = self.waste[-1]
            if self.is_valid_move_to_foundation(card, foundation_pile):
                self.foundation.add_card(foundation_pile, card)
                self.waste.pop()
                self.undo_stack.push(('move_to_foundation', 'waste', foundation_pile, card))
                self.redo_stack.clear()  

    def undo(self):
        if self.undo_stack.is_empty():
            print("No actions to undo.")
            return

        action = self.undo_stack.pop()
        self.redo_stack.push(action)

        print(f"Undo action: {action}")  

        
        if action[0] == 'draw' and len(action) == 2:
            cards = action[1]
            for card in reversed(cards):
                if card in self.waste:
                    self.waste.remove(card)
                    card.flip()
                    self.stock.enqueue(card)
                else:
                    print(f"Card {card} not found in waste pile")

    
        elif action[0] == 'move_to_tableau' and len(action) == 4:
            from_column, to_column, card = action[1], action[2], action[3]

            self.tableau.remove_card(to_column)
            self.waste.append(card)

            if isinstance(from_column, int):
                next_card = self.tableau.get_top_card(from_column)
                if next_card and not next_card.face_up:
                    next_card.flip()


        elif action[0] == 'move_to_foundation' and len(action) == 4:
            from_column, foundation_pile, card = action[1], action[2], action[3]
    
            self.foundation.remove_card(foundation_pile)
            self.waste.append(card)

    
        elif action[0] == 'move' and len(action) >= 4:
            from_column, to_column, card = action[1], action[2], action[3]
            to_foundation = action[4] if len(action) == 5 else False

            if to_foundation:
                self.foundation.remove_card(to_column)
                self.tableau.add_card(from_column, card)
            else:
                self.tableau.remove_card(to_column)
                self.tableau.add_card(from_column, card)

                if isinstance(from_column, int):
                    next_card = self.tableau.get_top_card(from_column)
                    if next_card and not next_card.face_up:
                        next_card.flip()

        elif action[0] == 'move_pile' and len(action) == 4:
            from_column, to_column, sequence = action[1], action[2], action[3]

            
            for card in reversed(sequence): 
                self.tableau.remove_card(to_column)
                self.tableau.add_card(from_column, card)

            # Flip the top card of the from_column if needed
            if isinstance(from_column, int):
                next_card = self.tableau.get_top_card(from_column)
                if next_card and not next_card.face_up:
                    next_card.flip()

        # Unknown action handling
        else:
            print(f"Unknown or incomplete undo action format: {action}")

    def redo(self):
        if self.redo_stack.is_empty():
            print("No actions to redo.")
            return

        action = self.redo_stack.pop()
        self.undo_stack.push(action)

        print(f"Redo action: {action}")  

    
        if action[0] == 'draw' and len(action) == 2:
            cards = action[1]
            for card in cards:
                if card in self.stock.queue:
                    self.stock.dequeue()
                    card.flip()
                    self.waste.append(card)
                else:
                    print(f"Card {card} not found in stockpile")

    
        elif action[0] == 'move_to_tableau' and len(action) == 4:
            from_column, to_column, card = action[1], action[2], action[3]
            if self.is_valid_move(card, to_column):
                self.waste.pop()  
                self.tableau.add_card(to_column, card)
            else:
                print(f"Redo move from waste to tableau is invalid for card {card} to column {to_column}")

        
        elif action[0] == 'move_to_foundation' and len(action) == 4:
            from_column, foundation_pile, card = action[1], action[2], action[3]
            if self.is_valid_move_to_foundation(card, foundation_pile):
                self.waste.pop()  
                self.foundation.add_card(foundation_pile, card)
            else:
                print(f"Redo move from waste to foundation is invalid for card {card}")


        elif action[0] == 'move' and len(action) >= 4:
            from_column, to_column, card = action[1], action[2], action[3]
            to_foundation = action[4] if len(action) == 5 else False

            if from_column == 'waste':
                self.waste.pop()  
                if to_foundation:
                    self.foundation.add_card(to_column, card)
                else:
                    self.tableau.add_card(to_column, card)
            else:
                if to_foundation:
                    self.tableau.remove_card(from_column)
                    self.foundation.add_card(to_column, card)
                else:
                    self.tableau.remove_card(from_column)
                    self.tableau.add_card(to_column, card)

        
                if isinstance(from_column, int):
                    next_card = self.tableau.get_top_card(from_column)
                    if next_card and not next_card.face_up:
                        next_card.flip()


        elif action[0] == 'move_pile' and len(action) == 4:
            from_column, to_column, sequence = action[1], action[2], action[3]

        
            if self.is_valid_move_sequence(sequence, to_column):
                for card in sequence:
                    self.tableau.remove_card(from_column)
                    self.tableau.add_card(to_column, card)
            else:
                print(f"Redo move of pile from column {from_column} to column {to_column} is invalid")

        else:
            print(f"Unknown redo action format: {action}")


    def get_face_up_sequence(self, column, selected_card):
       
        sequence = []
        found_selected_card = False
        for card in self.tableau.columns[column].to_list():
            if card == selected_card:
                found_selected_card = True
            if found_selected_card and card.face_up:
                sequence.append(card)
        return sequence

    def is_valid_move_sequence(self, sequence, target_column):
      
        if not sequence:
            return False
        # Check if the move is allowed based on game rules (e.g., descending order, alternating colors)
        return self.is_valid_move(sequence[0], target_column)

    def is_valid_move(self, card, to_column):
        top_card = self.tableau.get_top_card(to_column)
        if not top_card:
            return card.rank == 'King'
        if not top_card.face_up:
            return False
        return (self.is_alternating_color(card, top_card) and
                self.rank_value(card.rank) == self.rank_value(top_card.rank) - 1)

    def is_valid_move_to_foundation(self, card, foundation_pile):
        top_card = self.foundation.get_top_card(foundation_pile)
        if not top_card:
            return card.rank == 'Ace'
        return (card.suit == top_card.suit and
                self.rank_value(card.rank) == self.rank_value(top_card.rank) + 1)

    def is_alternating_color(self, card1, card2):
        red_suits = ['Hearts', 'Diamonds']
        black_suits = ['Clubs', 'Spades']
        return ((card1.suit in red_suits and card2.suit in black_suits) or
                (card1.suit in black_suits and card2.suit in red_suits))

    def rank_value(self, rank):
      
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        if rank in ranks:
            return ranks.index(rank) + 1
        return None

    def auto_complete(self):
        moved = True
        any_move_made = False
        iteration_count = 0  

        while moved:
            moved = False
            iteration_count += 1

            if iteration_count > 100:  # Safety guard to avoid infinite loops
                break

           
            for col in range(7):
                card = self.tableau.get_top_card(col)
                if card:
                    # Attempt to move the card to the foundation if possible
                    for foundation_pile in range(4):
                        if self.is_valid_move_to_foundation(card, foundation_pile):
                            self.move_card(col, foundation_pile, to_foundation=True)
                            moved = True
                            any_move_made = True
                            break 
                    if moved:
                        break  

                    for target_col in range(7):
                        if col != target_col:
                            if self.is_valid_move_sequence([card], target_col):
                                self.move_card(col, target_col)
                                moved = True
                                any_move_made = True
                                break
                            
                            sequence = self.get_face_up_sequence(col, card)
                            if sequence and self.is_valid_move_sequence(sequence, target_col):
                                self.move_pile(col, target_col, card)
                                moved = True
                                any_move_made = True
                                break
                    if moved:
                        break 

          
            if not moved and self.waste:
                card = self.waste[-1]

                for foundation_pile in range(4):
                    if self.is_valid_move_to_foundation(card, foundation_pile):
                        self.foundation.add_card(foundation_pile, card)
                        self.waste.pop()
                        moved = True
                        any_move_made = True
                        break
                if moved:
                    continue  

              
                for col in range(7):
                    if self.is_valid_move_sequence([card], col):
                        self.move_card_from_waste(col)
                        moved = True
                        any_move_made = True
                        break

            if not moved:
                break 
        return any_move_made

    def check_victory(self):
        return all(pile.size() == 13 for pile in self.foundation.piles)