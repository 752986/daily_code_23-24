from enum import Enum


class Unit(Enum):
	Kilometers = 0
	Miles = 1

	def fullName(self) -> str:
		match self:
			case self.Kilometers:
				return "kilometers"
			case self.Miles:
				return "miles"
			
	def opposite(self) -> "Unit":
		match self:
			case self.Kilometers:
				return self.Miles
			case self.Miles:
				return self.Kilometers
			

def convertDistance(distance: float, into: Unit) -> float:
	return distance * (0.62137 if into == Unit.Miles else 1.60934)


def main():
	unit: Unit
	match input("Do you want to enter distance as miles or kilometers? (type `k` or `m`)\n> ").lower():
		case "kilometers" | "k": unit = Unit.Kilometers
		case "meters" | "m": unit = Unit.Miles
		case _:
			print("Invalid unit input.")
			exit()
	
	distance = float(input(f"How many {unit.fullName()} would you like to scooter?\n> "))
	print(f"That is {round(convertDistance(distance, unit.opposite()), 5)} {unit.opposite().fullName()}.")

	distanceInMiles: float
	if unit == Unit.Miles:
		distanceInMiles = distance
	else:
		distanceInMiles = convertDistance(distance, Unit.Miles)

	time = (distanceInMiles / 15) * 60
	print(f"It will take {time:.1f} minutes.")

	costs: list[float] = [
		0.15 * time + 1.00,
		0.12 * max(time - 5, 0) + 2.50,
		0.06 * time + 5.00
	]

	best = costs.index(min(costs))
	letter = chr(ord("A") + best)
	print(f"You should use Company {letter}. It will cost ${costs[best]:.2f}.")

if __name__ == "__main__": main()
