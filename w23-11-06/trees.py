import pygame
import pygame.gfxdraw
from pygame.math import Vector2

def draw_tree(
	surface: pygame.Surface, 
	bottomleft: Vector2, 
	bottomright: Vector2, 
	n: int,
):
	# the vector going from a left corner to a right corner
	horizontal = bottomright - bottomleft
	# the vector going from a bottom corner to a top corner
	vertical = Vector2(horizontal.y, -horizontal.x)

	topleft = bottomleft + vertical
	topright = bottomright + vertical

	# the right angle corner of the missing triangle
	vertex = topleft + ((horizontal + vertical) * 0.5)

	# always draw its own square
	color = int((1 - (1 / (n + 1))) ** 2.2 * 255)
	pygame.gfxdraw.filled_polygon(surface, [bottomleft, topleft, topright, bottomright], (color, color, color))

	if n > 5:
		pygame.display.flip()

	# if max depth hasn't been reached also draw the leaf squares
	if n != 0:
		# draw leaf 1:
		draw_tree(
			surface, 
			topleft, 
			vertex, 
			n - 1, 
		)

		# draw leaf 2:
		draw_tree(
			surface, 
			vertex, 
			topright, 
			n - 1, 
		)	


def main():
	screen = pygame.display.set_mode((1000, 1000))

	draw_tree(screen, Vector2(600, 900), Vector2(1000, 900), 20)

	pygame.display.flip()

	input()

if __name__ == "__main__":
	main()
