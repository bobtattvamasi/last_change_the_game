from typing import NamedTuple

class Configuration(NamedTuple):
    WIDTH = 1200
    HEIGHT = 600
    GRAVITY = 1
    PLAYERWIDTH = 72

    # Menu Constants

    # MENU_FONT = pgzrun.Font("joystix.ttf", 50)  # Choose a suitable font (adjust size if needed)
    MENU_FONT_SIZE = 50
    MENU_BUTTON_COLOR = (255, 200, 100)  # Customize button color
    MENU_BUTTON_TEXT_COLOR = (0, 0, 0)  # Customize button text color
    MENU_BUTTON_PADDING = 20  # Adjust padding around button text

    # BACKGROUND_PICTURE = 'background/background1.png'
    BACKGROUND_PICTURE = 'background/cemetry3.png'

    MAX_ENEMIES = 3

    # Pathes to pictures for the sprites:
    path = "enemy/zombies/female"
    run_images_zombief = [f"{path}/walk1", f"{path}/walk2", f"{path}/walk3",
                          f"{path}/walk4", f"{path}/walk5", f"{path}/walk6",
                          f"{path}/walk7", f"{path}/walk8", f"{path}/walk9",
                          f"{path}/walk10"]

    pathZM = "enemy/zombies/male"
    run_images_zombieM = [f"{path}/walk1", f"{path}/walk2", f"{path}/walk3",
                          f"{path}/walk4", f"{path}/walk5", f"{path}/walk6",
                          f"{path}/walk7", f"{path}/walk8", f"{path}/walk9",
                          f"{path}/walk10"]

    bat_path = "enemy/bat"
    run_images_bat = [f"{bat_path}/bat_fly", f"{bat_path}/bat_hang", f"{bat_path}/bat_fly"]

    ghost_path = "enemy/ghosts/pix_ghost"
    run_images_ghost = [f"{ghost_path}/run1", f"{ghost_path}/run2"]

    dino_path = "enemy/dino"
    run_images_dino = [f"{dino_path}/run1", f"{dino_path}/run2", f"{dino_path}/run3", f"{dino_path}/run4",
                       f"{dino_path}/run5",
                       f"{dino_path}/run6", f"{dino_path}/run7", f"{dino_path}/run8"]

