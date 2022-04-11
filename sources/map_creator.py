# The # character states that a custom block exists there. It acts as a comment, and does nothing except skip the block (like a space)

BLOCK_WIDTH = 40 # Width of blocks

NORMAL_BLOCKS = {'p':'Platform', 'e':'Enemy', 'g':'Grass'} # All blocks just needing pos
DIRECTIONS = {'^':'"up"', '<':'"left"', '_':'"down"', '>':'"right"', 'x':'"slow"'} # Directions for Booster
ENEMY_INVINCIBLE = 'i'

line = "" # String with blocks line
lines_input = [] # List will all lines

width = int(input("Width: ")) # Width of map in pixels
height = int(input("Height: ")) # Height of map in pixels

if height % BLOCK_WIDTH != 0: # If map height is not makable with blocks
    raise Exception("Map height is not makable with blocks!") # Error
elif width % BLOCK_WIDTH != 0: # If map width is not makable with blocks
    raise Exception("Map width is not makable with blocks!") # Error

y_block_height = int(height / BLOCK_WIDTH) # Get height of map in blocks
x_block_height = int(width / BLOCK_WIDTH) # Get width of map in blocks

print(f"\nBlock Height: {y_block_height}")
print(f"Block Width:  {x_block_height}")

x_indicator = "\n" # Indicator for width

for x in range(x_block_height): # Set indicator width
    x_indicator += '-' # Indicator block

print(x_indicator) # Print indicator

for x in range(y_block_height): # For every block in map block height
    line_input = input() # Get input for block
    lines_input.append(line_input) # Add to list

for j, line_input in enumerate(lines_input): # For each line
    for i, char in enumerate(line_input): # For each character
        
        if char in NORMAL_BLOCKS: # Get block for char
            line += f"{ NORMAL_BLOCKS[char] }(({ BLOCK_WIDTH * i }, { height - BLOCK_WIDTH * (j + 1) })), " # Add block to line
            
        elif char in DIRECTIONS: # If direction in directions
            direction = DIRECTIONS[char] # Get direction of booster
            
            line += f"Booster(({ BLOCK_WIDTH * i }, { height - BLOCK_WIDTH * (j + 1) }), { direction }), " # Add block to line
        
        elif char == ENEMY_INVINCIBLE: # Invincible enemy
            line += f"Enemy(({ BLOCK_WIDTH * i }, { height - BLOCK_WIDTH * (j + 1) }), True), " # Add block to line
        
        elif char != ' ' and char != '#': # Is not a space or comment
            raise Exception(f"Unknown letter {char} inputed!") # Error
    
    line += '\n' # New line to keep code clean

while '\n\n' in line: # Keep running while there are double newlines
    line = line.replace('\n\n', '\n') # Remove double newlines

print() # Newline
print(line[0:len(line) - 3]) # Print line removing last comma and space
