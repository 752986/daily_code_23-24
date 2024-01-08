import pygame
import pygame.gfxdraw
from pygame.math import Vector2
import math

def rot90(v: Vector2) -> Vector2:
	return Vector2(v.y, -v.x)

def getPoints(level: int, p0: Vector2, p4: Vector2, isTop: bool = True) -> list[Vector2]:
	'''Returns all points except for the start point, to be appended to a larger polygon.'''
	if level == 0:
		return [p4]
	
	line = p4 - p0
	
	p1 = (line * (1/3)) + p0
	p3 = (line * (2/3)) + p0

	p2 = (line / 2 + p0) + (rot90(line * (math.sqrt(3) / 6)))

	result = [p0] if isTop else []

	result.extend(getPoints(level-1, p0, p1, False))
	result.extend(getPoints(level-1, p1, p2, False))
	result.extend(getPoints(level-1, p2, p3, False))
	result.extend(getPoints(level-1, p3, p4, False))

	return result


screen = pygame.display.set_mode((1000, 1000))

points = getPoints(10, Vector2(0, 0), Vector2(1000, 1000))

pygame.gfxdraw.aapolygon(screen, points, (255, 255, 255))

pygame.display.flip()

input()