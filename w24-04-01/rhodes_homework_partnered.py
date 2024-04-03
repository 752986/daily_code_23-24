unit = input("Do you want to enter distance as miles or kilometers (type m or k):").lower()
if  unit == 'm':
	miles = float(input("How many miles would you like to scooter?"))
	kilometers = miles*1.60934
	print("That is" +str(kilometers)+ "kilometers")
	time = miles*4
	print("Total time in minutes:" +str(time))
	companyA = 0.15*time+1
	if time < 5: 
		companyB = 2.5
	else:
		companyB = 0.12*time + 1.9
	companyC = 0.06*time + 5
	if companyA < companyB and companyA < companyC:
		print("You should use Company A. It will cost" +str(round(companyA, 2)))
	elif companyB < companyA and companyB < companyC:
		print("You should use Company B. It will cost" +str(round(companyB, 2)))
	elif  companyC < companyB and companyC < companyA:
		print("You should use CompanyC. It will cost" +str(round(companyC, 2)))
elif  unit == 'k':
	kilometers = float(input("How many kilometers would you like to scooter?"))
	miles = kilometers/1.60934
	print("That is" +str(miles)+ "miles")
	time = miles*4
	print("Total time in minutes:" +str(time))
	companyA = 0.15*time+1
	if time < 5: 
		companyB = 2.5
	else:
		companyB = 0.12*time + 1.9
	companyC = 0.06*time + 5
	if companyA < companyB and companyA < companyC:
		print("You should use Company A. It will cost" +str(round(companyA, 2)))
	elif companyB < companyA and companyB < companyC:
		print("You should use Company B. It will cost" +str(round(companyB, 2)))
	elif  companyC < companyB and companyC < companyA:
		print("You should use CompanyC. It will cost" +str(round(companyC, 2)))
else:
	print("Invalid unit!")
