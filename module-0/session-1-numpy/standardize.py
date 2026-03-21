import numpy as np

def standardize(X):
    """
    X : np.ndarray de shape (n, d)
    Retourne X_std : même shape, chaque colonne centrée-réduite.
    Gère le cas où l'écart-type est nul (division par zéro).
    Zéro boucle autorisée.
    """

    n, d = X.shape
    std = X.std(axis = 0) # (d,)
    std_safe = np.where(std == 0, 1, std) # Manière idiomatique de rendre le std safe
    mean = X.mean(axis = 0) # (d,)

    return (X - mean)/std_safe




# Tests
X = np.array([[1., 2., 5.],
              [3., 4., 5.],
              [5., 6., 5.]])

X_std = standardize(X)

# Chaque colonne doit avoir moyenne ≈ 0 et std ≈ 1 (sauf colonne constante)
print(X_std.mean(axis=0))   # [~0, ~0, 0]
print(X_std.std(axis=0))    # [~1, ~1, 0]  ← colonne constante reste 0

