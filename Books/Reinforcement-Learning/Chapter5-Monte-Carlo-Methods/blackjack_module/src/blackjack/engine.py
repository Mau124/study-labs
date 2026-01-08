import random
from enum import Enum, auto

class GameState(Enum):
    DRAW = auto()
    LOST = auto()
    WON = auto()
    PLAYING = auto()

class Action(Enum):
    HIT = auto()
    STICK = auto()

class Turn(Enum):
    PLAYER = auto()
    DEALER = auto()
    RESOLUTION = auto()

class Blackjack:

    def __init__(self):
        # Initialize game

        # Initialize deck
        self.deck = Deck()
        self.deck.shuffle()

        # Initialize player and dealer
        self.dealer = Dealer(self.deck.take_card(), self.deck.take_card())
        self.player = Player(self.deck.take_card(), self.deck.take_card())
        # self.dealer = Dealer(('C', 1), ('D', 10))
        # self.player = Player(('S', 1), ('H', 10))

        # Initialize states of the game
        self.turn = Turn.PLAYER

    def player_hit(self):
        """
        This function is used just for the graphic and cli modes

        :param self: auto reference
        """
        if self.turn == Turn.PLAYER:
            self.player.add_card(self.deck.take_card())
    
    def player_stick(self):
        """
        This function is used just for the graphic and cli modes
        
        :param self: auto reference
        """
        if self.turn == Turn.PLAYER:
            self.dealer.reveal_second_card()
            self.turn = Turn.DEALER

    def take_step(self, policy_player, policy_dealer) -> Action:
        action = Action.HIT
        if self.turn == Turn.PLAYER:
            action = self.take_player_action(policy_player)
        elif self.turn == Turn.DEALER:
            action = self.take_dealer_action(policy_dealer)
        return action

    def take_player_action(self, policy):
        if self.player.sum == 21:
            self.dealer.reveal_second_card()
            
            if len(self.player.cards) == 2:
                self.turn = Turn.RESOLUTION
            else:
                self.turn = Turn.DEALER

            return Action.STICK

        action = policy(self.player, self.dealer)
        if action == Action.HIT:
            self.player.add_card(self.deck.take_card())
        else:
            self.dealer.reveal_second_card()
            self.turn = Turn.DEALER
        return action

    def take_dealer_action(self, policy):
        action = policy(self.dealer)
        if action == Action.HIT:
            self.dealer.add_card(self.deck.take_card())
        else:
            self.turn = Turn.RESOLUTION
        return action

    def check_state(self) -> GameState:
        if self.turn == Turn.PLAYER:
            if self.player.sum > 21:
                return GameState.LOST
            elif self.player.sum == 21:
                return GameState.PLAYING
            else:
                return GameState.PLAYING
        elif self.turn == Turn.DEALER:
            if self.dealer.sum > 21:
                return GameState.WON
            elif self.dealer.sum == 21:
                if self.player.sum == self.dealer.sum:
                    return GameState.DRAW
                else:
                    return GameState.LOST
            else:
                return GameState.PLAYING
        elif self.turn == Turn.RESOLUTION:
            if self.player.sum > self.dealer.sum:
                return GameState.WON
            elif self.player.sum < self.dealer.sum:
                return GameState.LOST
            else:
                return GameState.DRAW

    def print_game(self):
        print(f'State of the Game')
        print('Dealer info')
        print(self.dealer)
        print('Player info')
        print(self.player)

class Player:

    def __init__(self, card1, card2):
        self.cards = []
        self.sum = 0
        self.usable_ace = False

        self.add_card(card1)
        self.add_card(card2)

    def add_card(self, card: tuple):
        self.cards.append(card)

        if card[1] != 1:
            if card[1] >= 10:
                self.sum += 10
            else:
                self.sum += card[1]

            if self.sum > 21 and self.usable_ace:
                self.sum -= 10
                self.usable_ace = False
        else: # You have an ace
            self.sum += 1
            if not self.usable_ace and self.sum + 10 <= 21:
                self.sum += 10
                self.usable_ace = True


    def __str__(self):
        cards = ''.join(str(card) for card in self.cards)
        msg = f"""
        Player Cards: {cards}
        Player Sum: {self.sum}
        Player Usable Ace: {self.usable_ace}
        """
        return msg


class Dealer(Player):

    def __init__(self, card1: tuple, card2: tuple):
        self.card1 = card1
        self.card2 = card2
        self.cards = []
        self.sum = 0
        self.usable_ace = False

        self.add_card(card1)

    def reveal_second_card(self):
        self.add_card(self.card2)

    def __str__(self):
        cards = ''.join(str(card) for card in self.cards)
        msg = f"""
        Dealer Cards: {cards}
        Dealer Sum: {self.sum}
        """
        return msg

class Deck:

    suits = ['C',  # clubs
             'D',  # diamonds
             'H',  # hearts
             'S']  # spades

    def __init__(self):
        self.cards = [(suit, rank) for suit in self.suits for rank in range(1, 13)]

    def shuffle(self):
        random.shuffle(self.cards)

    def take_card(self):
        return self.cards.pop()

    def __str__(self):
        msg = ''.join(str(card) for card in self.cards)
        return msg

    def __repr__(self):
        msg = ''.join(str(card) for card in self.cards)
        return msg