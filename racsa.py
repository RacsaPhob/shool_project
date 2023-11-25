def find_devision(function):
	if not('/') in function:
		return False
	else:
		count = 0
		devision_chs = []
		for ch in function:
			if ch=='/':
				devision_chs.append(count)
			count +=1
		expressions = []
		for devisions in devision_chs:
			count = 0
			count1 = 0
			new_function = function[devisions:]
			if '(' in new_function:

				for ch in new_function:
					count1 +=1
					if ch =='(':
						count +=1
					elif ch ==')':
						count -=1
						if count ==0:
							expressions.append((new_function[1:count1]))
		else:
			expressions.append((new_function[1:]))

		print(expressions)

find_devision('(x+3)/(x-3) ')