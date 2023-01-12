import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction

extension_info = {
    "title": "G-PingPong",
    "description": ":phelp - For All Commands",
    "version": "1.0",
    "author": "Kaan36875"
}

ext = Extension(extension_info, sys.argv)
ext.start()

#############HEADERS#############
SPEECH_OUT = 1314
SPEECH_IN = 1446
USER_MOVE = 3320
USE_FURNI = 99
WIRED_MOVE_FURNI = 3207
##################################

#############COMMANDS#############
HELP_CMD = ":phelp"
SETUP_CMD = ":psetup"
LEFT_CMD = ":pleft"
RIGHT_CMD = ":pright"
START_CMD = ":pstart"
STOP_CMD = ":pstop"
##################################

furniclick = False
setup = False
on = False
left = None          # The side you playing on

left_chair = []
left_tile = []
right_chair = []
right_tile = []
ball_id = 0          # Ball's Furni ID
left_ball = []       # Ball on left tile
right_ball = []      # Ball on right tile


def walk(x,y):       # Makes the user walk to coords
    ext.send_to_server('{h:'+str(USER_MOVE)+'}{i:'+str(x)+'}{i:'+str(y)+'}')
    
def chat(message):   # Sends client messages
    ext.send_to_client('{h:'+str(SPEECH_IN)+'}{i:0}{s:"'+str(message)+'"}{i:0}{i:1}{i:0}{i:0}')
                       
def speech(message): # User used the command
    global setup
    global left
    global on
    global left_chair
    global left_tile
    global right_chair
    global right_tile
    global ball_id
    global left_ball
    global right_ball
    
    (text,_,_) = message.packet.read('sii')
    if text == HELP_CMD:
        message.is_blocked = True
        chat(''+SETUP_CMD+': Starts the tile, ball setup')
        chat(''+START_CMD+': Starts the g-pingpong')
        chat(''+STOP_CMD+': Stops the g-pingpong')
        chat(''+LEFT_CMD+': Use if you are sitting on the left side.')
        chat(''+RIGHT_CMD+': Use if you are sitting on the right side.')
        return

    if text == LEFT_CMD:
        message.is_blocked = True
        left = True
        chat('Left chair selected!')
        return

    if text == RIGHT_CMD:
        message.is_blocked = True
        left = False
        chat('Right chair selected!')
        return

    if text == SETUP_CMD:
        message.is_blocked = True
        setup = True
        left_chair = []
        left_tile = []
        right_chair = []
        right_tile = []
        ball_id = 0
        left_ball = []
        right_ball = []
        chat('Please click the left chair.')
        return

    if text == START_CMD:
        message.is_blocked = True
        if not right_ball:
            chat('Please do the setup first! - '+SETUP_CMD+'')
            return
        if left == None:
            chat('Please select a side first! - '+LEFT_CMD+' , '+RIGHT_CMD+'')
            return
        on = True
        chat('G-PingPong started!')
        return

    if text == STOP_CMD:
        message.is_blocked = True
        on = False
        chat('G-PingPong stopped!')
        return
    
def setup(message): # User clicks to choose coords
    global setup
    global furniclick
    
    if setup:
        (x,y) = message.packet.read('ii')
        if not left_chair:
            left_chair.append(x)
            left_chair.append(y)
            chat(left_chair)
            chat('Please click the left tile.')
            return

        if not left_tile:
            left_tile.append(x)
            left_tile.append(y)
            chat(left_tile)
            chat('Please click the right chair.')
            return

        if not right_chair:
            right_chair.append(x)
            right_chair.append(y)
            chat(right_chair)
            chat('Please click the right tile.')
            return

        if not right_tile:
            right_tile.append(x)
            right_tile.append(y)
            chat(right_tile)
            chat('Please click the left ball tile.')
            return

        if not left_ball:
            left_ball.append(x)
            left_ball.append(y)
            chat(left_ball)
            chat('Please click the right ball tile.')
            return

        if not right_ball:
            right_ball.append(x)
            right_ball.append(y)
            chat(right_ball)
            chat('Please double-click the ball.')
            furniclick = True
            setup = False
            return
        
def set_ball(message): # Find ball's ID
    global furniclick
    global ball_id
    
    if furniclick:
        (furni_id,_) = message.packet.read('ii')
        ball_id = furni_id
        furniclick = False
        chat(str(ball_id))
        chat('Setup Complete! Type '+LEFT_CMD+' or '+RIGHT_CMD+' before start.')
        return

def pingpong(message):
    global left_chair
    global left_tile
    global right_chair
    global right_tile
    global ball_id
    global left_ball
    global right_ball
    global left
    
    if on:
        (_,_,x,y,_,ball,_,_,_) = message.packet.read('iiiiiissi')
        if ball_id == ball:
            if left:
                if x and y in left_ball:
                    walk(left_tile[0],left_tile[1])
                    return
                elif x and y in right_ball:
                    walk(left_chair[0],left_chair[1])
                    return
            elif not left:
                if x and y in left_ball:
                    walk(right_chair[0],right_chair[1])
                    return
                elif x and y in right_ball:
                    walk(right_tile[0],right_tile[1])
                    return
            
#######################################################################
ext.intercept(Direction.TO_SERVER, speech, SPEECH_OUT)
ext.intercept(Direction.TO_SERVER, setup, USER_MOVE)
ext.intercept(Direction.TO_SERVER, set_ball, USE_FURNI)
ext.intercept(Direction.TO_CLIENT, pingpong, WIRED_MOVE_FURNI)
#######################################################################
