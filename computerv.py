import sys
import re

def correct_symbols(string):
	if len([c for c in string if c not in '*/-+^=xX.1234567890 ']):
		raise ValueError('Incorrect input!')

def to_int(string: str):
	splitted = re.findall(r'\d+', string)
	number = int(splitted[0])
	if (len(splitted) == 2):
		number += int(splitted[1]) * (0.1 ** len(splitted[1]))
	return number

def is_x(i, part):
	degree = 1
	i += 1
	if (i + 1) < len(part) and part[i] == '^' and part[i + 1].isdigit():
		i += 1
		numb = '\0'
		while (i < len(part) and part[i].isdigit()):
			numb += part[i]
			i += 1
		degree = to_int(numb)
	return (i, degree)

def split_polynom(string):
	parts = string.replace(' ', '').split('=')
	if len(parts) != 2:
		raise ValueError('Incorrect input!')
	polynom = {}
	is_first_part = True
	for part in parts:
		i = 0
		while i < len(part):
			sign = 1
			if part[i] in '+-':
				sign = 1 if part[i] == '+' else -1
				i += 1
			if i < len(part) and (part[i] in 'xX'):
				coef = 1
				i, degree = is_x(i, part)
			elif i < len(part) and part[i].isdigit():
				numb = '\0'
				while (i < len(part) and (part[i].isdigit() or part[i] == '.')):
					numb += part[i]
					i += 1
				coef = to_int(numb)
				if (i < len(part) and part[i] != '*') or i == len(part):
					degree = 0
				elif (i + 1) < len(part) and part[i] == '*' and (part[i + 1] in 'xX'):
					i += 1
					i, degree = is_x(i, part)
				else:
					raise ValueError('Incorrect input!')
				polynom.setdefault(degree, 0)
				polynom[degree] += float(coef * sign if is_first_part else -coef * sign)
			else:
				raise ValueError('Incorrect input!')
		is_first_part = False
	return polynom

def reduced_form(polynom):
	string = '\0'
	is_first = True
	for key in sorted(polynom):
		if polynom[key] != 0:
			part = str(polynom[key])
			if part[0] == '-':
				part = part[0] + ' ' + part[1:]
			elif key != 0 and is_first == False:
				part = '+ ' + part
			part += ' * X^' + str(key) + ' '
			string += part
			is_first = False
	if string == '\0':
		string = '0 '
	string += '= 0'

	print('Reduced form:', string)
	print('Polynomial degree:', sorted(polynom)[-1])
	if sorted(polynom)[-1] > 2:
		raise ValueError('The degree is too big!')


def calculate_polynom(polynom):
	c = polynom.setdefault(0, 0)
	b = polynom.setdefault(1, 0)
	a = polynom.setdefault(2, 0)
	D = b ** 2 - 4 * a * c
	print('Coefficients of polynom:\n a = {0}\n b = {1}\n c = {2}'.format(a, b, c))

	if (a == 0 and b == 0 and c == 0):
		print('Each real number is a solution')
	elif a == 0 and b != 0:
		print('a = 0 so there is one solution:')
		print('x = -c / b = -({0}) / ({1}) = {2}'.format(c, b, -c / b))
	elif a == 0 and b == 0 and c != 0:
		print('There are no solutions!')
	else:
		print('Discriminant:\n D = b^2 - 4ac = ({0})^2 - 4 * ({1}) * ({2}) = {3}'.format(b, a, c, D))
		if D < 0:
			print('Discriminant is strictly negative, there is no solutions')
		elif D == 0:
			print('Discriminant is equal to 0, there is one solution:')
			print((-b) / (2 * a))
			print('x = -b / 2a = -({0}) / 2 * ({1}) = {2}'.format(b, a, (-b) / (2 * a)))
		else:
			print('Discriminant is strictly positive, the two solutions are:')
			print('x = (-b + √D) / 2a = (-({0}) + √{1}) / 2 * ({2}) = {3}'.format(b, D, a, (-b + D ** 0.5) / (2 * a)))
			print('x = (-b - √D) / 2a = (-({0}) - √{1}) / 2 * ({2}) = {3}'.format(b, D, a, (-b - D ** 0.5) / (2 * a)))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Invalid number of arguments")
	else:
		try:
			correct_symbols(sys.argv[1])
			polynom = split_polynom(sys.argv[1])
			reduced_form(polynom)
			calculate_polynom(polynom)
		except ValueError as err:
			print(err)
