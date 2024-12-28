from sprite_object import *
from collections import deque
import pygame as pg

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        
        # Scale weapon images
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images]
        )

        # Weapon position
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())

        # Reloading state
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

        # Load crosshair image
        crosshair_path = 'resources/sprites/weapon/crosshair/0.png'
        self.crosshair = pg.image.load(crosshair_path).convert_alpha()
        self.crosshair = pg.transform.smoothscale(self.crosshair, (40, 40))  # Adjust size as needed
        self.crosshair_pos = (HALF_WIDTH - self.crosshair.get_width() // 2,
                              HEIGHT // 2 - self.crosshair.get_height() // 2)

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        # Draw weapon
        self.game.screen.blit(self.images[0], self.weapon_pos)
        
        # Draw crosshair
        self.game.screen.blit(self.crosshair, self.crosshair_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
