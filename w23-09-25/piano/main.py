import pygame
from pygame.math import Vector2
from pygame.rect import Rect

BUTTONSIZE = 50
BLACKKEYS = [False, True, False, True, False, False, True, False, True, False, True, False]

pygame.init() # initializes Pygame
pygame.display.set_caption("python piano program") # sets the window title
screen = pygame.display.set_mode((800, 800)) # creates game screen
screen.fill((100, 100, 100))

# audio stuff!
pygame.mixer.init()
pygame.mixer.set_num_channels(24) # extra channels so keys don't step on each other
# skipping every other key so it fits a piano octave
notes = [pygame.mixer.Sound(f"./samples/key{(i * 2) + 1:02}.mp3") for i in range(12)]

Button = Rect
buttons: list[Button] = []
whiteKeys = 0
for i in range(12):
	if not BLACKKEYS[i]:
		whiteKeys += 1

	buttons.append(
		Button(
			whiteKeys * (BUTTONSIZE + 2) + (BUTTONSIZE / 2 if BLACKKEYS[i] else 0), 
			500 - (100 if BLACKKEYS[i] else 0), 
			BUTTONSIZE, 
			300
		) 
	)

# this holds onto what key the user has pressed
keyPressed: int | None = None
mousePos = Vector2(0, 0)

# gameloop
while True:    
	# event queue (bucket that holds stuff that happens in game and passes to one of the sections below)
	event = pygame.event.wait()
	
	if event.type == pygame.QUIT: # close game window
		break
	elif event.type == pygame.MOUSEBUTTONDOWN:
		for i, b in enumerate(buttons):
			if b.collidepoint(mousePos):
				keyPressed = i
				break
			keyPressed = None # if the mouse isn't over any key
	elif event.type == pygame.MOUSEBUTTONUP:
		keyPressed = None
	elif event.type == pygame.MOUSEMOTION:
		mousePos = Vector2(event.pos)
	
	# the keys 
	for i, b in enumerate(buttons):
		if keyPressed == i:
			pygame.draw.rect(screen, (200, 200, 200), b)
		else:
			pygame.draw.rect(screen, ((0, 0, 0) if BLACKKEYS[i] else (255, 255, 255)), b)

	if keyPressed != None:
		notes[keyPressed].play()
	
	pygame.display.flip() # always needed at the end of every game loop!
	
# end game loop
pygame.quit()
