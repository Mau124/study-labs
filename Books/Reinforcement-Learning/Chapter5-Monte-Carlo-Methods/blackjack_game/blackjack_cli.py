from blackjack.blackjack.blackjack import *
from blackjack.blackjack.policies import *

game = Blackjack()
while game.check_state() == GameState.PLAYING:
    game.print_game()
    game.take_step(policy_player=manual_policy, policy_dealer=policy_dealer)
    input()
print(game.check_state())
print(game.print_game())
