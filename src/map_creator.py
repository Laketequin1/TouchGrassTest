BLOCK_WIDTH = 40 # Width of blocks

NORMAL_BLOCKS = {'p':'Platform', 'e':'Enemy', 'g':'Grass'} # All blocks just needing pos

DIRECTIONS = {'^':'up', '<':'left', '_':'down', '>':'right'} # Directions for Booster

line = "" # String with blocks line

y_pos = input("Y Pos: ") # Inputs
height = input("Height: ") # Height of map in pixels
width = input("Width: ") # Width of map in pixels

'''
Get map size in blocks
Add indicator for width
Get input with amount of lines (Readlines(x))
'''
line_input = input("Enter Line: ") # Blocks input

for i, char in enumerate(line_input): # For each character
    if char in NORMAL_BLOCKS: # Get block for char
        line += f"{ NORMAL_BLOCKS[char] }(({ BLOCK_WIDTH * (i + 1) }, { y_pos })), " # Add block to line
        
    elif char in DIRECTIONS: # If direction in directions
        direction = DIRECTIONS[char] # Get direction of booster
        
        line += f"Booster(({ BLOCK_WIDTH * (i + 1) }, { y_pos }), { direction }), " # Add block to line
    
    elif char != ' ': # Is not a space
        raise Exception("Unknown letter inputed!") # Error

print(line[0:len(line) - 3]) # Print line removing last comma and space
