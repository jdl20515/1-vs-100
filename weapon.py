from sprite_object import *
from collections import deque
import pygame as pg

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        
        # Debug: Check if self.images exists in the parent class
        if not hasattr(self, 'images'):
            raise AttributeError("Parent class 'AnimatedSprite' did not initialize 'self.images'.")
        if not self.images:
            raise ValueError("No images loaded in 'AnimatedSprite'. Check the file paths and loading logic.")

        # Debug: Log original image dimensions
        try:
            print(f"Original image dimensions: {self.image.get_width()}x{self.image.get_height()}")
        except AttributeError:
            raise AttributeError("Failed to load the initial image in 'AnimatedSprite'. Check the 'path' parameter.")

        # Scale images
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images]
        )

        # Debug: Check if images were successfully scaled
        if not self.images:
            raise ValueError("Image scaling failed. Ensure valid images are loaded before scaling.")

        print(f"Loaded and scaled {len(self.images)} images for the weapon.")

        # Weapon position
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())

        # Debug: Log weapon position
        # print(f"Weapon position: {self.weapon_pos}")

        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                # Debug: Log frame rotation
                print(f"Animating shot: frame {self.frame_counter}/{self.num_images}")
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                    print("Reload animation completed.")

    def draw(self):
        # Debug: Check if image and weapon position are valid
        try:
            self.game.screen.blit(self.images[0], self.weapon_pos)
        except Exception as e:
            raise RuntimeError(f"Failed to draw weapon image: {e}")

    def update(self):
        self.check_animation_time()
        self.animate_shot()
