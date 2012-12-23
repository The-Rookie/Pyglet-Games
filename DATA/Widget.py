########################################
#
# Widget module for Game Box.
#
# Author: John Bullard
#
########################################


#############################################
# Imports.
#############################################

import pyglet


#############################################
# Classes.
#############################################


class Button(pyglet.sprite.Sprite):
    """ A button inside a game. """
    
    def __init__(self, x, y, width, height, color, bordercolor, text, batch, click_action, 
                 font_name = 'Arial', textcolor = (255, 255, 255, 255), bold = False):
        """ Initiate button class. """
        
        self.click_action = click_action
        self.type = 'Button'
        
        # Build an image.
        pattern = pyglet.image.SolidColorImagePattern((color))
        image = pyglet.image.create(width, height, pattern)

        # Center image.
        image.anchor_x, image.anchor_y = width/2, height/2

        # Create sprite out of image.
        pyglet.sprite.Sprite.__init__(self, image, x, y, batch = batch, group = pyglet.graphics.OrderedGroup(1))
        

        # Create label over top of button.
        if text != '':
        
            self.label = pyglet.text.Label(text, font_name = 'Arial', font_size = 12, bold = bold, x = x, y = y, anchor_x = 'center', anchor_y = 'center', color = textcolor, batch = batch)
        
        # Create border.
        self.top = batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (x-(width/2), y+(height/2)-1, x+(width/2), y+(height/2)-1)), ('c4B', bordercolor*2))
        self.left = batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (x-(width/2), y+(height/2), x-(width/2), y-(height/2))), ('c4B', bordercolor*2))
        self.right = batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (x+(width/2), y+(height/2), x+(width/2), y-(height/2)-1)), ('c4B', bordercolor*2))
        self.bottom = batch.add(2, pyglet.gl.GL_LINES, None, ('v2i', (x-(width/2), y-(height/2)-1, x+(width/2), y-(height/2)-1)), ('c4B', bordercolor*2))
    
    
    def move_border(self):
        """ Moves the border around button. """
        
        self.top.vertices = ((self.x-(self.image.width/2), self.y+(self.image.height/2)-1, self.x+(self.image.width/2), self.y+(self.image.height/2)-1))
        self.left.vertices = ((self.x-(self.image.width/2), self.y+(self.image.height/2), self.x-(self.image.width/2), self.y-(self.image.height/2)))
        self.right.vertices = ((self.x+(self.image.width/2), self.y+(self.image.height/2), self.x+(self.image.width/2), self.y-(self.image.height/2)-1))
        self.bottom.vertices = ((self.x-(self.image.width/2), self.y-(self.image.height/2)-1, self.x+(self.image.width/2), self.y-(self.image.height/2)-1))
    
    
    def collision(self, x, y):
        """ Check for collision with button. """
        
        return (0 < x - self.x+(self.image.width/2)+1 < self.image.width-1 and
                0 < y - self.y+(self.image.height/2)-1 < self.image.height+1)
                
    
    def remove(self):
        """ Removes button. """
        
        self.delete()
        self.label.delete()
        self.top.delete()
        self.left.delete()
        self.right.delete()
        self.bottom.delete()
    
        
class Input():
    """ A input box inside a game. """
    
    def __init__(self, x, y, width, height, maxlength, batch, active = True, background = False, background_color = [0, 0, 0, 0]):
        """ Initiate input class. """
        
        self.type = 'Input'
        self.maxlength = maxlength
        self.active = active
        
        # Create document.
        self.document = pyglet.text.document.UnformattedDocument()
        self.document.set_style(0, len(self.document.text), dict(font_name = 'Arial', font_size = 12, color = (255, 255, 255, 255)))
        
        # Create layout.
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, width, height, batch = batch)
        self.layout.x = x
        self.layout.y = y
        
        # Create caret.
        self.caret = pyglet.text.caret.Caret(self.layout)
        self.caret.color = (255, 255, 255)
        
        if active == True:
        
            self.caret.mark = 0
        
        if background == True:
        
            batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x-2, y+1, x+width+2, y+1, x+width+2, height+y, x-2, height+y]),
            ('c4B', background_color * 4))
    
    
    def collision(self, x, y):
        """ Check for collision with button. """
        
        return (0 < x - self.layout.x+3 < self.layout.width-3 and
                0 < y - self.layout.y < self.layout.height)
    
    
    def remove(self):
        """ Removes input. """
        
        self.caret.delete()
        self.layout.delete()
        