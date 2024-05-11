# game.py

from random import randint
import random
import pgzrun
import pygame
import os
import copy

from protagonist import Protagonist
from enemy import Enemy


from game_environment import *

class EnemyGenerator:
    def __init__(self, max_enemies, enemy_data):
        self.max_enemies = max_enemies
        self.enemy_data = enemy_data  # List of Enemy data structures
        self.enemies = []  # List of tuples: (enemy_data, Actor)

    def generate_enemy(self):
        """
        Randomly selects an enemy type from enemy_data and creates an enemy Actor.
        """
        enemy_type = random.choice(self.enemy_data)
        enemy_data_copy = copy.deepcopy(enemy_type)
        enemy_actor = Actor(enemy_data_copy.getImage())  # Create Actor based on image
        return enemy_data_copy, enemy_actor  # Return a tuple (enemy_data, Actor)

    def update(self):
        """
        Updates enemy list: removes dead enemies, generates new ones up to MAX_ENEMYS.
        """
        # Remove dead enemies
        for enemy_data, enemy_actor in self.enemies:
            if enemy_data.enemyDead():
                self.enemies.remove((enemy_data, enemy_actor))
            enemy_data.update()

        # Generate new enemies to maintain MAX_ENEMYS
        num_missing_enemies = self.max_enemies - len(self.enemies)
        for _ in range(num_missing_enemies):
            new_enemy_data, new_enemy_actor = self.generate_enemy()
            self.enemies.append((new_enemy_data, new_enemy_actor))

    def get_enemies(self):
        """
        Returns the list of tuples containing enemy data and Actor objects.
        """
        return self.enemies


TITLE = "You have the Last change to get the job! Show me what you're made of"

os.environ['SDL_VIDEO_CENTERED'] = '1'

background = Actor(C.BACKGROUND_PICTURE)
MENU_BACKGROUND = Actor("background/cemetery2.jpg")  # Add a background image for the menu

# Creating of main character
protagonistData = Protagonist()
protagonistActor = Actor(protagonistData.getImage())


# List of Enemy data structures (path, run_images)
enemy_data = [
        Enemy(C.path, C.run_images_zombief),
        Enemy(C.pathZM, C.run_images_zombieM),
        Enemy(C.bat_path, C.run_images_bat),
        Enemy(C.ghost_path, C.run_images_ghost),
        Enemy(C.dino_path, C.run_images_dino)
    ]

enemy_generator = EnemyGenerator(C.MAX_ENEMIES, enemy_data)

WIDTH = C.WIDTH
HEIGHT = C.HEIGHT

is_pause = False
score = 0
game_over = False

# Menu state and button functions
menu_active = True
music_on = True  # Assume music starts on
sounds_on = True  # Assume sounds start on

sounds.horrorambience.play(-1)

#---------------
# Create menu components
#---------------
def start_game():
    global menu_active
    menu_active = False

def toggle_music():
    global music_on
    music_on = not music_on  # Toggle music state

    if music_on:
        sounds.horrorambience.play(-1)
    else:
        sounds.horrorambience.stop()

def toggle_sounds():
    global sounds_on
    sounds_on = not sounds_on  # Toggle sounds state

def on_mouse_down(pos):
    #print("Mouse button clicked at", pos)
    if pos[1] <250 and pos[1] > 200 and pos[0]<700 and pos[0]> 500:
        #print("Start Game")
        start_game()
    if pos[1] <350 and pos[1] > 300 and pos[0]<700 and pos[0]> 500:
        #print("Toggle Music")
        toggle_music()
    if pos[1] <450 and pos[1] > 400 and pos[0]<700 and pos[0]> 500:
        #print("Toggle Sounds")
        toggle_sounds()
    if pos[1] < 550 and pos[1] > 500 and pos[0]<700 and pos[0]> 500:
        #print("Quit Game")
        quit_game()

def quit_game():
    quit()

def draw_menu_button(text, pos_y, action):
    # Create button rectangle based on text size and padding
    button_width = 140 + 2 * C.MENU_BUTTON_PADDING
    button_rect = Rect(WIDTH // 2 - button_width // 2, pos_y, button_width, 50)

    # Draw button background
    screen.draw.filled_rect(button_rect, C.MENU_BUTTON_COLOR)

    # Draw button text centered within the button
    text_x = button_rect.centerx - 140 // 2
    screen.draw.text(text, (text_x, pos_y + 5), color=C.MENU_BUTTON_TEXT_COLOR)


def draw_menu():
    MENU_BACKGROUND.draw()
    draw_menu_button("Start Game", HEIGHT // 3, start_game)
    draw_menu_button("Toggle Music" + (" (On)" if music_on else " (Off)"), HEIGHT // 2, toggle_music)
    draw_menu_button("Toggle Sounds" + (" (On)" if sounds_on else " (Off)"), 2 * HEIGHT // 3, toggle_sounds)
    draw_menu_button("Quit Game", HEIGHT - 100, quit_game)

#----------------------------

def draw():
    if menu_active:
        draw_menu()  # Draw the menu if active
    else:
        if is_pause:
            screen.draw.text("Pause", fontsize=72, color=(255, 0, 0), center=(C.WIDTH / 2, C.HEIGHT / 2))
            screen.draw.text("Instruction:\nSpace - hit; Up - jump; LEFT,RIGHT - move", fontsize=72, color=(255, 0, 0), center=(C.WIDTH / 2, C.HEIGHT / 2 + 80))
            return
        screen.clear()
        background.draw()

        protagonistActor.image = protagonistData.getImage()
        protagonistActor.draw()

        for i, (enemy_data, enemy_actor) in enumerate(enemy_generator.get_enemies()):

            enemy_actor.image = enemy_data.getImage()
            enemy_actor.draw()

        drawEnvironment(screen)

        screen.draw.text('Health: ' + str(protagonistData.health), (15, 10), color=(255, 255, 255), fontsize=30)
        screen.draw.text('Scores: ' + str(score), (15, 40), color=(255, 255, 255), fontsize=30)

        if protagonistData.playerDead():
            screen.blit('black_mask75', (0, 0))
            screen.draw.text("Game Over", fontsize=72, color=(255, 0, 0), center=(C.WIDTH/2, C.HEIGHT/2))

def update():
    global is_pause, score, game_over

    # if pressed ESC key - exit app
    if keyboard.ESCAPE:
        quit()

    if menu_active or game_over:
        return  # Skip game updates while in menu

    # if pressed P - pause
    if keyboard.P:
        is_pause = not is_pause

    if is_pause:
        return

    protagonistData.readKeyboard(keyboard)
    protagonistData.update()

    enemy_generator.update()  # Update enemy list (remove dead, generate new)

    for enemy_data, enemy_actor in enemy_generator.get_enemies():
        enemy_data.update()
        enemy_data.moveEnemy(protagonistData.x, protagonistData.y)

        enemy_data.floor = getGround(enemy_data.x, enemy_data.y)
        enemy_actor.midbottom = (enemy_data.x, enemy_data.y)

        if enemy_actor.colliderect(protagonistActor):
            protagonistData.loseProtagonistHealth(streight=enemy_data.attackStrength)

        if enemy_actor.distance_to(protagonistActor) < 100:
            enemy_data.loseEnemyHealth(streight=protagonistData.attackLength)
            if sounds_on:
                sounds.hit.play()

        if enemy_data.enemyDead():
            score += 1



    protagonistData.floor = getGround(protagonistData.x, protagonistData.y)

    protagonistActor.midbottom = (protagonistData.x, protagonistData.y)

    if protagonistData.playerDead():
        if sounds_on:
            sounds.gameover.play()
        game_over = True



pgzrun.go()