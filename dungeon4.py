'''this version loads the map prints it as a list and prints the starting position. if the user enters the word escapes then it quits the game otherwise it prints i dont understand. futhermore
it sees where it can move. if the usere enters a valid move posn then it moves ie the @ moves otherwise it doesnt move. also it converts all items in the grid to emojis and if the pla
yer reaches the end posn then it prints a congrats msg. if the players types help then a help.txt file is printed
author- saumya patel
date- 17/11/2023'''


MAP_FILE = 'cave_map.txt'

def load_map(map_file: str) -> list[list[str]]:
    """
    Loads a map from a file as a grid (list of lists)
    """
    #opens the files and uses readlines function, removes the newline and appends each elemtent into the grid list
    file_open = open(map_file, 'r')
    file = file_open.readlines()
    grid = []
    for i in file:
        remove = i.strip()
        grid.append(list(remove))
    return grid
    

def find_start(grid: list[list[str]]) -> list[int, int]:
    """
    Finds the starting position of the player on the map.
    """
    #grid2 created to be empty so that the S can be found in the nested list and its coordinates can be printed 
    grid2 = []
    for row1 in range(len(grid)): #iterates through each row
        for col1 in range(len(grid[row1])): #iterates throught each column/ elements in each row 
            if grid[row1][col1] == 'S': #if s is found then it appends it into the new list 
                grid2.append(row1)
                grid2.append(col1)
                return grid2 #prints the starting posn

def get_command() -> str:
    """
    Gets a command from the user.
    """
    user_input = input() #takes input from user
    return user_input

def display_map(grid: list[list[str]], player_position: list[int, int]) -> None:
    """
    Displays the map.
    """
    grid1 = []
    for row2 in grid:
        a_row = []
        for col2 in row2:
            a_row.append(col2)
        grid1.append(a_row)
    x_player_position = player_position[0]
    y_player_position = player_position[1]
    grid1[x_player_position][y_player_position]= '🧝'
    for i in range(len(grid1)):
        grid1_row = ''
        for j in range(len(grid1[i])):
            symbols_posn = grid1[i][j]
            if symbols_posn=='-':
                symbols_posn = '🧱'
            elif symbols_posn == '*':
                symbols_posn = '🟢'
            elif symbols_posn == 'S':
                symbols_posn = '🏠'
            elif symbols_posn =='F':
                symbols_posn = '🏺'
            grid1_row+=symbols_posn
        print(grid1_row)

def get_grid_size(grid: list[list[str]]) -> list[int, int]:
    """
    Returns the size of the grid.
    """
    row_numbers = len(grid) #will check the length of the grid to print the number of rows
    col_numbers = len(grid[0]) #will check the the length of the zeroth elements of a square matrix 
    return [row_numbers,col_numbers]

def is_inside_grid(grid: list[list[str]], position: list[int, int]) -> bool:
    """
    Checks if a given position is valid (inside the grid).
    """
    grid_rows, grid_cols = get_grid_size(grid)
    if (grid_rows-1 >= position[0]and position[0]>=0) and (grid_cols-1 >= position[1] and position[1]>=0):
        return True
    else:
        return False
    

def look_around(grid: list[list[str]], player_position: list[int, int]) -> list:
    """
    Returns the allowed directions.
    """
    allowed_objects = ('S', 'F', '*')
    row = player_position[0]
    col = player_position[1]
    directions = []
    if is_inside_grid(grid, [row - 1, col]) and grid[row - 1][col] in allowed_objects: #row-1 is moving one row up which is north
        directions.append('north')
    else:
        pass
    if is_inside_grid(grid, [row+1, col]): #moving one row down is row+1 ie south
        if grid[row+1][col] in allowed_objects:
            directions.append('south')
    else:
        pass
    if is_inside_grid(grid, [row, col+1]):  #moving one col left is col-1 ie east
        if grid[row][col+1] in allowed_objects:
            directions.append('east')
    else:
        pass

    if is_inside_grid(grid, [row, col-1]): #moving one col right is col+1 ie west
        if grid[row][col-1] in allowed_objects:
            directions.append('west')
    else: 
            pass
    return directions

def move(direction: str, player_position: list[int, int], grid: list[list[str]]) -> bool:
    
    '''Moves the player in the given direction.'''
    if direction not in look_around(grid,player_position):
        return False
    elif direction in look_around(grid,player_position):
        if direction.lower() == 'north': # player_pos[0] means row and row-1 is north
            player_position[0]-=1
        elif direction.lower() == 'west':# player_pos[1] means col and col-1 is west
            player_position[1]-=1
        elif direction.lower() == 'east': # player_pos[1] means col and col+1 is east
            player_position[1]+=1
        elif direction.lower() == 'south':# player_pos[0] means row and row+1 is south
            player_position[0]+=1
        return True
    

def check_finish(grid: list[list[str]], player_position: list[int, int]) -> bool:
    """
    Checks if the player has reached the exit.
    """
    if grid[player_position[0]][player_position[1]]=='F':
        return True
    else:
        return False

def display_help() -> None:
    """
    Displays a list of commands.
    """
    file_open = open('help.txt', 'r')
    file = file_open.read()
    return file


def main():
    
    '''Main entry point for the game.'''
    
    grid = load_map('cave_map.txt') #loads and prints grid for the file as a nested list
    
    player_position = find_start(grid)
    
    display_map(grid,player_position)
    
    
    print('the starting postion is: ' , player_position) #function that finds the starting posn for the grid is called
    
    get_grid_size(grid) #gets the size of the grid
    
    is_inside_grid(grid, player_position) #checks if player position is valid or not
    
    print('you can go', ', '.join(look_around(grid,player_position)))
    get_command_function=True #assigned true to a variable so it can be used in the while loopy
    
    while get_command_function and is_inside_grid(grid,player_position): #while loop used to call the get command function 
        user = get_command()
        if user == 'escape':
            get_command_function = False # used so that the while loop doesnt repeat
        
        elif user.lower() == 'show map':
            display_map(grid,player_position)
        #Based upon userinput these following funcs convert input to lower case call the lookaround function after mmoving the @ and then check where else u can move
        #if the user enters directions apart from the allowed direction in which he/she is allowed to go then it will tell theres no way here
        #if the player reaches F then it prints congragulations.....
        elif user.lower() == 'go north':
            if move('north',player_position,grid):
                print('you have moved north')
                if check_finish(grid,player_position):
                    print('congragulations! you have reached the exit!')
                    exit()
                else:
                    m = ', '.join(look_around(grid,player_position))
                    print(m)
                print('you can go', m )
        
            else:
                print('there is no way here')
                print('you can go ', ','.join(look_around(grid,player_position)))
            
        

        elif user.lower() == 'go south':
            if move('south',player_position,grid):
                print('you have moved south')
                if check_finish(grid,player_position):
                    print('congragulations!, you have reached the exit!')
                    exit()
                else:
                    m = ', '.join(look_around(grid,player_position))
                    print('you can go', m )
            
            else:
                print('there is no way here')
                print('you can go', ','.join(look_around(grid,player_position)))

       
        elif user.lower() == 'go east':
            if move('east',player_position,grid):
                print('you have moved east')
                if check_finish(grid,player_position):
                    print('congragulations!, you have reached the exit!')
                    exit()
                else:
                    m = ', '.join(look_around(grid,player_position))
                    print('you can go', m )
            else:
                print('there is no way here')
                print('you can go', ','.join(look_around(grid,player_position)))
    
        
        elif user.lower() == 'go west':
            if move('west',player_position,grid):
                print('you have moved west')
                if check_finish(grid,player_position):
                    print('congragulations!, you have reached the exit!')
                    exit()
                else: 
                    m = ', '.join(look_around(grid,player_position))
                    print('you can go', m )
            else:
                print('there is no way here')
                print('you can go', ','.join(look_around(grid,player_position)))
        elif user.lower()=='help': #it will display the help.txt if the user types help
            dis_help = display_help()
            print(dis_help)
            print('you can go', ','.join(look_around(grid,player_position)))
        else: #if its not escape then prints i dont understand and loop repeats
            print("I do not understand.")
            print('you can go', ','.join(look_around(grid,player_position)))


if __name__ == '__main__':
    main()

