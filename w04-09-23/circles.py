import math

import colorsys

import pygame
from pygame.math import Vector2


def hsl_to_pygame_rgb(h: float, s: float, l: float, a: float = 1.0) -> tuple[int, int, int]:
	color = colorsys.hls_to_rgb(h / math.tau, l, s)
	result = tuple(map(lambda x: int(x * 255), color))
	return result


def get_points_in_circle(n_points: int, radius: float = 1) -> list[Vector2]:
	return [
		Vector2(
			math.cos(t / n_points * math.tau) * radius, 
			math.sin(t / n_points * math.tau) * radius
		) 
		for t in range(n_points)
	]


def draw_iteration(
		surface: pygame.Surface, 
		factor: int, 
		n_points: int, 
		radius: float = 1, 
		start_hue: float = 0, 
		hue_change: float = 0.1, 
		time: float = 1, 
		color: tuple[int, int, int] = (200, 240, 255)
	):
	middle = Vector2(surface.get_rect().center)
	points = [p + middle for p in get_points_in_circle(n_points, radius)]
	# for point in points:
		# pygame.draw.circle(surface, (255,255,255), point, 2)
		# pygame.draw.line(surface, (255,255,255), ponts+middle, ponts+middle)

	hue = start_hue
	for i in range(len(points)):
		start = points[i]
		end = points[(i * factor) % len(points)]

		hue += hue_change / n_points
		
		pygame.draw.aaline(surface, hsl_to_pygame_rgb(hue, 0.7, 0.7, 0.7), start, end)
		pygame.display.flip()
		pygame.time.delay(int(time / n_points * 1000))


def main():
	screen = pygame.display.set_mode((800, 800))

	HUE_CHANGE = 2
	N_POINTS = 480

	running = True
	i = 0
	hue = 0
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


		screen.fill((0, 0, 0))
		if i % N_POINTS != 1: # skip boring n=1 iteration
			print(i)
			draw_iteration(screen, i, N_POINTS, 350, hue, HUE_CHANGE, 3.0)
			hue += HUE_CHANGE


		pygame.display.flip()
		i += 1
		pygame.time.delay(500)


if __name__ == "__main__":
	main()