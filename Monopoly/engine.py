import numpy as np
import random
import pygame as p
import os

# This script handles the creation and tracking of the current game state across it's numerous players.
HEIGHT = 512
WIDTH = 1000

PLAYER_SIZE = 20
PLAYER_COLOR = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (100, 0, 100)]
BOARD_SIZE = 512 #px

# Initiate Game Board
# This handle the creation of the board - ideally, this can also be used to save/load game files
# Takes a list of values which represents each player's position on the board
def init_game_board(player_positions, number_of_players=4):
    squares = np.zeros((40, number_of_players), dtype="int")
    for i in range(len(player_positions)):
        squares[player_positions[i], i] = 1

    return squares


# Generation of Property
def init_property():
    title_deeds = {"Brown": np.zeros(2, dtype="int"),
                   "Cyan": np.zeros(3, dtype="int"),
                   "Purple": np.zeros(3, dtype="int"),
                   "Orange": np.zeros(3, dtype="int"),
                   "Red": np.zeros(3, dtype="int"),
                   "Yellow": np.zeros(3, dtype="int"),
                   "Green": np.zeros(3, dtype="int"),
                   "Blue": np.zeros(2, dtype="int"),
                   "Rail": np.zeros(4, dtype="int"),
                   "Utility": np.zeros(2, dtype="int")}

    return title_deeds


# Map Position
def map_position(player_position):
    # Need a method which maps a player's position (0,1,...,39) to the appropriate property/square on the board.
    index = {0: "Go",
             1: "Brown1",
             2: "Community",
             3: "Brown2",
             4: "Income Tax",
             5: "Rail1",
             6: "Cyan1",
             7: "Chance",
             8: "Cyan2",
             9: "Cyan3",
             10: "Jail",
             11: "Purple1",
             12: "Utility1",
             13: "Purple2",
             14: "Purple3",
             15: "Rail2",
             16: "Orange1",
             17: "Community",
             18: "Orange2",
             19: "Orange3",
             20: "Free",
             21: "Red1",
             22: "Chance",
             23: "Red2",
             24: "Red3",
             25: "Rail3",
             26: "Yellow1",
             27: "Yellow2",
             28: "Utility2",
             29: "Yellow3",
             30: "Go To Jail",
             31: "Green1",
             32: "Green2",
             33: "Community",
             34: "Green3",
             35: "Rail4",
             36: "Chance",
             37: "Blue1",
             38: "Super Tax",
             39: "Blue2"
             }

    # Seperate String into Color and Index
    head = index[player_position].rstrip('0123456789')
    if head in ["Brown", "Cyan", "Purple", "Orange", "Red", "Yellow", "Green", "Blue", "Rail",
                "Utility"]:
        tail = int(index[player_position][len(head):])
        square = (head, tail)
    else:
        square = index[player_position]

    return square


# Costs of Property
def cost_property(property_tuple):
    # property should be a tuple containing the color of the set and the index of the property.
    # e.g ("Cyan", 2) would refer to the second Cyan property 'Euston Road'
    if type(property_tuple) == tuple:
        prices = {"Brown": np.ones(2, dtype="int") * 60,
                  "Cyan": np.ones(3, dtype="int") * [100, 100, 120],
                  "Purple": np.ones(3, dtype="int") * [140, 140, 160],
                  "Orange": np.ones(3, dtype="int") * [180, 180, 200],
                  "Red": np.ones(3, dtype="int") * [220, 220, 260],
                  "Yellow": np.ones(3, dtype="int") * [260, 260, 280],
                  "Green": np.ones(3, dtype="int") * [300, 300, 320],
                  "Blue": np.ones(2, dtype="int") * [350, 400],
                  "Rail": np.ones(4, dtype="int") * 200,
                  "Utility": np.ones(2, dtype="int") * 150}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    else:
        return 0


# Rent of Property
def rent(property_tuple, number_of_houses, dice_roll):
    if number_of_houses == 0:
        prices = {"Brown": np.ones(2, dtype="int") * [2, 4],
                  "Cyan": np.ones(3, dtype="int") * [6, 6, 8],
                  "Purple": np.ones(3, dtype="int") * [10, 10, 12],
                  "Orange": np.ones(3, dtype="int") * [14, 14, 16],
                  "Red": np.ones(3, dtype="int") * [18, 18, 20],
                  "Yellow": np.ones(3, dtype="int") * [22, 22, 24],
                  "Green": np.ones(3, dtype="int") * [26, 26, 28],
                  "Blue": np.ones(2, dtype="int") * [35, 50],
                  "Rail": np.ones(4, dtype="int") * 25,
                  "Utility": np.ones(2, dtype="int") * 4 * dice_roll}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    elif number_of_houses == 1:
        prices = {"Brown": np.ones(2, dtype="int") * [10, 20],
                  "Cyan": np.ones(3, dtype="int") * [30, 30, 40],
                  "Purple": np.ones(3, dtype="int") * [50, 50, 60],
                  "Orange": np.ones(3, dtype="int") * [70, 70, 80],
                  "Red": np.ones(3, dtype="int") * [90, 90, 100],
                  "Yellow": np.ones(3, dtype="int") * [110, 110, 120],
                  "Green": np.ones(3, dtype="int") * [130, 130, 150],
                  "Blue": np.ones(2, dtype="int") * [175, 200],
                  "Rail": np.ones(4, dtype="int") * 25,
                  "Utility": np.ones(2, dtype="int") * 4 * dice_roll}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    elif number_of_houses == 2:
        prices = {"Brown": np.ones(2, dtype="int") * [30, 60],
                  "Cyan": np.ones(3, dtype="int") * [90, 90, 100],
                  "Purple": np.ones(3, dtype="int") * [150, 150, 180],
                  "Orange": np.ones(3, dtype="int") * [200, 200, 220],
                  "Red": np.ones(3, dtype="int") * [250, 250, 300],
                  "Yellow": np.ones(3, dtype="int") * [330, 330, 360],
                  "Green": np.ones(3, dtype="int") * [390, 390, 450],
                  "Blue": np.ones(2, dtype="int") * [500, 600],
                  "Rail": np.ones(4, dtype="int") * 50,
                  "Utility": np.ones(2, dtype="int") * 10 * dice_roll}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    elif number_of_houses == 3:
        prices = {"Brown": np.ones(2, dtype="int") * [90, 180],
                  "Cyan": np.ones(3, dtype="int") * [270, 270, 300],
                  "Purple": np.ones(3, dtype="int") * [450, 450, 500],
                  "Orange": np.ones(3, dtype="int") * [550, 550, 600],
                  "Red": np.ones(3, dtype="int") * [700, 700, 750],
                  "Yellow": np.ones(3, dtype="int") * [800, 800, 850],
                  "Green": np.ones(3, dtype="int") * [900, 900, 1000],
                  "Blue": np.ones(2, dtype="int") * [1100, 1400],
                  "Rail": np.ones(4, dtype="int") * 100,
                  "Utility": np.ones(2, dtype="int") * 10 * dice_roll}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    elif number_of_houses == 4:
        prices = {"Brown": np.ones(2, dtype="int") * [160, 320],
                  "Cyan": np.ones(3, dtype="int") * [400, 400, 450],
                  "Purple": np.ones(3, dtype="int") * [625, 625, 700],
                  "Orange": np.ones(3, dtype="int") * [750, 750, 800],
                  "Red": np.ones(3, dtype="int") * [875, 875, 925],
                  "Yellow": np.ones(3, dtype="int") * [975, 975, 1025],
                  "Green": np.ones(3, dtype="int") * [1100, 1100, 1200],
                  "Blue": np.ones(2, dtype="int") * [1300, 1700],
                  "Rail": np.ones(4, dtype="int") * 200,
                  "Utility": np.ones(2, dtype="int") * 10 * dice_roll}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    elif number_of_houses == 5:
        prices = {"Brown": np.ones(2, dtype="int") * [250, 450],
                  "Cyan": np.ones(3, dtype="int") * [550, 550, 600],
                  "Purple": np.ones(3, dtype="int") * [750, 750, 900],
                  "Orange": np.ones(3, dtype="int") * [950, 950, 1000],
                  "Red": np.ones(3, dtype="int") * [1050, 1050, 1100],
                  "Yellow": np.ones(3, dtype="int") * [1150, 1150, 1200],
                  "Green": np.ones(3, dtype="int") * [1275, 1275, 1400],
                  "Blue": np.ones(2, dtype="int") * [1500, 2000],
                  "Rail": np.ones(4, dtype="int") * 200,
                  "Utility": np.ones(2, dtype="int") * 10 * dice_roll}

        cost = prices[property_tuple[0]][property_tuple[1] - 1]

        return cost
    else:
        return 0


# Roll Dice
def roll_dice():
    first_die = random.randint(1, 6)
    second_die = random.randint(1, 6)

    results = (first_die, second_die)

    return results


# Set Up Pygame Classes and Functions
class Background(p.sprite.Sprite):
    def __init__(self, image_file, location):
        p.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = p.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def draw_gameboard(image_file):
    image = Background(image_file, [0, 0])
    return image

def player_pos_px(board_position):
    # board_position references the tiles from 0 to 39

    if board_position == 0:
        player_pos_y = 475
        player_pos_x = 475
    elif board_position == 10:
        player_pos_y = 475
        player_pos_x = 45
    elif board_position == 20:
        player_pos_y = 45
        player_pos_x = 45
    elif board_position < 10:
        player_pos_y = 475
        player_pos_x = (11 - board_position) * 40.2
    elif board_position < 20:
        player_pos_y = (21 - board_position) * 40.2
        player_pos_x = 45
    elif board_position < 30:
        player_pos_y = 45
        player_pos_x = (board_position - 19) * 40.2
    elif board_position < 40:
        player_pos_y = (board_position - 29) * 40.2
        player_pos_x = 475

    position_tuple = (player_pos_x, player_pos_y)

    return position_tuple


# Define Game State
class GameState:
    def __init__(self, number_of_players=4, visual_game = True):
        # PyGame
        if visual_game:
            # Set Up Pygame
            p.init()
            self.font = p.font.SysFont('arial', 25)
            self.height = HEIGHT
            self.width = WIDTH
            self.display = p.display.set_mode((self.width, self.height))
            p.display.set_caption('Monopoly')
            self.clock = p.time.Clock()
        # General
        self.number_of_players = number_of_players
        self.board = init_game_board(np.zeros(self.number_of_players, dtype="int"), self.number_of_players)
        self.player_turn = 1
        self.player_position = 0
        self.bankrupt_players = np.zeros(self.number_of_players, dtype="bool")
        # Houses
        self.number_of_available_houses = 32
        self.number_of_available_hotels = 12
        self.houses = init_property()
        self.hotels = init_property()
        # Chance & Community Cards
        self.chance_cards = {0: "Advance To Go",
                             1: "Advance To Red3",
                             2: "Advance To Purple1",
                             3: "Advance To Nearest Utility",
                             4: "Advance To Nearest Rail",
                             5: "Collect 50",
                             6: "Get Out of Jail Free",
                             7: "Go Back 3",
                             8: "Go To Jail",
                             9: "Property Repairs",
                             10: "Pay 15",
                             11: "Advance To Rail1",
                             12: "Advance To Blue2",
                             13: "Pay Each Player 50",
                             14: "Collect 150"}
        self.community_cards = {0: "Advance To Go",
                                1: "Collect 200",
                                2: "Pay 50",
                                3: "Collect 50",
                                4: "Get Out of Jail Free",
                                5: "Got To Jail",
                                6: "Collect 50 Each Player",
                                7: "Collect 100",
                                8: "Collect 20",
                                9: "Collect 100",
                                10: "Pay 100",
                                11: "Pay 150",
                                12: "Collect 25",
                                13: "Property Repairs",
                                14: "Collect 10",
                                15: "Collect 100"}
        self.used_chance_cards = {}
        self.used_community_cards = {}
        # Player Details
        self.player_money = np.ones(number_of_players, dtype="int") * 1500
        self.number_of_turns_in_jail = np.zeros(number_of_players, dtype="int")
        self.free_jail = np.zeros((2, self.number_of_players), dtype="int")  # row represents chance or community
        self.owned_property = init_property()
        self.doubles_rolled = 0
        self.current_roll = roll_dice()

    def update_ui(self):
        self.display.fill("white")
        board_image = draw_gameboard(os.path.join('assets', "board.png"))
        self.display.blit(board_image.image, board_image.rect)

        # Draw Current Roll
        text = self.font.render(f"Player {self.player_turn} rolled {self.current_roll}", True, (0, 0, 0))
        self.display.blit(text, [550, self.height / 2])

        # Draw Players
        for player in range(self.number_of_players):
            position = player_pos_px(np.where(self.board[:, player] == 1)[0][0])
            p.draw.rect(self.display, PLAYER_COLOR[player], p.Rect(position[0] + player, position[1] + player, PLAYER_SIZE, PLAYER_SIZE))

        # Debugging
        text = self.font.render(f"Player 1 is at board position {self.player_position}", True, (0, 0, 0))
        self.display.blit(text, [550, self.height / 4])

        # TODO: Draw Owned Properties
        # TODO: Draw Houses

    def roll_dice(self):
        self.current_roll = roll_dice()
        if self.current_roll[0] == self.current_roll[1]:
            self.doubles_rolled += 1
        else:
            self.doubles_rolled = 0

    def move_player(self, player):
        previous_location = np.where(self.board[:, player] == 1)[0][0]
        new_location = (previous_location + sum(self.current_roll)) % 40
        self.board[previous_location, player] = 0  # Remove Old Position
        self.board[new_location, player] = 1
        self.player_position = new_location

    def collect_go(self, player):
        self.player_money[player] += 200

    def pay_rent(self, player_to_pay, player_to_earn, number_of_houses, property_tuple):
        self.player_money[player_to_earn] += rent(property_tuple, number_of_houses, sum(self.current_roll))
        self.player_money[player_to_pay] -= rent(property_tuple, number_of_houses, sum(self.current_roll))

    def buy_property(self, player, property_tuple):
        self.player_money[player] -= cost_property(property_tuple)
        self.owned_property[property_tuple[0]][
            property_tuple[1] - 1] = player + 1  # adjust so player goes starts from 1

    def resolve_chance_card(self, key, player):

        previous_player_position = self.player_position

        if key == 0:  # Advance to go
            self.board[previous_player_position, player] = 0  # Remove Old Position
            self.board[0, player] = 1
        elif key == 1:  # Advance to Red3
            self.board[previous_player_position, player] = 0
            self.board[24, player] = 1
        elif key == 2:  # Advance to Purple1
            self.board[previous_player_position, player] = 0
            self.board[11, player] = 1
        elif key == 3:  # Advance to Nearest Utility
            self.board[previous_player_position, player] = 0
            # Can only be in one of 3 places
            if previous_player_position == 7:
                self.board[12, player] == 1
            elif previous_player_position == 22:
                self.board[28, player]
            elif previous_player_position == 36:
                self.board[12, player] == 1
        elif key == 4:  # Advance to nearest rail
            self.board[previous_player_position, player] = 0
            # Can only be in one of 3 places
            if previous_player_position == 7:
                self.board[15, player] == 1
            elif previous_player_position == 22:
                self.board[25, player]
            elif previous_player_position == 36:
                self.board[5, player] == 1
        elif key == 5:  # Collect 50
            self.player_money[player] += 50
        elif key == 6:  # Get Out of Jail Free
            self.free_jail[0, player] += 1
        elif key == 7:  # Go Back 3:
            self.board[previous_player_position, player] = 0
            # Can only be in one of 3 places
            if previous_player_position == 7:
                self.board[4, player] == 1
            elif previous_player_position == 22:
                self.board[19, player]
            elif previous_player_position == 36:
                self.board[33, player] == 1
        elif key == 8:  # Go To Jail
            self.board[previous_player_position, player] = 0
            # Checks for jail happens outside this function
            self.board[30, player] = 1
        elif key == 9:  # Property Repairs
            None
        elif key == 10:  # Pay 15
            self.player_money[player] -= 15
        elif key == 11:  # Advance to Rail1
            self.board[previous_player_position, player] = 0
            self.board[5, player] = 1
        elif key == 12:  # Advance to Mayfair
            self.board[previous_player_position, player] = 0
            self.board[39, player] = 1
        elif key == 13:  # Pay Each Player 50
            self.player_money[player] -= sum(self.bankrupt_players) * 50
            for id in range(self.number_of_players):
                if self.bankrupt_players[id] == 0:
                    self.player_money[id] += 50
        elif key == 14:  # Collect 150
            self.player_money[player] += 150

    def resolve_community_card(self, key, player):

        previous_player_position = self.player_position

        if key == 0:  # Advance to go
            self.board[previous_player_position, player] = 0  # Remove Old Position
            self.board[0, player] = 1
        elif key == 1:  # Collect 200
            self.player_money[player] += 200
        elif key == 2:  # Pay 50
            self.player_money[player] -= 50
        elif key == 3:  # Collect 50
            self.player_money[player] += 50
        elif key == 4:  # Get Out of Jail Free
            self.free_jail[1, player] += 1
        elif key == 5:  # Go To Jail
            self.board[previous_player_position, player] = 0
            # Checks for jail happens outside this function
            self.board[30, player] = 1
        elif key == 6:  # Collect 50 From Each Player
            self.player_money[player] += sum(self.bankrupt_players) * 50
            for id in range(self.number_of_players):
                if self.bankrupt_players[id] == 0:
                    self.player_money[id] -= 50
        elif key == 7:  # Collect 100
            self.player_money[player] += 100
        elif key == 8:  # Collect 20
            self.player_money[player] += 20
        elif key == 9:  # Collect 100
            self.player_money[player] += 100
        elif key == 10:  # Pay 100
            self.player_money[player] -= 100
        elif key == 11:  # Pay 150
            self.player_money[player] -= 150
        elif key == 12:  # Collect 25
            self.player_money[player] += 25
        elif key == 13:  # Property Repairs
            None
        elif key == 14:  # Collect 10
            self.player_money[player] += 10
        elif key == 15:
            self.player_money[player] += 100
