from Monopoly import engine, helpers
import numpy as np
import pygame as p
import random

HEIGHT = 512
WIDTH = 1000
FPS = 60
IMAGES = {}  # TODO: Load all images outside of gameloop for efficiency

# TODO: Set this up as a class and have function which plays one player's turn (see snake game)
def run_pygame(number_of_players=4):
    # 1. Initialise the board game and determine who goes first
    game_state = engine.GameState()
    # Here we will assume that Player 1 always goes first for testing purposes.
    # game_state.player_turn = random.sample(range(1, number_of_players + 1)) # First Player

    # Player Metrics
    plot_player_money = np.ones((1, number_of_players)) * game_state.player_money

    while True:
        event = p.event.wait()
        if event.type == p.QUIT:
            p.quit()
            quit()
            break
        elif event.type == p.KEYDOWN:
            # Gameplay Loop
            # 2. Player rolls dice.
            game_state.roll_dice()
            # 2a. If player is in jail, ask if they want to pay 50 dollars to get out, roll for a double, or get out of jail free w/ card
            # 2b. If on the 3rd roll, player does not roll a double, force 50 dollar fee and proceed.
            # 3. Move player number of spaces determined by dice
            # TODO: Make this reference all players, not exclusively player 1
            game_state.move_player(1)
            # 4. If player passes go, collects 200
            # 5. If player lands on jail, go directly to jail and end turn.
            # 6. If player lands on chance or community chest, resolve card and proceed.
            # 7. If property is owned by another player, force player to pay.
            # 7a. Allow user to trade/mortgage/sell houses/etc. in order to pay the costs
            # 8. If space unowned, player can either
            # 8a. Pay for the property and become its owner
            # 8b. Put property up for bidding (player can still place bets on this bidding)
            # 9. Allow player to build houses/trade/sell/mortgage or end turn.
            # 10. Proceed to next players turn.
            # 11. Repeat until all but one player is bankrupt or max number of turns has been reached (tie.)
            game_state.update_ui()
            game_state.clock.tick(FPS)
            p.display.flip()


def run_game(number_of_players=4):
    game_state = engine.GameState()
    # Player Metrics
    plot_player_money = np.ones((1, number_of_players)) * game_state.player_money
    # Game ends when 3rd player is declared bankrupt
    # While loop deals with one full round of play from each player
    while sum(game_state.bankrupt_players) < number_of_players - 1:

        # Players Turn Handled by For Loop
        for player in range(number_of_players):
            # Only play for players still in the game
            if not game_state.bankrupt_players[player]:
                # Roll Dice
                dice_roll = sum(engine.roll_dice())
                previous_player_position = np.where(game_state.board[:, player] == 1)[0][0]
                current_player_position = (previous_player_position + dice_roll) % 40
                game_state.board[previous_player_position, player] = 0  # Remove Old Position
                game_state.board[current_player_position, player] = 1  # Update New Position

                # Pass Go?
                if current_player_position < previous_player_position:
                    game_state.player_money[player] += 200

                    # Plot Information
                    plot_player_money = np.vstack([plot_player_money, game_state.player_money])

                # Determine Where Player Landed
                current_tile = engine.map_position(current_player_position)
                if type(current_tile) == tuple:
                    # Check if unowned
                    property_ownership = game_state.owned_property[current_tile[0]][current_tile[1] - 1]
                    if property_ownership == 0:
                        # If unowned, buy if money is available
                        if (cost := engine.cost_property(current_tile)) <= game_state.player_money[player]:
                            game_state.owned_property[current_tile[0]][
                                current_tile[1] - 1] = player + 1  # indexed by player id
                            game_state.player_money[player] -= cost

                            # Plot Information
                            plot_player_money = np.vstack([plot_player_money, game_state.player_money])

                    else:
                        # If owned, pay up to relevant player.
                        print(
                            f"Player {player + 1} is paying player {property_ownership} for landing on {engine.map_position(current_player_position)}")
                        game_state.player_money[player] -= engine.rent(current_tile, 5, dice_roll)
                        game_state.player_money[property_ownership - 1] += engine.rent(current_tile, 5, dice_roll)

                        # Plot Information
                        plot_player_money = np.vstack([plot_player_money, game_state.player_money])

                elif current_tile == "Go To Jail":
                    game_state.board[current_player_position, player] = 0
                    game_state.board[10, player] = 1

                elif current_tile == "Community":
                    # Check if deck needs to be reshuffled.
                    if len(game_state.used_community_cards) == 0:
                        game_state.community_cards = game_state.used_community_cards
                        game_state.used_community_cards = {}

                    # # card_number, action = random.choice(list(game_state.community_cards.items()))
                    # # print(card_number)
                    # game_state.used_community_cards[card_number] = game_state.community_cards[card_number]
                    # del game_state.community_cards[card_number]

                # Check For Bankrupt Players
                if game_state.player_money[player] < 0:
                    # Declare Bankrupt and Remove Properties
                    print("Player " + str(player + 1) + " is bankrupt by Player " + str(property_ownership))
                    game_state.bankrupt_players[player] = 1
                    for color in game_state.owned_property:
                        bankrupt_properties = np.where(game_state.owned_property[color] == player + 1)
                        game_state.owned_property[color][bankrupt_properties] = 0

                if sum(game_state.bankrupt_players) == 1:
                    break

    print(game_state.bankrupt_players)
    print(game_state.player_money)
    print(game_state.owned_property)

    # Plot Results
    print(helpers.plot_metrics(plot_player_money, number_of_players))


def main():
    # Use a breakpoint in the code line below to debug your script.
    run_pygame()  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
