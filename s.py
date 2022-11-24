# %%
import numpy as np
import math
import sys
from datetime import datetime
inicio = datetime.now()

# %%
def lerProblema():
  aux = input()
  sAux = aux.split(" ", len(aux))
  n = int(sAux[0])
  m = int(sAux[1])

  aux = input()
  sAux = aux.split(" ", len(aux))

  c = []
  for i in range(len(sAux)):
    c.append(int(sAux[i]))

  A = np.zeros((n, m))
  b = []
  for i in range(n):
    aux = input()
    sAux = aux.split(" ", len(aux))
    b.append(int(sAux[-1]))
    for j in range(m):
      x = int(sAux[j])
      assert x <= 100
      A[i][j] = x
  return c, A, b

# %%
def criaTableau(c, A, b, x, y):
    tableau = np.zeros((x+1, y))
    v = np.identity(x)
    
    k = np.zeros((x))
    v = np.vstack([k, v])
    
    for i in range(y):
        tableau[0][i] = -c[i]

    for i in range(x):
        for j in range(y):
            tableau[i+1][j] = A[i][j]

    b = [0] + b
    bt = np.reshape(b,(x+1, 1))
    tableaufpi = np.concatenate((tableau, v), axis=1)
    tableaufpi = np.concatenate((tableaufpi, bt), axis=1)
    
    #for i in range(x):
    #    tableaufpi[i+1][y+x] = b[i]   
    
    return tableaufpi, v

# %%
def isOtima(tableau):
    z = tableau[0]
    for i in z[:-1]:
        if i < 0:
            return False
    return True

# %%
# Usando Regra de Bland
def pivotPosition(tableau):
    ilimitada = False
    inviavel = False

    z = tableau[0]
    for i in range(len(z)-1):
        if z[i] < 0:
            column = i
            break
    else:
        raise Exception("ERRO: Nao foi possivel encontar um valor na funcao Objetiva que permite a melhora!\n Favor Verificar o tableu e tentar novamente.")

    restricoes = []
    for eq in tableau[1:]:
        el = eq[column]
        #Possibilidade de inviabilidade
        if(eq[-1] < 0):
            if(all(h >= 0 for h in eq[:-1])):
                inviavel = True
        restricoes.append(math.inf if el <= 0 else eq[-1] / el)
    
    if(not(inviavel)):
        if all(x == math.inf for x in restricoes):
            ilimitada = True
    
    row = restricoes.index(min(restricoes))  
    return row+1, column, ilimitada, inviavel
    

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
            multiplierVero = (aux * np.array(novoVero[i])) 
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
    inviavel = False
    ilimitada = False

    tableau, vero = criaTableau(c, A, b, x, y)
    #print(isOtima(tableau))
    
    #print(tableau)
    #print(vero)

    while not(isOtima(tableau)):
        pivotRow, pivotCol, ilimitada, inviavel  = pivotPosition(tableau)
        if(ilimitada == True or inviavel == True):
            break
        pivot_position = pivotRow, pivotCol
        tableau, vero = eliminacaoGaussiana(tableau, pivot_position, vero)
        
        #print(np.matrix(tableau))
        #print(np.matrix(vero))

    #print(vero)
    if(inviavel == True):
        print("Inviavel")
        for i in vero[0]:
            print("%.7f" % i, end=" ")
    elif(ilimitada == True):
        sol =  get_solution(tableau)
        print("Ilimitada")
        for i in sol[0:y]:
            print("%.7f" % i, end=" ")
    else:   
        sol =  get_solution(tableau)
        print("Otima")
        print("%.7f" % tableau[0][-1])
        for i in sol[0:y]:
            print("%.7f" % i, end=" ")
        print("")
        for i in vero[0]:
            print("%.7f" % i, end=" ")

# %%

c, A, b = lerProblema()
simplex(c, A, b)

fim = datetime.now()
print("\nTempo total gasto: ", fim - inicio)