from stack import Stack

class Foundation:
    def __init__(self):
        self.piles = [Stack() for _ in range(4)]

    def add_card(self, pile: int, card: str) -> None:
        if 0 <= pile < 4:
            self.piles[pile].push(card)
        else:
            raise IndexError("Pile index out of range. Must be between 0 and 3.")

    def get_top_card(self, pile: int) -> str:
        if 0 <= pile < 4:
            return self.piles[pile].peek() if not self.piles[pile].is_empty() else None
        else:
            raise IndexError("Pile index out of range. Must be between 0 and 3.")

    def remove_card(self, pile: int) -> str:
        if 0 <= pile < 4:
            if not self.piles[pile].is_empty():
                return self.piles[pile].pop()
            else:
                raise IndexError("Cannot remove card from an empty pile.")
        else:
            raise IndexError("Pile index out of range. Must be between 0 and 3.")