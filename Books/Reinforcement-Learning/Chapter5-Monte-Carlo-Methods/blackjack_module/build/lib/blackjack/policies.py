from blackjack.engine import *

def policy_player(player: Player, dealer: Player) -> Action:
    if player.sum < 20:
        return Action.HIT
    else:
        return Action.STICK

def policy_dealer(dealer: Player) -> Action:
    if dealer.sum < 17:
        return Action.HIT
    else:
        return Action.STICK

def manual_policy(player: Player, dealer: Dealer) -> Action:
    action = input('Which action do you want to follow: ')
    if action == 'H':
        return Action.HIT
    else:
        return Action.STICK