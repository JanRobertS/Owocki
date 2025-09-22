import proba_optymalizacji_optymalizacji as Owocki

import numpy as np






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


if __name__ == "__main__":

    plansza = np.array([
    [3, 6, 7, 4, 4, 1],
    [5, 9, 3, 3, 5, 4],
    [2, 7, 8, 6, 8, 7],
    [5, 9, 4, 2, 4, 3],
    [8, 3, 9, 5, 5, 4],
    [5, 8, 3, 4, 3, 9]
])


#     plansza = np.array([
#     [9, 1, 5, 2, 2, 5, 7, 6, 3],
#     [4, 4, 6, 5, 4, 1, 4, 1, 3],
#     [5, 9, 5, 8, 7, 6, 4, 3, 5],
#     [3, 2, 8, 5, 2, 9, 8, 2, 9],
#     [6, 1, 6, 2, 3, 8, 9, 8, 1],
#     [6, 7, 4, 6, 6, 5, 3, 4, 1],
#     [4, 5, 1, 1, 1, 5, 3, 9, 5],
#     [3, 5, 4, 7, 6, 1, 9, 1, 9],
#     [8, 1, 5, 1, 3, 6, 7, 5, 7]
# ])

    brute_forse_rezultat, brute_forse_turn= Owocki.brute_force(np.copy(plansza), [])

    print("Greedy:", brute_forse_turn)
    print(brute_forse_rezultat)
    planszabf = np.copy(plansza)

    rezultatbf = []
    for xy in brute_forse_rezultat:
        planszabf, finishbf, rezultatybf = Owocki.move(xy,planszabf,rezultatbf)
        print("\nplansza:",planszabf,"\n rezultat:", rezultatybf)



    step = 3
    top = 3

    print("\nStep:", step, "\nTop:", top)

    rezultat = Owocki.find_optimal(np.copy(plansza), [], step, top)

    rezultat1 = rezultat[1]

    print("\nIlosc optymalna",len(rezultat[1]),"\n\n",rezultat1)

    # f = optimalization.find_optimal(step= step, top = top)

    # # f.print_resultat()
    rezultaty = []
    rezultat2 = [(np.int64(x), np.int64(y)) for x, y in rezultat1]
    print(rezultat2)

    plansza2 = np.copy(plansza)
    
    for xy in rezultat2:
        plansza2, finish, rezultaty = Owocki.move(xy,plansza2,rezultaty)
        print("\nplansza:",plansza2,"\n rezultat:", rezultaty)

    print(finish)