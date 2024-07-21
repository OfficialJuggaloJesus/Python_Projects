import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Solitaire')

# Define Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.face_up = False

# Example deck creation
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

deck = []
for suit in suits:
    for rank in ranks:
        deck.append(Card(suit, rank))

# Example tableau and foundation initialization
tableau = [[] for _ in range(7)]  # 7 columns
foundation = {suit: [] for suit in suits}  # 4 foundation piles, one for each suit

# Example function to deal cards
def deal_cards():
    for i in range(len(tableau)):
        for j in range(i, len(tableau)):
            tableau[j].append(deck.pop(0))
            if j == i:
                tableau[j][-1].face_up = True  # Flip only the last dealt card face up

deal_cards()

# Function to draw a card
def draw_card(screen, card, x, y):
    if card.face_up:
        # Draw face-up card
        pygame.draw.rect(screen, WHITE, (x, y, 70, 100))  # Example: white rectangle
        # Example: Render card text (suit and rank) on the rectangle
        font = pygame.font.Font(None, 36)
        text = font.render(f"{card.rank} of {card.suit}", True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))
    else:
        # Draw face-down card
        pygame.draw.rect(screen, (50, 120, 50), (x, y, 70, 100))  # Example: green rectangle
        # Example: Render a card back image on the rectangle
        card_back_image = pygame.image.load('card_back.png')  # Example: replace with actual card back image
        screen.blit(card_back_image, (x, y))

    # Draw card border
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 70, 100), 2)

# Function to draw tableau columns
def draw_tableau(screen, tableau):
    start_x = 50
    start_y = 150
    spacing_x = 100
    spacing_y = 120

    for col_idx, column in enumerate(tableau):
        x = start_x + col_idx * spacing_x
        y = start_y
        for card_idx, card in enumerate(column):
            draw_card(screen, card, x, y + card_idx * spacing_y)

# Function to draw foundation piles
def draw_foundation(screen, foundation):
    start_x = 400
    start_y = 50
    spacing_x = 100

    for idx, suit in enumerate(foundation):
        x = start_x + idx * spacing_x
        y = start_y
        if foundation[suit]:
            top_card = foundation[suit][-1]
            draw_card(screen, top_card, x, y)
        else:
            # Draw empty foundation pile outline or text indicating empty
            pygame.draw.rect(screen, (200, 200, 200), (x, y, 70, 100))
            font = pygame.font.Font(None, 36)
            text = font.render(suit, True, (0, 0, 0))
            screen.blit(text, (x + 5, y + 5))

# Function to move cards between tableau columns
def move_cards_between_tableau(source_col, dest_col, count):
    if len(tableau[source_col]) >= count and tableau[source_col][-count].face_up:
        valid_move = True
        for i in range(1, count):
            if not tableau[source_col][-i].face_up or \
                    ranks.index(tableau[source_col][-i].rank) != ranks.index(tableau[source_col][-i - 1].rank) - 1 or \
                    tableau[source_col][-i].suit == tableau[source_col][-i - 1].suit:
                valid_move = False
                break
        if valid_move:
            for i in range(count):
                tableau[dest_col].append(tableau[source_col].pop(-count))
            return True
    return False

# Function to move card to foundation
def move_card_to_foundation(card):
    if len(foundation[card.suit]) == 0 and card.rank == 'Ace':
        foundation[card.suit].append(card)
        return True
    elif len(foundation[card.suit]) > 0:
        top_card = foundation[card.suit][-1]
        if top_card.rank == ranks[ranks.index(card.rank) - 1] and top_card.suit == card.suit:
            foundation[card.suit].append(card)
            return True
    return False

def handle_click(pos):
    # Check if a tableau column is clicked
    if pos[1] >= 150:  # Check if Y position is in the range of tableau columns
        col_idx = (pos[0] - 50) // 100  # Calculate which tableau column was clicked based on X position
        if 0 <= col_idx < len(tableau):
            clicked_column = tableau[col_idx]
            # Check if a card in the tableau column was clicked
            card_idx = (pos[1] - 150) // 120  # Calculate which card in the column was clicked based on Y position
            if 0 <= card_idx < len(clicked_column):
                clicked_card = clicked_column[card_idx]
                if not clicked_card.face_up:
                    clicked_card.face_up = True  # Flip the card face up if it's face down
                else:
                    # Check if another tableau column or foundation pile is clicked
                    # Move the clicked card to foundation or another tableau column if valid
                    if move_card_to_foundation(clicked_card):
                        clicked_column.remove(clicked_card)
                    else:
                        for dest_col_idx in range(len(tableau)):
                            if move_cards_between_tableau(col_idx, dest_col_idx, card_idx + 1):
                                break

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse click events to interact with cards and game elements
            pos = pygame.mouse.get_pos()
            handle_click(pos)

    # Clear screen
    screen.fill(WHITE)

    # Draw tableau and foundation
    draw_tableau(screen, tableau)
    draw_foundation(screen, foundation)

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
