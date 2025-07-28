import random
import time
from collections import Counter

wind = ['wind east', 'wind south', 'wind west', 'wind north', 'wind red', 'wind green']
bing = ['bing ' + str(i) for i in range(1, 10)]
tiao = ['tiao ' + str(i) for i in range(1, 10)]
wan = ['wan ' + str(i) for i in range(1, 10)]

all_tiles = 4 * (wind + bing + tiao + wan)

def sort_tiles(tiles):
    wind_tiles = [tile for tile in tiles if 'wind' in tile]
    tiao_tiles = sorted([tile for tile in tiles if 'tiao' in tile], key=lambda x: int(x.split()[1]))
    wan_tiles = sorted([tile for tile in tiles if 'wan' in tile], key=lambda x: int(x.split()[1]))
    bing_tiles = sorted([tile for tile in tiles if 'bing' in tile], key=lambda x: int(x.split()[1]))
    return wind_tiles + tiao_tiles + wan_tiles + bing_tiles

def draw_tile(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def initialize_game(deck):
    player_tiles = [draw_tile(deck) for _ in range(14)]
    other_players_tiles = [[draw_tile(deck) for _ in range(13)] for _ in range(3)]
    return sort_tiles(player_tiles), other_players_tiles

def display_tiles(player_tiles, completed_sets, penged_sets):
    print("\nYour tiles:", " | ".join(sort_tiles(player_tiles)))
    if completed_sets:
        print("Completed sets:", " | ".join(" | ".join(set_group) for set_group in completed_sets))
    if penged_sets:
        print("Penged sets:", " | ".join(" | ".join(set_group) for set_group in penged_sets))

def discard_tile(player_tiles):
    display_tiles(player_tiles, completed_sets=[], penged_sets=[])
    discard = input("Which tile would you like to discard? Type the exact name: ")
    if discard in player_tiles:
        player_tiles.remove(discard)
    else:
        print("Invalid tile. Try again.")
        return discard_tile(player_tiles)
    return discard

# Check if the player can peng
def can_peng(player_tiles, discard_tile):
    return player_tiles.count(discard_tile) == 2

# Check if the player can chi
def can_chi(player_tiles, discard_tile):
    if discard_tile.startswith("wind"):
        return False
    tile_number = int(discard_tile.split()[1])
    suit = discard_tile.split()[0]
    return (
        (f"{suit} {tile_number - 1}" in player_tiles and f"{suit} {tile_number + 1}" in player_tiles)
    )

def find_chi_options(player_tiles, discard_tile):
    if discard_tile.startswith("wind"):
        return [] 

    tile_number = int(discard_tile.split()[1])
    suit = discard_tile.split()[0]
    options = []

    if f"{suit} {tile_number - 1}" in player_tiles and f"{suit} {tile_number + 1}" in player_tiles:
        options.append((f"{suit} {tile_number - 1}", f"{suit} {tile_number + 1}"))

    return options

def process_chi(player_tiles, discard_tile, chi_tiles, completed_sets):
    completed_sets.append([discard_tile] + list(chi_tiles))

    player_tiles.remove(discard_tile)
    for tile in chi_tiles:
        player_tiles.remove(tile)

def check_win(player_tiles):
    tile_counter = Counter(player_tiles)

    pairs = 0
    sets_of_three = 0

    for tile, count in tile_counter.items():
        if count >= 3:
            sets_of_three += count // 3
        if count >= 2:
            pairs += 1 

    # Check for 4 sets of three and 1 pair or 7 pairs
    if sets_of_three >= 4 and pairs >= 1:
        print("\nCongratulations! You won with 4 sets of three and 1 pair!")
        return True
    elif sum(count // 2 for count in tile_counter.values()) >= 7:
        print("\nCongratulations! You won with 7 pairs!")
        return True

    return False

def ask_for_peng_or_chi(player_tiles, discard_tile, completed_sets, penged_sets, current_player_index):
    if can_peng(player_tiles, discard_tile):
        action = input(f"Would you like to Peng {discard_tile}? (y/n): ")
        if action.lower() == 'y':
            player_tiles.append(discard_tile)
            penged_sets.append([discard_tile] * 3) 
            return 'peng'

    if current_player_index == 4: 
        chi_options = find_chi_options(player_tiles, discard_tile)
        if chi_options:
            display_tiles(player_tiles, completed_sets, [])
            print(f"\nYou can Chi {discard_tile}. Choose tiles to form the set:")
            for i, option in enumerate(chi_options):
                print(f"Option {i + 1}: {', '.join(option)}")
            option_choice = int(input("Choose the option number: ")) - 1
            if 0 <= option_choice < len(chi_options):
                selected_tiles = chi_options[option_choice]
                action = input(f"Would you like to Chi {discard_tile} with {', '.join(selected_tiles)}? (y/n): ")
                if action.lower() == 'y':
                    return 'chi', selected_tiles

    return None

def ask_for_peng_or_chi(player_tiles, discard_tile, completed_sets, penged_sets, current_player_index):
    if can_peng(player_tiles, discard_tile):
        action = input(f"Would you like to Peng {discard_tile}? (y/n): ")
        if action.lower() == 'y':
            penged_sets.append([discard_tile] * 3)
            player_tiles = [tile for tile in player_tiles if tile != discard_tile][:11]
            print(f"\nYou penged {discard_tile}.")
            return 'peng'

    if current_player_index == 4:
        chi_options = find_chi_options(player_tiles, discard_tile)
        if chi_options:
            display_tiles(player_tiles, completed_sets, [])
            print(f"\nYou can Chi {discard_tile}. Choose tiles to form the set:")
            for i, option in enumerate(chi_options):
                print(f"Option {i + 1}: {', '.join(option)}")
            option_choice = int(input("Choose the option number: ")) - 1
            if 0 <= option_choice < len(chi_options):
                selected_tiles = chi_options[option_choice]
                action = input(f"Would you like to Chi {discard_tile} with {', '.join(selected_tiles)}? (y/n): ")
                if action.lower() == 'y':
                    completed_sets.append([discard_tile] + list(selected_tiles))
                    player_tiles = [tile for tile in player_tiles if tile not in selected_tiles][:11]
                    print(f"\nYou chi-ed {discard_tile}.")
                    return 'chi'

    return None

# Main game 

def main():
    deck = all_tiles.copy()
    random.shuffle(deck)
    player_tiles, other_players_tiles = initialize_game(deck)

    completed_sets = []  # Sets formed by Chi
    penged_sets = []     # Sets formed by Peng

    print("\nLet's test out your mahjong abilities!")
    input("Press Enter to continue...")

    print("\nYou have been dealt 14 tiles.")
    discard = discard_tile(player_tiles)
    discard_pile = [discard]
    print(f"\nYou discarded {discard}. Now you have 13 tiles.")

    current_player_index = 1  

    while True:
        time.sleep(2)

        if current_player_index == 1: 
            display_tiles(player_tiles, completed_sets, penged_sets)
            new_tile = draw_tile(deck)
            print(f"\nYou drew: {new_tile}")
            keep_tile = input(f"Would you like to keep {new_tile}? (y/n): ")
            if keep_tile.lower() == 'y':
                player_tiles.append(new_tile)
                discard = discard_tile(player_tiles)
                discard_pile.append(discard)
                print(f"\nYou discarded {discard}.")
            else:
                print(f"\nYou did not keep {new_tile}.")

        else: 
            discard = draw_tile(deck)
            print(f"\nPlayer {current_player_index} discarded: {discard}")
            discard_pile.append(discard)

            if current_player_index == 4 or can_peng(player_tiles, discard):
                action = ask_for_peng_or_chi(player_tiles, discard, completed_sets, penged_sets, current_player_index)
                if action:
                    if action == 'peng':
                        discard = discard_tile(player_tiles)
                        discard_pile.append(discard)
                        print(f"\nYou discarded {discard}.")
                        current_player_index = 2 
                    elif action == 'chi':
                        discard = discard_tile(player_tiles)
                        discard_pile.append(discard)
                        print(f"\nYou discarded {discard}.")
                        current_player_index = 2  

        print("\nCurrent discard pile:", " | ".join(discard_pile))
        if check_win(player_tiles):
            break

        current_player_index = (current_player_index + 1) % 4  # Rotate turns

if __name__ == "__main__":
    main()
