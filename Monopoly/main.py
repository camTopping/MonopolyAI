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

    while sum(game_state.bankrupt_players) < number_of_players - 1:
        event = p.event.wait()
        if event.type == p.QUIT:
            p.quit()
            quit()
            break
        elif event.type == p.KEYDOWN:
            # Gameplay Loop
            player_turn = game_state.player_turn

            if game_state.number_of_turns_in_jail[player_turn] > 0:
                print(f"Player {player_turn}: Handling Jail Case ")
                # TODO: User input
                # 2a. If player is in jail, ask if they want to pay 50 dollars to get out, roll for a double, or get out of jail free w/ card
                # 2b. If on the 3rd roll, player does not roll a double, force 50 dollar fee and proceed.
                if game_state.free_jail[0, player_turn] == 1:
                    print("Get out of Jail Free")
                    # Use get out of jail free card and place back into cards
                    game_state.free_jail[0, player_turn] = 0
                    # Put card back in pile
                    game_state.chance_cards[4] = "Get Out of Jail Free"
                    game_state.chance_draw_order.insert(game_state.chance_card_number - 1, 4)

                    game_state.roll_dice()
                    game_state.number_of_turns_in_jail[player_turn] = 0
                    game_state.move_player(player_turn)
                elif game_state.free_jail[1, player_turn] == 1:
                    print("Get out of Jail Free")
                    # Use get out of jail free card and place back into cards
                    game_state.free_jail[1, player_turn] = 0
                    # Put card back in pile
                    game_state.community_cards[6] = "Get Out of Jail Free"
                    game_state.community_draw_order.insert(game_state.community_card_number - 1, 6)

                    game_state.roll_dice()
                    game_state.number_of_turns_in_jail[player_turn] = 0
                    game_state.move_player(player_turn)
                else:
                    game_state.roll_dice()
                    if game_state.doubles_rolled > 0:
                        print("Rolled Double, goes free.")
                        # Player goes free
                        game_state.number_of_turns_in_jail[player_turn] = 0
                        game_state.move_player(player_turn)
                    elif game_state.number_of_turns_in_jail[player_turn] == 3:
                        print("3 Turns in Jail and no double, pay 50.")
                        # Play pays 50 and moves
                        game_state.player_money[player_turn] -= 50
                        game_state.number_of_turns_in_jail[player_turn] = 0
                        game_state.move_player(player_turn)
                    else:
                        print(f"No Double, end turn. NoT: {game_state.number_of_turns_in_jail[player_turn]}")
                        game_state.number_of_turns_in_jail[player_turn] += 1

                        game_state.update_ui()
                        game_state.clock.tick(FPS)
                        p.display.flip()

                        game_state.get_next_player()
                        continue
            else:
                # 2. Player rolls dice.
                game_state.roll_dice()

                # 3. Move player number of spaces determined by dice
                game_state.move_player(player_turn)

            # 4. If player lands on chance or community chest, resolve card and proceed.
            current_tile = engine.map_position(game_state.player_position[player_turn])
            if type(current_tile) != tuple:
                if current_tile == "Chance":
                    drawn_card = game_state.chance_card_number
                    game_state.resolve_chance_card(player_turn)
                    # Show Card Event
                    show_chance_event = True
                    show_community_event = False
                elif current_tile == "Community":
                    drawn_card = game_state.community_card_number
                    game_state.resolve_community_card(player_turn)
                    # Show Card Event
                    show_chance_event = False
                    show_community_event = True
                else:
                    show_chance_event = False
                    show_community_event = False
            else:
                show_chance_event = False
                show_community_event = False

            current_tile = engine.map_position(game_state.player_position[player_turn])
            # 5. If player lands on jail, go directly to jail and end turn.
            if current_tile == "Go To Jail":
                game_state.go_to_jail(player_turn)

                game_state.update_ui()
                game_state.clock.tick(FPS)
                p.display.flip()

                game_state.get_next_player()
                continue

            # force update on current tile in case player move
            current_tile = engine.map_position(game_state.player_position[player_turn])

            # 6. If player passes go, collects 200
            # Going to Jail does not count as passing go
            if game_state.player_position[player_turn] < game_state.previous_player_position[player_turn]:
                game_state.collect_go(player_turn)

            # TODO: User based decision - no longer force
            # 7. If property is owned by another player, force player to pay.
            # 7a. Allow user to trade/mortgage/sell houses/etc. in order to pay the costs
            # 8. If space unowned, player can either
            # 8a. Pay for the property and become its owner
            if type(current_tile) == tuple:
                property_ownership = game_state.owned_property[current_tile[0]][current_tile[1] - 1]
                if property_ownership == 0:
                    # If unowned, buy if money is available
                    if (engine.cost_property(current_tile)) <= game_state.player_money[player_turn]:
                        game_state.buy_property(player_turn, current_tile)
                        # Plot Information
                        plot_player_money = np.vstack([plot_player_money, game_state.player_money])

                elif property_ownership - 1 != player_turn:
                    # If owned, pay up to relevant player.
                    print(
                        f"Player {player_turn} is paying player {property_ownership - 1} for landing on {engine.map_position(game_state.player_position[player_turn])}")
                    game_state.pay_rent(player_turn, property_ownership - 1, 0, current_tile)

                    # Plot Information
                    plot_player_money = np.vstack([plot_player_money, game_state.player_money])
            # 8b. Put property up for bidding (player can still place bets on this bidding)
            # TODO: Create bidding system

            # 9. Allow player to build houses/trade/sell/mortgage or end turn.
            # TODO: Create house building system
            # TODO: Create trading system
            # TODO: Create mortgage system

            # Update UI
            game_state.update_ui()
            if show_chance_event:
                game_state.draw_card_event(True, False, game_state.chance_draw_order[drawn_card])
            elif show_community_event:
                game_state.draw_card_event(False, True, game_state.community_draw_order[drawn_card])
            game_state.clock.tick(FPS)
            p.display.flip()

            # 10. Repeat until all but one player is bankrupt or max number of turns has been reached (tie.)
            # Check For Bankrupt Players
            game_state.check_bankrupt()

            # 11. Proceed to next players turn if not double
            if game_state.doubles_rolled == 0 or game_state.bankrupt_players[player_turn]:
                game_state.get_next_player()
            elif game_state.doubles_rolled < 3:
                print(f"Double Rolled")
            else:
                print("Speeding, go to jail")
                game_state.doubles_rolled = 0
                game_state.go_to_jail(player_turn)
                game_state.get_next_player()


    print(helpers.plot_metrics(plot_player_money, number_of_players))


def main():
    # Use a breakpoint in the code line below to debug your script.
    run_pygame()  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
