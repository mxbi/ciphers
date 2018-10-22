from . import util
from . import caesar
from . import models
from itertools import groupby, combinations
from operator import itemgetter

model = models.IsEnglish_v1()


class Viginere:
	def __init__(self, ciphertext):
		self.ciphertext = ciphertext
		self.clean = "".join([x for x in ciphertext.lower() if x in util.alphabet])

	def decrypt(self, key):
		plaintext = ""

		key_index = 0

		for letter in self.ciphertext:
			uppercase = False

			if letter in util.alphabet.upper():
				letter = letter.lower()
				uppercase = True

			if letter in util.alphabet:
				letter_index = util.alphabet.index(letter)
				rotation = util.alphabet.index(key[key_index])
				new_index = (letter_index - rotation) % 26
				new_letter = util.alphabet[new_index]
				key_index += 1
				key_index = key_index % len(key)

				if uppercase:
					new_letter = new_letter.upper()

				plaintext += new_letter
			else:
				plaintext += letter

		return plaintext

	# Detects all the repeated substrings of length 'repetition_length'
	# Calculates the gaps between subsequent instances of each repeated substring
	# And returns a dict of gap size vs number of times a gap of this size appears
	#
	# For example, if clean = 'catcatredqred' and repetition_length = 3, this returns {3: 1, 4: 1}
	# because it detects one gap of length 3 (between the two instances of 'cat') and one gap of length 4
	# (between the two instances of the word 'red').
	def gaps(self, repetition_length):
		# Find all substrings of length repetition_length
		windows = util.sliding(self.clean, repetition_length)

		# Pair them with indices
		# then sort them because for some reason that's required by itertools.groupby
		windows = sorted(enumerate(windows), key=itemgetter(1))
		# Group each (index, substring) pair by substring
		grouped = groupby(windows, key=itemgetter(1))
		# Filter out the substring, keep only the indices
		indices = [[index for index, a in v] for k, v in grouped]

		# Convert to list of all the gaps between subsequent indices of the same substring
		gaps = [l[1] - l[0] for x in indices for l in combinations(x, 2)]

		# Convert to dict of gap vs frequency of gap
		return dict((gap, gaps.count(gap)) for gap in set(gaps))

	# Take gcd of gaps between substrings of length 'repetition_length'
	# which is likely to the length of they key or a multiple of the length of the key
	# for some value of repetition_length
	def key_length_guess(self, repetition_length):
		gaps = self.gaps(repetition_length).keys()

		if not gaps:
			return None
		else:
			return util.gcd(*gaps)

	def frequency_analysis(self, key_length):
		key_guess = ""

		for i in range(key_length):
			x = len(self.clean) // key_length
			if i < len(self.clean) % key_length:
				x += 1

			common = "".join([self.clean[key_length * j + i] for j in range(x)])

			possibilities = [(letter, caesar.decrypt(common, letter)) for letter in util.alphabet]
			possibilities.sort(key=lambda v: util.chi_squared(v[1]))
			key_guess += possibilities[0][0]

		return key_guess#

	def guess(self, repetition_length=None):
		if repetition_length is None:
			repetition_length = 2

			possibilities = []

			while True:
				possibility = self.guess(repetition_length)
				if possibility is None:
					break

				possibilities.extend(possibility)
				repetition_length += 1

			possibilities = [(key, plaintext, model.predict(plaintext)) for key, plaintext in possibilities]

			possibilities.sort(key=lambda v: v[2], reverse=True)
			return possibilities

		else:
			key_length = self.key_length_guess(repetition_length)
			if key_length is None:
				return None

			key = self.frequency_analysis(key_length)
			return [(key, self.decrypt(key))]