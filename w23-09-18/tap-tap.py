import pygame
from pygame.math import Vector2
from pygame.rect import Rect

GRAVITY = 500
BALL_RADIUS = 20

score = 0

class Ball:
	def __init__(self, pos: Vector2):
		self.pos = pos
		self.vel = Vector2(0, 0)
		self.touchGround = False
		self.hasScored = False

	def update(self, delta: float,  backboard: Rect, basket: Rect, rim: Rect, events: list[pygame.event.Event]):
		global score

		# check input
		for event in events:
			if (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
				self.vel = Vector2(100, -300)

		if self.touchGround == False:
			# gravity
			self.vel.y += GRAVITY * delta

		# apply physics
		self.pos += self.vel * delta

		# ground collision
		if self.pos.y > 700:
			self.touchGround = True
			self.pos.y = 700
			self.vel.y *= -0.5
		else:
			self.touchGround = False

		# backboard side collision
		if (
			self.vel.x > 0 
			and self.pos.y + BALL_RADIUS > backboard.top + 5 # offset so it doesn't interfere with top collision
			and self.pos.y - BALL_RADIUS < backboard.bottom
			and self.pos.x + BALL_RADIUS > backboard.left # ┐
			and self.pos.x - BALL_RADIUS < backboard.left # ┴ only collide with the side
		):
			self.vel.x *= -1

		# backboard top collision
		if (
			self.vel.y > 0 
			and self.pos.y + BALL_RADIUS > backboard.top # ┐
			and self.pos.y - BALL_RADIUS < backboard.top # ┴ only collide with the top
			and self.pos.x + BALL_RADIUS > backboard.left + 5
			and self.pos.x - BALL_RADIUS < backboard.right
		):
			self.vel.y *= -1

		#rim collision
		if ( 
			self.pos.y + BALL_RADIUS > rim.top #     ┐
			and self.pos.y - BALL_RADIUS < rim.top # ┴ only collide with the top
			and self.pos.x + BALL_RADIUS > rim.left
			and self.pos.x - BALL_RADIUS < rim.right
		):
			self.vel.y *= -1

		# basket collision
		if (
			self.pos.y > basket.top #         ┐
			and self.pos.y < basket.top + 5 # ┴ only collide with the top
			and self.pos.x > basket.left
			and self.pos.x < basket.right
		):
			if self.vel.y > 0:
				if not self.hasScored:
					score += 1
					print(score)
					self.hasScored = True
			else:
				self.vel.y *= -1
		else:
			self.hasScored = False
		
		# wall wrapping
		if self.pos.x > 400:
			self.pos.x = 0
		elif self.pos.x < 0:
			self.pos.x = 400

	def draw(self, surface: pygame.Surface):
		pygame.draw.circle(surface, "#fba524", self.pos, BALL_RADIUS)


# setup
ball = Ball(Vector2(100, 700))
screen = pygame.display.set_mode((400, 800))
clock = pygame.time.Clock()
backboard = Rect(380, 350, 10, 100)
basket = Rect(325, 395, 55, 55)
rim = Rect(320, 395, 5, 5)
rim2 = Rect(320, 395, 60, 5) # only visual, not for collsion

# main loop
running = True
while running == True:
	delta = clock.tick(60) / 1000

	# input
	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			running = False
	
	# update
	ball.update(delta, backboard, basket, rim, events)
 
	# draw
	screen.fill((0, 0, 0))
	ball.draw(screen)
	
	pygame.draw.rect(screen, "#ffffff", backboard)
	pygame.draw.rect(screen, "#2a97fa", basket)
	pygame.draw.rect(screen, "#114f83", rim)
	pygame.draw.rect(screen, "#114f83", rim2)
	pygame.display.flip()
