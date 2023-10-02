import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
import random


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)


# pygame init:
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("spin game")


# definitions:
class GameObject:
	pos: Vector2

	def __init__(self, pos: Vector2):
		self.pos = pos

	def update(self, delta: float, gameobjects: list["GameObject"], surface: Surface):
		pass


class Turret(GameObject):
	fire_rate: float # shots/sec
	turn_rate: float # deg/sec
	cost: int
	direction: float
	timer: float

	def __init__(self, pos: Vector2, fire_rate: float, turn_rate: float):
		super().__init__(pos)
		self.fire_rate = 1 / fire_rate
		self.turn_rate = turn_rate
		self.direction = 0
		self.timer = random.random() * self.fire_rate

	def draw(self, surface: Surface):
		pass

	def fire(self, gameobjects: list[GameObject]):
		pass

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		super().update(delta, gameobjects, surface)

		self.timer -= delta
		if self.timer <= 0:
			self.fire(gameobjects)
			self.timer = random.random() * self.fire_rate * 2

		self.draw(surface)

class BasicTurret(Turret):
	cost = 0

	def __init__(self, pos: Vector2):
		super().__init__(pos, 2, 90)

	def draw(self, surface: Surface):
		pygame.draw.line(surface, "#884444", self.pos, self.pos + Vector2(10, 0).rotate(self.direction))

	def fire(self, gameobjects: list[GameObject]):
		gameobjects.append(BasicProjectile(self.pos.copy(), 20, Vector2(10, 0).rotate(self.direction)))

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		super().update(delta, gameobjects, surface)

		self.direction += self.turn_rate * delta



class Enemy(GameObject):
	health: int


class Projectile(GameObject):
	damage: int
	radius: float
	vel: Vector2
	max_hits: int
	hit_objs: list[Enemy]

	def __init__(self, pos: Vector2, speed: float, direction: Vector2):
		super().__init__(pos)
		self.vel = direction.normalize() * speed
		self.hit_objs = []

	def draw(self, surface: Surface):
		pass

	def checkCollision(self, gameobjects: list[GameObject]):
		for obj in gameobjects:
			if (
				isinstance(obj, Enemy) 
				and obj not in self.hit_objs 
				and obj.pos.distance_to(self.pos) <= self.radius
			):
				obj.health -= self.damage
				self.hit_objs.append(obj)
				if len(self.hit_objs) >= self.max_hits:
					gameobjects.remove(self)
					break


	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		self.pos += self.vel * delta
		self.checkCollision(gameobjects)
		self.draw(surface)

class BasicProjectile(Projectile):
	def __init__(self, pos: Vector2, speed: float, direction: Vector2):
		super().__init__(pos, speed, direction)
		self.damage = 5
		self.radius = 10
		self.max_hits = 1

	def draw(self, surface: Surface):
		pygame.draw.circle(surface, "#88aaff", self.pos, self.radius)


def main():
	# game setup:
	clock = pygame.time.Clock()

	gameobjects: list[GameObject] = []
	gameobjects.append(BasicTurret(SCREEN_SIZE / 2))

	# main loop:
	running = True
	while running:
		delta = clock.tick(FRAMERATE) / 1000

		# input:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


		# update:
		screen.fill("#000000")

		for obj in gameobjects:
			obj.update(delta, gameobjects, screen)

		pygame.display.flip()

if __name__ == "__main__":
	main()