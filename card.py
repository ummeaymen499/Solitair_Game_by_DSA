import random
from PIL import Image, ImageTk
import os

class Card:
    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
        self.image = self.load_image()  

    def __repr__(self):
        if self.face_up:
            return f"{self.rank} of {self.suit}"
        else:
            return "Card is face down"


    def flip(self):
        self.face_up = not self.face_up
        self.image = self.load_image() 

    def load_image(self):
        if self.face_up:
            image_path = os.path.join("images", f"{self.rank.lower()}_of_{self.suit.lower()}.png")
        else:
            image_path = os.path.join("images", "card_back.png")
        image = Image.open(image_path)
        image = image.resize((100, 150), Image.LANCZOS)  # Resize the image to 100x150 pixels
        return ImageTk.PhotoImage(image)

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = []  
        for suit in self.suits:
            for rank in self.ranks:
                card = Card(suit, rank)
                self.cards.append(card)
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        # Draw a card from the deck
        return self.cards.pop() if self.cards else None
    
    def is_empty(self):
        return len(self.cards) == 0