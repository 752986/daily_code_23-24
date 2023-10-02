import math

import pygame
from pygame.math import Vector2

clearthething = False
def get_points_in_circle(n_points: int, radius: float = 1) -> list[Vector2]:
	return [
		Vector2(
			math.cos(t / n_points * math.tau) * radius, 
			math.sin(t / n_points * math.tau) * radius
		) 
		for t in range(n_points)
	]


def draw_iteration(surface: pygame.Surface, factor: int, pointus: int, radius: float = 1, colordif: int = 255):
	middle = Vector2(surface.get_rect().center)
	points = [p + middle for p in get_points_in_circle(pointus, radius)]
	for ponts in points:
		pygame.draw.circle(surface, (255,255,255), ponts, 2)
		# pygame.draw.line(surface, (255,255,255), ponts+middle, ponts+middle)
	for i in range(len(points)):
		start = points[i]
		end = points[(i * factor) % len(points)]
		dist = math.sqrt(((end[0]-start[0])**2)+((end[1]-start[1])**2))
		stretchcolor = 255 - int((dist/(radius*2))*255)
		if stretchcolor > 255:
			stretchcolor = 255
		colordif *= 2
		red = ((255-colordif)+255) % 255 - stretchcolor
		blue = ((0+colordif)+255) % 255 - stretchcolor
		pygame.draw.aaline(surface, (red, 40, blue), start, end)
		pygame.display.flip()
		pygame.time.delay(30)


def main():
	screen = pygame.display.set_mode((800, 800))

	running = True
	i = 0
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		print(i)

		if clearthething:
			screen.fill((0, 0, 0))
		draw_iteration(screen, i, 120, 350, i*2 if i < 256 else 255)

		pygame.display.flip()
		i += 1
		pygame.time.delay(500)


if __name__ == "__main__":
	main()