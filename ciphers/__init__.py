from operator import itemgetter

from . import substitution, models, util, viginere, caesar

__version__ = '0.0.1'


# List of all the encryption methods which can be used to attempt to decrypt given ciphertext
methods = [caesar, viginere]


# Iterates through the given encryption methods and tries to decrypt the ciphertext with each one
# Then sorts all the possibilities by how English they look
def guess(ciphertext):
	possibilities = []

	# Try each method
	for method in methods:
		# Add method name to each tuple before adding possibilities to list
		for possibility in method.guess(ciphertext):
			possibilities.append((method.name,) + possibility)

	# Sort by 3rd position in tuple, which is English score
	possibilities.sort(key=itemgetter(3), reverse=True)
	return possibilities
