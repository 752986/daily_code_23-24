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

class Matrix3_3:
	# dear lord I should really just be using numpy for all of this
	ax: float
	ay: float
	az: float
	bx: float
	by: float
	bz: float
	cx: float
	cy: float
	cz: float

	def __init__(self, ax: float, ay: float, az: float, bx: float, by: float, bz: float, cx: float, cy: float, cz: float):
		self.ax = ax
		self.ay = ay
		self.az = az
		self.bx = bx
		self.by = by
		self.bz = bz
		self.cx = cx
		self.cy = cy
		self.cz = cz

	def scaled(self, scalar: float) -> "Matrix3_3":
		return Matrix3_3(
			self.ax * scalar,
			self.ay * scalar,
			self.az * scalar,
			self.bx * scalar,
			self.by * scalar,
			self.bz * scalar,
			self.cx * scalar,
			self.cy * scalar,
			self.cz * scalar
		)
	
	def mul(self, v: Vector3) -> Vector3:
		return Vector3(
			self.ax * v.x + self.bx * v.y + self.cx * v.z,
			self.ay * v.x + self.by * v.y + self.cy * v.z,
			self.az * v.x + self.bz * v.y + self.cz * v.z,
		)

	def inverse(self) -> "Matrix3_3":
		# don't ask me how any of this math works, I found it online

		determinant = 1 / (
			self.ax * self.by * self.cz - 
			self.ax * self.bz * self.cy - 
			self.ay * self.bx * self.cz +
			self.az * self.bx * self.cy +
			self.ay * self.bz * self.cx -
			self.az * self.by * self.cx
		)

		return Matrix3_3(
			self.by * self.cz - self.bz * self.cy,
			self.az * self.cy - self.ay * self.cz,
			self.ay * self.bz - self.az * self.by,
			self.bz * self.cx - self.bx * self.cz,
			self.ax * self.cz - self.az * self.cx,
			self.az * self.bx - self.ax * self.bz,
			self.bx * self.cy - self.by * self.cx,
			self.ay * self.cx - self.ax * self.cy,
			self.ax * self.by - self.ay * self.bx
		).scaled(determinant)

class Camera:
	pos: Vector3
	facing: Vector3

	def __init__(self, pos: Vector3, facing: Vector3 = Vector3(0, 0, 1)):
		self.pos = pos
		self.facing = facing.normalize()

	def set_angle(self, angle: Vector3):
		self.facing = Vector3(0, 0, 1).rotate_rad(1, angle)

	def rotate(self, angle: Vector3):
		self.facing.rotate_rad_ip(1, angle)

	def rotate_y(self, angle: float):
		self.facing.rotate_rad_ip(angle, Vector3(0, -1, 0))

	def set_facing(self, facing: Vector3):
		self.facing = facing.normalize()

	def project(self, v: Vector3) -> Vector3:
		'''Project a Vector3 into the camera's space'''
		forward = self.facing
		right = forward.cross(Vector3(0, -1, 0)).normalize()
		up = forward.cross(right)

		# print(f"f{forward} r{right} u{up}")

		matrix = Matrix3_3(right.x, right.y, right.z, up.x, up.y, up.z, forward.x, forward.y, forward.z)
		
		return matrix.inverse().mul(v - self.pos)

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
			# elif event.type == pygame.KEYDOWN:
			# 	if event.key == pygame.K_LEFT:
			# 		camera.rotate(Vector3(0, math.radians(45), 0))
			# 	if event.key == pygame.K_RIGHT:
			# 		camera.rotate(Vector3(0, -math.radians(45), 0))
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					camera.rotate_y(math.radians(10))
				if event.key == pygame.K_RIGHT:
					camera.rotate_y(-math.radians(10))

			keys = pygame.key.get_pressed() 
			if keys[pygame.K_w]:
				camera.pos.z += 20
			if keys[pygame.K_s]:
				camera.pos.z -= 20
			if keys[pygame.K_a]:
				camera.pos.x -= 200
			if keys[pygame.K_d]:
				camera.pos.x += 200
			if keys[pygame.K_q]:
				camera.pos.y -= 200
			if keys[pygame.K_e]:
				camera.pos.y += 200

		# rel = Vector2(pygame.mouse.get_rel())
		# if rel != Vector2(0, 0):
		# 	camera.rotate(Vector3(rel.y, rel.x, 0) * 0.001)

		# draw:
		screen.fill("#000000")

		for p in particles:
			p.update(delta, screen, camera)

		pygame.display.flip()

if __name__ == "__main__":
	main()
