########################################
#
# Title: Would You Rather?
#
# Genre: Arcade
#
# Author: John Bullard
#
# http://therookiedev.blogspot.com/
#
# Created: 12/12/2012
#
########################################


#############################################
# Imports.
#############################################

import pyglet, random
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

# Colors.
WHITE = (255, 255, 255, 255)
RED = (100, 0, 0, 255)

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, caption = "Would You Rather?")

# Center window.
mainWindow.set_location(mainWindow.screen.width/2 - mainWindow.width/2, mainWindow.screen.height/2 - mainWindow.height/2)

# Mouse.
MOUSE_X = mainWindow.screen.width/2 - mainWindow.width/2
MOUSE_Y = mainWindow.screen.height/2 - mainWindow.height/2
MOUSE_LEFT_CLICKED = False


def main_menu():
    """ Main menu in the game. """
    
    global batch, menu, widgets_list, focus
        
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Menu.
    menu = True
    
    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-1, BUTTON_W, BUTTON_H, RED, WHITE, 'Start Game', batch, 'new_question()'), 
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-32, BUTTON_W, BUTTON_H, RED, WHITE, 'Create Question', batch, 'create_question()'), 
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-63, BUTTON_W, BUTTON_H, RED, WHITE, 'Exit Game', batch, 'pyglet.app.exit()')]
    
    focus = None
    
    # Create labels.
    pyglet.text.Label('Would You Rather?', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-100, anchor_x = 'center', anchor_y = 'center', batch = batch)
                    
            
def new_question():
    """ Creates a new level. """
    
    global batch, menu, widgets_list, focus
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Menu.
    menu = False
    
    # Create widgets.
    load_questions()
    question = questions[random.randint(0, len(questions)-1)]
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-1, len(question[0])*10, BUTTON_H, RED, WHITE, question[0], batch, 'new_question()'),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-50, len(question[1])*10, BUTTON_H, RED, WHITE, question[1], batch, 'new_question()'),
                    Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Quit', batch, 'main_menu()'), 
                    Widget.Button(SCREEN_W-BUTTON_W/2-4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Skip', batch, 'new_question()')]
    
    focus = None
    
    # Create labels.
    pyglet.text.Label('Would You Rather?', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-75, anchor_x = 'center', anchor_y = 'center', batch = batch)
    pyglet.text.Label('OR', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = SCREEN_H/2-25, anchor_x = 'center', anchor_y = 'center', batch = batch)
        

def load_questions():
    """ Loads all questions from file. """
    
    global questions
    
    questionsfile = open("DATA/WYR/questions.txt").read().splitlines()
    questions = []
    group = []
    num = 0
    for line in questionsfile:
    
        if line != '':
    
            group.append(line)
            num += 1
        
        if num == 2:
        
            questions.append(group)
            num = 0
            group = []
            
    
def create_question():
    """ Allows the player to create a question. """
    
    global batch, menu, focus, widgets_list, info
        
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Menu.
    menu = False
    
    # Create widgets.
    widgets_list = [Widget.Input(SCREEN_W/3-33, SCREEN_H/2+13, 310, 20, 50, batch),
                    Widget.Input(SCREEN_W/3-33, SCREEN_H/2-37, 310, 20, 50, batch),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-75, BUTTON_W, BUTTON_H, RED, WHITE, 'Create Question', batch, 'save_question()'), 
                    Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Main Menu', batch, 'main_menu()'),
                    Widget.Button(SCREEN_W-BUTTON_W/2-4, 17, BUTTON_W, BUTTON_H, RED, WHITE, 'Start Game', batch, 'new_question()')]
    
    focus = widgets_list[0]
    widgets_list[1].caret.visible = False
    
    # Create labels.
    info = pyglet.text.Label('Type in your question in the boxes below.', font_name = 'Arial', font_size = 24, x = SCREEN_W/2, y = SCREEN_H-100, 
                             anchor_x = 'center', anchor_y = 'center', batch = batch)
    pyglet.text.Label('1.', font_name = 'Arial', font_size = 12, x = SCREEN_W/3-45, y = SCREEN_H/2+25, anchor_x = 'center', anchor_y = 'center', batch = batch)
    pyglet.text.Label('OR', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = SCREEN_H/2, anchor_x = 'center', anchor_y = 'center', batch = batch)
    pyglet.text.Label('2.', font_name = 'Arial', font_size = 12, x = SCREEN_W/3-45, y = SCREEN_H/2-25, anchor_x = 'center', anchor_y = 'center', batch = batch)


def save_question():
    """ Saves created question. """
    
    global focus
    
    # Write new question to file.
    questionsfile = open("DATA/WYR/questions.txt", "a")
    questionsfile.write('\n\n'+widgets_list[0].document.text+'\n')
    questionsfile.write(widgets_list[1].document.text)
    questionsfile.close()
    
    # Reset input widgets.
    focus = widgets_list[0]
    widgets_list[0].document.text = ''
    widgets_list[0].caret.visible = True
    widgets_list[1].document.text = ''
    widgets_list[1].caret.visible = False
    info.text = 'Question created successfully.'
    pyglet.clock.schedule_once(change_info, 2.5)
    
    # Reload questions.
    load_questions()
    

def change_info(dt):
    """ Changes info back to original text. """
    
    info.text = 'Type in your question in the boxes below.'
    
    
@mainWindow.event
def on_mouse_motion(x, y, dx, dy):
    """ Determines what happens on mouse movement. """
    
    global MOUSE_X, MOUSE_Y
    
    MOUSE_X = x
    MOUSE_Y = y
        

@mainWindow.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """ Highlights text in active input box. """
    
    if focus is not None and focus.collision(x, y):
    
        focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers) 

                
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
def on_key_press(symbol, modifiers):
    """ Handles the key presses. """
    
    global focus 
    
    if symbol == key.ESCAPE and menu == False:
        
        main_menu()
        return pyglet.event.EVENT_HANDLED
        
        
@mainWindow.event
def on_text(text):
    """ Add text to active input box. """
    
    if focus is not None and len(focus.document.text) < focus.maxlength:
    
        focus.caret.on_text(text)
                

@mainWindow.event
def on_text_motion(motion):
    """ Delete text from active input box. """
    
    if focus is not None:
    
        focus.caret.on_text_motion(motion)
            
        
@mainWindow.event
def on_draw():
    """ Draws everything to screen. """
    
    global MOUSE_LEFT_CLICKED, focus
    
    # Clearn screen.
    mainWindow.clear()
    
    # Draw Widgets.
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
            
            elif widget.type == 'Input':
                
                cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_TEXT)
                mainWindow.set_mouse_cursor(cursor)  
                
                if MOUSE_LEFT_CLICKED == True:
                    
                    if focus != widget:
                        
                        focus.caret.visible = False
                        focus = widget
                        focus.caret.visible = True
                    
                    else:
                        
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