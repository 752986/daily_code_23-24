import math
import pygame
import pygame.gfxdraw

class Vector2:
	x: float
	y: float

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def length(self) -> float:
		return math.sqrt((self.x * self.x) + (self.y * self.y))
	
	def to_pygame_vector(self) -> pygame.Vector2:
		return pygame.Vector2(self.x, self.y)
	
	def __add__(self, other: "Vector2") -> "Vector2":
		return Vector2(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other: "Vector2") -> "Vector2":
		return Vector2(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other: float) -> "Vector2":
		return Vector2(self.x * other, self.y * other)
	
class Matrix2D:
	x1: float
	x2: float
	y1: float
	y2: float

	def __init__(self, x1: float, x2: float, y1: float, y2: float):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2

	@staticmethod
	def from_rotation(angle: float) -> "Matrix2D":
		'''Create a rotation matrix with the specified angle.'''
		c = math.cos(angle)
		s = math.sin(angle)
		return Matrix2D(c, -s, s, c)
	
	def __mul__(self, other: Vector2) -> Vector2:
		return Vector2(
			(self.x1 * other.x) + (self.x2 * other.y), 
			(self.y1 * other.x) + (self.y2 * other.y)
		)


def draw_tree(
	surface: pygame.Surface, 
	bottomleft: Vector2, 
	bottomright: Vector2, 
	n: int,
):
	size = (bottomright - bottomleft).length()

	# always draw its own square
	# compute points of square:
	points = [
		(size * p).rotate(rotation) 
	for p in [
		Vector2(0, 0), 
		Vector2(1, 0), 
		Vector2(1, -1), 
		Vector2(0, -1)
	]]

	if side:
		points = [Vector2(p.x * -1, p.y) for p in points]
	
	points = [p + pos for p in points]

	# draw square:
	color = int((1/(n + 1)) ** 2.2 * 255)
	pygame.gfxdraw.polygon(surface, points, (color, color, color))

	# if max depth hasn't been reached also draw the leaf squares
	if n != 0:
		# draw leaf 1:
		draw_tree(
			surface, 
			size * 0.707106, # size * √2, see trees_math.md
			points[2], # start at top-left corner
			rotation + 45, # rotate 45 degrees ccw
			n - 1, 
			False
		)

		# draw leaf 2:
		draw_tree(
			surface, 
			size * 0.707106, # size * √2, see trees_math.md
			points[3], # start at top-right corner
			rotation - 45, # rotate 45 degrees ccw
			n - 1, 
			True
		)	


def main():
	screen = pygame.display.set_mode((1000, 1000))

	draw_tree(screen, Vector2(500, 500), Vector2(600, 500), 3)

	pygame.display.flip()

	input()

if __name__ == "__main__":
	main()