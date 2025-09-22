## Gra 7x7 owocki

import numpy as np
from scipy import ndimage
from typing import List, Tuple
import copy

import time
import multiprocessing as mp



class Fruits: #symulacja gry w owoce
    def __init__(self, board: List[List[int]] = None, size: int = 7):

        #inicjalizacja planszy z ręki albo randomowa
        self.board = board
        if board is None:
            self.board = self._create_board(size)
        

        #wielkość planszy, która zawsze jest kwadratowa
        self.shape_board = self.board.shape
        
    
        self._family_fruit = [] #tablica z współrzędnymi sąsiadujących tych samych owoców tj. współrzędne spójnego komponentu

        self.resultat = [] # kroki podjęte do rozwiązania
        self.finished = False

        self.score = float("-inf")

    def _create_board(self, size) -> List[List[int]]: # Tworzenie random tablicy 
        return np.random.randint(1, 10, size=(size, size))
    
    
    def get_hash(self):
        return tuple(tuple(row) for row in self.board)
    
    def print_resultat(self):
        if self.finished:
            print("\nRozwiazana")
        else:
            print("\nNierozwiazana")

        if self.resultat:
            print("\nRezultat\n")
            for xy in self.resultat:
                print("x:", xy[0], "| y:", xy[1], "\n")
        else:
            print("\nPUSTA\n")

      
    def _search(self, xy: Tuple[int, int]): # algorytm rekurencyjny, szukający sąsiadujących spójnych komponentów 
        self._family_fruit.append([xy[0],xy[1]]) # dodanie do tablicy komponentu, który sprawdzamy w pierwszym kroku, a następnie tych samym komponentów, kóre przeszy warunki
        fruit = self.board[xy[0],xy[1]] # jaki owoc został wykryty na tym miejscu


        if fruit == 0: # warunek braku owocu
            return

        #współrzędne 
        x = xy[0]
        y = xy[1]

        #tablice pomocnicze 
        table = [] # tablica tymczasowa do trzymania współrzędnych, które są możliwymi spójnymi komponentami sąsiadującymi głównego komponentu
        table_of_fruit = [] # komponenty, które są spójnymi sąsiadami komponetu

        #warunki sąsiedztwa 
        if x != self.shape_board[0] - 1:
            table.append([x+1, y])
        if x != 0:
            table.append([x-1, y])
        if y != self.shape_board[1] - 1:
            table.append([x, y+1])
        if y != 0:
            table.append([x, y-1])

        # sprawdzenie czy sąsiad jest spójnym komponentem z głównym komponentem
        for place in table:
            if self.board[place[0], place[1]] == fruit and not(place in self._family_fruit):
                table_of_fruit.append(place)

        #rekurencja, jeśli punkt już nie znajduje się w tablicy to poszukaj sąsiadów od tego punktu
        for place in table_of_fruit:
            if not(place in self._family_fruit):
                self._search(place)
            
        return
    

    def search_component(self, xy):
        fruit_type = self.board[xy[0], xy[1]]
        if fruit_type == 0:
            return []
        
        mask = self.board == fruit_type
        labeled, _ = ndimage.label(mask)
        label_id = labeled[xy[0], xy[1]]
        if label_id == 0:
            return []

        coords = np.argwhere(labeled == label_id)

        self._family_fruit.append(coords)

        self._family_fruit = self._family_fruit[0].tolist()
    
    def search_neighbors(self, xy: Tuple[int, int]):
        self.search_component(xy)
        neighbors = self._family_fruit
        self._clear_family_fruit()

        return neighbors


    def _pop_fruits(self): #nieużywane
        while self._family_fruit:
            xy = self._family_fruit.pop(0) 
            self.board[xy[0]][xy[1]] = 0

    def _gravity(self): # funkcja, która usuwa całe spójne komponenty i niepuste komponenty spadają grawitacyjnie
        while self._family_fruit: #dopóki tablica ze spójnymi komponentami nie jest pusta
            row, col = self._family_fruit.pop(0) #rząd i kolumna aktualnie sprawdzana i usuwana z tablicy spójnych komponentów 

            # print("row:",row,"\ncol:",col) #CLEAR
            
            self.board[row, col] = 0 #czyszczenie owocu 
            
            # jeśli nie jest na samym dole to przesuń grawitacyjnie w dół wszystko powyżej i na samej górze wyczyść
            if row > 0: 
                self.board[1:row+1, col] = self.board[0:row, col]
                self.board[0, col] = 0

            # print() #CLEAR
            # print(self.board) #CLEAR

    def _sort_family_fruit(self): # sortowanie tablicy po y, x, aby uniknąć błędów z gravity 
        self._family_fruit = sorted(self._family_fruit , key=lambda k: [k[1], k[0]])
            

    def _clear_family_fruit(self): #czyszczenie tablicy _family_fruit
        self._family_fruit = []

    def is_empty(self):
        if np.all(self.board == 0):
            return True
        else:
            return False

    def game_finished(self):
        if self.is_empty():
            self.finished = True
        else:
            self.finished = False


    def move(self, xy: Tuple[int, int]): # "kliknięcie" czyli ruch w grze
        if self.board[xy[0]][xy[1]] != 0:
            self.resultat.append(xy) #dodawanie ruchów wykonanych na planszy

            self.search_component(xy) #poszukanie sąsiadujących spójnych komponetów od kliknięcia

            # print() #CLEAR
            # print(self._family_fruit) #CLEAR
            # print() #CLEAR
            
            self._sort_family_fruit() # posortowanie listy spójnych komponentów 

            # print() #CLEAR
            # print(self._family_fruit) #CLEAR
            # print() #CLEAR

            self._gravity() # usunięcie spójnego komponentu i zadziałanie grawitacyjne

            self.game_finished()

            #self._clear_family_fruit() # czyszczenie listy ze spójnymi komponentami

    def clear_table_amount_neighbors(self): #czyszczenie tablicy table_amount_neighbors
        self.table_amount_neighbors = np.zeros(self.shape_board)

        self.table_unique_amount_neighbors = np.zeros(self.shape_board)


    # def search_all_board(self): # wyszukiwanie największego kompozytu na planszy
    #     self.clear_table_amount_neighbors() # czyszczenie tablicy z ilością sąsiadów dla danego kompozytu

    #     i = 0

    #     for x in range(0,self.shape_board[0]): # przechodzimy po x 
    #         for y in range(0,self.shape_board[1]): # przechodzimy po y
    #             if self.table_amount_neighbors[x][y] == 0 and self.board[x][y] != 0: # sprawdzanie czy już to miejsce nie jest zapisane i czy nie jest puste 


    #                 self._search([x,y]) #  

    #                 # zapisywanie do wszyskich elementów tego sprawdzanego kompozytu liczbę ich spójnych sąsiadów 
    #                 for xy in self._family_fruit:
    #                     self.table_amount_neighbors[xy[0]][xy[1]] = len(self._family_fruit)

    #                     self.table_unique_amount_neighbors[xy[0]][xy[1]] = 1000* len(self._family_fruit) + i

    #                 i+=1
    #                 self._clear_family_fruit() #czyszczenie tablicy z spójnymi sąsiadami
    #     # return table_amount_neighbors

    
    def search_all_board(self):
        self.clear_table_amount_neighbors()  # czyszczenie tablic pomocniczych
        
        i = 0
        # przechodzimy po wszystkich typach owoców (1,2,3,...)
        for fruit_type in np.unique(self.board):
            if fruit_type == 0:
                continue  # pomijamy puste pola

            # maska tylko dla jednego typu owocu
            mask = self.board == fruit_type  

            # etykietowanie spójnych komponentów
            labeled, num_features = ndimage.label(mask)

            # dla każdego znalezionego komponentu
            for label_id in range(1, num_features + 1):
                coords = np.argwhere(labeled == label_id)  # wszystkie pola w tym komponencie
                size = len(coords)

                for x, y in coords:
                    self.table_amount_neighbors[x][y] = size
                    self.table_unique_amount_neighbors[x][y] = 1000 * size + i

                i += 1




visited = {}

def process_board(args):
    if len(visited) > 1_000_000:
        print("visited przekroczyło 1_000_000")
        visited.clear()
    board, res, self_obj = args
    results = []
    moves = self_obj.all_moves(Fruits(board))
    for move in moves:
        f = Fruits(np.copy(board))
        f.resultat = copy.deepcopy(res) #zmiana z deeap
        f.move(move)

        # results.append((f.board, f.resultat))
        # if f.finished:
        #     return f

        h = hash(f.board.tobytes())
        if not(h in visited):
            results.append((f.board, f.resultat))
            if f.finished:
                return f
            visited[h] = True
            
    return results

def score_board(args):
    board, res, self_obj = args
    fruit = Fruits(board)
    score = self_obj.heurystyka(fruit)
    return score



class Optimalization: # Algorytm optymializujący grę w owoce
    def __init__(self, board: List[List[int]]):
        self.board = np.copy(board) # zapis analizowane planszy

        self.best_fruit = None # najlepszy obiekt z rozwiązaniem dotychczas

        # self.clear_table_amount_neighbors() 

        self.brute_force_turn = self.brute_force(self.board) # liczba ruchów dla algorytmu BruteForse

        self.cache = {}



    # def clear_table_amount_neighbors(self): #czyszczenie tablicy table_amount_neighbors
    #     self.table_amount_neighbors = np.zeros(self.shape_board)

    # def _LB_components(self, LB_components_fruit: Fruits) -> int: # zapisanie LB_components czyli liczba_spójnych_komponentów — trzeba co najmniej tyle kliknięć (przynajmniej na pierwszy rzut oka).
    #     LB_components = LB_components_fruit.LB_components # zapis LB_components

    #     return LB_components # retun LB_components
    
    # def _LB_size(self, board: List[List[int]]):# LB_size = ceil( liczba_nie-pustych_komórek / max_rozmiar_komponentu ) — każdy ruch usuwa ≤ max_rozmiar_komponentu komórek, więc potrzebujesz co najmniej tyle ruchów.
    #     fruit = Fruits(board)

    #     self.search_all_board(fruit)
    #     LB_size = np.ceil(np.count_nonzero(fruit.board) / np.argmax(self.table_amount_neighbors))

    #     del fruit
    #     return LB_size


    # def search_all_board(self, fruit: Fruits, LB: bool = False): # wyszukiwanie największego kompozytu na planszy
    #     self.clear_table_amount_neighbors() # czyszczenie tablicy z ilością sąsiadów dla danego kompozytu

    #     if LB:
    #         fruit.LB_components = 0 # zerowanie liczba_spójnych_komponentów — trzeba co najmniej tyle kliknięć (przynajmniej na pierwszy rzut oka).

    #     for x in range(0,self.shape_board[0]): # przechodzimy po x 
    #         for y in range(0,self.shape_board[1]): # przechodzimy po y
    #             if self.table_amount_neighbors[x][y] == 0 and fruit.board[x][y] != 0: # sprawdzanie czy już to miejsce nie jest zapisane i czy nie jest puste 

    #                 if LB:
    #                     fruit.LB_components += 1 # zliczanie liczba_spójnych_komponentów — trzeba co najmniej tyle kliknięć (przynajmniej na pierwszy rzut oka).

    #                 fruit._search([x,y]) # 
    #                 self.table_amount_neighbors[x][y] = len(fruit._family_fruit) # zapisywanie ile jest taodwołanie się do funkcji która szuka wszystkich spójnych sąsiadówki samych elementów w tym kompozycie 

    #                 # zapisywanie do wszyskich elementów tego sprawdzanego kompozytu liczbę ich spójnych sąsiadów 
    #                 for xy in fruit._family_fruit:
    #                     self.table_amount_neighbors[xy[0]][xy[1]] = len(fruit._family_fruit)

    #                 fruit._clear_family_fruit() #czyszczenie tablicy z spójnymi sąsiadami

    def best_move_brute_forse(self, fruit: Fruits):
        fruit.search_all_board() # wyszukanie ilości sąsiadów danych kompozytów
        xy = np.unravel_index(np.argmax(fruit.table_amount_neighbors), fruit.shape_board) # największy kompozyt (czli z największa ilością sąsiadów) [pierwszy największy]
        
        return xy


    def brute_force(self, board: List[List[int]]) -> int: #algorytm BruteForce, który "klika" zawsze największe elementy kompozytu
        self.brute_fruit = Fruits(np.copy(board)) # tworzenie nowego obiektu dla rozwiązania BruteForce

        while np.max(self.brute_fruit.board) != 0: # warunek niepustej planszy

            self.brute_fruit.search_all_board() # wyszukanie ilości sąsiadów danych kompozytów

            xy = np.unravel_index(np.argmax(self.brute_fruit.table_amount_neighbors), self.brute_fruit.shape_board) # największy kompozyt (czli z największa ilością sąsiadów) [pierwszy największy]
            self.brute_fruit.move(xy) # wywołanie ruchu dla największego kompozytu

            # print(self.brute_fruit.board) #CLEAR

        return len(self.brute_fruit.resultat) # zwraca ilośc tur dla BruteForce
    

    def heurystyka(self, fruit: Fruits):
        # if len(self.cache) > 1_000_000:
        #     self.cache.clear()
        # h = hash(fruit.board.tobytes())
        # if h in self.cache:
        #     return self.cache[h]
        
        w_alone = 20
        w_duble = 5
        w_triple = 2

        w_unique_fruits = 3

        fruit.search_all_board()

        unique_fruits = len(np.unique(fruit.board - 1))

        fruit.score = -w_alone* np.sum(fruit.table_amount_neighbors == 1) -w_duble * np.sum(fruit.table_amount_neighbors == 2)/2 -w_triple * np.sum(fruit.table_amount_neighbors == 3)/3 + np.sum(fruit.table_amount_neighbors > 3)/2 -w_unique_fruits * unique_fruits 
        # self.cache[h] = fruit.score

        return fruit.score

    # def find_optimal(self, step: int = 5, top: int = 5):

    #     fruit = Fruits(np.copy(self.board))
    #     fruits = [(fruit.board,fruit.resultat)]
            


    #     i = 0
    #     j = 0 
    #     if i >= 1:
    #         j=i
            
    #     while True:
    #         print("Iteracja:",i)

    #         start = time.time()

    #         for _ in range(0, step+j*3):
    #             fruits2 = []
    #             for board, res in fruits:
    #                 moves = self.all_moves(Fruits(np.copy(board)))
                    
    #                 for move in moves:
    #                     f = Fruits(np.copy(board))
    #                     f.resultat = copy.deepcopy(res)
    #                     f.move(move)
    #                     fruits2.append((f.board,f.resultat))

    #                     # print(f.finished)
    #                     if f.finished:
    #                         return f
    #                 moves = []

    #             fruits = fruits2
    #             fruits2 = []

    #         tabel_score = []
    #         for board, res in fruits:
    #             tabel_score.append(self.heurystyka(Fruits(np.copy(board))))

    #         # print(tabel_score)
    #         top5_index =  np.argpartition(np.array(tabel_score), -top)[-top:]

    #         tabel_score = []

    #         for index in top5_index:
    #             new_fruits = []
    #             new_fruits.append(fruits[index])
            
    #         fruits = []

    #         top5_index = []

    #         fruits = new_fruits
    #         new_fruits = []
        
            
    #         end = time.time()

    #         print(i," Iteracja trwala:", end - start, "sekund")
    #         i += 1


 # Funkcja pomocnicza MUSI być na górnym poziomie


    def find_optimal(self, step: int = 5, top: int = 5):

        fruit = Fruits(np.copy(self.board))
        fruits = [(fruit.board, fruit.resultat)]

        i = 0
        j=0


        pool = mp.Pool(processes=mp.cpu_count())

        while True:

            if i>5:
                j=+1

            print("Iteracja:", i)
            start = time.time()

            for _ in range(0, step + j):
                results = pool.map(process_board, [(board, res, self) for board, res in fruits])

                fruits2 = []
                for r in results:
                    if isinstance(r, Fruits):
                        return r
                    else:
                        fruits2.extend(r)

                fruits = fruits2
                fruits2 = []

            tabel_score = []

            # for board, res in fruits:
            #     tabel_score.append(self.heurystyka(Fruits(np.copy(board))))

            # top5_index = np.argpartition(np.array(tabel_score), -top)[-top:]

            # new_fruits = []
            # for index in top5_index:
            #     new_fruits.append(fruits[index])

            tabel_score = pool.map(score_board, [(board, res, self) for board, res in fruits])

            tabel_score = np.array(tabel_score)
            top5_index = np.argpartition(tabel_score, -top)[-top:]

            new_fruits = [fruits[index] for index in top5_index]
            fruits = new_fruits

            end = time.time()
            print(i, " Iteracja trwała:", end - start, "sekund")
            i += 1



    def all_moves(self, fruit: Fruits):

        fruit.search_all_board()

        unique_values = np.unique(fruit.table_unique_amount_neighbors)

        moves = []

        for values in unique_values:
            moves.append([np.where(fruit.table_unique_amount_neighbors == values)[0][0],np.where(fruit.table_unique_amount_neighbors == values)[1][0]])

        return moves






























    """Moj kod niedzialajacy

    def dfs(self, fruit: Fruits, depth, limit, visited): # algorytm do wyszukania najlepszego rozwiązania 

        if fruit.is_empty():   
            return True, fruit
        
        lb = self._LB_size(fruit.board)

        if depth + lb > limit:
            return False, None
        
        h = fruit.get_hash()
        if visited.get(h, float("inf")) <= depth:
            return False, None
        visited[h] = depth

        self.search_all_board(fruit)
        seen = np.zeros(self.shape_board, dtype=bool)
        moves = []

        for x in range(0, self.shape_board[0]):
            for y in range(0, self.shape_board[1]):
                if self.table_amount_neighbors[x,y] > 0 and seen[x,y] == False:
                    fruit._search((x,y))

        
        pass


    def solve_IDA(self, board: List[List[int]]): # całość rozwiązania dla algorytmu IDA*
        best = self.brute_force_turn
        self.best_fruit = self.brute_fruit

        for limit in range(self._LB_size(board), best):
            visited = {}
            best_decision, best_fruit = self.dfs(board,0,limit,visited)
            if best_decision:
                best = limit
                self.best_fruit = best_fruit
                return best, self.best_fruit

        return best, self.best_fruit




    def LB(self, board): #dolne ograniczenia (lower bounds) #nieużywane
        # LB_components = liczba_spójnych_komponentów — trzeba co najmniej tyle kliknięć (przynajmniej na pierwszy rzut oka).
        # LB_size = ceil( liczba_nie-pustych_komórek / max_rozmiar_komponentu ) — każdy ruch usuwa ≤ max_rozmiar_komponentu komórek, więc potrzebujesz co najmniej tyle ruchów.
        fruit_LB = Fruits(board)
        self.search_all_board(fruit_LB, LB = True) # wyszukanie wszystkich componentów
        LB_components = self._LB_components(fruit_LB)
        LB_size = self._LB_size(fruit_LB)

        del fruit_LB

        LB = max(LB_components, LB_size)

        return LB

    """

