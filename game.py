import copy

# 1. Map to objects function
def map2objects(game_map):
    """Generates a dictionary with the coordinates of the robot, the boxes and the storages from a given map
    Args:
        my_map (str): Map of the game
    Returns:
        objects (list): Dictionary with the coordinates of the robot, the boxes, the storages and the blanks
    """
    blanks = []
    boxes = []
    storages = []
    y = game_map.count("\n")
    x = 0
    
    # Blanks are the empty spaces where the robot and the boxes can move.
    # In this case, the blanks are the spaces that are not walls. 
    for i in game_map:
        if i == "R":
            blanks.append((x,y))
            robot = (x,y)
        elif i==" ":
            blanks.append((x,y))
        elif i=="B":
            boxes.append((x,y))
            blanks.append((x,y))
        elif i=="S":
            # Storages are also blanks
            storages.append((x,y))
            blanks.append((x,y))
        elif i == "\n":
            y -= 1
            x = -1
        x += 1
    objects = {"state": {"robot":robot, "boxes":boxes, "storages":storages}, "blanks":blanks}
    return objects

# 2. Game class for the Pukoban game
class Game:
    # Constructor
    def __init__(self, initialization_state, blanks_coords):
        """Initializes the game from a given state
        Args:
            state (dict): Dictionary with the coordinates of the robot, the boxes and the storages
            blanks_coords (list): Coordinates of the blanks. Blanks are the empty spaces where the robot and the boxes can move.
        """
        self.robot = initialization_state["robot"]
        self.boxes = initialization_state["boxes"]
        self.storages = initialization_state["storages"]
        self.blanks = blanks_coords
        
    def check_win(self):
        #Check if all the storages are filled with boxes (can have more boxes than storages)
        if all(item in self.storages for item in self.boxes):
            return True
        else:
            return False
        
    def get_moving_coords(self, direction):
        """
        Check if the robot can move in the given direction
            Parameters:
                direction (tuple): (Direction to move in, type of movement)
            Returns:
                moving_coords (list): Coordinates of the robot and box after moving, 
        """
        robot_coords = self.robot
        blanks_coords = self.blanks
        boxes_coords = self.boxes
          
        # Get the coordinates of the robot after moving
        if direction[0] == "L":
            robot_moving_coords = (robot_coords[0] - 1, robot_coords[1])
        elif direction[0] == "R":
            robot_moving_coords = (robot_coords[0] + 1, robot_coords[1])
        elif direction[0] == "U":
            robot_moving_coords = (robot_coords[0], robot_coords[1] + 1) 
        elif direction[0] == "D":
            robot_moving_coords = (robot_coords[0], robot_coords[1] - 1)        
        
        
        # Get the coordinates of the box before (box_coords) and after moving (box_moving_coords)
        if direction[1] == "P":
            if direction[0] == "L":
                box_moving_coords = (robot_coords[0] - 2, robot_coords[1])
                box_coords = (robot_coords[0] - 1, robot_coords[1])
            elif direction[0] == "R":
                box_moving_coords = (robot_coords[0] + 2, robot_coords[1])
                box_coords = (robot_coords[0] + 1, robot_coords[1])
            elif direction[0] == "U":
                box_moving_coords = (robot_coords[0], robot_coords[1] + 2)
                box_coords = (robot_coords[0], robot_coords[1] + 1)
            elif direction[0] == "D":
                box_moving_coords = (robot_coords[0], robot_coords[1] - 2)
                box_coords = (robot_coords[0], robot_coords[1] - 1)
        elif direction[1] == "p":
            box_moving_coords = robot_coords
            if direction[0] == "L":
                box_coords = (robot_coords[0] + 1, robot_coords[1])
            elif direction[0] == "R":
                box_coords = (robot_coords[0] - 1, robot_coords[1])
            elif direction[0] == "U":
                box_coords = (robot_coords[0], robot_coords[1] - 1)
            elif direction[0] == "D":
                box_coords = (robot_coords[0], robot_coords[1] + 1)
        
        moving_coords = {}
         
        # Check if the robot can move in the given direction
        # If it can, return the coordinates of the robot and the box after moving
        # If it can't, return an empty list
            
        if direction[1] == "-":
            if robot_moving_coords in blanks_coords:
                moving_coords["robot"] = robot_moving_coords
        elif direction[1] == "P":
            if robot_moving_coords in boxes_coords and box_moving_coords in blanks_coords and box_coords in boxes_coords:
                moving_coords["robot"] = robot_moving_coords
                moving_coords["box"] = box_moving_coords
                moving_coords["box_prior_coords"] = box_coords 
        elif direction[1] == "p":
            if robot_moving_coords in blanks_coords and box_coords in boxes_coords:
                moving_coords["robot"] = robot_moving_coords
                moving_coords["box"] = box_moving_coords
                moving_coords["box_prior_coords"] = box_coords 
        
        return moving_coords
       
    def check_action(self, direction):
        """Checks if the robot can move in the given direction
        Args:
            direction (tuple): (Direction to move in, type of movement)
        Returns:
            True if the robot can move in the given direction, False otherwise
        """
        moving_coords = self.get_moving_coords(direction).copy()
        current_boxes = self.boxes.copy()
        
        # 1. Check if the coordinates are not empty (the movement is valid)
        invalid_movement = False
        if not moving_coords:
            invalid_movement = True
            
        # 2. Check if the robot is moving into a box (not when pushing or pulling)
        robot_into_box = False
        # if not invalid_movement:
        if "robot" in moving_coords.keys() and "box" not in moving_coords.keys():
            if moving_coords["robot"] in current_boxes:
                robot_into_box = True
        
        # 3. Check if a box is moved into a position where there is another box
        colliding_boxes = False
        if "box" in moving_coords.keys():
            for box in current_boxes:
                if box == moving_coords["box"]:
                    colliding_boxes = True

        if invalid_movement or colliding_boxes or robot_into_box:
            return False
        else:    
            return True

    def state_after_action(self, direction):
        """Computes the state of the game after the robot moves in the given direction

        Args:
            direction (tuple): (Direction to move in, type of movement)
        """
        if not self.check_action(direction):
            return("Invalid movement")
        else:
            moving_coordinates = {}
            state_after_action = {}
            current_state = {}
            moving_coordinates = copy.deepcopy(self.get_moving_coords(direction))
            current_state = copy.deepcopy(self.get_current_state())
            state_after_action = copy.deepcopy(current_state)
            
            if "box" not in moving_coordinates.keys():
                state_after_action["robot"] = moving_coordinates["robot"]
            else:
                if direction[1] == "P":
                    state_after_action["boxes"].remove(moving_coordinates["box_prior_coords"])
                    state_after_action["boxes"].append(moving_coordinates["box"])
                    
                    state_after_action["robot"] = moving_coordinates["robot"]
                if direction[1] == "p":
                    state_after_action["boxes"].remove(moving_coordinates["box_prior_coords"])
                    state_after_action["boxes"].append(moving_coordinates["box"])
                
                    state_after_action["robot"] = moving_coordinates["robot"]
            return(state_after_action)

          
    def get_current_state(self):
        """Returns the current state of the game
        Returns:
            current_state list: coordinates of the robot, the boxes, the storages, and the blanks
        """
        robot_coords = self.robot
        boxes_coords = self.boxes
        storages_coords = self.storages
        
        current_state_list = {"robot":robot_coords, "boxes":boxes_coords, "storages":storages_coords}
        return current_state_list
    
    def successor_function(self):
        """Generates all possible states from the current state
            Parameters:
                None
            Returns:
                next_states (list): List of possible movements of the robot
        """
        directions = ["L", "R", "U", "D"]
        movements = ["-", "P", "p"]
        next_states = []
        for direction in directions:
            for movement in movements:
                if self.check_action((direction, movement)):
                    next_states = next_states + [self.state_after_action((direction, movement))]    
        return next_states
    