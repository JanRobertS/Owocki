import proba_optymalizacji_optymalizacji as Owocki
import numpy as np
from scipy.optimize import differential_evolution
import os

SAVE_FILE = "checkpoint_pop.npz"
FINAL_FILE = "wynik_ostateczny.npz"

# --- generowanie stałych plansz (z ziarnem losowości) ---
def make_boards(num_boards=10, size=9, seeds=None):
    boards = []
    for i in range(num_boards):
        s = (seeds[i] if seeds is not None else i + 1234)
        rng = np.random.RandomState(s)
        b = rng.randint(1, 10, size=(size, size)).astype(np.int32)
        boards.append(b)
    return boards

# --- funkcja celu dla optymalizacji ---
def objective_de(x, boards):
    print("nowe parametry:", x)
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
        l = Owocki.find_optimal_parm(b_copy, resultat, params, 1, 100)
        moves_counts.append(l)

    mean_moves = float(np.mean(moves_counts))
    std_moves = float(np.std(moves_counts))

    return mean_moves + 0.1 * std_moves

# --- callback zapisujący populację co iterację ---
def save_checkpoint(xk, convergence):
    if last_result is not None:
        pop = last_result.population
        np.savez(SAVE_FILE, pop=pop)
        print(f"✔ Zapisano checkpoint (populacja {pop.shape})")
    return False  # kontynuuj optymalizację

if __name__ == "__main__":

    boards = make_boards(num_boards=5, size=5, seeds=[100+i for i in range(10)])

    bounds = [
        (0, 20),   # w_alone
        (0, 15),   # w_duble
        (0, 10),   # w_triple
        (-10, 10), # w_unique_fruits
    ]

    # wczytaj checkpoint jeśli istnieje
    init = "latinhypercube"
    if os.path.exists(SAVE_FILE):
        data = np.load(SAVE_FILE)
        init = data["pop"]
        print("▶ Wczytano populację z checkpointu:", init.shape)

    # globalny holder na wynik, dostępny w callbacku
    last_result = None

    result = differential_evolution(
        lambda x: objective_de(x, boards),
        bounds,
        maxiter=1000,
        popsize=15,
        polish=True,
        disp=True,
        init=init,
        callback=save_checkpoint
    )

    last_result = result  # zapisz końcowy wynik

    # --- zapis ostateczny ---
    np.savez(
        FINAL_FILE,
        best_x=result.x,
        best_fun=result.fun,
        final_population=result.population
    )
    print(f"\n✔ Wynik końcowy zapisany do {FINAL_FILE}")

    print("\nNajlepsze parametry:", result.x)
    print("Najlepszy wynik (średnia ruchów):", result.fun)

    # walidacja na nowych planszach
    test_boards = make_boards(num_boards=5, size=8, seeds=[200+i for i in range(5)])
    val = objective_de(result.x, test_boards)
    print("Wynik na nowych planszach:", val)






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