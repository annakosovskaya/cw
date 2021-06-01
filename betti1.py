import numpy as np
from numpy import linalg as la


# ввод вершин симплициального комплекса
def input_v():
    v_arr = []
    for i in range(int(input())):  # ввести число вершин
        vector = [int(x) for x in input().split()]  # ввести вершину через пробел без запятых
        v_arr.append(vector)
    return v_arr


# возвращает матрицу из вершин с индексами из index
def v_index(index):
    x = index[0]
    y = index[1]
    z = index[2]
    return np.array([v[x], v[y], v[z]])


# лежит ли ребро в симплексе
def subset(rib, triangle):
    return rib[0] in triangle and rib[1] in triangle


# подсчет ранга матрицы
def matrix_rank(A):
    line = 0  # счетчик номера строки
    col = 0  # счетчик номера столбца
    flag = False  # понадобится, чтобы выйти из цикла

    while line != len(A):
        line_new = line
        # будем искать строку с ненулевым элементом на месте col
        while A[line_new][col] == 0:
            line_new += 1
            # перебрали все строки, а ненулевой элемент так и не нашли
            if line_new == len(A):
                col += 1  # тогда перейдем к следующему столбцу
                if col == len(A[0]):
                    flag = True
                    break
                line_new = line  # перейдем к новой строке
        if flag:
            break
        # поднимем ту строку с ненулевым элементом
        A[[line, line_new]] = A[[line_new, line]]

        # на месте col во всех строках, кроме line, должны быть нули
        for i in range(len(A)):
            if A[i][col] != 0 and i != line:
                A[i] -= A[line]
        A %= 2  # вернем элементы в поле Z_2
        line += 1
        col += 1

    # посчитаем число ненулевых строк
    rank = len(A)
    for i in range(rank):
        if sum(A[i]) == 0:  # выкидываем нулевые строки из подсчета
            rank -= 1
    return rank


# множество вершин симплициального комплекса на (Z_2)^3
v_arr = [[0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0],
         [1, 0, 1], [1, 1, 0], [1, 1, 1]]

# ввод вершин: сначала ввести число вершин, потом вершины: в столбик, координаты через пробел
v_arr = input_v()

v = np.array(v_arr)
num_v = len(v_arr)

# всевозможные комбинации вершин (наборы индексов)
set_arr = [[x, y, z] for x in range(0, num_v)
           for y in range(1, num_v)
           for z in range(2, num_v) if x < y < z]

# симлпексы-треугольники
ind_triangles = []

for index in set_arr:
    mat = v_index(index)
    if la.det(mat) % 2 != 0:  # вершины образуют симплекс, если лнз
        ind_triangles.append(mat.tolist())

# симплексы-ребра
ribs = []

for i in range(num_v):
    for j in range(i + 1, num_v):
        ribs.append([v_arr[i], v_arr[j]])  # берем все ребра

# имена столбцов -- треугольники, строк -- ребра
matrix_B = np.zeros((len(ribs), len(ind_triangles)))

for i in range(len(ribs)):
    for j in range(len(ind_triangles)):
        # проверяем, лежит ли ребро в симплексе, и добавляем 0 или 1
        matrix_B[i][j] += subset(ribs[i], ind_triangles[j])

B = matrix_rank(matrix_B)

# имена столбцов -- ребра, строк -- вершины
matrix_Z = np.zeros((num_v, len(ribs)))
for i in range(num_v):
    for j in range(len(ribs)):
        ans = v_arr[i] in ribs[j]
        # элемент (i, j) равен 1, если вершина i лежит на ребре j, иначе 0
        matrix_Z[i][j] += ans

Z = len(ribs) - matrix_rank(matrix_Z)

b1 = Z - B
print(b1)
