from config import Configuration as C

import pygame


class Protagonist:
    def __init__(self):
        self.path = "protagonist/knight/"
        self.image = f'{self.path}idle1'
        self.runningImages = [f'{self.path}run1', f'{self.path}run2', f'{self.path}run2', f'{self.path}run3', f'{self.path}run4', f'{self.path}run5', f'{self.path}run6',
                              f'{self.path}run7', f'{self.path}run8', f'{self.path}run9', f'{self.path}run10']
        self.runningImageIndex = 0
        self.x = C.WIDTH / 2
        self.y = C.HEIGHT / 2
        self.floor = self.y
        self.moveSpeed = 5
        self.isAttacking = False
        self.isJumping = False
        self.velocity_y = 0
        self.velocity_x = 0
        self.maxSpeed = 10
        self.accel = 1
        self.jumpPower = 20
        self.glidingSpeed = 2
        self.attackLength = 0
        self.playerIsDead = False
        self.health = 10000

        self.right_direction = True

        self.clock = pygame.time.Clock()

    def getImage(self):
        '''
            This method returns the current image of the
        '''
        return self.image

    def update(self):
        dt = self.clock.tick(60)
        if self.y > C.HEIGHT:
            self.killPlayer()
        # this condition checks if you are on the ground
        if (self.y >= self.floor and self.velocity_y > 0):
            self.velocity_y = 0
            self.y = self.floor
            self.isJumping = False
        else:
            self.isJumping = True

        if self.x < 0:
            self.x = C.WIDTH

        if self.x > C.WIDTH:
            self.x = 0

        self.y += self.velocity_y
        self.velocity_y += C.GRAVITY

        self.x += self.velocity_x

        if self.right_direction:
            self.image = f'{self.path}idle1'
        else:
            self.image = f"{self.path}idle1_left"

        if self.velocity_x != 0:
            if self.velocity_x < 0:  # Character moving left
                self.image = f"{self.runningImages[self.runningImageIndex]}_left"
            else:  # Character moving right or not moving
                self.image = f"{self.runningImages[self.runningImageIndex]}"
            self.runningImageIndex += 1
            if self.runningImageIndex >= len(self.runningImages):
                self.runningImageIndex = 0

        if self.isAttacking:
            if self.right_direction:
                self.image = f'{self.path}attack3'
                self.image = f'{self.path}attack6'
            else:
                self.image = f'{self.path}attack3_left'
                self.image = f'{self.path}attack6_left'

        if self.playerIsDead:
            if self.right_direction:
                self.image = f'{self.path}dead'
            else:
                self.image = f'{self.path}dead_left'

    def readKeyboard(self, keyboard):
        if self.playerIsDead:
            return
        accelerating = False
        if keyboard.RIGHT:
            self.right_direction = True
            self.velocity_x += self.accel
            if self.velocity_x > self.maxSpeed:
                self.velocity_x = self.maxSpeed
            elif self.velocity_x < 0:
                self.velocity_x += 2 * self.accel
            accelerating = True
        if keyboard.LEFT:
            self.right_direction = False
            self.velocity_x -= self.accel
            if self.velocity_x < -self.maxSpeed:
                self.velocity_x = -self.maxSpeed  #
            elif self.velocity_x > 0:
                self.velocity_x -= 2 * self.accel
            accelerating = True

        # For attacking!!!
        if keyboard.SPACE and self.attackLength < 10:
            self.isAttacking = True
            self.attackLength += 1
        else:
            self.isAttacking = False
        if not keyboard.SPACE:
            self.attackLength = 0

        if keyboard.UP and self.isJumping == False:
            self.isJumping = True
            self.velocity_y = -self.jumpPower

        if not accelerating:
            if self.velocity_x > 0:
                self.velocity_x -= self.accel
            elif self.velocity_x < 0:
                self.velocity_x += self.accel

    def killPlayer(self):
        self.playerIsDead = True
        self.velocity_x = 0

    def playerDead(self):
        return self.playerIsDead

    def loseProtagonistHealth(self, streight = 1):
        self.health -= streight
        if self.health <= 0:
            self.killPlayer()

