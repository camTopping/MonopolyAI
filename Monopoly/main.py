from Monopoly import engine, helpers
import numpy as np

def run_game(number_of_players=4):
    player_id = 0
    game_state = engine.GameState()

    # Player Metrics
    plot_player_money = np.ones((1, number_of_players)) * game_state.player_money

    # Game ends when 3rd player is declared bankrupt
    # While loop deals with one full round of play from each player
    while sum(game_state.bankrupt_players) < 3:

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
                            game_state.owned_property[current_tile[0]][current_tile[1] - 1] = player + 1  # indexed by player id
                            game_state.player_money[player] -= cost

                            # Plot Information
                            plot_player_money = np.vstack([plot_player_money, game_state.player_money])

                    else:
                        # If owned, pay up to relevant player.
                        print(f"Player {player + 1} is paying player {property_ownership} for landing on {engine.map_position(current_player_position)}")
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

    # Plot Results\
    print(helpers.plot_metrics(plot_player_money, number_of_players))

def main():
    # Use a breakpoint in the code line below to debug your script.
    run_game()  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
