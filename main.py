import pygame, sys, json, os
#=================================================================================================
# Platformer Engine made by: Tyler Dillard, 2022
# Thank you so much for using this as a base or reference for whatever project you're making!
# If there's anything I would do better, please tell me.
#=================================================================================================

# General Stuff
pygame.init()
clock = pygame.time.Clock()

screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Platformer Engine")

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 0, 255)

red = pygame.Color(255, 0, 0)
invisible = pygame.Color(0, 0, 0, 0)

# Stores dir path to layout.json and opens the file for use
if getattr(sys, "frozen", False): # Checks if file useds to run code is an executable or .py
    dir_name = os.path.dirname(sys.executable)
elif (__file__):
    dir_name = os.path.dirname(__file__)

file_dir = os.path.join(dir_name, "layout.json")

file = open(file_dir, "r+")

# Classes
class Tile:
    objs = []
    tile_size = 40
    
    def __init__(self, x_pos, y_pos):
        self.rect = pygame.Rect(x_pos, y_pos, Tile.tile_size-1, Tile.tile_size-1)
        # Adds instance to list
        Tile.objs.append(self)
    
    @classmethod
    def Update(cls, color):
        for obj in cls.objs:
            
            # Automatically pushes the player out of tile if the left or right rects are colliding with it.
            if P1.rightrect.colliderect(obj):
                P1.rect.right = obj.rect.left
            if P1.leftrect.colliderect(obj):
                P1.rect.left = obj.rect.right
                
            # Draws the tiles
            pygame.draw.rect(screen, color, obj)
    
    @classmethod # Checks if the player's left or right rect is colliding with a wall. Returns True if it is
    def wallCollideCheck(cls):
        for obj in cls.objs:
            if P1.rightrect.colliderect(obj) or P1.leftrect.colliderect(obj):
                return True
    
    @classmethod # Checks if player is touching the ground. Returns true if it is
    def groundCheck(cls):
        for obj in cls.objs:
            if P1.groundrect.colliderect(obj):
                return True

    @classmethod
    def ceilingCheck(cls):
        for obj in cls.objs:
            if P1.ceilrect.colliderect(obj):
                return True
    

class Player:
    mod_speed = 4 # Player left or right speed.
    max_jumptime = 30 # The maximum amout of frames the player is jumping - 60 = 1 second
    gravity = 4 # How fast the player will fall
    
    hover_time = 0.1 * 1000 # how much seconds the player will hover at the end of their jump.
    
    def __init__(self, tile_x, tile_y):
        # Main Rect - The one that the player will see.
        self.rect = pygame.Rect(0, 0, 40, 80)
        self.rect.midleft = tile_x, tile_y
        # Ceiling Rect - Stops the player from going any higher if it touches any ceilings
        self.ceilrect = pygame.Rect(0, 0, 30, 5)
        # Ground Rect - Checks of the player is touching the ground.
        self.groundrect = pygame.Rect(0, 0, 30, 5)
        # Left and Right Rects - Checks if the player is touching a wall
        self.leftrect = pygame.Rect(0, 0, 5, 70)
        self.rightrect = pygame.Rect(0, 0, 5, 70)
        
        self.last = pygame.time.get_ticks() # Get the current tick count
        
        self.speed = 0
        self.jumptime = 0 
        self.jumping = False # If the player is jumping or not.
    
    def Update(self):
        self.now = pygame.time.get_ticks() # Gets the current tick count every frame.
        
        # Automatically moves player left or right based on the value of self.speed.
        if not Tile.wallCollideCheck(): # If the value is 0 or the left or right rect is colliding with a wall, the player will not move.
            self.rect.x += self.speed
        
        # Stops the player from going outside the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
        
        # Takes the player back to it's spawnpoint if it falls out the screen
        if self.rect.y > 800:
            self.rect.midleft = spawn_x, spawn_y
        
        # Aligns left or right rects to the sides of player.
        self.leftrect.midleft = self.rect.midleft
        self.rightrect.midright = self.rect.midright
        # Aligns Ceiling Rect to the top of Player
        self.ceilrect.topleft = self.rect.x+5, self.rect.y
        # Aligns Ground Rect to the bottom of Player
        self.groundrect.bottomleft = self.rect.x+5, self.rect.y+81
        
        # Gravity - Automatically moves the player down by the value of self.fallspeed
        # Will not work if player is touching the ground, self.jump is True, or the player's hover_time isn't over yet
        if not Tile.groundCheck() and self.jumping == False and self.now - self.last >= Player.hover_time: 
            self.rect.y += Player.gravity
        
        # This will activate if the player presses the jump key.
        if self.jumping == True:
            # Checks if the player's jumptime is greater than a value if it is, then the player will stop jumping and hovertime will start.
            if self.jumptime >= Player.max_jumptime:
                self.jumping = False
                self.jumptime = 0
                # Starts hover time
                self.last = self.now
            elif not Tile.ceilingCheck(): # Checks if player in not touching the ceiling
                self.rect.y -= 4
                self.jumptime += 1 # Adds 1 to self.jumptime every frame
            else: # If true, cut jump short
                self.jumptime = Player.max_jumptime
            
        # Draws everything
        self.Draw()
    
    def input(self):
        # Moves the player if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.speed += Player.mod_speed
            if event.key == pygame.K_LEFT:
                self.speed -= Player.mod_speed
            # This will make the player jump unless the player is not touching the ground and self.jumping does not equal False
            if event.key == pygame.K_SPACE and self.jumping == False and Tile.groundCheck():
                self.jumping = True
                
        # Stop the player when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.speed -= Player.mod_speed
            if event.key == pygame.K_LEFT:
                self.speed += Player.mod_speed
    
    def Draw(self):
        # Draws everything
        pygame.draw.rect(screen, invisible, self.leftrect)
        pygame.draw.rect(screen, invisible, self.rightrect)
        pygame.draw.rect(screen, invisible, self.ceilrect)
        pygame.draw.rect(screen, invisible, self.groundrect)
        pygame.draw.rect(screen, blue, self)
                

# Variables
tile_list = [] # Stores every tile loaded into the screen.

layout = json.load(file) # Stores the layout useds to generate the level | "-" = Air, "X" = Tile, "P" = Player Spawn

# Draws layout from layout.json
print("Layout Loaded:")
for row_index,row in enumerate(layout["level"]):
    print(row)
    for col_index,col in enumerate(row):
        if col == "X":
            x = col_index * Tile.tile_size
            y = row_index * Tile.tile_size
            
            tile_list.append(Tile(x, y))
        elif col == "P":
            spawn_x = col_index * Tile.tile_size
            spawn_y = row_index * Tile.tile_size
            
            P1 = Player(spawn_x, spawn_y)

print("Everything seems to be working...")
# Game Loop
while True:
    for event in pygame.event.get():
        # Allows the player to quit the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Checks for player input
        P1.input()
    
    # Refreshes the screen
    screen.fill(black)
    
    # Updates the class instances
    P1.Update()
    
    Tile.Update(white)
    
    # Updates the screen.
    pygame.display.flip()
    clock.tick(60)