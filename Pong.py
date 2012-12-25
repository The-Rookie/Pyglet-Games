########################################
#
# Title: Simulate
#
# Genre: Arcade
#
# Author: John Bullard
#
# http://therookiedev.blogspot.com/
#
# Created: 12/15/2012
#
########################################


#############################################
# Imports.
#############################################

import pyglet, random, math
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
BUTTON_H= 24

# Paddle size.
PADDLE_W = 8
PADDLE_H = 32

# Ball size. *Cough*
BALL_W = 8
BALL_H = 8

# Colors.
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# Create window.
mainWindow = pyglet.window.Window(SCREEN_W, SCREEN_H, vsync = False, caption = "Pong")

# Center window.
mainWindow.set_location(mainWindow.screen.width/2 - mainWindow.width/2, mainWindow.screen.height/2 - mainWindow.height/2)

# Mouse.
MOUSE_X = mainWindow.screen.width/2 - mainWindow.width/2
MOUSE_Y = mainWindow.screen.height/2 - mainWindow.height/2
MOUSE_LEFT_CLICKED = False

# Keyboard.
KEYMAP = key.KeyStateHandler()


class Player(pyglet.sprite.Sprite):
    """ A player in the game. """
    
    def __init__(self, x, y, color, batch):
        """ Initiate the player class. """

        # Build an image for the paddle.
        pattern = pyglet.image.SolidColorImagePattern((color))
        image = pyglet.image.create(PADDLE_W, PADDLE_H, pattern)

        # Offset image.
        image.anchor_x, image.anchor_y = 4, 16

        # Create sprite out of image.
        pyglet.sprite.Sprite.__init__(self, image, x, y, batch = batch)
        
        # Set players score.
        self.score = 0
        
   
    def ai(self):
        """ Handles AI if two players is not active. """
        
        if ball.vx > 0:
            
            if ball.y-self.image.anchor_y > self.y and self.y+self.image.anchor_y < 360:
                
                self.y += 4
                
            elif ball.y+self.image.anchor_y < self.y and self.y-self.image.anchor_y > 0:
            
                self.y -= 4

        
class Ball(pyglet.sprite.Sprite):
    """ A ball in the game. """
    
    def __init__(self, color):
        """ Initiate ball class. """
        
        # Build an image for the ball.
        pattern = pyglet.image.SolidColorImagePattern((color))
        image = pyglet.image.create(BALL_W, BALL_H, pattern)
        
        # Offset image.
        image.anchor_x, image.anchor_y = 4, 4

        # Create sprite out of image.
        pyglet.sprite.Sprite.__init__(self, image, batch=batch)

        # Reset.
        self.reset()
    
    
    def update(self, dt):
        """ Updates the balls position. """
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        if self.x > SCREEN_W:
            
            player1.score += 1
            scoreLabel1.text = str(player1.score)
            self.reset() 
        
        elif self.x < 0:    
            
            player2.score += 1
            scoreLabel2.text = str(player2.score)
            self.reset()
            
        self.collision()
     
     
    def reset(self):
        """ Place the ball in the center of screen and send it in a random direction. """
        
        global active
        
        # Place ball in center of screen.
        self.x, self.y = SCREEN_W/2, 180
        
        # Reset players.
        player1.y = 180
        player2.y = 180
        
        # Reset active.
        active = False
        
        # Go a random direction.
        angle = random.random()*math.pi/2 + random.choice([-math.pi/4, 3*math.pi/4])

        # Convert it to velocity.
        self.vx, self.vy = math.cos(angle)*300, math.sin(angle)*300
    
    
    def collision(self):
        """ Check for collisions. """
        
        # Playing area.
        if self.y > 360-self.image.anchor_y:

            self.y = 360-self.image.anchor_y
            self.vy = -self.vy

        elif self.y < 0+self.image.anchor_y:

            self.y = 0+self.image.anchor_y
            self.vy = -self.vy
        
        # Player 1 paddle.
        if (0 < self.x - self.image.anchor_x - player1.x+(player1.image.width/2) < player1.image.width and
            -self.image.anchor_y < self.y - player1.y+(player1.image.height/2) <  player1.image.height+self.image.anchor_y):
        
                self.x = player1.x+player1.image.width
                self.vx = -self.vx+10

                # Bounce off of paddle.
                self.vy += (self.y - player1.y)/2
            
        # Player 2 paddle.
        if (0 < self.x + self.image.anchor_x - player2.x+(player1.image.width/2) < player2.image.width and
            -self.image.anchor_y < self.y - player2.y+(player2.image.height/2) <  player2.image.height+self.image.anchor_y):
        
                self.x = player2.x-player2.image.width
                self.vx = -self.vx-10

                # Bounce off of paddle.
                self.vy += (self.y - player2.y)/2
        
        
def main_menu():
    """ Main menu in the game. """
    
    global batch, menu, widgets_list
        
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Menu.
    menu = True
    
    # Create widgets.
    widgets_list = [Widget.Button(SCREEN_W/2, SCREEN_H/2-1, BUTTON_W, BUTTON_H, WHITE, WHITE, '1 Player', batch, 'start_game(False)', textcolor = BLACK), 
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-32, BUTTON_W, BUTTON_H, WHITE, WHITE, '2 Players', batch, 'start_game(True)', textcolor = BLACK), 
                    Widget.Button(SCREEN_W/2, SCREEN_H/2-63, BUTTON_W, BUTTON_H, WHITE, WHITE, 'Exit Game', batch, 'pyglet.app.exit()', textcolor = BLACK)]
                  
    # Create labels.
    pyglet.text.Label('Pong', font_name = 'Arial', font_size = 32, x = SCREEN_W/2, y = SCREEN_H-100, anchor_x = 'center', anchor_y = 'center', batch = batch)


def start_game(twoplayers):
    """ Starts game. """
    
    global batch, menu, active, MULTIPLAYER, widgets_list, player1, player2, ball, scoreLabel1, scoreLabel2, info, keymap
    
    # Reset batch for rendering.
    batch = pyglet.graphics.Batch()
    
    # Unschedule update.
    pyglet.clock.unschedule(update)
    
    # Menu.
    menu = False
    
    # Reset active and schedule.
    active = False
    
    # Multiplayer.
    MULTIPLAYER = twoplayers
    
    # Reset widgets.
    widgets_list = []
    
    # Create players.
    player1 = Player(32, 180, WHITE, batch)
    player2 = Player(SCREEN_W-32, 180, WHITE, batch)
    
    # Create ball.
    ball = Ball(WHITE)
    
    # Create labels.
    pyglet.text.Label('Player 1', font_name = 'Arial', font_size = 20, x = 84, y = SCREEN_H-30, anchor_x = 'center', anchor_y = 'center', batch = batch)
    scoreLabel1 = pyglet.text.Label(str(player1.score), font_name = 'Arial', font_size = 42, x = 84, y = SCREEN_H-75, anchor_x = 'center', anchor_y = 'center', batch = batch)
    if MULTIPLAYER == True:
        pyglet.text.Label('Player 2', font_name = 'Arial', font_size = 20, x = SCREEN_W-64, y = SCREEN_H-30, anchor_x = 'center', anchor_y = 'center', batch = batch)
        info = pyglet.text.Label('Press the Space Bar to start. W/S moves player 1, Arrow keys move player 2.', font_name = 'Arial', font_size = 12, 
        x = SCREEN_W/2, y = 210, anchor_x = 'center', anchor_y = 'center', batch = batch)
    
    else:
        pyglet.text.Label('CPU', font_name = 'Arial', font_size = 20, x = SCREEN_W-64, y = SCREEN_H-30, anchor_x = 'center', anchor_y = 'center', batch = batch)
        info = pyglet.text.Label('Press the Space Bar to start. W/S moves player 1.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = 210, 
                                 anchor_x = 'center', anchor_y = 'center', batch = batch)
    scoreLabel2 = pyglet.text.Label(str(player2.score), font_name = 'Arial', font_size = 42, x = SCREEN_W-64, y = SCREEN_H-75, anchor_x = 'center', anchor_y = 'center', batch = batch)
    
    # Divider.
    batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (0, 360, SCREEN_W, 360)))
    
    # Schedule update function.
    pyglet.clock.schedule_interval(update, 1.0/60.0)

    
def update(dt):
    """ Updates the player/computer/ball and checks who won. """
    
    global active, info
    
    # Push keymap events.
    mainWindow.push_handlers(KEYMAP)
    
    if active == True:
    
        if KEYMAP[key.W]:
        
            if player1.y+player1.image.anchor_y < 360:
        
                player1.y += 4
        
        elif KEYMAP[key.S]:
        
            if player1.y-player1.image.anchor_y > 0:
        
                player1.y -= 4
        
        if MULTIPLAYER == True:
        
            if KEYMAP[key.UP]:
        
                if player2.y+player2.image.anchor_y < 360:
        
                    player2.y += 4
        
            elif KEYMAP[key.DOWN]:
        
                if player2.y-player2.image.anchor_y > 0:
        
                    player2.y -= 4
                    
        else:
            
            player2.ai()
            
        # Update ball.
        ball.update(dt)
        
        if player1.score == 10:
            
            info = pyglet.text.Label('Player 1 wins!', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = 210, anchor_x = 'center', anchor_y = 'center', batch = batch)
            info2 = pyglet.text.Label('Press the Space Bar to restart.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = 160, anchor_x = 'center', anchor_y = 'center', batch = batch)
            active = False
            
        elif player2.score == 10:
            
            if MULTIPLAYER == True:
                
                info = pyglet.text.Label('Player 2 wins!', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = 210, anchor_x = 'center', anchor_y = 'center', batch = batch)
                
            else:
                
                info = pyglet.text.Label('CPU wins!', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = 210, anchor_x = 'center', anchor_y = 'center', batch = batch)
                
            info2 = pyglet.text.Label('Press the Space Bar to restart.', font_name = 'Arial', font_size = 12, x = SCREEN_W/2, y = 160, anchor_x = 'center', anchor_y = 'center', batch = batch)
            active = False
              

@mainWindow.event
def on_key_press(symbol, modifiers):
    """ Handles the key presses. """
    
    global active
    
    if symbol == key.SPACE and menu == False:
        
        if player1.score == 10 or player2.score == 10:
            
            start_game(MULTIPLAYER)
            
        else:
        
            active = True
            info.delete()
            
    elif symbol == key.ESCAPE and menu == False:
        
        main_menu()
        return pyglet.event.EVENT_HANDLED
    
    elif symbol == key.R and menu == False:
        
        start_game(MULTIPLAYER)

        
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