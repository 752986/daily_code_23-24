import pygame
from pygame.math import Vector2
from pygame.color import Color
import math


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)

# pygame init:
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("")


# definitions:
def elasticCollision(mass1: float, vel1: float, mass2: float, vel2: float) -> tuple[float, float]:
	'''Returns the resulting velocities of body1 and body2, respectively.'''
	newVel1 = ((2 * mass1) / (mass1 + mass2) * vel1) - ((mass1 - mass2) / (mass1 + mass2) * vel2)
	newVel2 = ((mass1 - mass2) / (mass1 + mass2) * vel1) + ((2 * mass2) / (mass1 + mass2) * vel2)

	return newVel1, newVel2

class Square:
	pos: float # x position, pixels
	vel: float # x velocity, pixels per second
	mass: float # kg
	size: float # side length, pixels
	color: Color # display color

	def __init__(self, pos: float, vel: float, mass: float, size: float, color: Color = Color(255, 255, 255)):
		self.pos = pos
		self.vel = vel
		self.mass = mass
		self.size = size
		self.color = color

	def update(self, delta: float, others: "list[Square]"):
		# delta is seconds
		for s in others:
			if self.pos < s.pos + s.size and self.pos + self.size > s.pos:
				newVels = elasticCollision(self.mass, self.vel, s.mass, s.vel)
				self.vel = newVels[0]
				s.vel = newVels[1]
		self.pos += self.vel * delta


	def apply_impulse(self, force: float):
		# force is m/s^2
		self.vel += force / self.mass

	def draw(self, screen: pygame.Surface):
		pygame.draw.rect(screen, self.color, ((self.pos, SCREEN_SIZE.y - self.size), (self.size, self.size)))


def main():
	# game setup:
	clock = pygame.time.Clock()

	s1 = Square(100, 0, 1, 100)
	s2 = Square(500, -50, 100, 150)
	# wall = Square(-100, 0, math.inf, 100)

	squares = [s1, s2]

	# main loop:
	running = True
	while running:
		delta = 0.01 #clock.tick(FRAMERATE) / 1000

		# input:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# draw:
		screen.fill("#000000")

		for s in squares:
			s.update(delta, squares)
			s.draw(screen)

		pygame.display.flip()

if __name__ == "__main__":
	main()
