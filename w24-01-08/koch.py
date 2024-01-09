import pygame
import pygame.gfxdraw
from pygame.math import Vector2
import math
import random

def rot90(v: Vector2) -> Vector2:
	return Vector2(v.y, -v.x)

def getPoints(level: int, p0: Vector2, p4: Vector2, *, isFirst: bool = True) -> list[Vector2]:
	'''Returns all points except for the start point, to be appended to a larger polygon.'''
	if level == 0:
		return [p4]
	
	line = p4 - p0
	
	p1 = (line / 3) + p0
	p3 = (line * (2/3)) + p0

	p2 = (line / 2 + p0) + (rot90(line * 0.28867513459481287)) # rot90(line / 3 * (sqrt(3) / 2))

	result = [p0] if isFirst else []

	result.extend(getPoints(level-1, p0, p1, isFirst=False))
	result.extend(getPoints(level-1, p1, p2, isFirst=False))
	result.extend(getPoints(level-1, p2, p3, isFirst=False))
	result.extend(getPoints(level-1, p3, p4, isFirst=False))

	return result


def getSnowflakePoints(level: int, pos: Vector2, radius: float, angle: float = 0):
	p0 = pos + Vector2(0, radius).rotate(angle)
	p1 = pos + Vector2(0, radius).rotate(angle + 120)
	p2 = pos + Vector2(0, radius).rotate(angle + 240)

	result = getPoints(level, p0, p1, isFirst=False) # isFirst=False because p0 is included in the last side
	result.extend(getPoints(level, p1, p2, isFirst=False))
	result.extend(getPoints(level, p2, p0, isFirst=False))

	return result


class Snowflake:
	def __init__(self, pos: Vector2):
		self.pos = pos
		self.vel = Vector2(random.random() * 40 - 20, random.random() * 100)
		self.size = random.random() * 50
		self.angle = random.random() * 360
		self.amoment = random.random() * 20 - 10

	def move(self, delta: float):
		self.pos += self.vel*delta
		self.angle += self.amoment*delta

	def draw(self, screen: pygame.Surface):
		pen = getSnowflakePoints(4, self.pos, self.size, self.angle)
		pygame.gfxdraw.aapolygon(screen, pen, (255,255,255))
		pygame.gfxdraw.filled_polygon(screen, pen, (255,255,255))


screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

snowflakes = [Snowflake(Vector2(random.random() * 1000, 0)) for _ in range(100)]

while True:
	delta = clock.tick(60) / 1000

	for flake in snowflakes:
		flake.move(delta)

	screen.fill((0, 0, 0))
	for flake in snowflakes:
		flake.draw(screen)

	pygame.display.flip()