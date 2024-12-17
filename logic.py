import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity_score(v1, v2):
    v1 = np.array(v1).reshape(1, -1)
    v2 = np.array(v2).reshape(1, -1)
    return cosine_similarity(v1, v2)[0][0]