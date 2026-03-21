import numpy as np

def pairwise_distances(X):
    """
    X : np.ndarray de shape (n, d)
    Retourne D : np.ndarray de shape (n, n)
    D[i,j] = norme euclidienne entre X[i] et X[j]
    Zéro boucle autorisée.
    """

    n, d = X.shape
    norms = np.linalg.norm(X,axis=1)**2
    return np.sqrt(np.maximum(norms.reshape(n,1) + norms.reshape(1,n) - 2*X@X.T, 0))

    pass

# Test de validation
np.random.seed(42)
X = np.random.randn(5, 3)
D = pairwise_distances(X)

assert D.shape == (5, 5), "Shape incorrecte"
assert np.allclose(D, D.T), "La matrice doit être symétrique"
assert np.allclose(np.diag(D), 0,  atol=1e-6), "La diagonale doit être nulle"

# Vérification sur un cas simple
X2 = np.array([[0., 0.], [3., 4.]])
D2 = pairwise_distances(X2)
assert np.isclose(D2[0, 1], 5.0), f"Distance attendue : 5.0, obtenu : {D2[0,1]}"
print("Tous les tests passent.")

