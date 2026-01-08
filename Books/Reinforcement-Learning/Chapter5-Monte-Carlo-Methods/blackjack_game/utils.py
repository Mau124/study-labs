import pygame
from blackjack.engine import *

# screen constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60
TRUE_WHITE = (255, 255, 255)

# constants for placement
DEALER_LABEL_Y = 100
DEALER_AREA_X = 100
DEALER_AREA_Y = 150
PLAYER_LABEL_Y = 350
PLAYER_AREA_X = 100
PLAYER_AREA_Y = 400

INFO_TEXT_X = 800
DIFF_BETWEEN_ELEMENTS = 50
DIFF_BETWEEN_CARDS = 120

class Game:

    def __init__(self):
        self.state = Blackjack()

    def restart_game(self):
        self.state = Blackjack()

class Title:
    def __init__(self, pos, text, font):
        self.pos = pos
        self.text = text
        self.font = font

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, TRUE_WHITE)
        text_rect = text_surface.get_rect(center=self.pos)
        surface.blit(text_surface, text_rect)

class Label:
    def __init__(self, pos, text, font):
        self.pos = pos
        self.text = text
        self.font = font

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, TRUE_WHITE)
        text_rect = text_surface.get_rect(topleft=self.pos)
        surface.blit(text_surface, text_rect)

    def update_text(self, text):
        self.text = text

class Image:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Button:

    HOVERED_COLOR = (200, 200, 200)
    BUTTON_COLOR = (150, 150, 150)

    def __init__(self, rect, text, font, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.HOVERED_COLOR if hovered else self.BUTTON_COLOR

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)

        text_button = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_button, text_button.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.callback()

def draw_hidden_dealer_card(screen: pygame.Surface):
    x = DEALER_AREA_X + DIFF_BETWEEN_CARDS
    y = DEALER_AREA_Y

    dir = 'images/card_back_red.png'

    image = Image(pos=(x, y), image=load_img(dir))
    image.draw(screen)

def draw_cards(screen: pygame.Surface, game: Game):
    player_x = PLAYER_AREA_X
    player_y = PLAYER_AREA_Y

    for card in game.state.player.cards:
        suit = convert_suit(card[0])
        number = convert_number(card[1])

        dir = f'images/{number}_of_{suit}.png'

        image = Image(pos=(player_x, player_y), image=load_img(dir))
        image.draw(screen)

        player_x += DIFF_BETWEEN_CARDS
    
    dealer_x = DEALER_AREA_X
    dealer_y = DEALER_AREA_Y

    for card in game.state.dealer.cards:
        suit = convert_suit(card[0])
        number = convert_number(card[1])

        dir = f'images/{number}_of_{suit}.png'

        image = Image(pos=(dealer_x, dealer_y), image=load_img(dir))
        image.draw(screen)

        dealer_x += DIFF_BETWEEN_CARDS

def convert_suit(suit: str) -> str:

    conversion_suits = {
        'C': 'clubs',
        'H': 'hearts',
        'S': 'spades',
        'D': 'diamonds'
    }

    return conversion_suits[suit]

def convert_number(number: int) -> str:
    if number == 1:
        return 'ace'

    if number == 11:
        return 'jack'
    
    if number == 12:
        return 'queen'
    
    if number == 13:
        return 'king'
    
    return str(number)

def load_img(dir: str)-> pygame.Surface:
    try:
        # Load the image and convert it for faster blitting (especially for .png with alpha)
        image = pygame.image.load(dir).convert_alpha()
        image = pygame.transform.scale(image, (100, 150))
        return image
    except pygame.error as message:
        print(f"Cannot load image: {dir}. Error: {message}")
        pygame.quit()
        exit()