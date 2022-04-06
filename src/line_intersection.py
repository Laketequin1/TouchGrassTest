def det(a, b): # Get denominator value
        return a[0] * b[1] - a[1] * b[0]

def line_intersection(platform_line, player_line, side): # Return the intercept pos of two lines. If the lines do not intercept return False
    xdiff = (platform_line[0][0] - platform_line[1][0], player_line[0][0] - player_line[1][0]) # Differences of x cordiante on both lines
    ydiff = (platform_line[0][1] - platform_line[1][1], player_line[0][1] - player_line[1][1]) # Differences of y cordiante on both lines
    
    div = det(xdiff, ydiff)
    if div == 0: # Lines do not intercept
       return False

    d = (det(*platform_line), det(*player_line))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    
    if side == 'x':
        if platform_line[0][0] != platform_line[1][0]:
            raise Exception('Platform lines are not square')
        
        if y < min(platform_line[0][1], platform_line[1][1]) or y > max(platform_line[0][1], platform_line[1][1]) or y < min(player_line[0][1], player_line[1][1]) or y > max(player_line[0][1], player_line[1][1]):
            return False
    elif side == 'y':
        if platform_line[0][1] != platform_line[1][1]:
            raise Exception('Platform lines are not square')
        
        #print(f"Platform: {platform_line[0][0], platform_line[1][0]}")
        #print(f"Player: {player_line[0][0], player_line[1][0]}")
        
        if x < min(platform_line[0][0], platform_line[1][0]) or x > max(platform_line[0][0], platform_line[1][0]) or x < min(player_line[0][0], player_line[1][0]) or x > max(player_line[0][0], player_line[1][0]):
            return False
    else:
        raise Exception("Side input needs to be either 'x' or 'y'")
        
    return x, y