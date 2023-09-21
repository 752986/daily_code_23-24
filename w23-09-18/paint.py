import pygame
from pygame.color import Color
from pygame.math import Vector2
from pygame.surface import Surface


class Segment:
	start: Vector2
	end: Vector2

	def __init__(self, start: Vector2, end: Vector2):
		self.start = start
		self.end = end

	def length(self) -> float:
		return (self.start - self.end).length()

class Brush:
	size: float
	color: Color

	def draw(self, surface: Surface, segment: Segment):
		pass

	def drawControls(self, surface: Surface)