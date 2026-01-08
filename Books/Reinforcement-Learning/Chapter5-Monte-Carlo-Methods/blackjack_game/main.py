import pygame
from blackjack.engine import *
from utils import *
from blackjack.policies import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

game = Game()

###############################################################################
# Functions as callbacks for the buttons
###############################################################################
def hit():
   game.state.player_hit()

def stick():
   game.state.player_stick()

def dealer_take_step():
   game.state.take_dealer_action(policy=policy_dealer)

def play_again():
   print('Play again')
   game.restart_game()

###############################################################################
# Titles and labels definitions
###############################################################################
game_title = Title((SCREEN_WIDTH//2, 30), 'BlackJack Game', font)

dealer_label = Label((DEALER_AREA_X, DEALER_LABEL_Y), 'Dealer', font)
sum_dealer = Label((INFO_TEXT_X, DEALER_AREA_Y), 'Sum: 18', font)

player_label = Label((PLAYER_AREA_X, PLAYER_LABEL_Y), 'Player', font)
sum_player = Label((INFO_TEXT_X, PLAYER_AREA_Y), 'Sum: 7', font)
usable_ace = Label((INFO_TEXT_X, PLAYER_AREA_Y+DIFF_BETWEEN_ELEMENTS), 'Usable Ace: True', font)

win_label = Title((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 'You have won!!!', font)
lost_label = Title((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 'You have lost!!!', font)
draw_label = Title((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 'It is a draw!!', font)

###############################################################################
# Buttons definitions
###############################################################################
hit_button = Button((50, 600, 180, 75), "Hit", font, hit)
stick_button = Button((875, 600, 180, 75), "Stick", font, stick)

dealer_step_button = Button((SCREEN_WIDTH//2-90, 600, 180, 75), "Dealer Step", font, dealer_take_step)

play_again_button = Button((SCREEN_WIDTH//2-90, 600, 180, 75), 'Play again', font, play_again)

###############################################################################
# Functions to update texts and draw texts
###############################################################################
def update_texts(game: Game):
    sum_dealer.update_text(f'Sum: {str(game.state.dealer.sum)}')
    sum_player.update_text(f'Sum: {str(game.state.player.sum)}')
    usable_ace.update_text(f'Usable Ace: {game.state.player.usable_ace}')

def draw_texts(screen: pygame.Surface):
    game_title.draw(screen)
    dealer_label.draw(screen)
    sum_dealer.draw(screen)
    player_label.draw(screen)
    sum_player.draw(screen)
    usable_ace.draw(screen)

###############################################################################
# Game
###############################################################################
while running:

    for event in pygame.event.get():

        if game.state.check_state() != GameState.PLAYING:
            play_again_button.handle_event(event)

        if game.state.check_state() == GameState.PLAYING:
            if game.state.turn == Turn.PLAYER:
                hit_button.handle_event(event)
                stick_button.handle_event(event)
            elif game.state.turn == Turn.DEALER:
                dealer_step_button.handle_event(event)

        if event.type == pygame.QUIT:
            running = False

    # Fill the background with the correct color
    screen.fill("#1B4719")

    # Draw the image onto the screen surface at the center position
    if game.state.turn == Turn.PLAYER:
        draw_hidden_dealer_card(screen)
    draw_texts(screen)
    draw_cards(screen, game)

    # Update the texts on the labels
    update_texts(game)

    # Check game state
    if game.state.check_state() == GameState.LOST:
        lost_label.draw(screen)
    if game.state.check_state() == GameState.WON:
        win_label.draw(screen)
    if game.state.check_state() == GameState.DRAW:
        draw_label.draw(screen)
    if game.state.check_state() != GameState.PLAYING:
        play_again_button.draw(screen)

    if game.state.check_state() == GameState.PLAYING: 
        if game.state.turn == Turn.PLAYER:
            hit_button.draw(screen)
            stick_button.draw(screen)
        if game.state.turn == Turn.DEALER:
            dealer_step_button.draw(screen)

    # Updates the screen, so the user can see the image
    pygame.display.flip()

    # Controls how fast the game is running
    # Limits maximum number of frames
    clock.tick(FPS)

pygame.quit()