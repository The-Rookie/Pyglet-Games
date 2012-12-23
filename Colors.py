########################################
#
# Title: Colors
#
# Genre: Arcade
#
# Author: John Bullard
#
# http://therookiedev.blogspot.com/
#
# Created: 12/17/2012
#
########################################


#############################################
# Imports.
#############################################

import pyglet, os, random, shelve
from pyglet.window import mouse, key
import DATA.Widget as Widget


#############################################
# Globals.
#############################################

# Screen size.
SCREEN_W = 640
SCREEN_H = 480

# Button size.
BUTTON_W = 150
BUTTON_H = 24

# Square size.
SQUARE_W = 16
SQUARE_H = 16

# Colors.
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
BLACK = (0, 0, 0, 255)
COLORS = [WHITE, RED, GREEN, BLUE, YELLOW]

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, vsync = False, caption = "Colors")

# Center window.
mainWindow.set_location(mainWindow.screen.width/2 - mainWindow.width/2, mainWindow.screen.height/2 - mainWindow.height/2)

# Mouse.
MOUSE_X = mainWindow.screen.width/2 - mainWindow.width/2
MOUSE_Y = mainWindow.screen.height/2 - mainWindow.height/2
MOUSE_LEFT_CLICKED = False

# Keyboard.
KEYMAP = key.KeyStateHandler()


class Square(pyglet.sprite.Sprite):
    """ A square in the game. """
    
    def __init__(self, x, y, color, batch):
        """ Initiate the square class. """

        # Build an image for the square.
        pattern = pyglet.image.SolidColorImagePattern((color))
        image = pyglet.image.create(SQUARE_W, SQUARE_H, pattern)

        # Offset image.
        image.anchor_x, image.anchor_y = 8, 8

        # Create sprite out of image.
        pyglet.sprite.Sprite.__init__(self, image, x, y, batch = batch, group = pyglet.graphics.OrderedGroup(0))
        
        # Set players score.
        self.score = 0
        
    
    def collisions(self):
        """ Checks for collisions. """
        
        for enemy in enemies[:]:
        
            if self.x-self.image.anchor_x <= enemy.x+enemy.image.anchor_x and self.x+self.image.anchor_x >= enemy.x-enemy.image.anchor_x:
            
                if self.y-self.image.anchor_y <= enemy.y+enemy.image.anchor_y and self.y+self.image.anchor_y >= enemy.y-enemy.image.anchor_y:
                    
                    if enemy.color == self.color:
                    
                        self.score += 50
                        enemies.remove(enemy)
                    
                    else:
                        
                        player.batch = None
                        pyglet.clock.unschedule(update_score)
                        pyglet.clock.unschedule(change_color)
                        pyglet.text.Label('Game Over', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H/2, anchor_x = 'center', anchor_y = 'center', batch = batch)
                        break

                        
def main_menu():
    """ Main menu in the game. """
    
    global batch, active, widgets_list, enemies
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Reset active.
    active = False
    
    # Unschedule.
    unschedule_everything()
    
    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-1, BUTTON_W, BUTTON_H, WHITE, WHITE, 'Start Game', batch, 'start_game()'),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-32, BUTTON_W, BUTTON_H, WHITE, WHITE, 'High Scores', batch, 'high_scores()'),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-63, BUTTON_W, BUTTON_H, WHITE, WHITE, 'Exit Game',  batch, 'pyglet.app.exit()')]
            
    # Empty list for enemies.
    enemies = []
    
    # Create labels.
    pyglet.text.Label('Colors', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-100, anchor_x = 'center', anchor_y = 'center', batch = batch)
    
    # Schedule update function.
    pyglet.clock.schedule_interval(update, 1.0/45.0)
    pyglet.clock.schedule_interval(add_enemy, 0.5)
    

def start_game():
    """ Starts the game. """
    
    global batch, widgets_list, active, player, enemies, scoreLabel
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Unschedule everything.
    pyglet.clock.unschedule(update)
    pyglet.clock.unschedule(update_score)
    pyglet.clock.unschedule(add_enemy)
    pyglet.clock.unschedule(change_color)
    
    # Reset widgets.
    widgets_list = []
    
    # Set active.
    active = True
    
    # Unschedule.
    unschedule_everything()
    
    # Create player.
    player = Square(SCREEN_W/2, 8, WHITE, batch)
    player.color = random.choice(COLORS)[0:3]
    
    # Empty list for enemies.
    enemies = []
    
    # Create labels.
    scoreLabel = pyglet.text.Label(str(player.score), font_name = 'Arial', font_size = 32, x = SCREEN_W-14, y = SCREEN_H-32, anchor_x = 'right', anchor_y = 'center', batch = batch)
    
    # Schedule update function.
    pyglet.clock.schedule_interval(update, 1.0/60.0)
    pyglet.clock.schedule_interval(update_score, 0.5)
    pyglet.clock.schedule_interval(add_enemy, 0.2)
    pyglet.clock.schedule_interval(change_color, 5)


def high_scores():
    """ Displays high scores. """
    
    global batch, widgets_list
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Unschedule.
    unschedule_everything()
    
    # Create widgets.
    widgets_list = [Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, WHITE, WHITE, 'Main Menu', batch, 'main_menu()'),
                    Widget.Button(SCREEN_W-BUTTON_W/2-4, 17, BUTTON_W, BUTTON_H, WHITE, WHITE, 'Start Game', batch, 'start_game()')]

    # Load highscores.
    highscores_shelf = shelve.open('DATA\Colors\highscores')
    highscores = []
    
    for key in highscores_shelf:
        
        highscores.append(highscores_shelf[key])
        
    highscores_shelf.close()
    
    # Sort highscores.
    highscores = sorted(highscores, key = lambda score: score[1], reverse = True)
    
    # Display highscores.
    y = 0
    for i in range(10):
        
        if i <= len(highscores)-1:
        
            pyglet.text.Label(highscores[i][0]+'    -    '+str(highscores[i][1]), font_name = 'Arial', font_size = 12, x = SCREEN_W/2-35, y = SCREEN_H/2+80-y, 
                              anchor_x = 'left', anchor_y = 'center', batch = batch)
            y += 25
            
    # Create labels.
    x = 0
    for i in range(10):
        
        if i+1 == 10:
            
            x = 5
            
        pyglet.text.Label(str(i+1)+'.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2-60-x, y = SCREEN_H/2+80-(i*25), anchor_x = 'center', anchor_y = 'center', batch = batch)
        
    pyglet.text.Label('High Scores', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-75, anchor_x = 'center', anchor_y = 'center', batch = batch)
    

def update(dt):
    """ Updates the player movement. """
    
    mainWindow.push_handlers(KEYMAP)
    
    if active == True:
    
        # Eight-way movement.
        if KEYMAP[key.W] and player.y+player.image.anchor_y < SCREEN_H:
        
            player.y += 4
    
        if KEYMAP[key.S] and player.y-player.image.anchor_y > 0:
        
            player.y -= 4
    
        if KEYMAP[key.D] and player.x+player.image.anchor_x < SCREEN_W:
        
            player.x += 4
        
        if KEYMAP[key.A] and player.x-player.image.anchor_x > 0:
        
            player.x -= 4
        
        # Collisions.
        player.collisions()
            
    for enemy in enemies[:]:
        
        enemy.y -= 4
        if enemy.y+enemy.image.anchor_y < 0:
            
            enemies.remove(enemy)
      
        
def update_score(dt):
    """ Updates score. """
    
    player.score += 1
    scoreLabel.text = str(player.score)


def add_enemy(dt):
    """ Adds and enemy to the game. """
    
    for i in range(3):
    
        enemy = Square(random.randint(0, SCREEN_W), SCREEN_H, WHITE, batch)
        enemy.color = random.choice(COLORS)[0:3]
        enemies.append(enemy)
    

def change_color(dt):
    """ Changes the player's color. """
    
    player.color = random.choice(COLORS)[0:3]
    

def unschedule_everything():
    """ Unschedules everything. *duh* """
    
    pyglet.clock.unschedule(update)
    pyglet.clock.unschedule(add_enemy)
    
    
@mainWindow.event
def on_key_press(symbol, modifiers):
    """ Handles the key presses. """
    
    if symbol == key.ESCAPE:
        
        pyglet.clock.unschedule(update)
        pyglet.clock.unschedule(add_enemy)
        main_menu()
        return pyglet.event.EVENT_HANDLED
    
    elif symbol == key.R:
        
        start_game()
        
            
@mainWindow.event
def on_mouse_motion(x, y, dx, dy):
    """ Determines what happens on mouse movement. """
    
    global MOUSE_X, MOUSE_Y
    
    MOUSE_X = x
    MOUSE_Y = y
        
    
@mainWindow.event   
def on_mouse_press(x, y, button, modifiers):
    """ Determines what happens on a mouse click. """
    
    global MOUSE_LEFT_CLICKED
    
    if button == mouse.LEFT:
    
        MOUSE_LEFT_CLICKED = True

        
@mainWindow.event  
def on_mouse_release(x, y, button, modifiers):
    """ Determines what happens on a mouse release. """
    
    global MOUSE_LEFT_CLICKED
    
    if button == mouse.LEFT:
    
        MOUSE_LEFT_CLICKED = False


@mainWindow.event
def on_draw():
    """ Draws everything to screen. """
    
    global MOUSE_LEFT_CLICKED
    
    # Clear screen.
    mainWindow.clear()
        
    # Draw Widgets.
    if len(widgets_list) > 0:
        num = 0
        for widget in widgets_list:
        
            if widget.collision(MOUSE_X, MOUSE_Y):
            
                if widget.type == 'Button':
                
                    widget.opacity = 155
                    cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_HAND)
                    mainWindow.set_mouse_cursor(cursor)
                
                    if MOUSE_LEFT_CLICKED == True:
                        
                        eval(widget.click_action)
                        MOUSE_LEFT_CLICKED = False
            
                    break
            
            else:
        
                widget.opacity = 255
        
            num += 1
        
            if num == len(widgets_list)-1:
            
                cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_DEFAULT)
                mainWindow.set_mouse_cursor(cursor)  
    
    # No widgets.
    else:
        
        cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_DEFAULT)
        mainWindow.set_mouse_cursor(cursor)
                
    # Draw batch.
    batch.draw()

                              
# Run the game.
main_menu()
pyglet.app.run()