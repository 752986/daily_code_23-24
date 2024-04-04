# Fishing minigame based on stardew valley fishing using model-view-controller pattern

#TODO: state machine for gameplay loop, casting and waiting phases, scoring, different fish types

from typing import Literal
import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
import random


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)

PADDLE_SIZE = 0.2 # fraction of full height
PADDLE_SPEED = 1 # fraction per second per second, acceleration
FISH_CHANGE_TIME = 0.5 # seconds, time to new vel
FISH_SPEED = 0.2 # fraction per second per second, max speed
PROGRESS_GAIN = 0.1 # fraction per second
PROGRESS_LOSS = 0.2 # fraction per second


# pygame init:
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Fishing Game")


# definitions:
class FishingGame:
	# constants:
	WIDTH = 64
	HEIGHT = 500
	PROGRESS_WIDTH = 12
	PADDING = 8

	# model:
	progress: float # 0..1, percent complete
	fishPos: float # 0..1, fish center position
	fishVel: float # fish velocity
	fishAccel: float # fish acceleration
	fishTimer: float # time until new fish acceleration
	paddlePos: float # 0..1, paddle top position
	paddleVel: float # paddle velocity
	pos: Vector2 # top left of game widget
	state: Literal["playing", "lost", "won"] # game state enum

	def __init__(self, pos: Vector2):
		self.progress = 0.25
		self.fishPos = random.random()
		self.fishVel = 0.0
		self.fishTimer = 0.0
		self.paddlePos = self.fishPos + (PADDLE_SIZE / 2)
		self.paddleVel = 0.0
		self.pos = pos
		self.state = "playing"

	def touchingFish(self) -> bool:
		return self.paddlePos >= self.fishPos >= self.paddlePos - PADDLE_SIZE

	# view:
	def draw(self, surface: Surface):
		# static elements
		borderBox = Rect(
			self.pos, 
			Vector2(
				self.WIDTH, 
				self.HEIGHT
			)
		)

		fishBox = Rect(
			self.pos + Vector2(self.PADDING), 
			Vector2(
				self.WIDTH - self.PROGRESS_WIDTH - self.PADDING * 2, 
				self.HEIGHT - self.PADDING * 2
			)
		)

		progressBox = Rect(
			fishBox.topright,
			Vector2(
				self.PROGRESS_WIDTH,
				self.HEIGHT - self.PADDING * 2
			)
		)

		pygame.draw.rect(surface, "#b9b9b9", borderBox) # background / border
		pygame.draw.rect(surface, "#1f9ecd", fishBox) # water background
		pygame.draw.rect(surface, "#9e9e9e", progressBox) # progress background

		# dynamic elements
		progressHeight = progressBox.height * self.progress
		progressBar = Rect(
			Vector2(
				progressBox.left,
				progressBox.top + (progressBox.height - progressHeight)
			),
			Vector2(
				self.PROGRESS_WIDTH,
				progressHeight
			)
		)

		paddleHeight = PADDLE_SIZE * fishBox.height
		paddleY = fishBox.height * (1 - self.paddlePos)
		paddleBox = Rect(
			Vector2(
				fishBox.left,
				fishBox.top + paddleY
			),
			Vector2(
				fishBox.width,
				paddleHeight
			)
		)

		#TODO: make this code work with arbitrary height fish images
		fishY = fishBox.height * (1 - self.fishPos)
		fish = Rect(
			Vector2(
				fishBox.left,
				fishBox.top + fishY
			),
			Vector2(
				fishBox.width,
				4
			)
		)

		pygame.draw.rect(surface, "#f5b700", progressBar) # progress bar
		pygame.draw.rect(surface, "#24bd75" if self.touchingFish() else "#00653a", paddleBox) # paddle
		pygame.draw.rect(surface, "#ac85cf", fish) # fish

	# controller:
	def update(self, delta: float, keys: pygame.key.ScancodeWrapper):
		if self.state != "playing": # stop when game is over
			return

		# paddle control
		if keys[pygame.K_SPACE]:
			self.paddleVel += PADDLE_SPEED * delta
		else:
			self.paddleVel -= PADDLE_SPEED * delta
		self.paddlePos += self.paddleVel * delta

		if not 1 > self.paddlePos > PADDLE_SIZE:
			self.paddlePos = min(max(self.paddlePos, PADDLE_SIZE), 1) # clamp between 0 and 1, taking into account height of paddle
			self.paddleVel = 0

		# fish control
		if self.fishTimer > 0:
			self.fishTimer -= delta
		else:
			self.fishTimer = FISH_CHANGE_TIME
			self.fishVel = (random.random() * 2 - 1) * FISH_SPEED

		self.fishPos += self.fishVel * delta

		if not 1 > self.fishPos > 0:
			self.fishPos = min(max(self.fishPos, 0), 1) # clamp between 0 and 1
			self.fishTimer = 0 # "reroll" new velocity

		# progress update
		if self.touchingFish():
			self.progress += PROGRESS_GAIN * delta
		else:
			self.progress -= PROGRESS_LOSS * delta

		# scoring
		if self.progress >= 1:
			self.state = "won"
		elif self.progress <= 0:
			self.state = "lost"


def main():
	# game setup:
	clock = pygame.time.Clock()
	game = FishingGame(Vector2(100, 100))

	# main loop:
	running = True
	while running:
		delta = clock.tick(FRAMERATE) / 1000

		# input:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		keys = pygame.key.get_pressed()

		game.update(delta, keys)

		# draw:
		screen.fill("#000000")
		game.draw(screen)

		pygame.display.flip()

if __name__ == "__main__":
	main()
