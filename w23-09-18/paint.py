# TODO: effect stack, comments, ui, more controls, stroke stabilizatoin, possible save to image?

import pygame
import pygame.gfxdraw
from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface

import cProfile


pygame.init()

SCREEN_SIZE = Vector2(1500, 900)
MOVE_THRESHOLD = 4
FRAMERATE = 120
_FRAME_TIME = 1000 // FRAMERATE

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
	return path[index + 1].pos - path[index].pos

def normal(path: Path, index: int) -> Vector2:
	'''Takes a node index and returns its normal vector.'''
	t = tangent(path, index)
	if t == Vector2(0, 0):
		return Vector2(0, 0)
	return rot90(t).normalize()
	
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
	def apply(self, path: Path):
		pass

class Taper(PathEffect):
	size: float
	def __init__(self, size: float):
		self.size = size

	def apply(self, path: Path):
		n_start = 0
		total_length = 0
		while total_length < self.size and	n_start < len(path) // 2:
			total_length += length(path, n_start)
			n_start += 1

		n_end = 0
		total_length = 0
		while total_length < self.size and n_end < len(path) // 2:
			total_length += length(path, len(path) - n_end - 2)
			n_end += 1

		for i in range(n_start):
			path[i].radius *= (i /	n_start)
		for i in range(n_end):
		 	path[-i].radius *= (i /	n_end)
	
class Smooth(PathEffect):
	factor: float
	def __init__(self, factor: float):
		self.factor = factor

	def apply(self, path: Path):
		# result = deepcopy(path)

		for i in range(1, len(path) - 1):
			path[i].pos = path[i].pos.lerp(path[i + 1].pos, self.factor)

		# result = [PathNode(path[i].pos.lerp(path[i + 1].pos, self.factor), path[i].radius) for i in range(len(path) - 1)]

		# return result
		
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
		self.radius = size / 2
		self.color = color

	def draw(self, surface: Surface, path: Path):
		pass

class Chisel(Brush):
	def draw(self, surface: Surface, path: Path):
		points_up: list[Vector2] = []
		points_down: list[Vector2] = []

		for i in range(len(path)):
			offset = (normal(path, i) * path[i].radius * self.radius)
			points_up.append(path[i].pos + offset)
			points_down.append(path[i].pos - offset)

		for i in range(len(path) - 1):
			pygame.gfxdraw.aapolygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
		for i in range(len(path) - 1):
			pygame.gfxdraw.filled_polygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)

class Felt(Brush):
	def draw(self, surface: Surface, path: Path):
		points_up: list[Vector2] = []
		points_down: list[Vector2] = []
 
		for i in range(len(path)):
			offset = (normal(path, i) * path[i].radius * self.radius)
			points_up.append(path[i].pos + offset)
			points_down.append(path[i].pos - offset)

		for i in range(len(path) - 1):
			pygame.gfxdraw.aapolygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
		pygame.gfxdraw.aacircle(surface, int(path[0].pos.x), int(path[0].pos.y), int(self.radius * path[0].radius), self.color)
		pygame.gfxdraw.aacircle(surface, int(path[-1].pos.x), int(path[-1].pos.y), int(self.radius * path[-1].radius), self.color)

		for i in range(len(path) - 1):
			pygame.gfxdraw.filled_polygon(surface, [points_up[i], points_up[i + 1], points_down[i + 1], points_down[i]], self.color)
		pygame.gfxdraw.filled_circle(surface, int(path[0].pos.x), int(path[0].pos.y), int(self.radius * path[0].radius), self.color)
		pygame.gfxdraw.filled_circle(surface, int(path[-1].pos.x), int(path[-1].pos.y), int(self.radius * path[-1].radius), self.color)

def main():
	screen = pygame.display.set_mode(SCREEN_SIZE)
	last_draw = 0

	current_color = 0
	brush = Chisel(5, COLORS[current_color])

	taper = Taper(20)
	smooth = Smooth(0.5)
	effects: list[PathEffect] = [
		smooth,
		# taper
	]

	path: Path = []
	temp_path: Path = []

	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

	temp_layer = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
	canvas = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
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
				# only add points if the mouse has moved enough
				# this is for performance, but it also gives better angles
				accumulated_motion += Vector2(event.rel)
				if accumulated_motion.length() > MOVE_THRESHOLD:
					path.append(PathNode(Vector2(event.pos), 1.0))
					accumulated_motion = Vector2(0, 0)

				# a path with only 1 point can't be drawn
				if len(path) > 1:
					# apply effects
					temp_path = [PathNode(node.pos, node.radius) for node in path]
					for effect in effects:
						effect.apply(temp_path)
					
					# draw the stroke
					temp_layer.fill((0, 0, 0, 0))
					brush.draw(temp_layer, temp_path)

					updated = True
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				# finalize stroke
				canvas.blit(temp_layer, (0, 0))
				path = []
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					current_color = (current_color + 1) % len(COLORS)
					brush.color = COLORS[current_color]

		# reduced draw rate for smoother strokes
		if updated and pygame.time.get_ticks() - last_draw >= _FRAME_TIME:
			screen.fill("#c8c6c2")
			screen.blit(canvas, (0, 0))
			screen.blit(temp_layer, (0, 0))

			pygame.display.flip()

			last_draw = pygame.time.get_ticks()
			updated = False

# cProfile.run("main()", sort="time")
main()
