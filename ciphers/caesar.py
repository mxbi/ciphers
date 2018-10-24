from operator import itemgetter

from .util import alphabet, is_english_model

name = "caesar"


# Apply caesar shift on text using the character 'key'
# Encrypt if direction = 1
# Decrypt if direction = -1
def apply(text, key, direction):
	key = key.lower()
	shift = direction * alphabet.index(key)

	result = ""

	for letter in text:
		uppercase = False

		if letter in alphabet.upper():
			letter = letter.lower()
			uppercase = True

		if letter in alphabet:
			new_letter = alphabet[(alphabet.index(letter) + shift) % 26]
			if uppercase:
				new_letter = new_letter.upper()
			result += new_letter
		else:
			result += letter

	return result


def encrypt(plaintext, key):
	return apply(plaintext, key, 1)


def decrypt(ciphertext, key):
	return apply(ciphertext, key, -1)


# Iterate through all possible caesar shifts (by each letter of the alphabet) and sort them by how English the decrypted plaintext looks
def guess(ciphertext):
	possibilities = [(key, decrypt(ciphertext, key)) for key in alphabet]
	possibilities = [(key, plaintext, is_english_model.predict(plaintext)) for key, plaintext in possibilities]
	possibilities.sort(key=itemgetter(2), reverse=True)
	return possibilities
