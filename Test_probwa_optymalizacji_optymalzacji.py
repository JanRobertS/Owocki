import proba_optymalizacji_optymalizacji as Owocki

import numpy as np


from scipy.optimize import differential_evolution





# board = np.ones((5, 5), dtype=int)
# board[2, 3] = 2
# board[2, 2] = 2
# board[3, 2] = 2

# board[3, 3] = 5


# board[0, 2] = 3
# board[0, 3] = 3

# board[4, 2] = 4
# board[4, 3] = 4

# board[1, 2] = 5
# board[1, 3] = 5

# board[0, 0] = 6
# board[2, 0] = 6
# board[4, 0] = 6
# board[4, 1] = 6

# board[2, 1] = 4

# board[2, 4] = 5






# print(board)

# fruit = Fruits(board)

# fruit.search([0,0])
# fruit._gravity()

# print()

# print(fruit.board)


# print(board)

# print()


# board = np.ones((4, 4), dtype=int)
# board[0, 1] = 3
# board[0, 2] = 2
# board[1, 1] = 4
# board[1, 2] = 3
# board[1, 3] = 2
# board[2, 0] = 2
# board[2, 1] = 2
# board[3, 0] = 2
# board[3, 1] = 3
# board[3, 2] = 4
# board[3, 3] = 2


# --- generowanie stałych plansz (z ziarnem losowości) ---
def make_boards(num_boards=5, size=9, seeds=None):
    boards = []
    for i in range(num_boards):
        s = (seeds[i] if seeds is not None else i + 1234)
        rng = np.random.RandomState(s)
        b = rng.randint(1, 10, size=(size, size)).astype(np.int32)
        boards.append(b)
    return boards


# --- funkcja celu dla optymalizacji ---
def objective_de(x, boards):
    print("nowe parametry:",x)
    # x to [w_alone, w_duble, w_triple, w_unique_fruits]
    params = {
        'w_alone': x[0],
        'w_duble': x[1],
        'w_triple': x[2],
        'w_unique_fruits': x[3],
    }

    moves_counts = []
    for b in boards:
        b_copy = np.copy(b)
        resultat = []
        # Liczymy ruchy brute_force (możesz podmienić na find_optimal)
        l = Owocki.find_optimal_parm(b_copy, resultat, params, 1 , 10)
        moves_counts.append(l)

    mean_moves = float(np.mean(moves_counts))
    print(mean_moves)
    std_moves = float(np.std(moves_counts))

    # Możesz dodać karę za wariancję
    return mean_moves + 0.1 * std_moves

if __name__ == "__main__":

    # przygotujmy 10 plansz do "treningu"
    boards = make_boards(num_boards=5, size=5, seeds=[100+i for i in range(10)])

    # zakresy parametrów: (min,max) dla każdego
    bounds = [
        (0, 20),  # w_alone
        (0, 15),  # w_duble
        (0, 10),  # w_triple
        (-10, 10),   # w_unique_fruits
    ]

    result = differential_evolution(
        lambda x: objective_de(x, boards),
        bounds,
        maxiter=40,       # liczba iteracji
        popsize=15,       # rozmiar populacji
        polish=True,      # dodatkowy lokalny minimizer na końcu
        disp=True         # wypisuje postęp
    )

    print("\nNajlepsze parametry:", result.x)
    print("Najlepszy wynik (średnia ruchów):", result.fun)

    # Test na nowych planszach (walidacja)
    test_boards = make_boards(num_boards=5, size=8, seeds=[200+i for i in range(5)])
    val = objective_de(result.x, test_boards)
    print("Wynik na nowych planszach:", val)








#     plansza = np.array([
#     [3, 6, 7, 4, 4, 1],
#     [5, 9, 3, 3, 5, 4],
#     [2, 7, 8, 6, 8, 7],
#     [5, 9, 4, 2, 4, 3],
#     [8, 3, 9, 5, 5, 4],
#     [5, 8, 3, 4, 3, 9]
# ])


# #     plansza = np.array([
# #     [9, 1, 5, 2, 2, 5, 7, 6, 3],
# #     [4, 4, 6, 5, 4, 1, 4, 1, 3],
# #     [5, 9, 5, 8, 7, 6, 4, 3, 5],
# #     [3, 2, 8, 5, 2, 9, 8, 2, 9],
# #     [6, 1, 6, 2, 3, 8, 9, 8, 1],
# #     [6, 7, 4, 6, 6, 5, 3, 4, 1],
# #     [4, 5, 1, 1, 1, 5, 3, 9, 5],
# #     [3, 5, 4, 7, 6, 1, 9, 1, 9],
# #     [8, 1, 5, 1, 3, 6, 7, 5, 7]
# # ])

#     brute_forse_rezultat, brute_forse_turn= Owocki.brute_force(np.copy(plansza), [])

#     print("Greedy:", brute_forse_turn)
#     print(brute_forse_rezultat)
#     planszabf = np.copy(plansza)

#     rezultatbf = []
#     for xy in brute_forse_rezultat:
#         planszabf, finishbf, rezultatybf = Owocki.move(xy,planszabf,rezultatbf)
#         print("\nplansza:",planszabf,"\n rezultat:", rezultatybf)



#     step = 3
#     top = 3

#     print("\nStep:", step, "\nTop:", top)

#     rezultat = Owocki.find_optimal(np.copy(plansza), [], step, top)

#     rezultat1 = rezultat[1]

#     print("\nIlosc optymalna",len(rezultat[1]),"\n\n",rezultat1)

#     # f = optimalization.find_optimal(step= step, top = top)

#     # # f.print_resultat()
#     rezultaty = []
#     rezultat2 = [(np.int64(x), np.int64(y)) for x, y in rezultat1]
#     print(rezultat2)

#     plansza2 = np.copy(plansza)
    
#     for xy in rezultat2:
#         plansza2, finish, rezultaty = Owocki.move(xy,plansza2,rezultaty)
#         print("\nplansza:",plansza2,"\n rezultat:", rezultaty)

#     print(finish)