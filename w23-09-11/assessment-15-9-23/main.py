# problem 1
# ---------

def biggest_of_three(a: int, b: int, c: int) -> int:
	if a > b and a > c:
		return a
	elif b > c:
		return b
	else:
		return c
	
a, b, c = (int(n) for n in input("Input three numbers saparated by spaces\n> ").split(" "))

print(biggest_of_three(a, b, c))


# problem 2
# ---------
print()

my_list = [int(input(f"{i+1:2}/10> ")) for i in range(10)]
mult_list = [i * 2 for i in my_list]

print(mult_list)