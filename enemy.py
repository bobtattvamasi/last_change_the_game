from config import Configuration as C
import math
import random


class Enemy:
    def __init__(self, folder_name, run_images, fps=60, speed=1):
        self.path = f"{folder_name}/"
        self.image = f"{self.path}idle1"
        self.runningImages = run_images
        self.runningImageIndex = 0
        self.velocity_y = 0
        self.velocity_x = 0
        self.speed = speed
        self.y = random.randint(0, C.HEIGHT)
        self.x = random.randint(0, C.WIDTH)
        self.floor = self.y
        self.isJumping = False
        self.jumpPower = 25
        self.accel = 1
        self.enemyIsDead = False
        self.health = 100
        self.attackStrength = 1

        self.animation_time = 0  # Time elapsed for current animation frame
        self.animation_fps = fps  # Frames per second for animation


    def getImage(self):
        return self.image

    def moveEnemy(self, targetX, targetY, gravity=0.5):
        """
                Updates the enemy's position to move towards the protagonist.

                Args:
                    protagonist_x (float): The x-coordinate of the protagonist.
                    protagonist_y (float): The y-coordinate of the protagonist.
                    gravity (float, optional): The gravitational force affecting the enemy. Defaults to 0.5.
                """

        # Calculate distance to protagonist in both x and y directions
        dx = targetX - self.x
        dy = targetY - self.y

        # Normalize the direction vector to avoid diagonal speed scaling
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            normalized_dx = dx / distance
            normalized_dy = dy / distance
        else:
            normalized_dx = 0
            normalized_dy = 0

        # Set velocity based on normalized direction and desired speed
        self.velocity_x = normalized_dx * self.speed
        self.velocity_y = normalized_dy * self.speed

        # Handle enemy jumping (optional)
        if self.isJumping:
            self.velocity_y += gravity  # Apply gravity during jump
            if self.y >= targetY:  # Landed after jump
                self.isJumping = False
                self.velocity_y = 0

        # Update enemy position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Handle edge wrapping (optional)
        if self.x < 0:
            self.x = 0
        elif self.x > C.WIDTH:  # Assuming C.WIDTH is the screen width
            self.x = C.WIDTH



    def update(self):
        if not self.enemyIsDead:
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.velocity_y += C.GRAVITY
            if(self.y >= self.floor and self.velocity_y > 0):
                self.velocity_y = 0
                self.y = self.floor

            #self.image = f'{self.path}idle1'

            # Update animation based on animation FPS and elapsed time
            self.animation_time += 1 / self.animation_fps

            # if self.velocity_x != 0:
            if self.animation_time >= 1 / len(self.runningImages):  # Update image if enough time passed
                self.animation_time = 0
                if self.velocity_x > 0:
                    self.image = self.runningImages[self.runningImageIndex]
                else:
                    self.image = f"{self.runningImages[self.runningImageIndex]}_left"
                self.runningImageIndex += 1
                if self.runningImageIndex >= len(self.runningImages):
                    self.runningImageIndex = 0
                    if self.velocity_x > 0:
                        self.image = f'{self.path}idle1'
                    else:
                        self.image = f'{self.path}idle1_left'
        else:
            self.image = f'{self.path}dead'

    def killEnemy(self):
        self.enemyIsDead = True
        self.velocity_x = 0
        self.attackStrength = 0
        self.speed = 0


    def enemyDead(self):
        return self.enemyIsDead

    def loseEnemyHealth(self, streight = 10):
        self.health -= streight
        if self.health <= 0:
            self.killEnemy()
