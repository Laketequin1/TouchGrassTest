#A custom made import that interacts with collisions
	
def CheckCollisionList(rect_list1, rect_list2): #A function that checks if any rectangles from a list are inside any rectangles from the other list, returning True if there is a collision, and False if there is not. Takes input as StaticMethod.CheckCollisionList( [ [x_pos, y_pos, width, height], [x_pos, y_pos, width, height] ], [ [x_pos, y_pos, width, height], [x_pos, y_pos, width, height] ] )
	
	is_collision = False #There is no collision
	
	for rect1 in rect_list1: #Gets each square in list 1
		if not is_collision: #If collision not been detected so far
			rectX1 = rect1[0] #Simplify rect to individual variables
			rectY1 = rect1[1]
			rect_width1 = rect1[2]
			rect_height1 = rect1[3]
		
			for rect2 in rect_list2: #Gets each square in list 2
				if not is_collision: #If collision not been detected so far
					rectX2 = rect2[0] #Simplify rect to individual variables
					rectY2 = rect2[1]
					rect_width2 = rect2[2]
					rect_height2 = rect2[3]
				
					if rectX2 < rectX1 + rect_width1 and rectX1 < rectX2 + rect_width2 and rectY2 < rectY1 + rect_height1 and rectY1 < rectY2 + rect_height2: #Checks: If the left of square2 is smaller than the right of square1; If the left of square1 is smaller than the right of square2; If the top of square1 is smaller than the bottom of square2; If the bottom of square1 is smaller than the top of square2
						is_collision = True #If all that is true, the squares collide, so we set is_collision to True
	
	return is_collision #We return is_collision state, True if we collided, False if we didn't

def CheckCollision(rect1, rect2): #A function that checks the two rectangles are colliding, returning True if there is a collision, and False if there is not. Takes input as Collision.CheckCollision( [x_pos, y_pos, width, height], [x_pos, y_pos, width, height] )
	
	is_collision = False #There is no collision
	
	#Square 1
	rectX1 = rect1[0] #Simplify rect to individual variables
	rectY1 = rect1[1]
	rect_width1 = rect1[2]
	rect_height1 = rect1[3]
	
	
	#Square 2
	rectX2 = rect2[0] #Simplify rect to individual variables
	rectY2 = rect2[1]
	rect_width2 = rect2[2]
	rect_height2 = rect2[3]
	
	if rectX2 < rectX1 + rect_width1 and rectX1 < rectX2 + rect_width2 and rectY2 < rectY1 + rect_height1 and rectY1 < rectY2 + rect_height2: #Checks: If the left of square2 is smaller than the right of square1; If the left of square1 is smaller than the right of square2; If the top of square1 is smaller than the bottom of square2; If the bottom of square1 is smaller than the top of square2
		is_collision = True #If all that is true, the squares collide, so we set is_collision to True
		
	return is_collision #We return is_collision state, True if we collided, False if we didn't

def Main(): #As this is an import, we use this to make sure Main() only runs when this is specifically started, not imported
	
	def Console(): #To repeat proccess
		
		user_input = input("CheckCollision: 1, CheckCollisionList: 2  -  ") #Asks user what he is using, CheckCollision which they have to type 1, or CheckCollisionList which they have to type 2
		
		if user_input == "1": #If 1 typed
			print(CheckCollision(input("Rect1  -  "), input("Rect2  -  "))) #Run function with the inputs
		elif user_input == "2": #If 2 typed
			print(CheckCollision(input("Rect_list1  -  "), input("Rect_list2  -  "))) #Run function with the inputs
		else: #Option not correctly accepted
			print("Not correct choice") #Tell user off, and continue
			
		Console() #Run again
			
	Console() #Start Console
	
if __name__ == "__main__": #As this is an import, we use this to make sure Main() only runs when this is specifically started, not imported
	Main() #Run Main()
