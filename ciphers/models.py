import re
import numpy as np

class IsEnglish_v1:
	def __init__(self):
		import tensorflow.keras as k
		self.k = k

		self.model = k.models.load_model('ciphers/models/isenglish_v1.keras')
		self.model_length = 100
		self.clean_expr = re.compile('[^a-zA-Z]+')

	def _clean_input(self, text):
		cleaned_text = re.sub(self.clean_expr, '', text).lower()
		cleaned_indices = np.array([ord(c) - 97 for c in cleaned_text])
		return cleaned_indices

	def _preprocess_input(self, text, n_samples):
		text = list(text)
		if len(text) < self.model_length:
			print("[WARN] Input sequence is length {}, less than model's length of {}. Looping sequence to match")
			substring = text
			while len(text) < self.model_length:

				text += substring

		window_max_pos = len(text) - 100
		batch_x = []
		# Randomly sample 128 100-length substrings
		for i in range(n_samples):
			left = np.random.randint(0, window_max_pos)
			batch_x.append(text[left:left+100])

		return batch_x

	def predict(self, text, n_samples=16):
		batch_x = self._preprocess_input(self._clean_input(text), n_samples)
		ps = self.model.predict_on_batch(np.array(batch_x))
		return np.mean(ps)

	def predict_multiple(self, texts, n_samples=16):
		batch_x = []
		for text in texts:
			batch_x.extend(self._preprocess_input(self._clean_input(text), n_samples))
		ps = self.model.predict_on_batch(np.array(batch_x))
		return [p.mean() for p in np.array_split(ps, len(texts))]
