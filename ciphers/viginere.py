import util
from itertools import groupby
from operator import itemgetter

class Viginere:
	def __init__(self, ciphertext):
		self.ciphertext = ciphertext
		self.clean = "".join([x for x in ciphertext.lower() if x in util.alphabet])

	def decrypt(self, key):
		pass

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
		gaps = [l[1] - l[0] for x in indices for l in util.sliding(x, 2)]

		# Convert to dict of gap vs frequency of gap
		return dict((gap, gaps.count(gap)) for gap in set(gaps))
