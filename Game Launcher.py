########################################
#
# Title: Game Launcher
#
# Author: John Bullard
#
# http://therookiedev.blogspot.com/
#
# Created: 12/12/2012
#
# Build: 1
#
########################################


#############################################
# Imports.
#############################################

import pyglet, os
from pyglet.window import mouse, key
import DATA.Widget as Widget


#############################################
# Globals.
#############################################

# Screen size.
SCREEN_W = 640
SCREEN_H = 480

# Button size.
BUTTON_W = 200
BUTTON_H = 24

# Colors.
BROWN = (47, 38, 39, 255)
RED = (132, 59, 53, 255)
BACKGROUND = (0.63, 0.54, 0.41, 1)

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, vsync = False, caption = "Game Launcher")

# Center window.
mainWindow.set_location(mainWindow.screen.width/2 - mainWindow.width/2, mainWindow.screen.height/2 - mainWindow.height/2)

# Set background color.
pyglet.gl.glClearColor(*BACKGROUND)

# Mouse.
MOUSE_X = mainWindow.screen.width/2 - mainWindow.width/2
MOUSE_Y = mainWindow.screen.height/2 - mainWindow.height/2
MOUSE_LEFT_CLICKED = False


def main_menu():
    """ Main menu in the program. """
    
    global batch, widgets_list
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()

    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2-BUTTON_W-5, SCREEN_H/2-1, BUTTON_W, BUTTON_H, RED, BROWN, 'Would You Rather', batch, "os.system('WYR.py')"),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-1, BUTTON_W, BUTTON_H, RED, BROWN, 'Simulate', batch, "os.system('Simulate.py')"), 
                    Widget.Button(SCREEN_W/2+BUTTON_W+5, SCREEN_H/2-1, BUTTON_W, BUTTON_H, RED, BROWN, 'Pong',  batch, "os.system('Pong.py')"), 
                    Widget.Button(SCREEN_W/2-BUTTON_W-5, SCREEN_H/2-32, BUTTON_W, BUTTON_H, RED, BROWN, 'Game of Fifteen', batch, "os.system('GoF.py')"), 
                    Widget.Button(SCREEN_W/2+BUTTON_W+5, SCREEN_H/2-32, BUTTON_W, BUTTON_H, RED, BROWN, 'Exit', batch, 'pyglet.app.exit()')]
                  
    # Create labels.
    pyglet.text.Label('Game Launcher', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-100, anchor_x = 'center', anchor_y = 'center', batch = batch)
                    
                    
@mainWindow.event
def on_mouse_motion(x, y, dx, dy):
    """ Stores mouse position when the mouse moves.. """
    
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
    
    # Draw batch.
    batch.draw()
                              
                              
# Run the game.
main_menu()
pyglet.app.run()