# TODO: comments, ui, more controls, stroke smoothing, possible save to image?

import pygame
import pygame.gfxdraw
from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface

from copy import deepcopy


SCREEN_SIZE = Vector2(1500, 900)
MOVE_THRESHOLD = 4

COLORS = [Color(c) for c in [
	"#2f2e2b",
	"#a13130",
	"#b45c00",
	"#a17f00",
	"#456b00",
	"#007a7f",
	"#285aaf",
	"#6e40aa",
	"#a62ba0"
]]


def rot90(v: Vector2) -> Vector2:
	return Vector2(v.y, -v.x)


class PathNode:
	pos: Vector2
	radius: float

	def __init__(self, pos: Vector2, radius: float):
		self.pos = pos
		self.radius = radius


Path = list[PathNode]
def length(path: Path, index: int) -> float:
	'''Takes a segment index and returns its length.'''
	if index + 1 >= len(path):
		raise IndexError
	
	return (path[index + 1].pos - path[index].pos).length()

def tangent(path: Path, index: int) -> Vector2:
	'''Takes a node index and returns its (non-normalized) tangent vector.'''
	if index + 1 == len(path):
		return path[index].pos - path[index - 1].pos
	else:
		return path[index + 1].pos - path[index].pos

def normal(path: Path, index: int) -> Vector2:
	'''Takes a node index and returns its normal vector.'''
	t = tangent(path, index)
	if t.length_squared() == 0:
		return Vector2(0, 0)
	else:
		return rot90(tangent(path, index)).normalize()


class PathEffect:
	def apply(self, path: Path) -> Path:
		return path

class Taper(PathEffect):
	size: float
	def __init__(self, size: float):
		self.size = size

	def apply(self, path: Path) -> Path:
		result = deepcopy(path)

		n_segments = 0
		total_length = 0
		while total_length < self.size and n_segments < len(result) - 1:
			total_length += length(result, n_segments)
			n_segments += 1
		for i in range(n_segments):
			result[i].radius *= i / n_segments

		n_segments = 0
		total_length = 0
		while total_length < self.size and n_segments < len(result):
			total_length += length(result, len(result) - n_segments - 2)
			n_segments += 1
		for i in range(n_segments):
			result[-i].radius *= i / n_segments

		return result
		

class Brush:
	radius: float
	color: Color

	def __init__(self, size: float, color: Color):
		self.radius = size
		self.color = color

	def draw(self, surface: Surface, path: Path):
		pass

class Marker(Brush):
	def draw(self, surface: Surface, path: Path):
		# pygame.draw.circle(surface, self.color, path[0].pos, self.radius)
		# pygame.draw.circle(surface, self.color, path[-1].pos, self.radius)
		
		points_up: list[Vector2] = []
		points_down: list[Vector2] = []

		for i in range(len(path)):
			points_up.append(path[i].pos + (normal(path, i) * path[i].radius * self.radius))
			points_down.append(path[i].pos - (normal(path, i) * path[i].radius * self.radius))

		points_up.extend(reversed(points_down))
		
		for i in range(len(path) - 1):
			pygame.gfxdraw.aapolygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
			pygame.gfxdraw.filled_polygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)


screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)

current_color = 0
brush = Marker(5, COLORS[0])

taper = Taper(20)

path: Path = []

pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

temp_layer = pygame.Surface(SCREEN_SIZE)
canvas = pygame.Surface(SCREEN_SIZE)
canvas.fill((255, 255, 255))
screen.fill("#c8c6c2")
pygame.display.flip()

updated = False

accumulated_motion = Vector2(0, 0)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
			accumulated_motion += Vector2(event.rel)
			if accumulated_motion.length() > MOVE_THRESHOLD:
				path.append(PathNode(Vector2(event.pos), 1.0))
				accumulated_motion = Vector2(0, 0)

			if len(path) > 1:
				temp_layer.fill((255, 255, 255))
				# temp_path = smooth(decimate(path, 0.1), 0.8)
				# brush.draw(temp_layer, path)
				# canvas.blit(temp_layer, (0, 0))
				brush.draw(temp_layer, taper.apply(path))

				updated = True
		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			canvas.blit(temp_layer, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
			path = []
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			current_color = (current_color + 1) % len(COLORS)
			brush.color = COLORS[current_color]


	if updated:
		screen.fill("#c8c6c2")
		screen.blit(canvas, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
		screen.blit(temp_layer, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

		pygame.display.flip()
		updated = False
