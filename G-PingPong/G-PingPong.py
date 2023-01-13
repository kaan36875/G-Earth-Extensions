import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from g_python.hpacket import HPacket

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

furniclick = in_setup = on = False
left = None                      # The side you playing on

# Coord for both side, x[0] left, x[1] right
chair = [[], []]
tile = [[], []]
ball = [[], []]

ball_id = None                      # Ball's Furni ID


def walk(x, y):       # Makes the user walk to coords
    ext.send_to_server(HPacket(USER_MOVE, int(x), int(y)))


def chat(message):   # Sends client messages
    ext.send_to_client(HPacket(SPEECH_IN, 0, str(message), 0, 1, 0, 0))

def reset():
    global chair, tile, ball, ball_id

    chair = [[], []]
    tile = [[], []]
    ball = [[], []]

    ball_id = None


def speech(p): # User used the command
    global in_setup, left, on

    text, _, _ = p.packet.read('sii')

    if text == HELP_CMD:
        p.is_blocked = True
        chat(f'''
            {SETUP_CMD} : Starts the tile, ball setup \n
            {START_CMD} : Starts the g-pingpong \n
            {STOP_CMD} : Stops the g-pingpong \n
            {LEFT_CMD} : Use if you are sitting on the left side. \n
            {RIGHT_CMD} : Use if you are sitting on the right side.
        ''')

    elif text == LEFT_CMD:
        p.is_blocked = True
        left = True
        chat('Left chair selected!')

    elif text == RIGHT_CMD:
        p.is_blocked = True
        left = False
        chat('Right chair selected!')

    elif text == SETUP_CMD:
        p.is_blocked = True
        reset()
        in_setup = True
        chat('Please click the left chair.')

    elif text == START_CMD:
        p.is_blocked = True

        if not ball:
            chat(f'Please do the setup first! - {SETUP_CMD}')
        elif left is None:
            chat(f'Please select a side first! - {LEFT_CMD} , {RIGHT_CMD}')
        else:
            on = True
            chat('G-PingPong started!')

    elif text == STOP_CMD:
        p.is_blocked = True
        on = False
        chat('G-PingPong stopped!')


def setup(p): # User clicks to choose coords
    global in_setup, furniclick

    if in_setup:
        x, y = p.packet.read('ii')
        chat('Please click the left chair.')
        
        if not chair[0]:
            chair[0] = [x, y]
            chat(f"Left chair : {chair[0]}")
            chat('Please click the left tile.')

        elif not tile[0]:
            tile[0] = [x, y]
            chat(f"Left tile : {tile[0]}")
            chat('Please click the right chair.')

        elif not chair[1]:
            chair[1] = [x, y]
            chat(f"Right chair : {chair[1]}")
            chat('Please click the right tile.')

        elif not tile[1]:
            tile[1] = [x, y]
            chat(f"Right chair : {tile[1]}")
            chat('Please click the left ball tile.')

        elif not ball[0]:
            ball[0] = [x, y]
            chat(f"Left ball : {ball[0]}")
            chat('Please click the right ball tile.')

        elif not ball[1]:
            ball[1] = [x, y]
            chat(f"Right ball : {ball[1]}")
            chat('Please double-click the ball.')
            furniclick = True
            in_setup = False


def set_ball(p): # Find ball's ID
    global furniclick, ball_id

    if furniclick:
        ball_id, _ = p.packet.read('ii')
        furniclick = False
        chat(f"{ball_id=}")
        chat(f'Setup Complete! \n Type {LEFT_CMD} or {RIGHT_CMD} before start.')


def pingpong(p):
    _, _, x, y, _, furni, _, _, _ = p.packet.read('iiiiiissi')

    if not on or ball_id != furni:
        return

    if left:
        if ball[0] == [x, y]:
            walk(tile[0], tile[1])
        elif ball[1] == [x, y]:
            walk(chair[0], chair[1])
    else:
        if ball[0] == [x, y]:
            walk(chair[0], chair[1])
        elif ball[1] == [x, y]:
            walk(tile[0], tile[1])


ext.intercept(Direction.TO_SERVER, speech, SPEECH_OUT)
ext.intercept(Direction.TO_SERVER, setup, USER_MOVE)
ext.intercept(Direction.TO_SERVER, set_ball, USE_FURNI)
ext.intercept(Direction.TO_CLIENT, pingpong, WIRED_MOVE_FURNI)
