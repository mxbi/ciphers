def apply_substitution(ciphertext, cipher_alphabet, plain_alphabet='abcdefghijklmnopqrstuvwxyz', case_sensitive=False):
	"""
	Applies a mapping from cipher_alphabet->plain_alphabet on the ciphertext.

	:param ciphertext: The ciphertext to apply the substitution to
	:param cipher_alphabet: The keys for the substitution
	:param plain_alphabet: The
	:param case_sensitive: Whether the substitution is applied case-sensitive or not. Default: False (i.e. a and A treated the same)
	:return: The deciphered ciphertext
	"""
	if not case_sensitive:
		ciphertext = ciphertext.lower()
		cipher_alphabet = cipher_alphabet.lower()
		plain_alphabet = plain_alphabet.lower()

	for p, c in zip(plain_alphabet, cipher_alphabet):
		ciphertext = ciphertext.replace(p, c)

	return ciphertext
