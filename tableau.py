from linked_list import LinkedList

class Tableau:
    def __init__(self):
        # Initialize a list of 7 columns using LinkedLists
        self.columns = [LinkedList() for _ in range(7)]

    def add_card(self, column, card):
        self.columns[column].append(card)

    def remove_card(self, column):
        if self.columns[column].is_empty():
            return None
        return self.columns[column].pop()

    def get_top_card(self, column_index):
        if self.columns[column_index]:  
            top_card = self.columns[column_index].get_last()  
            if top_card and not top_card.face_up:  
                top_card.flip()
            return top_card
        return None

    def get_pile(self, column, start_card):
        pile = LinkedList()
        current = self.columns[column].head
        while current and current.data != start_card:
            current = current.next
        
        while current:
            pile.append(current.data)
            current = current.next
        return pile

    def remove_pile(self, column, start_card):
       
        pile = LinkedList()
        current = self.columns[column].head
        prev = None

        while current and current.data != start_card:
            prev = current
            current = current.next

        if current:
            while current:
                pile.append(current.data)
                current = current.next
            
            if prev:
                prev.next = None
            else:
                self.columns[column].head = None

        return pile

    def is_column_empty(self, column):
        return self.columns[column].is_empty()

    def __str__(self):
        """Represent the tableau as a string for easy debugging."""
        return "\n".join([f"Column {i + 1}: {str(self.columns[i])}" for i in range(7)])

