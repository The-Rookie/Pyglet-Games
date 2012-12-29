########################################
#
# Title: Simulate
#
# Genre: Puzzle
#
# Author: John Bullard
#
# http://therookiedev.blogspot.com/
#
# Created: 12/13/2012
#
########################################


#############################################
# Imports.
#############################################

import pyglet, random, shelve
from pyglet.window import mouse, key
import DATA.Widget as Widget


#############################################
# Globals.
#############################################

# Screen size.
SCREEN_W = 640
SCREEN_H = 480

# Box size.
BOX_W = 128
BOX_H = 128

# Button size.
BUTTON_W = 150
BUTTON_H= 24

# Colors.
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
RED = (100, 0, 0, 255)
BRIGHTRED = (255, 0, 0, 255)
GREEN = (0, 155, 0, 255)
BRIGHTGREEN = (0, 255, 0, 255)
BLUE = (0, 0, 155, 255)
BRIGHTBLUE = (0, 0, 255, 255)
YELLOW = (155, 155, 0, 255)
BRIGHTYELLOW = (255, 255, 0, 255)

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, caption = "Simulate")

# Center window.
mainWindow.set_location(mainWindow.screen.width/2 - mainWindow.width/2, mainWindow.screen.height/2 - mainWindow.height/2)

# Mouse.
MOUSE_X = mainWindow.screen.width/2 - mainWindow.width/2
MOUSE_Y = mainWindow.screen.height/2 - mainWindow.height/2
MOUSE_LEFT_CLICKED = False

# Load sounds.
SOUNDS = [pyglet.resource.media('DATA/Simulate/beep1.ogg', False), pyglet.resource.media('DATA/Simulate/beep2.ogg', False),
          pyglet.resource.media('DATA/Simulate/beep3.ogg', False), pyglet.resource.media('DATA/Simulate/beep4.ogg', False)]

          
def main_menu():
    """ Main menu in the game. """
    
    global batch, active, widgets_list
        
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # States.
    active = True

    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-1, BUTTON_W, BUTTON_H, RED, WHITE, 'Start Game', batch, 'start_game()'), 
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-32, BUTTON_W, BUTTON_H, RED, WHITE, 'High Scores', batch, 'high_scores()'),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-63, BUTTON_W, BUTTON_H, RED, WHITE, 'Exit Game', batch, 'pyglet.app.exit()')]
                  
    # Create labels.
    pyglet.text.Label('Simulate', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-100, anchor_x = 'center', anchor_y = 'center', batch = batch)
        
    
def start_game():
    """ Starts game. """
    
    global batch, active, widgets_list, pattern, previous_pattern, score, info, score_label
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # State.
    active = False
    
    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2-70, SCREEN_H/2+75, BOX_W, BOX_H, BRIGHTYELLOW, BLACK, '', batch, "check_pattern('YELLOW')"), 
                    Widget.Button(SCREEN_W/2+70, SCREEN_H/2+75, BOX_W, BOX_H, BRIGHTBLUE, BLACK, '', batch, "check_pattern('BLUE')"), 
                    Widget.Button(SCREEN_W/2-70, SCREEN_H/2-65, BOX_W, BOX_H, BRIGHTRED, BLACK, '', batch, "check_pattern('RED')"), 
                    Widget.Button(SCREEN_W/2+70, SCREEN_H/2-65, BOX_W, BOX_H, BRIGHTGREEN, BLACK, '', batch, "check_pattern('GREEN')"), 
                    Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Quit', batch, 'main_menu()'), 
                    Widget.Button(SCREEN_W-BUTTON_W/2-4, 17, BUTTON_W, BUTTON_H, RED, WHITE,'Restart', batch, 'start_game()')]
    
    # Reset pattern/score.
    pattern = []
    previous_pattern= []
    score = 0
    
    # Create labels.
    info = pyglet.text.Label('Simulate the pattern by clicking the squares to gain points.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = SCREEN_H-50, 
                             anchor_x = 'center', anchor_y = 'center', batch = batch)
    score_label = pyglet.text.Label('Score: '+str(score), font_name = 'Arial', font_size = 12, bold = True, x = SCREEN_W/2, y = 68, anchor_x = 'center', anchor_y = 'center', batch = batch)
    
    # Create new pattern.
    create_new_pattern()


def high_scores():
    """ Displays high scores. """
    
    global batch, widgets_list
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Create widgets.
    widgets_list = [Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Main Menu', batch, 'main_menu()'),
                    Widget.Button(SCREEN_W-BUTTON_W/2-4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Start Game', batch, 'start_game()')]

    # Load highscores.
    highscores_shelf = shelve.open('DATA\Simulate\highscores')
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
        
            pyglet.text.Label(highscores[i][0]+'   -   '+str(highscores[i][1]), font_name = 'Arial', font_size = 12, x = SCREEN_W/2-80, y = SCREEN_H/2+80-y, 
                              anchor_x = 'left', anchor_y = 'center', batch = batch)
            y += 25
            
    # Create labels.
    x = 0
    for i in range(10):
        
        if i+1 == 10:
            
            x = 5
            
        pyglet.text.Label(str(i+1)+'.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2-90-x, y = SCREEN_H/2+80-(i*25), anchor_x = 'center', anchor_y = 'center', batch = batch)
        
    pyglet.text.Label('High Scores', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-75, anchor_x = 'center', anchor_y = 'center', batch = batch)
    

def save_high_score():
    """ Saves high score to file. """
    
    # Remove widgets.
    widgets_list[len(widgets_list)-1].remove()
    widgets_list.remove(widgets_list[len(widgets_list)-1])
    text = widgets_list[len(widgets_list)-1].document.text
    widgets_list[len(widgets_list)-1].remove()
    widgets_list.remove(widgets_list[len(widgets_list)-1])
    
    # Save score.
    highscores_shelf = shelve.open('DATA\Simulate\highscores')
    highscores_shelf[str(len(highscores_shelf.keys()))] = [text, score]
    highscores_shelf.close()
    
    # Add top times widget/label and change info.
    pyglet.text.Label('Score saved.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2+6, y = 42, anchor_x = 'center', anchor_y = 'center', batch = batch)
    widgets_list.append(Widget.Button(SCREEN_W/2+4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'High Scores', batch, "high_scores()"))
    info.text = 'Click restart to start a new game.'
    
    
def check_pattern(color):
    """ Checks if button clicked matches pattern. """
    
    global score
    
    # Play sounds.
    if color == 'YELLOW':
        
        play_sounds([SOUNDS[0]])
    
    elif color == 'BLUE':
        
        play_sounds([SOUNDS[1]])
        
    elif color == 'RED':
        
        play_sounds([SOUNDS[2]])
        
    elif color == 'GREEN':
        
        play_sounds([SOUNDS[3]])
        
    if color == pattern[0]:
        
        pattern.remove(pattern[0])
        
        if len(pattern) == 0:
            
            score += 1
            score_label.text = 'Score: '+str(score)
            create_new_pattern()
    
    else:
        
        # Play all sounds at once.
        play_sounds(SOUNDS)
        
        # Change info.
        info.text = 'Save your score below or click restart to start a new game.'
        
        # Create widgets.
        widgets_list.append(Widget.Input(SCREEN_W/2-(BUTTON_W/2)+4, 32, BUTTON_W, 20, 12, batch))
        widgets_list.append(Widget.Button(SCREEN_W/2+4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Save Score', batch, "save_high_score()"))
            
            
def create_new_pattern():
    """ Creates a new pattern. """
    
    global active, pattern, previous_pattern
    
    active = False
    
    for widget in widgets_list:
        
        widget.opacity = 255
        batch.draw()
        
    # Create sequence in pattern.
    pattern = previous_pattern[:]
    pattern.append(random.choice(('YELLOW', 'BLUE', 'RED', 'GREEN')))
    previous_pattern = pattern[:]
    
    pyglet.clock.schedule_once(light_buttons, 1.5, 0)
    pyglet.clock.schedule_once(unlight_buttons, 2.3)
    

def light_buttons(dt, num):
    """ Lights up buttons and plays sounds in pattern. """
    
    if len(pattern)-1 >= num:
    
        color = pattern[num]

        for widget in widgets_list:
            
            if widget.type == 'Button':
            
                if 'YELLOW' in widget.click_action:
                    
                    if color == 'YELLOW':
                    
                        widget.color = (155, 155, 0)
                        play_sounds([SOUNDS[0]])
                        
                elif 'BLUE' in widget.click_action:
                    
                    if color == 'BLUE':
                    
                        widget.color = (0, 0, 155)
                        play_sounds([SOUNDS[1]])
                    
                elif 'RED' in widget.click_action:
                    
                    if color == 'RED':
                    
                        widget.color = (100, 0, 0)
                        play_sounds([SOUNDS[2]])
                        
                elif 'GREEN' in widget.click_action:
                    
                    if color == 'GREEN':
                    
                        widget.color = (0, 155, 0)
                        play_sounds([SOUNDS[3]])
    
        
        if len(pattern)-1 != num:
        
            pyglet.clock.schedule_once(light_buttons, 1.5, num+1)
            pyglet.clock.schedule_once(unlight_buttons, 2.3)
    
        else:
        
            pyglet.clock.schedule_once(activate, 1)
        
                    
def unlight_buttons(dt):
    """ Unlights buttons. """

    for widget in widgets_list:
        
        if widget.type == 'Button':
        
            if 'YELLOW' in widget.click_action:
                    
                widget.color = (255, 255, 0)
                        
            elif 'BLUE' in widget.click_action:
        
                widget.color = (0, 0, 255)
                        
            elif 'RED' in widget.click_action:

                widget.color = (255, 0, 0)
                        
            elif 'GREEN' in widget.click_action:
                     
                widget.color = (0, 255, 0)                 

    
def activate(dt):
    """ Allow the player to move. """
    
    global active
    
    active = True

    
def play_sounds(sounds):
    """ Plays given sounds. """
    
    for sound in sounds:
        
        sound.play()
        
    
@mainWindow.event
def on_mouse_motion(x, y, dx, dy):
    """ Determines what happens on mouse movement. """
    
    global MOUSE_X, MOUSE_Y
    
    MOUSE_X = x
    MOUSE_Y = y


@mainWindow.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """ Highlight text. """
    
    for widget in widgets_list:
        
        if widget.collision(x, y):
        
            if widget.type == 'Input':
        
                widget.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)            
 
 
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
def on_text(text):
    """ Add text to input box if active. """
    
    for widget in widgets_list:
        
        if widget.type == 'Input':
            
            if len(widget.document.text) <= widget.maxlength:
    
                widget.caret.on_text(text)

                
@mainWindow.event
def on_text_motion(motion):
    """ Delete text from input box. """
    
    for widget in widgets_list:
        
        if widget.type == 'Input':
        
            widget.caret.on_text_motion(motion)

            
@mainWindow.event
def on_key_press(symbol, modifiers):
    """ Determines what happens on key press. """
    
    if symbol == key.ENTER:
        
        for widget in widgets_list:
            
            if widget.type == 'Input':
                
                save_high_score()

            
@mainWindow.event
def on_draw():
    """ Draws everything to screen. """
    
    global MOUSE_LEFT_CLICKED, active

    # Clear screen.
    mainWindow.clear()
    
    # Draw Widgets.
    num = 0
    for widget in widgets_list:
        
        if widget.collision(MOUSE_X, MOUSE_Y):
            
            if widget.type == 'Button':
                
                if active == True:
                    
                    widget.opacity = 155
                    cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_HAND)
                    mainWindow.set_mouse_cursor(cursor)
                    
                    if MOUSE_LEFT_CLICKED == True:
                    
                        eval(widget.click_action)
                        MOUSE_LEFT_CLICKED = False
                    
                    break
                
                elif widget.click_action == 'main_menu()' or widget.click_action == 'start_game()':
                    
                    widget.opacity = 155
                    cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_HAND)
                    mainWindow.set_mouse_cursor(cursor)
                    
                    if MOUSE_LEFT_CLICKED == True:
                        
                        eval(widget.click_action)
                        MOUSE_LEFT_CLICKED = False
                    
                    break
            
            elif widget.type == 'Input':
                
                cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_TEXT)
                mainWindow.set_mouse_cursor(cursor)  
                
                if MOUSE_LEFT_CLICKED == True:
                    
                    widget.caret.on_mouse_press(MOUSE_X, MOUSE_Y, mouse.LEFT, None)
                    MOUSE_LEFT_CLICKED = False
                 
                break
            
        else:
        
            widget.opacity = 255
        
        num += 1
        
        if num == len(widgets_list)-1:
            
            cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_DEFAULT)
            mainWindow.set_mouse_cursor(cursor)  
    
    # Draw batch.
    batch.draw()

    
# Run the game.
main_menu()
pyglet.app.run()