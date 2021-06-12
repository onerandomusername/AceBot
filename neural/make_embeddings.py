import os
import pickle
from collections import Counter

import torch
from torchtext.data.utils import get_tokenizer

from torch_config import CORPUS_DIR, EMBEDDINGS_DIR, GLOVE_DIR

tokenizer = get_tokenizer('basic_english')
counter = Counter()

for dir, subdir, files in os.walk(f'{CORPUS_DIR}/proc'):
	dir = dir.replace(r'\\', '/')

	for file in files:
		with open(f'{dir}/{file}', 'r') as f:
			text = f.read()

		counter.update(tokenizer(text))

glove_wti: dict = pickle.load(open(f'{GLOVE_DIR}/word2idx.pkl', 'rb'))
glove_vectors: torch.Tensor = torch.load(f'{GLOVE_DIR}/vectors.pkl')

embed_idx = 0
embed_wti = dict()
embed_vectors = []

for word in counter.keys():
	glove_idx = glove_wti.get(word, None)

	if glove_idx is None:
		continue

	embed_wti[word] = embed_idx
	embed_vectors.append(glove_vectors[glove_idx])
	embed_idx += 1

if not os.path.exists(EMBEDDINGS_DIR):
	os.mkdir(EMBEDDINGS_DIR)

pickle.dump(embed_wti, open(f'{EMBEDDINGS_DIR}/wti.pkl', 'wb'))
torch.save(torch.stack(embed_vectors), f'{EMBEDDINGS_DIR}/vectors.pkl')
