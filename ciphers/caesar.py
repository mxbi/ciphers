from .util import alphabet


def encrypt(plaintext, key):
	index = alphabet.index(key)

	return "".join([alphabet[(alphabet.index(letter) + index) % 26] for letter in plaintext])


def decrypt(ciphertext, key):
	index = alphabet.index(key)

	return "".join([alphabet[(alphabet.index(letter) - index) % 26] for letter in ciphertext])