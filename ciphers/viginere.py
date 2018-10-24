from . import util
from . import caesar
from itertools import groupby, combinations
from operator import itemgetter

name = "viginere"


# Apply viginere cipher to text using key
# Encrypt if direction = 1
# Decrypt if direction = -1
def apply(text, key, direction):
	result = ""

	# Which letter of the key to shift by
	key_index = 0

	for letter in text:
		if letter.lower() in util.alphabet:  # if letter is in the alphabet...
			new_letter = caesar.apply(letter, key[key_index], direction)  # ...shift letter depending on the key
			key_index += 1
			key_index = key_index % len(key)
			result += new_letter
		else:       # ignore letters outside the alphabet
			result += letter

	return result


# Encrypt text using key
def encrypt(plaintext, key):
	return apply(plaintext, key, 1)


# Decrypt text using key
def decrypt(ciphertext, key):
	return apply(ciphertext, key, -1)


# Detects all the repeated substrings of length 'repetition_length'
# Calculates the gaps between subsequent instances of each repeated substring
# And returns a dict of gap size vs number of times a gap of this size appears
#
# For example, if clean = 'catcatredqred' and repetition_length = 3, this returns {3: 1, 4: 1}
# because it detects one gap of length 3 (between the two instances of 'cat') and one gap of length 4
# (between the two instances of the word 'red').
def gaps(clean, repetition_length):
	# Find all substrings of length repetition_length
	windows = util.sliding(clean, repetition_length)

	# Pair them with indices
	# then sort them because for some reason that's required by itertools.groupby
	windows = sorted(enumerate(windows), key=itemgetter(1))
	# Group each (index, substring) pair by substring
	grouped = groupby(windows, key=itemgetter(1))
	# Filter out the substring, keep only the indices
	indices = [[index for index, a in v] for k, v in grouped]

	# Convert to list of all the gaps between subsequent indices of the same substring
	gaps_list = [l[1] - l[0] for x in indices for l in combinations(x, 2)]

	# Convert to dict of gap vs frequency of gap
	return dict((gap, gaps_list.count(gap)) for gap in set(gaps_list))


# Take gcd of gaps between substrings of length 'repetition_length'
# which is likely to the length of they key or a multiple of the length of the key
# for some value of repetition_length
def key_length_guess(clean, repetition_length):
	gaps_list = gaps(clean, repetition_length).keys()

	# If no gaps are found (no repetitions of length 'repetition_length'), return None
	if not gaps_list:
		return None
	else:
		return util.gcd(*gaps_list)  # otherwise, return gcd of all gaps


# Guesses the key given the key length using expected frequencies of English letters
def frequency_analysis(clean, key_length):
	key_guess = ""

	# For each letter of the key...
	for i in range(key_length):
		upper_bound = len(clean) // key_length
		if i < len(clean) % key_length:
			upper_bound += 1

		# ... find all the letters in the ciphertext which are rotated by that letter
		common = ''.join([clean[key_length * j + i] for j in range(upper_bound)])

		# Shift these letters by all 26 letters of alphabet...
		possibilities = [(letter, caesar.decrypt(common, letter)) for letter in util.alphabet]

		# ...and sort them by chi squared to select most probable outcome
		possibilities.sort(key=lambda v: util.chi_squared(v[1]))

		# add the optimal letter to the key guess
		key_guess += possibilities[0][0]

	return key_guess


# Guesses the key by looking for repetitions of length 'repetition_length'
def guess_with_repetition_length(ciphertext, clean, repetition_length):
	# Guess the key length
	key_length = key_length_guess(clean, repetition_length)
	if key_length is None:
		return None

	# Guess the key from the key_length
	key = frequency_analysis(clean, key_length)
	plaintext = decrypt(ciphertext, key)
	# Give it a score from 0 to 1 (higher is better) indicating how much the text seems like English
	score = util.is_english_model.predict(plaintext)

	return key, plaintext, score


# Attempts to decrypt the given ciphertext, assuming that the ciphertext is encrypted using viginere, by trying different repetition lengths
def guess(ciphertext):
	# Cleaned ciphertext with only lower case letters from the alphabet
	clean = ''.join([letter for letter in ciphertext.lower() if letter in util.alphabet])

	# Start at repetition length of 2 (1 doesn't make sense as that's just checking for repeated letters)
	repetition_length = 2

	possibilities = []

	while True:
		possibility = guess_with_repetition_length(ciphertext, clean, repetition_length)
		if possibility is None:  # Stop once repetition length is so high that no repetitions are found
			break

		if possibility[0] not in [key for key, _, _ in possibilities]:  # check that possibility isn't duplicate already suggested by other repetition lengths
			possibilities.append(possibility)

		repetition_length += 1  # Keep increasing repetition length

	# sort by score
	possibilities.sort(key=itemgetter(2), reverse=True)
	return possibilities
