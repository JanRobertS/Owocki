import pygame
import Gra_7x7_owocki as owocki
import numpy as np

#główne inicjalizowanie
pygame.init()

# Bazowa rozdzielczość gry
BASE_W, BASE_H = 1024, 1024
base_surface = pygame.Surface((BASE_W, BASE_H))
screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)

pop_sound = pygame.mixer.Sound("Sound\\Pop2.wav")
pop_sound.set_volume(0.5)
win_sound = pygame.mixer.Sound("Sound\\Win.wav")
win_sound.set_volume(0.7)


clock = pygame.time.Clock()

running = True
mouse_click = False

# wczytywanie planszy
image_board_7x7 = pygame.image.load("Grafiki\\plansza_7x7.png").convert()
image_win = pygame.image.load("Grafiki\\Wygrana.png").convert()
font = pygame.font.Font(None, size=50)
font_win = pygame.font.SysFont("comicsansms", size=80)

#wczytywanie grafik owoców
fruits_dict = {
    1: "Ananas",
    2: "Apple",
    3: "Avacodo",
    4: "Banana",
    5: "Blackberry",
    6: "Blueberry",
    7: "Cherry",
    8: "Chilli",
    9: "Dragon_Fruit",
    10: "Eggplant",
    11: "Granate",
    12: "Grapes",
    13: "Lemon",
    14: "Orange",
    15: "Peach",
    16: "Pear",
    17: "Pepper",
    18: "Pumpkin",
    19: "Strawberry",
    20: "Tomato",
    21: "UFO",
    22: "Watermelon"
}
fruits_dict_img = {
    0 : False
}
fruits_dict_img_BIGer = {
    0 : False
}
fruits_dict_img_red = {
    0 : False
}
for key, value in fruits_dict.items():
    image_path = f"Grafiki/Owoce/{value}.png"
    fruits_dict_img[key] = pygame.image.load(image_path).convert_alpha()
    fruits_dict_img_BIGer[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*6 , fruits_dict_img[key].get_height()*6))
    fruits_dict_img[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*5 , fruits_dict_img[key].get_height()*5))

    new_img = fruits_dict_img[key].copy()
    new_img.fill((255, 150, 150, 255), special_flags=pygame.BLEND_RGBA_MULT)
    fruits_dict_img_red[key] = new_img

# inicjalizacja gry owoce
fruits = owocki.Fruits()
    
#     np.array([
#     [5, 2, 3, 2, 2, 2, 5],
#     [3, 2, 2, 2, 4, 2, 5],
#     [3, 2, 4, 5, 3, 3, 3],
#     [1, 2, 1, 2, 4, 2, 4],
#     [1, 4, 1, 1, 5, 1, 5],
#     [1, 2, 3, 1, 4, 1, 1],
#     [4, 1, 1, 3, 3, 4, 5],
# ]))

# optimal_i = 0
# optimal_move = [(np.int64(0), np.int64(4)), (np.int64(1), np.int64(1)), (np.int64(0), np.int64(6)), (np.int64(2), np.int64(4)), (np.int64(4), np.int64(2)), (np.int64(2), np.int64(3)), (np.int64(4), np.int64(5)), (np.int64(2), np.int64(4)), (np.int64(4), np.int64(0)), (np.int64(1), np.int64(2)), (np.int64(2), np.int64(0)), (np.int64(3), np.int64(0)), (np.int64(6), np.int64(1)), (np.int64(4), np.int64(3)), (np.int64(3), np.int64(2)), (np.int64(4), np.int64(1)), (np.int64(4), np.int64(2)), (np.int64(4), np.int64(6)), (np.int64(5), np.int64(6)), (np.int64(5), np.int64(0)), (np.int64(5), np.int64(1)), (np.int64(5), np.int64(2)), (np.int64(5), np.int64(3)), (np.int64(6), np.int64(2)), (np.int64(5), np.int64(4)), (np.int64(5), np.int64(5)), (np.int64(6), np.int64(0)), (np.int64(6), np.int64(1)), (np.int64(6), np.int64(4)), (np.int64(6), np.int64(5))]
# optimal_fruit = optimal_move[optimal_i]
# optimal_famili_fruits = fruits.search_neighbors(optimal_fruit)

print(fruits.board)

optymalization = owocki.Optimalization(fruits.board.copy())
brute_forse_turn = optymalization.brute_force_turn
best_xy_BF = optymalization.best_move_brute_forse(fruits)
best_famili_fruit_BF =  fruits.search_neighbors(best_xy_BF)

# optimal_fruit = optymalization.find_optimal()
# optimal_move = optimal_fruit.resultat[0]


# print(optimal_famili_fruits)
print(best_famili_fruit_BF)

#wyliczanie która to kratka
board_x_start = 141
board_x_end = 883
board_y_start = 194
board_y_end = 919

cols = 7
rows = 7

square_width = (board_x_end - board_x_start) / cols
square_height = (board_y_end - board_y_start) / rows
square = False



def get_square_index(x_click, y_click):
    size = screen.get_size()

    board_x_start = 141 * (size[0]/BASE_W)
    board_x_end = 883 * (size[0]/BASE_W)
    board_y_start = 194 * (size[1]/BASE_H)
    board_y_end = 919 * (size[1]/BASE_H)

    cols = 7
    rows = 7
    square_width = (board_x_end - board_x_start) / cols
    square_height = (board_y_end - board_y_start) / rows

    if board_x_start <= x_click <= board_x_end and board_y_start <= y_click <= board_y_end:
        col = int((x_click - board_x_start) / square_width)
        row = int((y_click - board_y_start) / square_height)
        if row < 7 and col < 7:
            return row, col
        else:
            return None
    else:
        return None  # kliknięcie poza planszą

#pusta lista sasiadow aktualnie trzymanej przez myszkę
mpos_on_famili_fruit = []

blink = 0
blink_limit = 200
blink_speed = 3

while running:
    base_surface.blit(image_board_7x7, (0,0))

    if fruits.finished:
        base_surface.blit(image_win, (0,0))
        # text_win = font_win.render("Wygrana",True,(0,0,0))
        # text_win_rect = text_win.get_rect(center=(1024/2, 1024/2))
        # screen.blit(text_win, text_win_rect)
        text_win_info = font_win.render(f"Ukończyłeś w {len(fruits.resultat)} tur!",True,(0,0,0))
        text_win_info_rect = text_win_info.get_rect(center=(1024/2, 1024/2))
        base_surface.blit(text_win_info, text_win_info_rect)
        

    else:
        text_number_of_turn = font.render(f"Ilość posunięć: {len(fruits.resultat)}",True,(0,0,0))
        base_surface.blit(text_number_of_turn, (20,20))

        text_best_number_of_turn = font.render(f"Zrób w: {brute_forse_turn} tur",True,(0,0,0))
        base_surface.blit(text_best_number_of_turn, (750,20))

        mpos = pygame.mouse.get_pos()
        mpos_on_fruit = get_square_index(mpos[0],mpos[1])
        if mpos_on_fruit:
            mpos_on_famili_fruit = fruits.search_neighbors(mpos_on_fruit)

        x = 0
        y = 0
        for x in range(0,7): 
            for y in range(0,7):
                if fruits.board[y][x]:
                    if [y,x] in mpos_on_famili_fruit:
                        base_surface.blit(fruits_dict_img_BIGer[fruits.board[y][x]], (150+105*x,203+102*y))
                    # elif [y,x] in optimal_famili_fruits:
                    #     base_surface.blit(fruits_dict_img_red[fruits.board[y][x]], (150+105*x,203+102*y))
                    elif [y,x] in best_famili_fruit_BF and len(best_famili_fruit_BF) > 1: 
                        if blink < blink_limit/2:
                            alfa_fuits = fruits_dict_img[fruits.board[y][x]].copy()
                            alfa_fuits.set_alpha(max(0, 255 - (blink)))
                            base_surface.blit(alfa_fuits, (155+105*x,208+102*y))
                        elif blink >= blink_limit/2 and len(best_famili_fruit_BF) > 1:
                            alfa_fuits = fruits_dict_img[fruits.board[y][x]].copy()
                            alfa_fuits.set_alpha(max(0, 255 - blink_limit + (blink)))
                            base_surface.blit(alfa_fuits, (155+105*x,208+102*y))
                            if blink >= blink_limit:
                                blink = 0

                    else:
                        base_surface.blit(fruits_dict_img[fruits.board[y][x]], (155+105*x,208+102*y))

    blink += blink_speed



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            print(event.pos, event.button, event.touch)
            if event.button == 1:
                mouse_click = True
                mouse_pos = event.pos
                square = get_square_index(mouse_pos[0],mouse_pos[1])
                print(square)
        elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    if square:
        if fruits.board[square[0]][square[1]] != 0:
            fruits.move(square)
            pop_sound.play()
            square = False

            best_xy_BF = optymalization.best_move_brute_forse(fruits)
            best_famili_fruit_BF =  fruits.search_neighbors(best_xy_BF)

            # optimal_i += 1
            # optimal_fruit = optimal_move[optimal_i]
            # optimal_famili_fruits = fruits.search_neighbors(optimal_fruit)


            # optymalization.board = np.copy(fruits.board)
            # optimal_fruit = optymalization.find_optimal()
            # optimal_move = optimal_fruit.resultat[0]
            # optimal_famili_fruits = fruits.search_neighbors(optimal_move)

            if fruits.finished:
                win_sound.play()


    scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
    screen.blit(scaled_surface, (0, 0))

    clock.tick(60)
    pygame.display.flip()


pygame.quit()