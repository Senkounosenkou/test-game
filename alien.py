import pygame
from setting import*
import random

# エイリアンクラス
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, alien_bullets):
        super().__init__()
        self.image = pygame.image.load(ALIEN_IMG_PATH).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.all_sprites = all_sprites
        self.alien_bullets = alien_bullets

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.speed = -self.speed
            self.rect.y += 40
        if random.randint(1, 300) == 1:  # 1/300の確率で弾を発射
            bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
            self.all_sprites.add(bullet)
            self.alien_bullets.add(bullet)


# エイリアンの弾クラス
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
