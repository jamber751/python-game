from enum import Enum

class GameState(Enum):
    INTRO = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3