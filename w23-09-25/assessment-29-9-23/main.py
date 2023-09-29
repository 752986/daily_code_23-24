import random

class LightBulb:
	on: bool
	color: str
	burnedOut: bool

	def __init__(self, color: str):
		self.on = False
		self.color = color
		self.burnedOut = False

	def __str__(self) -> str:
		return f"lightbulb with color {self.color} is {'burned out' if self.burnedOut else 'on' if self.on else 'off'}"
	
	def turnOn(self):
		self.on = True
		if random.random() <= 0.05:
			self.burnOut()

	def turnOff(self):
		self.on = False

	def burnOut(self):
		self.burnedOut = True


def main():
	bulbs = [LightBulb("#" + hex(random.randint(0, 0xffffff)).removeprefix("0x")) for _ in range(3)]
	for _ in range(50):
		for bulb in bulbs:
			if random.random() >= 0.5:
				bulb.turnOn()
			else:
				bulb.turnOff()
			
			print(bulb)

		print()

if __name__ == "__main__":
	main()