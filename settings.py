def init():
    global SCALE_FACTOR, MAX_FRAME_RATE, WINDOW_SIZE
    SCALE_FACTOR = 3
    MAX_FRAME_RATE = 60
    WINDOW_SIZE = (1000, 600)
    
    global G, H, WEIGHT
    G=1
    H=1
    WEIGHT=1