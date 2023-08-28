# problem 6:
result = -5 + 9*9
	
print(result)


# problem 7:
result = 20 - 17*7
	
print(result)


# problem 8:
result = 2 + 0.4*20
	
print(result)


# problem 3:
result = -5
# the range starts at 2 because the overall iterations start at n=1, and that has "run" before the loop even starts
# the range ends at 4+1 because it should end *on* 4, but python ranges end one before the end
for _ in range(2, 4+1):
	result = result + 9
	
print(result)


# problem 4:
result = 20
for _ in range(2, 3+1):
	result = result - 17

print(result)

	
# problem 5:
result = 2
for _ in range(2, 5+1):
	result = result + 0.4
	
print(result)