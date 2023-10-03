import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
import random


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)
CENTER = SCREEN_SIZE / 2


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

	def __init__(self, pos: Vector2, fire_rate: float, turn_rate: float, cost: int):
		super().__init__(pos)
		self.fire_rate = 1 / fire_rate
		self.turn_rate = turn_rate
		self.cost = cost
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
	def __init__(self, pos: Vector2):
		super().__init__(pos, 0.5, 30, 0)

	def draw(self, surface: Surface):
		pygame.draw.line(surface, "#884444", self.pos, self.pos + Vector2(10, 0).rotate(self.direction))

	def fire(self, gameobjects: list[GameObject]):
		gameobjects.append(BasicProjectile(self.pos.copy(), 50, Vector2(10, 0).rotate(self.direction)))

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		super().update(delta, gameobjects, surface)

		self.direction += self.turn_rate * delta


class Enemy(GameObject):
	health: int
	vel: Vector2
	size: float

	def __init__(self, pos: Vector2, speed: float, size: float, health: int):
		super().__init__(pos)
		self.vel = (CENTER - self.pos).normalize() * speed
		self.radius = size / 2
		self.health = health

	def draw(self, surface: Surface):
		pass

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		self.pos += self.vel * delta

		self.draw(surface)

		if self.health <= 0:
			gameobjects.remove(self)

class Slime(Enemy):
	def __init__(self, pos: Vector2):
		super().__init__(pos, 20, 10, 5)

	def draw(self, surface: Surface):
		pygame.draw.rect(surface, "#88ff44", (self.pos - Vector2(5, 5), (10, 10)))

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		super().update(delta, gameobjects, surface)


class Projectile(GameObject):
	damage: int
	vel: Vector2
	max_hits: int
	hit_objs: list[Enemy]

	def __init__(self, pos: Vector2, speed: float, direction: Vector2, damage: int, max_hits: int):
		super().__init__(pos)
		self.vel = direction.normalize() * speed
		self.damage = damage
		self.max_hits = max_hits
		self.hit_objs = []

	def draw(self, surface: Surface):
		pass

	def checkCollision(self, gameobjects: list[GameObject]): # TODO: enemies check collisions
		for obj in gameobjects:
			if (
				isinstance(obj, Enemy) 
				and obj not in self.hit_objs 
				and obj.pos.distance_to(self.pos) <= obj.radius
			):
				obj.health -= self.damage
				self.hit_objs.append(obj)
				if len(self.hit_objs) >= self.max_hits:
					gameobjects.remove(self)
					break

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		self.pos += self.vel * delta
		self.checkCollision(gameobjects)
		if not Rect((0, 0), SCREEN_SIZE).collidepoint(self.pos):
			gameobjects.remove(self)
		self.draw(surface)

class BasicProjectile(Projectile):
	def __init__(self, pos: Vector2, speed: float, direction: Vector2):
		super().__init__(pos, speed, direction, 5, 1)

	def draw(self, surface: Surface):
		pygame.draw.circle(surface, "#88aaff", self.pos, 1)


class Gamestate:
	player_damage = 5
	turret_level = 1
	turret_speed = 1.0
	enemy_level = 1

class Manager(GameObject):
	def __init__(self, pos: Vector2, state: Gamestate):
		super().__init__(pos)
		self.state = state

class EnemySpawner(Manager):
	pass

class PlayerDamage(Manager):
	def checkCollision(self, gameobjects: list[GameObject]):
		for obj in gameobjects:
			if (
				isinstance(obj, Enemy)
				and pygame.mouse.get_pressed()[0]
				and obj.pos.distance_to(pygame.mouse.get_pos()) <= obj.radius
			):
				obj.health -= self.state.player_damage

	def update(self, delta: float, gameobjects: list[GameObject], surface: Surface):
		self.checkCollision(gameobjects)
	

def main():
	# game setup:
	clock = pygame.time.Clock()

	gamestate = Gamestate()

	gameobjects: list[GameObject] = []
	gameobjects.append(PlayerDamage(Vector2(0, 0), gamestate))
	gameobjects.append(BasicTurret(SCREEN_SIZE / 2))
	for _ in range(10): #TODO: replace with EnemySpawner
		gameobjects.append(Slime(Vector2(random.random() * SCREEN_SIZE.x, random.random() * SCREEN_SIZE.y)))

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