# Requirements
- Python
- G-Python

[Tutorial](https://github.com/sirjonasxx/G-Python#installation)

# Commands
- :phelp - to see all commands
- :psetup - Starts the chair, tile, and ball setup
- :rstart - Starts the G-PingPong
- :pstop - Stops the G-PingPong
- :pleft - Use this if you are playing on the left side
- :pright - Use this if you are playing on the right side


# Headers

This extension are made for retro, you need to change the header

- Open the [file](https://github.com/Laande/G-Earth-Extensions/blob/main/G-PingPong/G-PingPong.py)
- Change the header on theses line [17-21](https://github.com/Laande/G-Earth-Extensions/blob/main/G-PingPong/G-PingPong.py#L16-L20)

How to

- For example `SPEECH_OUT`, open the packet logger, send a message and take the header of the packet
- `SPEECH_IN` when someone talk
- `USER_MOVE` packet outgoing (blue) walk on a tile
- `USE_FURNI` double click on a furni (outgoing)
- `WIRED_MOVE_FURNI` when a furni is moove by a wired (set position & state), incoming packet
=======
