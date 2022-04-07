BLOCK_WIDTH = 40 # Width of blocks

NORMAL_BLOCKS = {'p':'Platform', 'e':'Enemy', 'g':'Grass'} # All blocks just needing pos
SPECIAL_BLOCKS = {'b':'Booster'} # Blocks that have extra stuff

DIRECTIONS = {'8':'up', '4':'left', '2':'down', '6':'right'} # Directions for Booster

line = "" # String with blocks line

y_pos = input("Y Pos: ") # Inputs
line_input = input("Enter Line: ")

for i, char in enumerate(line_input): # For each character
    if char in NORMAL_BLOCKS: # Get block for char
        line += f"{ NORMAL_BLOCKS[char] }(({ BLOCK_WIDTH * (i + 1) }, { y_pos })), " # Add block to line
        
    elif char in SPECIAL_BLOCKS: # Get block for char booster
        
        raw_direction = line_input[i + 1] # Get next char
        
        if raw_direction in DIRECTIONS: # If direction in directions
            direction = DIRECTIONS[raw_direction] # Get direction of booster
        else:
            raise Exception("No direction stated for a booster! (8, 4, 2, 6)") # Error
        
        line += f"{ SPECIAL_BLOCKS[char] }(({ BLOCK_WIDTH * (i + 1) }, { y_pos }), { direction }), " # Add block to line
    
    elif char != ' ' and not char in DIRECTIONS: # Is not a space
        raise Exception("Unknown letter inputed!") # Error

print(line) # Print line