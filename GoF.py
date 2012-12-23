########################################
#
# Title: Game of Fifteen
#
# Genre: Puzzle
#
# Author: John Bullard
#
# http://therookiedev.blogspot.com/
#
# Created: 12/18/2012
#
########################################


#############################################
# Imports.
#############################################

import pyglet, os, shelve, random
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

# Piece size.
PIECE_W = 80
PIECE_H = 80

# Board size.
BOARD_W = 4
BOARD_H = 4

# Slides for new puzzle.
SLIDES = 100

# Colors.
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
BOARD = (0, 50, 255, 255)
GREEN = (0, 204, 0, 255)
BACKGROUND = (0.011, 0.211, 0.286, 1)

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, vsync = False, caption = "Game of Fifteen")

# Center window.
mainWindow.set_location(mainWindow.screen.width/2 - mainWindow.width/2, mainWindow.screen.height/2 - mainWindow.height/2)

# Set background color.
pyglet.gl.glClearColor(*BACKGROUND)

# Mouse.
MOUSE_X = mainWindow.screen.width/2 - mainWindow.width/2
MOUSE_Y = mainWindow.screen.height/2 - mainWindow.height/2
MOUSE_LEFT_CLICKED = False


def main_menu():
    """ Main menu in the game. """
    
    global batch, menu, widgets_list, active
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Menu.
    menu = True
    
    # Unschedule everything.
    unschedule_everything()

    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-1, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Start Game', batch, "start_game()"),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-32, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Top Times', batch, "top_times()"),
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-63, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Exit Game', batch, 'pyglet.app.exit()')]
    
    # Active.
    active = True
    
    # Create labels.
    pyglet.text.Label('Game of Fifteen', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-100, anchor_x = 'center', anchor_y = 'center', batch = batch)
                    

def start_game():
    """ Main menu in the game. """
    
    global batch, widgets_list, menu, active, solved, board, solved_board, sequence, player_sequence, time, time_label, info
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Unschedule everything. *duh*
    unschedule_everything()
    
    # Create widgets.
    widgets_list = [Widget.Button(BUTTON_W/2+4, 48, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Reset', batch, "reset_puzzle(0)"),
                    Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Restart', batch, "start_game()"),
                    Widget.Button(SCREEN_W-(BUTTON_W/2)-4, 48, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Solve', batch, 'solve_puzzle(0)'),
                    Widget.Button(SCREEN_W-(BUTTON_W/2)-4, 17, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Quit', batch, 'main_menu()'),
                    Widget.Button(160+(PIECE_W/2), 410-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '1', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(240+(PIECE_W/2), 410-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '2', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(320+(PIECE_W/2), 410-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '3', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(400+(PIECE_W/2), 410-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '4', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(160+(PIECE_W/2), 330-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '5', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(240+(PIECE_W/2), 330-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '6', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(320+(PIECE_W/2), 330-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '7', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(400+(PIECE_W/2), 330-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '8', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(160+(PIECE_W/2), 250-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '9', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(240+(PIECE_W/2), 250-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '10', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(320+(PIECE_W/2), 250-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '11', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(400+(PIECE_W/2), 250-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '12', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(160+(PIECE_W/2), 170-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '13', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(240+(PIECE_W/2), 170-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '14', batch, 'move_piece(widget)', bold = True),
                    Widget.Button(320+(PIECE_W/2), 170-PIECE_H/2+1, PIECE_W, PIECE_H, GREEN, BLACK, '15', batch, 'move_piece(widget)', bold = True)]
    
    # Menu.
    menu = False
    
    # Active/solved variables.
    active = False
    solved = False
    
    # Create a solved board.
    solved_board = create_solved()
    
    # Create board.
    board = create_solved()
    
    # Solve sequence.
    sequence = []
    
    # Players move sequence.
    player_sequence = []
    
    # Generate puzzle.
    pyglet.clock.schedule_once(generate_puzzle, 1, SLIDES)
    
    # Create time label/list.
    time = [0, 0]
    time_label = pyglet.text.Label('0:00', font_name = 'Arial', font_size = 16, x = SCREEN_W/2, y = 68, bold = True, anchor_x = 'center', anchor_y = 'center', batch = batch)
    info = pyglet.text.Label('Generating new puzzle...', font_name = 'Arial', font_size = 16, x = SCREEN_W/2, y = SCREEN_H-32, anchor_x = 'center', anchor_y = 'center', batch = batch)
    
    # Create board.
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (158, 411, 481, 411)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (159, 411, 159, 89)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (481, 412, 481, 89)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (160, 89, 481, 89)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (158, 412, 483, 412)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (158, 411, 158, 89)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (482, 412, 482, 89)), ('c4B', (BOARD*2)))
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (158, 88, 483, 88)), ('c4B', (BOARD*2)))
    

def top_times():
    """ Displays high scores. """
    
    global batch, widgets_list
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Create widgets.
    widgets_list = [Widget.Button(BUTTON_W/2+4, 17, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Main Menu', batch, 'main_menu()'),
                    Widget.Button(SCREEN_W-BUTTON_W/2-4, 17, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Start Game', batch, 'start_game()')]

    # Load times.
    toptimes_shelf = shelve.open('DATA\\Game of Fifteen\\toptimes')
    times = []
    
    for key in toptimes_shelf:
        
        times.append(toptimes_shelf[key])
        
    toptimes_shelf.close()
    
    # Sort times.
    times = sorted(times, key = lambda score: score[1], reverse = False)
    
    # Convert time to correct format.
    for time in times[:]:
        
        if time[1][1] < 10:
            
            time[1] = str(time[1][0])+':0'+str(time[1][1])
            
        else:
            
            time[1] = str(time[1][0])+':'+str(time[1][1])
            
    # Display times.
    y = 0
    for i in range(10):
        
        if i <= len(times)-1:
        
            pyglet.text.Label(times[i][0]+'   -   '+str(times[i][1]), font_name = 'Arial', font_size = 12, x = SCREEN_W/2-45, y = SCREEN_H/2+80-y, 
                              anchor_x = 'left', anchor_y = 'center', batch = batch)
            y += 25
            
    # Create labels.
    x = 0
    for i in range(10):
        
        if i+1 == 10:
            
            x = 5
            
        pyglet.text.Label(str(i+1)+'.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2-60-x, y = SCREEN_H/2+80-(i*25), anchor_x = 'center', anchor_y = 'center', batch = batch)
        
    pyglet.text.Label('Top Times', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-75, anchor_x = 'center', anchor_y = 'center', batch = batch)

    
def save_time():
    """ Saves the players time to a file. """
    
    # Remove widgets.
    widgets_list[len(widgets_list)-1].remove()
    widgets_list.remove(widgets_list[len(widgets_list)-1])
    text = widgets_list[len(widgets_list)-1].document.text
    widgets_list[len(widgets_list)-1].remove()
    widgets_list.remove(widgets_list[len(widgets_list)-1])
    
    # Save time.
    toptimes_shelf = shelve.open('DATA\\Game of Fifteen\\toptimes')
    toptimes_shelf[str(len(toptimes_shelf.keys()))] = [text, time]
    toptimes_shelf.close()
    
    # Add top times widget/label and change info.
    pyglet.text.Label('Time saved.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2+6, y = 42, anchor_x = 'center', anchor_y = 'center', batch = batch)
    widgets_list.append(Widget.Button(SCREEN_W/2+4, 17, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Top Times', batch, "top_times()"))
    info.text = 'Click restart to start a new game.'
 

def create_solved():
    """ Creates a solved puzzle. """
    
    counter = 1
    tempboard = []
    
    for x in range(BOARD_W):
    
        column = []
        
        for y in range(BOARD_H):
        
            column.append(counter)
            counter += BOARD_W
            
        tempboard.append(column)
        counter -= BOARD_W * (BOARD_H - 1) + BOARD_W - 1

    tempboard[BOARD_W-1][BOARD_H-1] = None
    
    return tempboard
    

def generate_puzzle(dt, slides):
    """ Creates a new puzzle. """
    
    global active
    
    if slides > 1:
        
        # Find piece to move.
        while True:
            
            # Make sure it wasn't the last piece to be moved.
            widget = random.choice(widgets_list)
            
            if sequence == [] or widget != sequence[len(sequence)-1]:
                
                # Move puzzle piece.
                exit = move_piece(widget)
                
                if exit:

                    # Add piece to end of sequence.
                    sequence.append(widget)
                    break
        
        slides -= 1
        pyglet.clock.schedule_once(generate_puzzle, 0.15, slides)
        
    else:
        
        # Update info.
        info.text = 'Click a tile to move it. '
        
        # Set schedules.
        pyglet.clock.schedule_interval(update_time, 1)
        
        # Set active.
        active = True


def reset_puzzle(dt):
    """ Resets the puzzle. """
    
    global active, time
    
    # Set game state to inactive.
    active = False
    
    # Reset time.
    time = [0, 0]
    time_label.text = '0:00'
    
    # Unschedule everything.
    unschedule_everything()
    
    # Set info text.
    info.text = 'Reseting..'
    
    # Reset player's moves.
    if player_sequence != []:
        
        move_piece(player_sequence[len(player_sequence)-1])
        player_sequence.pop(len(player_sequence)-1)
        pyglet.clock.schedule_once(reset_puzzle, 0.15)
    
    # End of sequence.
    else:
        
        if solved == False:
        
            # Update info.
            info.text = 'Reset! Click a tile to move it.'
        
            # Set schedules.
            pyglet.clock.schedule_interval(update_time, 1)
        
        else:
            
            # Update info.
            info.text = 'Reset! Click restart to start a new game.'   
        
        active = True
        

def solve_puzzle(dt):
    """ Solves the puzzle """
    
    global active, solved, time
    
    # Set game state to inactive.
    active = False
    solved = True
    
    # Reset time.
    time = [0, 0]
    time_label.text = '0:00'
    
    # Unschedule everything.
    unschedule_everything()
    
    # Set info text.
    info.text = 'Solving...'
    
    # Solved puzzle.
    if board != solved_board:
    
        # Reset player's moves first.
        if player_sequence != []:
        
            move_piece(player_sequence[len(player_sequence)-1])
            player_sequence.pop(len(player_sequence)-1)
            pyglet.clock.schedule_once(solve_puzzle, 0.15)
        
        # Move puzzle pieces till end of sequence.
        elif sequence != []:
    
            move_piece(sequence[len(sequence)-1])
            sequence.pop(len(sequence)-1)
            pyglet.clock.schedule_once(solve_puzzle, 0.15)
    
    # Solved.
    else:
        
        active = True
        info.text = 'Solved! Click restart to start a new game.'
        
        
def update_time(dt):
    """ Updates the time. """
    
    time[1] += 1
    
    if time[1] == 60:
        
        time[0] += 1
        time[1] = 0
    
    if time[1] < 10:
        
        time_label.text = str(time[0])+':0'+str(time[1])
    
    else:
        
        time_label.text = str(time[0])+':'+str(time[1])
        

def move_piece(widget):
    """ Moves puzzle piece. """
    
    for x in range(BOARD_W):
        
        for y in range(BOARD_H):
            
            if board[x][y] == None:
                
                # Left/Right.
                if widget.y-((410-PIECE_H/2)-(80*y)) == 1:
                    
                    if widget.x-((160+(PIECE_W/2)) + (80*x)) == 80 or widget.x-((160+(PIECE_W/2)) + (80*x))== -80:
                    
                        board[x][y] = int(widget.label.text)
                        board[((widget.x)-(160+PIECE_W/2))/80][((410+PIECE_H/2)-(widget.y))/80] = None
                        pyglet.clock.schedule_once(slide, 0.03, widget, (160+(PIECE_W/2)) + (80*x), widget.y)
                        
                        # Exit if generating puzzle.
                        if active == False:
                            
                            return True
                        
                        player_sequence.append(widget)
                        
                # Up/down.
                elif widget.x-((160+(PIECE_W/2)) + (80*x)) == 0:
                    
                    if widget.y-((410-PIECE_H/2)-(80*y)) == 81 or widget.y-((410-PIECE_H/2)-(80*y)) == -79:
                        
                        board[x][y] = int(widget.label.text)
                        board[((widget.x)-(160+PIECE_W/2))/80][((410+PIECE_H/2)-(widget.y))/80] = None
                        pyglet.clock.schedule_once(slide, 0.03, widget, widget.x, (410-PIECE_H/2+1)-(80*y))
                        
                        # Exit if generating puzzle.
                        if active == False:
                            
                            return True
                            
                        player_sequence.append(widget)
                    
                return
               

def slide(dt, widget, x, y):
    """ Creates a slide type animation. """
    
    global input, save
    
    if widget.x < x:

        widget.x += 20
        widget.label.x = widget.x
        pyglet.clock.schedule_once(slide, 0.03, widget, x, y)
        
    elif widget.x > x:
        
        widget.x -= 20
        widget.label.x = widget.x
        pyglet.clock.schedule_once(slide, 0.03, widget, x, y)
    
    elif widget.y < y:
        
        widget.y += 20
        widget.label.y = widget.y
        pyglet.clock.schedule_once(slide, 0.03, widget, x, y)
    
    elif widget.y > y:
        
        widget.y -= 20
        widget.label.y = widget.y
        pyglet.clock.schedule_once(slide, 0.03, widget, x, y)
    
    elif active == True and solved == False:
        
        if board == solved_board:
            
            # Change info.
            info.text = 'Solved! Save your time below or click restart to start a new game.'
            
            # Create widgets.
            widgets_list.append(Widget.Input(SCREEN_W/2-(BUTTON_W/2)+4, 32, BUTTON_W, 20, 15, batch))
            widgets_list.append(Widget.Button(SCREEN_W/2+4, 17, BUTTON_W, BUTTON_H, GREEN, BLACK, 'Save Time', batch, "save_time()"))
            
            # Unschedule everything.
            unschedule_everything()
    
    widget.move_border()
    

def unschedule_everything():
    """ Unschedules everything. """
    
    pyglet.clock.unschedule(move_piece)
    pyglet.clock.unschedule(update_time)
    pyglet.clock.unschedule(generate_puzzle)
    pyglet.clock.unschedule(reset_puzzle)
    pyglet.clock.unschedule(solve_puzzle)
    
            
@mainWindow.event
def on_mouse_motion(x, y, dx, dy):
    """ Determines what happens on mouse movement. """
    
    global MOUSE_X, MOUSE_Y
    
    MOUSE_X = x
    MOUSE_Y = y

 
@mainWindow.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """ Highlights text in input box. """
    
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
def on_key_press(symbol, modifiers):
    """ Handles the key presses. """
    
    if symbol == key.ESCAPE and menu == False:
        
        main_menu()
        return pyglet.event.EVENT_HANDLED
    
    elif symbol == key.R and menu == False:
    
        start_game()
        
    elif symbol == key.ENTER:
        
        for widget in widgets_list:
            
            if widget.type == 'Input':
                
                save_time()

        
@mainWindow.event
def on_text(text):
    """ Add text to input box. """
    
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
def on_draw():
    """ Draws everything to screen. """
    
    global MOUSE_LEFT_CLICKED
    
    # Clear screen.
    mainWindow.clear()
    
    # Draw Widgets.
    num = 0
    selected = False
    for widget in widgets_list:
        
        if widget.collision(MOUSE_X, MOUSE_Y):
                
            if widget.type == 'Button':
                    
                # Deactivate pieces and solve/reset buttons if puzzle is being generated.
                str = ['move_piece(widget)', 'reset_puzzle(0)', 'solve_puzzle(0)']
                if widget.click_action not in str or active == True:

                    widget.opacity = 155
                    selected = True
                    cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_HAND)
                    mainWindow.set_mouse_cursor(cursor)
                
                    if MOUSE_LEFT_CLICKED == True:
                        
                        widget.opacity = 255
                        eval(widget.click_action)
                        MOUSE_LEFT_CLICKED = False
            
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
            
            if selected == False:
            
                cursor = mainWindow.get_system_mouse_cursor(mainWindow.CURSOR_DEFAULT)
                mainWindow.set_mouse_cursor(cursor)  
          
    # Draw batch.
    batch.draw()
                           
                              
# Run the game.
main_menu()
pyglet.app.run()