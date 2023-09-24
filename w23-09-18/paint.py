# TODO: effect stack, comments, ui, more controls, stroke stabilizatoin, possible save to image?

import pygame
import pygame.gfxdraw
from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface

import cProfile

from copy import deepcopy


SCREEN_SIZE = Vector2(1500, 900)
MOVE_THRESHOLD = 4

COLORS = [Color(c) for c in [
	"#2f2e2b",
	"#a13130",
	"#b45c00",
	"#d1a500",
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
	
# def smoothnormal(path: Path, index: int) -> Vector2:
# 	'''Takes a node index and returns its normal vector.'''
# 	if index == 0:
# 		return normal(path, index)
# 	else:
# 		return (normal(path, index).lerp(normal(path, index - 1), 0.5)).normalize()

def sharpness(path: Path, index: int) -> float:
	if index == 0:
		return 0
	return tangent(path, index).dot(tangent(path, index - 1)) - 1 * -0.5
	

class PathEffect:
	def apply(self, path: Path) -> Path:
		return path

class Taper(PathEffect):
	size: float
	def __init__(self, size: float):
		self.size = size

	def apply(self, path: Path) -> Path:
		result = deepcopy(path) # TODO: get rid of this deepcopy

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
	
class Smooth(PathEffect):
	factor: float
	def __init__(self, factor: float):
		self.factor = factor

	def apply(self, path: Path) -> Path:
		# result = deepcopy(path)

		# for i in range(len(result) - 1):
		# 	result[i].pos = result[i].pos.lerp(result[i + 1].pos, self.factor)

		result = [PathNode(path[i].pos.lerp(path[i + 1].pos, self.factor), path[i].radius) for i in range(len(path) - 1)]

		return result
		
# def decimate(path: Path, factor: float) -> Path:
# 	step = int(1 / factor)

# 	result: Path = []
# 	result.append(path[0])
# 	for i in range(0, len(path) - 2, step):
# 		result.append(
# 			PathNode(
# 				path[i + 1].pos.lerp(
# 					path[i + 2].pos, 
# 					factor
# 				), 
# 				path[i].radius
# 			)
# 		)
# 	result.append(path[-1])
# 	return result


class Brush:
	radius: float
	color: Color

	def __init__(self, size: float, color: Color):
		self.radius = size
		self.color = color

	def draw(self, surface: Surface, path: Path):
		pass

class Chisel(Brush):
	def draw(self, surface: Surface, path: Path):
		points_up: list[Vector2] = []
		points_down: list[Vector2] = []

		for i in range(len(path)):
			points_up.append(path[i].pos + (normal(path, i) * path[i].radius * self.radius))
			points_down.append(path[i].pos - (normal(path, i) * path[i].radius * self.radius))

		for i in range(len(path) - 1):
			pygame.gfxdraw.aapolygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
		for i in range(len(path) - 1):
			pygame.gfxdraw.filled_polygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)

class Felt(Brush):
	def draw(self, surface: Surface, path: Path):
		points_up: list[Vector2] = []
		points_down: list[Vector2] = []
 
		for i in range(len(path)):
			points_up.append(path[i].pos + (normal(path, i) * path[i].radius * self.radius))
			points_down.append(path[i].pos - (normal(path, i) * path[i].radius * self.radius))

		# points_up.extend(reversed(points_down))
		
		# pygame.gfxdraw.aapolygon(surface, points_up, self.color)
		for i in range(len(path) - 1):
			pygame.gfxdraw.aapolygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
		pygame.gfxdraw.aacircle(surface, int(path[0].pos.x), int(path[0].pos.y), int(self.radius), self.color)
		pygame.gfxdraw.aacircle(surface, int(path[-1].pos.x), int(path[-1].pos.y), int(self.radius), self.color)

		for i in range(len(path) - 1):
			pygame.gfxdraw.filled_polygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
		pygame.gfxdraw.filled_circle(surface, int(path[0].pos.x), int(path[0].pos.y), int(self.radius), self.color)
		pygame.gfxdraw.filled_circle(surface, int(path[-1].pos.x), int(path[-1].pos.y), int(self.radius), self.color)


def main():
	screen = pygame.display.set_mode(SCREEN_SIZE)

	current_color = 0
	brush = Chisel(5, COLORS[0])

	taper = Taper(20)
	smooth = Smooth(0.5)

	path: Path = []

	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

	temp_layer = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
	canvas = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
	canvas.fill((0, 0, 0, 0))
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
					temp_layer.fill((0, 0, 0, 0))
					# temp_path = smooth(decimate(path, 0.1), 0.8)
					# brush.draw(temp_layer, path)
					# canvas.blit(temp_layer, (0, 0))
					brush.draw(temp_layer, taper.apply(path))

					updated = True
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				canvas.blit(temp_layer, (0, 0))
				path = []
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				current_color = (current_color + 1) % len(COLORS)
				brush.color = COLORS[current_color]


		if updated:
			screen.fill("#c8c6c2")
			screen.blit(canvas, (0, 0))
			screen.blit(temp_layer, (0, 0))

			pygame.display.flip()
			updated = False

cProfile.run("main()")
