from os import system, name
import time
import random
import json

# Choose a random map from the given list of maps
mapfiles = ["cave_map.txt", "arcadian_map.txt", "ghost_town_map.txt", "cloud_map.txt"]
rando_num = random.randint(0, len(mapfiles)-1)
MAP_FILE = mapfiles[rando_num]


def clear():
    """Clears the screen."""
    # for windows
    if name == 'nt':
        _ = system('cls')


def load_map(map_file: str) -> list[list[str]]:
    """Loads a map from a file as a grid (list of lists)."""
    with open(map_file, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]


def find_start(grid: list[list[str]]) -> list[int]:
    """Finds the starting position of the player on the map."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return [row, col]
    raise ValueError("No starting position 'S' found in the map.")


def get_command() -> str:
    """Gets a command from the user."""
    return input(">> ").strip().lower()


def display_map(grid: list[list[str]], player_position: list[int]) -> None:
    """Displays the map."""
    grid_copy = [row.copy() for row in grid]
    x, y = player_position
    grid_copy[x][y] = '🧝'
    
    emoji_map = {'-': '🧱', '*': '🟢', 'S': '🏠', 'F': '🏺', 'I': '🗝️'}
    
    for row in grid_copy:
        print("".join(emoji_map.get(cell, cell) for cell in row))


def get_grid_size(grid: list[list[str]]) -> list[int]:
    """Returns the size of the grid."""
    return [len(grid), len(grid[0])]


def is_inside_grid(grid: list[list[str]], position: list[int]) -> bool:
    """Checks if a given position is valid (inside the grid)."""
    rows, cols = get_grid_size(grid)
    return 0 <= position[0] < rows and 0 <= position[1] < cols


def look_around(grid: list[list[str]], player_position: list[int]) -> list[str]:
    """Returns the allowed directions."""
    allowed_objects = ('S', 'F', '*', 'I')
    directions = []
    row, col = player_position
    
    if is_inside_grid(grid, [row - 1, col]) and grid[row - 1][col] in allowed_objects:
        directions.append('north')
    if is_inside_grid(grid, [row + 1, col]) and grid[row + 1][col] in allowed_objects:
        directions.append('south')
    if is_inside_grid(grid, [row, col + 1]) and grid[row][col + 1] in allowed_objects:
        directions.append('east')
    if is_inside_grid(grid, [row, col - 1]) and grid[row][col - 1] in allowed_objects:
        directions.append('west')
        
    return directions


def move(direction: str, player_position: list[int], grid: list[list[str]]) -> bool:
    """Moves the player in the given direction."""
    if direction not in look_around(grid, player_position):
        return False
    
    if direction == 'north':
        player_position[0] -= 1
    elif direction == 'south':
        player_position[0] += 1
    elif direction == 'east':
        player_position[1] += 1
    elif direction == 'west':
        player_position[1] -= 1
    
    return True


def check_finish(grid: list[list[str]], player_position: list[int]) -> bool:
    """Checks if the player has reached the exit."""
    return grid[player_position[0]][player_position[1]] == 'F'


def check_key(grid: list[list[str]], player_position: list[int]) -> bool:
    """Checks if the player has reached the key."""
    return grid[player_position[0]][player_position[1]] == 'I'


def display_help() -> None:
    """Displays a list of commands."""
    with open('help.txt', 'r') as file:
        print(file.read())


def save_game(filename: str, grid: list[list[str]], player_position: list[int], inventory: int) -> None:
    """Saves the current game state to a file."""
    game_state = {
        'grid': grid,
        'player_position': player_position,
        'inventory': inventory,
        'map_file': MAP_FILE
    }
    with open(filename, 'w') as file:
        json.dump(game_state, file)
    print(f"Game saved to {filename}")


def load_game(filename: str) -> tuple[list[list[str]], list[int], int]:
    """Loads the game state from a file."""
    with open(filename, 'r') as file:
        game_state = json.load(file)
    return game_state['grid'], game_state['player_position'], game_state['inventory']


def main():
    """Main entry point for the game."""
    global MAP_FILE
    try:
        grid, player_position, inventory = load_game('savegame.json')
        print("Loaded saved game.")
    except FileNotFoundError:
        grid = load_map(MAP_FILE)
        player_position = find_start(grid)
        inventory = 0
        print('Welcome to the game!')
        time.sleep(2)
        clear()

    display_map(grid, player_position)
    if inventory == 0:
        print("The Inventory is empty!")
    print('You can go', ', '.join(look_around(grid, player_position)))
    
    while True:
        command = get_command()

        if command == 'escape':
            print("Exiting the game.")
            print(f"You have finished with {inventory*10} points")
            break
        elif command == 'show map':
            display_map(grid, player_position)
        elif command.startswith('go '):
            direction = command.split()[1]
            if move(direction, player_position, grid):
                clear()
                if check_finish(grid, player_position):
                    print('Congratulations! You have reached the exit!')
                    print(f"You have finished with {inventory*10} points")
                    break
                elif check_key(grid, player_position):
                    print('Congratulations! You have collected the key!')
                    inventory += 1
                    print(f"You have collected {inventory} {'item' if inventory == 1 else 'items'}")
                    display_map(grid, player_position)
                    print('You can go', ', '.join(look_around(grid, player_position)))
                else:
                    display_map(grid, player_position)
                    print('You can go', ', '.join(look_around(grid, player_position)))
            else:
                print('There is no way here')
                print('You can go', ', '.join(look_around(grid, player_position)))
        elif command == 'help':
            display_help()
        elif command == 'inventory':
            print(f"You have collected {inventory} {'item' if inventory == 1 else 'items'}")
        elif command == 'save':
            save_game('savegame.json', grid, player_position, inventory)
        elif command == 'load':
            grid, player_position, inventory = load_game('savegame.json')
            print("Game loaded.")
            clear()
            display_map(grid, player_position)
            print('You can go', ', '.join(look_around(grid, player_position)))
        else:
            print("I do not understand.")
            print('You can go', ', '.join(look_around(grid, player_position)))


if __name__ == '__main__':
    main()
