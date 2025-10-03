import numpy as np
from scipy import ndimage
from typing import List, Tuple
import copy

import time
import multiprocessing as mp

from numba import njit
import zlib




def _create_board(size): # Tworzenie random tablicy 
    return np.random.randint(1, 10, size=(size, size))



def print_resultat(_finished,_resultat ):
    if _finished:
        print("\nRozwiazana")
    else:
        print("\nNierozwiazana")

    if _resultat:
        print("\nRezultat\n")
        for xy in _resultat:
            print("x:", xy[0], "| y:", xy[1], "\n")
    else:
        print("\nPUSTA\n")



# def _search(_xy, _family_fruit, _board, _shape_board): # algorytm rekurencyjny, szukający sąsiadujących spójnych komponentów 
#     _family_fruit.append([_xy[0],_xy[1]]) # dodanie do tablicy komponentu, który sprawdzamy w pierwszym kroku, a następnie tych samym komponentów, kóre przeszy warunki
#     fruit = _board[_xy[0],_xy[1]] # jaki owoc został wykryty na tym miejscu


#     if fruit == 0: # warunek braku owocu
#         return

#     #współrzędne 
#     x = _xy[0]
#     y = _xy[1]

#     #tablice pomocnicze 
#     table = [] # tablica tymczasowa do trzymania współrzędnych, które są możliwymi spójnymi komponentami sąsiadującymi głównego komponentu
#     table_of_fruit = [] # komponenty, które są spójnymi sąsiadami komponetu

#     #warunki sąsiedztwa 
#     if x != _shape_board[0] - 1:
#         table.append([x+1, y])
#     if x != 0:
#         table.append([x-1, y])
#     if y != _shape_board[1] - 1:
#         table.append([x, y+1])
#     if y != 0:
#         table.append([x, y-1])

#     # sprawdzenie czy sąsiad jest spójnym komponentem z głównym komponentem
#     for place in table:
#         if _board[place[0], place[1]] == fruit and not(place in _family_fruit):
#             table_of_fruit.append(place)

#     #rekurencja, jeśli punkt już nie znajduje się w tablicy to poszukaj sąsiadów od tego punktu
#     for place in table_of_fruit:
#         if not(place in _family_fruit):
#             _search(place)
        
#     return


def search_component(_xy, _board):
    fruit_type = _board[_xy[0], _xy[1]]
    if fruit_type == 0:
        return []
    
    mask = _board == fruit_type
    labeled, _ = ndimage.label(mask)
    label_id = labeled[_xy[0], _xy[1]]
    if label_id == 0:
        return []

    coords = np.argwhere(labeled == label_id)

    # _family_fruit.append(coords)

    # _family_fruit = _family_fruit[0].tolist()

    # return _family_fruit

    return coords.tolist()


    
def search_neighbors(_xy,_board,_family_fruit):
    _family_fruit = search_component(_xy,_board)
    neighbors = _family_fruit
    _family_fruit = []

    return neighbors, _family_fruit

def _pop_fruits(_board, _family_fruit): #nieużywane
    while _family_fruit:
        xy = _family_fruit.pop(0) 
        _board[xy[0]][xy[1]] = 0
    return _board



def _gravity(_family_fruit, _board): # funkcja, która usuwa całe spójne komponenty i niepuste komponenty spadają grawitacyjnie
    while _family_fruit: #dopóki tablica ze spójnymi komponentami nie jest pusta
        row, col = _family_fruit.pop(0) #rząd i kolumna aktualnie sprawdzana i usuwana z tablicy spójnych komponentów 

        # print("row:",row,"\ncol:",col) #CLEAR
        
        _board[row, col] = 0 #czyszczenie owocu 
        
        # jeśli nie jest na samym dole to przesuń grawitacyjnie w dół wszystko powyżej i na samej górze wyczyść
        if row > 0: 
            _board[1:row+1, col] = _board[0:row, col]
            _board[0, col] = 0

        # print() #CLEAR
        # print(self.board) #CLEAR
    return _board


@njit
def gravity_numba(family_fruit, board):
    for i in range(family_fruit.shape[0]):
        row = family_fruit[i, 0]
        col = family_fruit[i, 1]
        board[row, col] = 0
        if row > 0:
            for r in range(row, 0, -1):
                board[r, col] = board[r-1, col]
            board[0, col] = 0
    return board

# @njit
# def gravity_numba(family_fruit, board):
#     # np.lexsort nie działa w Numba, ale można ręcznie posortować
#     # prosty bubble sort lub insertion sort dla małych komponentów
#     n = family_fruit.shape[0]
#     for i in range(1, n):
#         key_row, key_col = family_fruit[i,0], family_fruit[i,1]
#         j = i - 1
#         while j >=0 and (family_fruit[j,1] > key_col or (family_fruit[j,1] == key_col and family_fruit[j,0] > key_row)):
#             family_fruit[j+1] = family_fruit[j]
#             j -= 1
#         family_fruit[j+1,0] = key_row
#         family_fruit[j+1,1] = key_col

#     # dalej standardowa grawitacja
#     for i in range(n):
#         row = family_fruit[i, 0]
#         col = family_fruit[i, 1]
#         board[row, col] = 0
#         if row > 0:
#             for r in range(row, 0, -1):
#                 board[r, col] = board[r-1, col]
#             board[0, col] = 0
#     return board


def is_empty(_board):
    if np.all(_board == 0):
        return True
    else:
        return False

def game_finished(_board):
    if is_empty(_board):
        _finished = True
    else:
        _finished = False

    return _finished

def move(xy, _board, _resultat): # "kliknięcie" czyli ruch w grze
    if _board[xy[0]][xy[1]] != 0:
        _resultat.append(xy) #dodawanie ruchów wykonanych na planszy

        _family_fruit = search_component(xy,_board) #poszukanie sąsiadujących spójnych komponetów od kliknięcia

        # print() #CLEAR
        # print(self._family_fruit) #CLEAR
        # print() #CLEAR
        
        _family_fruit = sorted(_family_fruit , key=lambda k: [k[1], k[0]]) # posortowanie listy spójnych komponentów 

        # print() #CLEAR
        # print(self._family_fruit) #CLEAR
        # print() #CLEAR
        family_fruit_array = np.array(_family_fruit, dtype=np.int32)
        _board = gravity_numba(family_fruit_array,_board) # usunięcie spójnego komponentu i zadziałanie grawitacyjne


        #self._clear_family_fruit() # czyszczenie listy ze spójnymi komponentami
    return _board, game_finished(_board), _resultat


def search_all_board(_board):
    _table_amount_neighbors = np.zeros_like(_board, dtype=np.int16)
    _table_unique_amount_neighbors = np.zeros_like(_board, dtype=np.int32)
    
    i = 0
    # przechodzimy po wszystkich typach owoców (1,2,3,...)
    for fruit_type in np.unique(_board):
        if fruit_type == 0:
            continue  # pomijamy puste pola

        # maska tylko dla jednego typu owocu
        mask = _board == fruit_type  

        # etykietowanie spójnych komponentów
        labeled, num_features = ndimage.label(mask)

        # dla każdego znalezionego komponentu
        for label_id in range(1, num_features + 1):
            coords = np.argwhere(labeled == label_id)  # wszystkie pola w tym komponencie
            size = len(coords)

            for x, y in coords:
                _table_amount_neighbors[x][y] = size
                _table_unique_amount_neighbors[x][y] = 1000 * size + i

            i += 1
    return _table_amount_neighbors, _table_unique_amount_neighbors


@njit
def search_all_board_numba(board):
    n, m = board.shape
    table_amount_neighbors = np.zeros_like(board, dtype=np.int16)
    visited = np.zeros_like(board, dtype=np.bool_)

    for i in range(n):
        for j in range(m):
            if board[i,j] != 0 and not visited[i,j]:
                fruit = board[i,j]
                stack = [(i,j)]
                coords = []

                while stack:
                    x, y = stack.pop()
                    if visited[x, y]:
                        continue
                    visited[x, y] = True
                    coords.append((x,y))

                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < n and 0 <= ny < m:
                            if board[nx, ny] == fruit and not visited[nx, ny]:
                                stack.append((nx, ny))

                size = len(coords)
                for x, y in coords:
                    table_amount_neighbors[x, y] = size

    return table_amount_neighbors



visited = {}




def all_moves(_board):

    _table_amount_neighbors, _table_unique_amount_neighbors = search_all_board(_board)

    unique_values = np.unique(_table_unique_amount_neighbors)

    moves = []

    # for values in unique_values:
    #     moves.append([np.where(_table_unique_amount_neighbors == values)[0][0],np.where(_table_unique_amount_neighbors == values)[1][0]])

    indices = np.argwhere(_table_unique_amount_neighbors > 0)
    unique_labels = _table_unique_amount_neighbors[indices[:,0], indices[:,1]]
    _, idx = np.unique(unique_labels, return_index=True)
    moves = indices[idx].tolist()

    return moves



# def process_board(_board, _resultat):

#     print("Board:", _board ," resultat:",_resultat)
#     if len(visited) > 1_000_000:
#         print("visited przekroczyło 1_000_000")
#         visited.clear()
#     fruits = []

#     moves = all_moves(_board)
#     for mo in moves:
#         _board_copy = np.copy(_board)
#         _resultat_copy = copy.deepcopy(_resultat)
#         _board_new, _finished, _resultat_copy = move(mo, _board_copy, _resultat_copy)

#         # results.append((f.board, f.resultat))
#         # if f.finished:
#         #     return f

#         h = hash(_board_new.tobytes())
#         if h not in visited:
#             fruits.append((_board_new, _resultat_copy))
#             visited[h] = True
#             if _finished:
#                 return [_board_new, _resultat_copy], _finished
#     return fruits, _finished


def process_board(_board, _resultat):
    # print("Board:", _board ," resultat:",_resultat)

    fruits = []
    finished = False

    moves = all_moves(_board)
    for mo in moves:
        _board_copy = np.copy(_board)
        _resultat_copy = _resultat.copy()
        _board_new, _finished, _resultat_copy = move(mo, _board_copy, _resultat_copy)

        h = zlib.crc32(_board_new.tobytes())
        if h not in visited:
            fruits.append((_board_new, _resultat_copy))
            visited[h] = True
            if _finished:
                finished = True
                return [(_board_new, _resultat_copy)], finished  # Zawsze zwracamy listę

    return fruits, finished  # Zawsze tuple (lista, finished)


def process_board_parm(_board, _resultat):
    # print("Board:", _board ," resultat:",_resultat)

    fruits = []
    finished = False

    moves = all_moves(_board)
    for mo in moves:
        _board_copy = np.copy(_board)
        _resultat_copy = _resultat.copy()
        _board_new, _finished, _resultat_copy = move(mo, _board_copy, _resultat_copy)

        h = zlib.crc32(_board_new.tobytes())
        if h not in visited:
            fruits.append((_board_new, _resultat_copy))
            visited[h] = True
            if _finished:
                finished = True
                return _resultat_copy, finished  # Zawsze zwracamy listę

    return fruits, finished  # Zawsze tuple (lista, finished)

def heurystyka(_board):
    # if len(self.cache) > 1_000_000:
    #     self.cache.clear()
    # h = hash(fruit.board.tobytes())
    # if h in self.cache:
    #     return self.cache[h]
    
    w_alone = 8
    w_duble = 5
    w_triple = 1

    w_unique_fruits = 1/7

    _table_amount_neighbors = search_all_board_numba(_board)

    unique_fruits = len(np.unique(_board[_board > 0]))

    _score = -w_alone* np.sum(_table_amount_neighbors == 1) -w_duble * np.sum(_table_amount_neighbors == 2)/2 
    -w_triple * np.sum(_table_amount_neighbors == 3)/3 + np.sum(_table_amount_neighbors > 3)/20 
    -w_unique_fruits * unique_fruits 
    # self.cache[h] = fruit.score

    return _score

def heurystyka_parm(_board, parm):
    # if len(self.cache) > 1_000_000:
    #     self.cache.clear()
    # h = hash(fruit.board.tobytes())
    # if h in self.cache:
    #     return self.cache[h]


    
    w_alone = parm.get('w_alone', 8.0)
    w_duble = parm.get('w_duble', 5.0)
    w_triple = parm.get('w_triple', 1.0)

    w_unique_fruits = parm.get('w_unique_fruits', (1/7))

    _table_amount_neighbors = search_all_board_numba(_board)

    unique_fruits = len(np.unique(_board[_board > 0]))

    _score = -w_alone* np.sum(_table_amount_neighbors == 1) -w_duble * np.sum(_table_amount_neighbors == 2)/2 
    -w_triple * np.sum(_table_amount_neighbors == 3)/3 + np.sum(_table_amount_neighbors > 3)/20 
    -w_unique_fruits * unique_fruits 
    # self.cache[h] = fruit.score

    return _score




def score_board(_board):
    score = heurystyka(_board)
    return score

def score_board_parm(_board, parm):
    score = heurystyka_parm(_board, parm)
    return score




def best_move_brute_forse(_board):
    _table_amount_neighbors = search_all_board_numba(_board) # wyszukanie ilości sąsiadów danych kompozytów
    xy = np.unravel_index(np.argmax(_table_amount_neighbors), _board.shape) # największy kompozyt (czli z największa ilością sąsiadów) [pierwszy największy]
    return xy


def brute_force(_board, _resultat): #algorytm BruteForce, który "klika" zawsze największe elementy kompozytu

    while np.max(_board) != 0: # warunek niepustej planszy

        _table_amount_neighbors = search_all_board_numba(_board) # wyszukanie ilości sąsiadów danych kompozytów

        _xy = np.unravel_index(np.argmax(_table_amount_neighbors), _board.shape) # największy kompozyt (czli z największa ilością sąsiadów) [pierwszy największy]
        _board, _finished, _resultat = move(_xy,_board,_resultat) # wywołanie ruchu dla największego kompozytu

        # print(self.brute_fruit.board) #CLEAR

    return _resultat, len(_resultat)

def find_optimal_worker(_board, _resultat, step, top, queue):
    _fruits = [(_board, _resultat)]
    _i = 0
    _j = 0
    _k = 0

    _pool = mp.Pool(processes=mp.cpu_count()-3)
    _finished = False

    while not _finished:
        if _i > 5:
            _j = 1

        _start = time.time()

        # Rozwijamy wszystkie możliwe plansze przez kilka kroków
        for _ in range(step + _j):
            _k+=1
            res_list = _pool.starmap(process_board, [(_b, _r) for _b, _r in _fruits])

            _fruits2 = []

            for fruits_chunk, _finished in res_list:
                if _finished:
                    queue.put(("DONE", fruits_chunk[0]))
                    _pool.close()
                    _pool.join()
                    return

                _fruits2.extend(fruits_chunk)

            _fruits = _fruits2
            queue.put((None,_k))

        # Liczymy oceny dla wszystkich plansz
        _tabel_score = _pool.map(score_board, [_b for _b, _ in _fruits])
        _tabel_score = np.array(_tabel_score)
        a = len(_tabel_score)
        if (top - a) > 0 :
            top = len(_tabel_score)
        _top_index = np.argpartition(_tabel_score, -top)[-top:]

        # Zachowujemy tylko najlepsze plansze
        _fruits = [_fruits[_idx] for _idx in _top_index]

        _end = time.time()
        # generator oddaje aktualny stan
        _i += 1


def find_optimal_parm(_board, _resultat, parm, step: int = 5, top: int = 5):
    _fruits = [(_board, _resultat)]
    _i = 0
    _j = 0

    _pool = mp.Pool(processes=mp.cpu_count()-2)
    finished = False

    while not finished:
        # if _i > 9:
        #     _j = 2 
        # elif _i > 5:
        #     _j = 1

        if _i > 5:
            _j = 1 

        # Rozwijamy wszystkie możliwe plansze przez kilka kroków
        for _ in range(step + _j):
            res_list = _pool.starmap(process_board_parm, [(_b, _r) for _b, _r in _fruits])

            # if _i < 2:
            #     print(res_list)
                
            _fruits2 = []
            finished = False

            for fruits_chunk, _finished in res_list:
                if _finished:
                    finished = True
                    return len(fruits_chunk)  # gotowe rozwiązanie
                _fruits2.extend(fruits_chunk)

            _fruits = _fruits2


        # Liczymy oceny dla wszystkich plansz
        _tabel_score = _pool.starmap(score_board_parm, [(_b, parm) for _b, _ in _fruits])

        _tabel_score = np.array(_tabel_score)

        a = len(_tabel_score)
        if (top - a) > 0 :
            top = len(_tabel_score)

        _top5_index = np.argpartition(_tabel_score, -top)[-top:]

        # Zachowujemy tylko najlepsze plansze
        _fruits = [_fruits[_idx] for _idx in _top5_index]

        _i += 1




    
    

def find_optimal(_board, _resultat, step: int = 5, top: int = 5):
    _fruits = [(_board, _resultat)]
    _i = 0
    _j = 0

    _pool = mp.Pool(processes=mp.cpu_count())
    finished = False

    while not finished:
        # if _i > 9:
        #     _j = 2 
        # elif _i > 5:
        #     _j = 1

        if _i > 5:
            _j = 1 

        _start = time.time()

        # Rozwijamy wszystkie możliwe plansze przez kilka kroków
        for _ in range(step + _j):
            res_list = _pool.starmap(process_board, [(_b, _r) for _b, _r in _fruits])

            # if _i < 2:
            #     print(res_list)
                
            _fruits2 = []
            finished = False

            for fruits_chunk, _finished in res_list:
                if _finished:
                    finished = True
                    return fruits_chunk[0]  # gotowe rozwiązanie
                _fruits2.extend(fruits_chunk)

            _fruits = _fruits2


        # Liczymy oceny dla wszystkich plansz
        _tabel_score = _pool.map(score_board, [_b for _b, _ in _fruits])

        _tabel_score = np.array(_tabel_score)
        _top5_index = np.argpartition(_tabel_score, -top)[-top:]

        # Zachowujemy tylko najlepsze plansze
        _fruits = [_fruits[_idx] for _idx in _top5_index]

        _end = time.time()
        print(_i, " Iteracja trwała:", round(_end - _start, 2), "sekund")
        _i += 1



