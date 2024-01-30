import pygame
from pygame.math import Vector2, Vector3
from pygame.rect import Rect
from pygame.color import Color
import math
import random


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)

MAX_DIST = 100
SPEED = 20
SPREAD = 10000
TAIL = 3
FOV = 3
N_PARTICLES = 3000



# pygame init:
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("")


# definitions:
def perspective_project(v: Vector3, fov: float) -> Vector2:
	'''Project a Vector3 into screen space with perspective, assuming camera is looking along +Z'''
	if v.z <= 0:
		return Vector2(0, 0)
	return (v.xy / v.z * fov) + (SCREEN_SIZE / 2)

class Camera:
	pos: Vector3
	facing: Vector3

	def __init__(self, pos: Vector3, facing: Vector3 = Vector3(0, 0, 1)):
		self.pos = pos
		self.facing = facing.normalize()

	def set_angle(self, angle: Vector3):
		self.facing = Vector3(0, 0, 1).rotate_rad(1, angle)

	def rotate(self, angle: Vector3):
		self.facing.rotate_ip_rad(1, angle)

	def set_facing(self, facing: Vector3):
		self.facing = facing.normalize()

	def project(self, v: Vector3) -> Vector3:
		'''Project a Vector3 into the camera's space'''
		#TODO!
		# return v.project(self.facing)
		return v

class Particle:
	pos: Vector3
	vel: Vector3
	color: Color

	def __init__(self, pos: Vector3, vel: Vector3, color: Color):
		self.pos = pos
		self.vel = vel
		self.color = color

	def update(self, delta: float, surface: pygame.Surface, camera: Camera):
		self.pos += self.vel * delta
		if self.pos.z < 0:
			self.pos.z = MAX_DIST

		view_pos = perspective_project(camera.project(self.pos), FOV)
		tail_view_pos = perspective_project(camera.project(self.pos + Vector3(0, 0, TAIL)), FOV)

		pygame.draw.line(surface, self.color, view_pos, tail_view_pos)


def main():
	# game setup:
	clock = pygame.time.Clock()

	camera = Camera(Vector3(0, 0, 0))

	particles: list[Particle] = []
	for _ in range(N_PARTICLES):
		# generate random point within circle
		point = Vector2((random.random() - 0.5) * SPREAD * 2, (random.random() - 0.5) * SPREAD * 2)
		while point.length() > SPREAD:
			point = Vector2((random.random() - 0.5) * SPREAD * 2, (random.random() - 0.5) * SPREAD * 2)

		particles.append(
			Particle(
				Vector3(point.x, point.y, random.random() * MAX_DIST), 
				Vector3(0, 0, -SPEED),
				Color((255, 255, 255))
			)
		)

	# main loop:
	running = True
	while running:
		delta = clock.tick(FRAMERATE) / 1000

		# input:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# draw:
		screen.fill("#000000")

		for p in particles:
			p.update(delta, screen, camera)

		pygame.display.flip()

if __name__ == "__main__":
	main()
