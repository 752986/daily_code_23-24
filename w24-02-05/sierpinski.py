# based on this image: https://commons.wikimedia.org/wiki/File:Arrowhead_curve_1_through_6.png

import pygame
from pygame.math import Vector2

def trapezoid(p0: Vector2, p3: Vector2) -> tuple[Vector2, Vector2, Vector2, Vector2]:
	'''Calculates 4 points forming a trapezoid from the 2 points forming the base.'''
	base = p3 - p0 # vector spanning the base of the trapezoid
	p1 = p0 + Vector2(
		(0.25 * base.x) + (0.4330125 * base.y),
		(-0.4330125 * base.x) + (0.25 * base.y)
	) # rotate base 60deg ccw and scale by 0.5 (via matrix math)
	p2 = p1 + (base * 0.5) # base * 0.5 == top section

	return (p0, p1, p2, p3)

def triangle(start: Vector2, end: Vector2, depth: int, screen: pygame.Surface):
	if depth == 0:
		pygame.draw.line(screen, (255, 255, 255), start, end)
		return
	
	p0, p1, p2, p3 = trapezoid(start, end)

	triangle(p1, p0, depth - 1, screen)
	triangle(p1, p2, depth - 1, screen)
	triangle(p3, p2, depth - 1, screen)

screen = pygame.display.set_mode((1200, 800))

triangle(Vector2(200, 725), Vector2(1000, 725), 7, screen)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()
