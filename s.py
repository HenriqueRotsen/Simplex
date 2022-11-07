# %%
import numpy as np
import math

# %%
"""
n = int(input())
assert (n >= 1 and n <= 100)
m = int(input())
assert (m >= 1 and m <= 100)

pl = np.zeros((n, m))
for i in range(n):
  for j in range(m):
    x = int(input())
    assert x <= 100
    pl[i][j] = x
print(pl)
"""


# %%
def criaTableau(c, A, b, x, y):
    tableau = np.zeros((x+1, y+1))
    v = np.identity(x)
    
    k = np.zeros((x))
    v = np.vstack([k, v])
    
    for i in range(y):
        tableau[0][i] = -c[i]

    for i in range(x):
        for j in range(y):
            tableau[i+1][j] = A[i][j]

    for i in range(x):
        tableau[i+1][y] = b[i]   
    
    return tableau, v

# %%
def isOtima(tableau):
    z = tableau[0]
    for i in z[:-1]:
        if i > 0:
            return False
    return True

# %%
# Usando Regra de Bland
def pivotPosition(tableau):
    z = tableau[0]
    for i in range(len(z)-1):
        if z[i] > 0:
            column = i
            break
    else:
        raise Exception("ERRO: Nao foi possivel encontar um valor na funcao Objetiva que permite a melhora!\n Favor Verificar o tableu e tentar novamente.")

    restricoes = []
    for eq in tableau[1:]:
        el = eq[column]
        restricoes.append(math.inf if el <= 0 else eq[-1] / el)

    if all(x == math.inf for x in restricoes):
        print("===============================\n\n          ILIMITADA\n\n===============================")

    row = restricoes.index(min(restricoes))
    return row+1, column
    

# %%
def eliminacaoGaussiana(tableau, pivot_position, vero):
    novoTableau = [[] for eq in tableau]
    novoVero = [[] for eq in vero]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    
    # Dividindo a linha do pivo por ele mesmo, para virar 1.
    novoTableau[i] = np.array(tableau[i]) / pivot_value
    
    # Dividindo a linha do vero pelo pivo.
    novoVero[i] = np.array(vero[i]) / pivot_value

    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(novoTableau[i]) * tableau[eq_i][j]
            novoTableau[eq_i] = np.array(tableau[eq_i]) - multiplier

            aux = np.array(novoTableau[i][j]) * tableau[eq_i][j]
            multiplierVero = (aux *np.array(vero[i])) 
            novoVero[eq_i] = np.array(vero[eq_i]) - multiplierVero
    
    return novoTableau, novoVero

# %%
def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1

def get_solution(tableau):
    columns = np.array(tableau[1:]).T
    solutions = []
    for column in columns[:-1]:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)

    return solutions

# %%
def simplex(c, A, b):
    x = len(A)
    y = len(A[0])
    
    tableau, vero = criaTableau(c, A, b, x, y)
    print(isOtima(tableau))
    
    print(tableau)
    print(vero)

    while not(isOtima(tableau)):
        pivot_position = pivotPosition(tableau)
        tableau, vero = eliminacaoGaussiana(tableau, pivot_position, vero)
        
        print(np.matrix(tableau))
        print(np.matrix(vero))

    print(vero)
    return get_solution(tableau)

# %%
c = [-3, -4, 5, -5]
A = [[1, 1, 0, 0], [-1, 0, -5, 5], [2, 1, 1, -1], [-2, -1, -1, 1]]
b = [5, -10, 10, -10]
s = simplex(c, A, b)
print(s)


