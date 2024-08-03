import json
from os import system,name
import time
MAP_FILE = 'cave_map.txt'
HELP_FILE = 'help.txt'
SAVE_FILE = 'save_game.json'
def clear():
    """Clears the screen."""
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
    return input().strip().lower()

def display_map(grid: list[list[str]], player_position: list[int], inventory: list[str]) -> None:
    """Displays the map."""
    grid_copy = [row.copy() for row in grid]
    x, y = player_position
    grid_copy[x][y] = '🧝'
    
    emoji_map = {'-': '🧱', '*': '🟢', 'S': '🏠', 'F': '🏺', 'I': '🗝️'}
    print()
    for row in grid_copy:
        print("".join(emoji_map.get(cell, cell) for cell in row))
    print()
    print(f"Inventory: {', '.join(inventory) if inventory else 'Empty'}")

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
        directions.append('North')
    if is_inside_grid(grid, [row + 1, col]) and grid[row + 1][col] in allowed_objects:
        directions.append('South')
    if is_inside_grid(grid, [row, col + 1]) and grid[row][col + 1] in allowed_objects:
        directions.append('East')
    if is_inside_grid(grid, [row, col - 1]) and grid[row][col - 1] in allowed_objects:
        directions.append('West')
        
    return directions

def move(direction: str, player_position: list[int], grid: list[list[str]]) -> bool:
    """Moves the player in the given direction."""
    if direction not in look_around(grid, player_position):
        return False
    
    if direction == 'North':
        player_position[0] -= 1
    elif direction == 'South':
        player_position[0] += 1
    elif direction == 'East':
        player_position[1] += 1
    elif direction == 'West':
        player_position[1] -= 1
    
    return True

def check_finish(grid: list[list[str]], player_position: list[int]) -> bool:
    """Checks if the player has reached the exit."""
    return grid[player_position[0]][player_position[1]] == 'F'

def display_help() -> None:
    """Displays a list of commands."""
    with open(HELP_FILE, 'r') as file:
        print(file.read())

def save_game(player_position: list[int], inventory: list[str], grid: list[list[str]]) -> None:
    """Saves the current game state to a file."""
    game_state = {
        'player_position': player_position,
        'inventory': inventory,
        'grid': grid
    }
    with open(SAVE_FILE, 'w') as file:
        json.dump(game_state, file)
    print("Game saved successfully.")

def load_game() -> tuple:
    """Loads the game state from a file."""
    with open(SAVE_FILE, 'r') as file:
        game_state = json.load(file)
    print("Game loaded successfully.")
    return game_state['player_position'], game_state['inventory'], game_state['grid']

def main():
    """Main entry point for the game."""
    grid = load_map(MAP_FILE)
    player_position = find_start(grid)
    inventory = []
    score = 0
    print('Welcome to the game!')
    time.sleep(2)
    print()
    print(f"This is the {MAP_FILE[0].upper()}{MAP_FILE[1:len(MAP_FILE)-8]} map")
    time.sleep(2)
    clear()
    display_map(grid, player_position, inventory)
    print('You can go', ', '.join(look_around(grid, player_position)))
    
    while True:
        command = get_command()
        
        if command == 'escape':
            print("Exiting the game.")
            break
        elif command == 'show map':
            display_map(grid, player_position, inventory)
        elif command.startswith('go '):
            direction = command.split()[1]
            if move(direction, player_position, grid):
                print(f'You have moved {direction}')
                clear()
                display_map(grid, player_position, inventory)
                if grid[player_position[0]][player_position[1]] == 'I':
                    print('You found an item!')
                    inventory.append('Item')
                    grid[player_position[0]][player_position[1]] = '*'
                    score += 10
                if check_finish(grid, player_position):
                    print('Congratulations! You have reached the exit!')
                    print(f'Your final score is: {score}')
                    break
                else:
                    print('You can go', ', '.join(look_around(grid, player_position)))
            else:
                print('There is no way here')
                print('You can go', ', '.join(look_around(grid, player_position)))
        elif command == 'help':
            clear()
            display_map(grid, player_position, inventory)
            display_help()
        elif command == 'save':
            save_game(player_position, inventory, grid)
        elif command == 'load':
            player_position, inventory, grid = load_game()
            display_map(grid, player_position, inventory)
        else:
            clear()
            display_map(grid, player_position, inventory)
            print("I do not understand.")
            print('You can go', ', '.join(look_around(grid, player_position)))

if __name__ == '__main__':
    main()
