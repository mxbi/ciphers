from functools import reduce

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

frequencies = {}


# Euclid's algorithm to find gcd of a list of numbers
def gcd(*args):

	# gcd of two numbers
	def gcd_two(a, b):
		if b == 0:
			return a
		return gcd(b, a % b)

	return reduce(gcd_two, args)


def letter_counts(text):
	return dict((letter, text.count(letter)) for letter in alphabet)


def chi_squared(text):
	counts = letter_counts(text)

	total = 0

	for (letter, observed) in counts:
		expected = frequencies[letter] * len(text)
		difference = observed - expected
		total += difference * difference / expected

	return total
