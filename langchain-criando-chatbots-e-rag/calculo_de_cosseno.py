import numpy as np

# Vetores de exemplo
vetor_a = np.array([1, 2, 3])
vetor_b = np.array([4, 5, 6])

# Cálculo do produto escalar e das normas
produto_escalar = np.dot(vetor_a, vetor_b)
norma_a = np.linalg.norm(vetor_a)
norma_b = np.linalg.norm(vetor_b)

# Cálculo da similaridade de cosseno
similaridade = produto_escalar / (norma_a * norma_b)
print(f'Similaridade de Cosseno: {similaridade}')
