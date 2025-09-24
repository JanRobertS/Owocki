import pygame
import Gra_7x7_owocki as owocki
import proba_optymalizacji_optymalizacji as optymalizacja
import numpy as np

from Button import Button

#główne inicjalizowanie
pygame.init()

def play():
    BASE_W, BASE_H = 1024, 1024

    base_surface = pygame.Surface((BASE_W, BASE_H))
    screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)


    clock = pygame.time.Clock()



    pygame.display.set_caption("Play")

    pop_sound = pygame.mixer.Sound("Sound\\Pop2.wav")
    pop_sound.set_volume(0.5)
    win_sound = pygame.mixer.Sound("Sound\\Win.wav")
    win_sound.set_volume(0.7)
    mouse_click = False

    # wczytywanie planszy
    image_board_7x7 = pygame.image.load("Grafiki\\plansza_9x9.png").convert()
    image_win = pygame.image.load("Grafiki\\Wygrana.png").convert()
    font = pygame.font.Font(None, size=50)
    font_win = pygame.font.Font("Czcionki\\ByteBounce.ttf", size=80)


    running = True
    mouse_click = False


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

    print(fruits.board)

    optymalization = owocki.Optimalization(fruits.board.copy())
    brute_forse_turn = optymalization.brute_force_turn
    best_xy_BF = optymalization.best_move_brute_forse(fruits)
    best_famili_fruit_BF =  fruits.search_neighbors(best_xy_BF)


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


    init_time = False


    while running:
        base_surface.blit(image_board_7x7, (0,0))

        if not init_time:
            if blink > 190:
                init_time = True

        if fruits.finished:
            base_surface.blit(image_win, (0,0))
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
                if event.button == 1 and init_time:
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

                if fruits.finished:
                    win_sound.play()


        scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        clock.tick(60)
        pygame.display.flip()


    pygame.quit()

def optimum():

    BASE_W, BASE_H = 1024, 1224

    base_surface = pygame.Surface((BASE_W, BASE_H))
    screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)


    clock = pygame.time.Clock()

    base_surface.fill("#1a88e2")

    plansza = pygame.image.load("Grafiki\\plansza_9x9.png").convert()
    
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    base_surface.blit(plansza)

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

    for key, value in fruits_dict.items():
        image_path = f"Grafiki/Owoce/{value}.png"
        fruits_dict_img[key] = pygame.image.load(image_path).convert_alpha()
        fruits_dict_img_BIGer[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*6 , fruits_dict_img[key].get_height()*6))
        fruits_dict_img[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*5 , fruits_dict_img[key].get_height()*5))

    # inicjalizacja gry owoce
    fruits = owocki.Fruits()


    while True:
        pygame.display.set_caption("Optimum")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


        scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        clock.tick(60)
        pygame.display.flip()
                    

def menu():
    BASE_W, BASE_H = 1024, 1024

    base_surface = pygame.Surface((BASE_W, BASE_H))
    screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)


    clock = pygame.time.Clock()

    while True:
        
        pygame.display.set_caption("Menu")

        menu = pygame.image.load("Grafiki\\ekran_startowy.png").convert()

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        

        PLAY_BUTTON = Button(image=None, pos=(525,305), text_input="PLAY",
                            font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=200),
                            base_color="#d7fcd4", hovering_color="White") 
        
        OPTIMUM_BUTTON = Button(image=None, pos=(525,485), text_input="OPTIMUM",
                    font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=130),
                    base_color="#d7fcd4", hovering_color="White")     

        OPTIONS_BUTTON = Button(image=None, pos=(525,655), text_input="OPTIONS",
                    font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=140),
                    base_color="#d7fcd4", hovering_color="White")     
        
        QUIT_BUTTON = Button(image=None, pos=(525,835), text_input="QUIT",
                    font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=200),
                    base_color="#d7fcd4", hovering_color="White") 
        



        base_surface.blit(menu)

        for button in [PLAY_BUTTON, OPTIMUM_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(base_surface)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIMUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    optimum()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    break


        scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        clock.tick(60)
        pygame.display.flip()




if __name__ == "__main__":
    menu()
    pygame.quit()



