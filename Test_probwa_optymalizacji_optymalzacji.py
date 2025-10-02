# opt_with_eval_log.py
import proba_optymalizacji_optymalizacji as Owocki
import numpy as np
from scipy.optimize import differential_evolution
import os
import csv
import time

SAVE_LOG = "eval_log.csv"
FINAL_FILE = "wynik_ostateczny.npz"

def make_boards(num_boards=10, size=9, seeds=None):
    boards = []
    for i in range(num_boards):
        s = (seeds[i] if seeds is not None else i + 1234)
        rng = np.random.RandomState(s)
        b = rng.randint(1, 10, size=(size, size)).astype(np.int32)
        boards.append(b)
    return boards

# -------------------------
# LOG helper: dopisz jedno wywołanie (atomowo-ish)
# -------------------------
def log_evaluation(x, val, logfile=SAVE_LOG):
    """
    Dopisuje linijkę: timestamp, val, x0, x1, ...
    """
    line = [time.time(), float(val)] + [float(xx) for xx in np.asarray(x).ravel()]
    # upewnij się, że plik istnieje z nagłówkiem
    write_header = not os.path.exists(logfile)
    # append lines
    with open(logfile, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            header = ["ts", "val"] + [f"x{i}" for i in range(len(line)-2)]
            writer.writerow(header)
        writer.writerow(line)
        f.flush()
        os.fsync(f.fileno())

# -------------------------
# objective_de: liczy wartość i loguje
# -------------------------
def objective_de(x, boards):
    # x: array-like [w_alone, w_duble, w_triple, w_unique_fruits]
    print("Parametry: ",x)
    params = {
        'w_alone': float(x[0]),
        'w_duble': float(x[1]),
        'w_triple': float(x[2]),
        'w_unique_fruits': float(x[3]),
    }

    moves_counts = []
    for b in boards:
        b_copy = np.copy(b)
        resultat = []
        # UWAGA: find_optimal_parm w Twoim module może używać multiprocessing wewnątrz
        l = Owocki.find_optimal_parm(b_copy, resultat, params, 1, 100)
        moves_counts.append(l)

    mean_moves = float(np.mean(moves_counts))
    print("Wynik sredni: ",mean_moves)

    std_moves = float(np.std(moves_counts))
    val = mean_moves + 0.1 * std_moves

    # logujemy każde wywołanie (x i val)
    try:
        log_evaluation(x, val, SAVE_LOG)
    except Exception as e:
        # nie przerywamy optymalizacji jeśli log nie zadziała
        print("Nie udało się zapisać logu:", e)

    return val

# -------------------------
# Wczytaj najlepsze K z logu (jeśli istnieje)
# -------------------------
def load_top_k_from_log(k, logfile=SAVE_LOG):
    if not os.path.exists(logfile):
        return None
    rows = []
    with open(logfile, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return None
        for row in reader:
            if len(row) < 3:
                continue
            # row format: ts, val, x0, x1, ...
            ts = float(row[0])
            val = float(row[1])
            xs = [float(v) for v in row[2:]]
            rows.append((val, xs))
    if not rows:
        return None
    # sortuj po val rosnąco (mniejsze = lepsze)
    rows.sort(key=lambda t: t[0])
    topk = [np.array(xs) for val, xs in rows[:k]]
    return topk

# -------------------------
# zbuduj init populację z top_k (reszta losowa)
# -------------------------
def build_init_from_topk(topk, bounds, popsize):
    dim = len(bounds)
    pop = np.empty((popsize, dim))
    # wypełnij losowo
    for i in range(dim):
        lo, hi = bounds[i]
        pop[:, i] = np.random.uniform(lo, hi, size=popsize)
    # wstaw topk kolejno do poczatku populacji
    for idx, x in enumerate(topk):
        if idx >= popsize:
            break
        pop[idx, :] = x
    return pop

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    # ustawienia
    boards = make_boards(num_boards=10, size=9, seeds=[100+i for i in range(10)])
    bounds = [
        (0, 20),   # w_alone
        (0, 15),   # w_duble
        (0, 10),   # w_triple
        (-10, 10), # w_unique_fruits
    ]

    popsize = 10
    maxiter = 200

    # spróbuj wczytać top K z logu i zbudować init
    TOP_K = min(15, popsize)  # weź 5 najlepszych (albo mniej gdy popsize mały)
    topk = load_top_k_from_log(TOP_K, SAVE_LOG)
    if topk:
        init_pop = build_init_from_topk(topk, bounds, popsize)
        print(f" Wczytano {len(topk)} najlepszych z {SAVE_LOG} i zbudowano init_pop.")
        init = init_pop
    else:
        init = "latinhypercube"
        print("Brak logu - startuję od zera.")

    # uruchom DE
    result = differential_evolution(
        lambda x: objective_de(x, boards),
        bounds,
        maxiter=maxiter,
        popsize=popsize,
        polish=True,
        disp=True,
        init=init
    )

    # zapisz wynik ostateczny
    np.savez(
        FINAL_FILE,
        best_x=result.x,
        best_fun=float(result.fun)
    )
    print(f"\n✔ Wynik końcowy zapisany do {FINAL_FILE}")
    print("Najlepsze parametry:", result.x)
    print("Najlepszy wynik (średnia ruchów):", result.fun)



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