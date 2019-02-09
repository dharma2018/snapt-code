class Embedding(object):
    def __init__(self,vocab_file,vectors_file):
        with open(vocab_file, 'r') as f:
			# vocab_file을 읽어서 단어 단위로 분리, 토크나이징
			# 파이썬 rstrip ()은 문자열의 지정된 문자열의 끝을 (기본값은 공백입니다) 삭제
            words = [x.rstrip().split(' ')[0] for x in f.readlines()]

        with open(vectors_file, 'r') as f:
            vectors = {}
            for line in f:
                vals = line.rstrip().split(' ') # key
                vectors[vals[0]] = [float(x) for x in vals[1:]] # value

        vocab_size = len(words)
        vocab = {w: idx for idx, w in enumerate(words)}
        ivocab = {idx: w for idx, w in enumerate(words)}

        vector_dim = len(vectors[ivocab[0]])
        W = np.zeros((vocab_size, vector_dim))
        for word, v in vectors.items():
            if word == '<unk>':
                continue
            W[vocab[word], :] = v

        # normalize each word vector to unit variance
        W_norm = np.zeros(W.shape)
        d = (np.sum(W ** 2, 1) ** (0.5))
        W_norm = (W.T / d).T

        self.W = W_norm
        self.vocab = vocab
        self.ivocab = ivocab
