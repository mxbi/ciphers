from functools import reduce

from . import models

alphabet = 'abcdefghijklmnopqrstuvwxyz'

frequencies = {
	'a': 0.08167,
	'b': 0.01492,
	'c': 0.02782,
	'd': 0.04253,
	'e': 0.12702,
	'f': 0.02228,
	'g': 0.02015,
	'h': 0.06094,
	'i': 0.06966,
	'j': 0.00153,
	'k': 0.00772,
	'l': 0.04025,
	'm': 0.02406,
	'n': 0.06749,
	'o': 0.07507,
	'p': 0.01929,
	'q': 0.00095,
	'r': 0.05987,
	's': 0.06327,
	't': 0.09056,
	'u': 0.02758,
	'v': 0.00978,
	'w': 0.02360,
	'x': 0.00150,
	'y': 0.01974,
	'z': 0.00074,
}

is_english_model = models.IsEnglish_v1()


# Repeated application of Euclid's algorithm to find gcd of a list of numbers
def gcd(*args):

	# gcd of two numbers
	def gcd_two(a, b):
		if b == 0:
			return a
		return gcd(b, a % b)

	return reduce(gcd_two, args)


# Given a string, creates a map of letters vs number of times the letter appears in the text
# eg 'aabccc' returns {'a': 2, 'b': 1, 'c': 3} with every other letter mapping to 0.
def letter_counts(text):
	return dict((letter, text.count(letter)) for letter in alphabet)


# How much does the text's letter frequencies match up with the expected frequencies of English?
# Returns a number between 0 and infinity. Lower means more like English frequencies.
def chi_squared(text):
	counts = letter_counts(text)

	total = 0

	for (letter, observed) in counts.items():
		expected = frequencies[letter] * len(text)
		difference = observed - expected
		total += difference * difference / expected

	return total


# Returns a sliding window of length n over the input
# eg sliding('abcdef', 2) returns a generator which yields ['ab', 'bc', 'cd', 'de', 'ef']
# Works on both lists and strings
def sliding(seq, n):
	# Take first n elements of the sequence
	window = seq[:n]

	# If length of string is less than n don't yield anything...
	if len(window) == n:
		yield window  # ...otherwise, yield the first n elements as the first window

	# For each remaining element...
	for elem in seq[n:]:
		window = window[1:]  # ...remove the first element of the window...

		# ...and add a new element
		if type(seq) is str:
			window += elem
		else:
			window.append(elem)

		yield window  # Yield the new window, slid along by one element
