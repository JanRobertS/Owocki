import pygame
import Gra_7x7_owocki as owocki
import proba_optymalizacji_optymalizacji as optymalizacja
import numpy as np
import multiprocessing as mp

from Button import Button

#główne inicjalizowanie
pygame.init()



def play(board = None, best_opti = None):
    BASE_W, BASE_H = 1024, 1024

    board = np.array([
    [ 1.,  2.,  3.,  4.,  2.,  5.,  6.,  7.,  7.],
    [ 7.,  6.,  8.,  9.,  6.,  7., 10.,  4., 11.],
    [12., 13.,  1., 14.,  6.,  7.,  1., 15., 10.],
    [ 5., 10.,  9., 16., 14., 17., 15., 11., 18.],
    [ 7.,  5.,  2., 15., 10.,  9., 17., 15.,  5.],
    [15., 11., 11.,  8.,  9.,  2., 18., 10.,  9.],
    [ 9., 18.,  8., 18., 14.,  6.,  6., 13.,  3.],
    [17.,  6.,  5.,  5.,  9., 13.,  6., 17., 18.],
    [16.,  1., 13.,  4.,  6.,  6.,  7., 14.,  5.]
])

    base_surface = pygame.Surface((BASE_W, BASE_H))
    screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)

    clock = pygame.time.Clock()

    size_on_board = 75
    start_board_pixel_X = 187
    start_board_pixel_Y = 176

    pygame.display.set_caption("Play")

    pop_sound = pygame.mixer.Sound("Sound\\Pop2.wav")
    pop_sound.set_volume(0.5)
    win_sound = pygame.mixer.Sound("Sound\\Win.wav")
    win_sound.set_volume(0.7)

    # wczytywanie planszy
    image_board = pygame.image.load("Grafiki\\plansza_9x9.png").convert()
    image_win = pygame.image.load("Grafiki\\Wygrana.png").convert()
    font = pygame.font.Font(None, size=50)
    font_win = pygame.font.Font("Czcionki\\ByteBounce.ttf", size=80)

    running = True

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
        fruits_dict_img_BIGer[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*4 , fruits_dict_img[key].get_height()*5))
        fruits_dict_img[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*3 , fruits_dict_img[key].get_height()*4))

    # inicjalizacja gry owoce
    board_size = 9
    fruits = owocki.Fruits(board=board, size=board_size)
    print(fruits.board)

    if not best_opti:
        optymalization = owocki.Optimalization(fruits.board.copy())
        brute_forse_turn = optymalization.brute_force_turn
        best_xy_BF = optymalization.best_move_brute_forse(fruits)
    else:
        brute_forse_turn = len(best_opti)
        best_xy_BF = best_opti.pop(0)

    best_famili_fruit_BF =  fruits.search_neighbors(best_xy_BF)

    #wyliczanie która to kratka
    board_x_starta = 174
    board_x_enda = 848
    board_y_starta = 174
    board_y_enda = 844

    square = False

    def get_square_index(x_click, y_click):
        size = screen.get_size()

        board_x_start = board_x_starta * (size[0]/BASE_W)
        board_x_end = board_x_enda * (size[0]/BASE_W)
        board_y_start = board_y_starta * (size[1]/BASE_H)
        board_y_end = board_y_enda * (size[1]/BASE_H)

        cols = board_size
        rows = board_size
        square_width = (board_x_end - board_x_start) / cols
        square_height = (board_y_end - board_y_start) / rows

        if board_x_start <= x_click <= board_x_end and board_y_start <= y_click <= board_y_end:
            col = int((x_click - board_x_start) / square_width)
            row = int((y_click - board_y_start) / square_height)
            if row < board_size and col < board_size:
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
        base_surface.blit(image_board, (0,0))

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
            for x in range(0,board_size): 
                for y in range(0,board_size):
                    if fruits.board[y][x]:
                        if [y,x] in mpos_on_famili_fruit:
                            base_surface.blit(fruits_dict_img_BIGer[fruits.board[y][x]], (start_board_pixel_X-7+size_on_board*x,start_board_pixel_Y-7+size_on_board*y))
                        elif [y,x] in best_famili_fruit_BF : 
                            if len(best_famili_fruit_BF) > 1 or best_opti:
                                if blink < blink_limit/2:
                                    alfa_fuits = fruits_dict_img[fruits.board[y][x]].copy()
                                    alfa_fuits.set_alpha(max(0, 255 - (blink)))
                                    base_surface.blit(alfa_fuits, (start_board_pixel_X+size_on_board*x,start_board_pixel_Y+size_on_board*y))
                                elif blink >= blink_limit/2:
                                    alfa_fuits = fruits_dict_img[fruits.board[y][x]].copy()
                                    alfa_fuits.set_alpha(max(0, 255 - blink_limit + (blink)))
                                    base_surface.blit(alfa_fuits, (start_board_pixel_X+size_on_board*x,start_board_pixel_Y+size_on_board*y))
                                    if blink >= blink_limit:
                                        blink = 0

                        else:
                            base_surface.blit(fruits_dict_img[fruits.board[y][x]], (start_board_pixel_X+size_on_board*x,start_board_pixel_Y+size_on_board*y))

        blink += blink_speed


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                print(event.pos, event.button, event.touch)
                if event.button == 1 and init_time:
                    mouse_pos = event.pos
                    square = get_square_index(mouse_pos[0],mouse_pos[1])
                    print(square)
            elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if square:
            if fruits.board[square[0]][square[1]] != 0:
                fruits.move(square)
                fruits.print_resultat() #TODO do USUNIECIA
                pop_sound.play()
                square = False

                if not fruits.finished:
                    if not best_opti:
                        best_xy_BF = optymalization.best_move_brute_forse(fruits)
                    else:
                        best_xy_BF = best_opti.pop(0)
                    best_famili_fruit_BF =  fruits.search_neighbors(best_xy_BF)

                if fruits.finished:
                    win_sound.play()


        scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        clock.tick(60)
        pygame.display.flip()


    pygame.quit()

def optimalization(board):
    board = np.array([
    [ 1.,  2.,  3.,  4.,  2.,  5.,  6.,  7.,  7.],
    [ 7.,  6.,  8.,  9.,  6.,  7., 10.,  4., 11.],
    [12., 13.,  1., 14.,  6.,  7.,  1., 15., 10.],
    [ 5., 10.,  9., 16., 14., 17., 15., 11., 18.],
    [ 7.,  5.,  2., 15., 10.,  9., 17., 15.,  5.],
    [15., 11., 11.,  8.,  9.,  2., 18., 10.,  9.],
    [ 9., 18.,  8., 18., 14.,  6.,  6., 13.,  3.],
    [17.,  6.,  5.,  5.,  9., 13.,  6., 17., 18.],
    [16.,  1., 13.,  4.,  6.,  6.,  7., 14.,  5.]
])

    print(board)
    
    def draw_progress_bar(surface, x, y, width, height, progress):
        # progress w zakresie 0.0–1.0
        pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2)  # ramka
        inner_width = int(width * progress)
        pygame.draw.rect(surface, (50, 200, 50), (x, y, inner_width, height))  # wypełnienie

    step = 2
    top = 200

    BASE_W, BASE_H = 600, 150
    screen = pygame.display.set_mode((BASE_W, BASE_H))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Optymalization")


    running = True
    progress = 0.0

    queue = mp.Queue()

    p = mp.Process(target=optymalizacja.find_optimal_worker,
                   args=(np.copy(board), [], step, top, queue))
    p.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while not queue.empty():
            msg = queue.get()
            if msg[0] == "DONE":
                best = msg[1]
                running = False
            else:
                iteration = msg[1]
                progress = min(iteration /50, 1.0)

        screen.fill((30, 30, 30))
        draw_progress_bar(screen, 50, 60, 500, 30, min(progress, 1.0))
        pygame.display.flip()
        clock.tick(30)

    p.join()

    rezultat1 = best[1]
    rezultat2 = [(np.int64(x), np.int64(y)) for x, y in rezultat1]
    # po zakończeniu pokaż normalną grę
    play(board=board, best_opti=rezultat2)

def optimum(board_size = 9):

    BASE_W, BASE_H = 1024, 1224

    base_surface = pygame.Surface((BASE_W, BASE_H))
    screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Algorytm")

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

        fruits_dict_img_BIGer[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*5 , fruits_dict_img[key].get_height()*5))
        fruits_dict_img[key] = pygame.transform.scale(fruits_dict_img[key], (fruits_dict_img[key].get_width()*4 , fruits_dict_img[key].get_height()*4))




    size_on_board = 75
    start_board_pixel_X = 179
    start_board_pixel_Y = 176

    #wyliczanie która to kratka
    board_x_starta = 174
    board_x_enda = 848
    board_y_starta = 174
    board_y_enda = 844

    square = False
    click = False

    AKCEPT_BUTTON = Button(image=None, pos=(525,930), text_input="AKCEPT",
                        font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=175),
                        base_color="#d7fcd4", hovering_color="White") 
    
    RESET_BUTTON = Button(image=None, pos=(935,510), text_input="RESET",
                        font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=50),
                        base_color="#d7fcd4", hovering_color="White") 

    def get_square_index(x_click, y_click):
        size = screen.get_size()

        board_x_start = board_x_starta * (size[0]/BASE_W)
        board_x_end = board_x_enda * (size[0]/BASE_W)
        board_y_start = board_y_starta * (size[1]/BASE_H)
        board_y_end = board_y_enda * (size[1]/BASE_H)

        cols = board_size
        rows = board_size
        square_width = (board_x_end - board_x_start) / cols
        square_height = (board_y_end - board_y_start) / rows

        if board_x_start <= x_click <= board_x_end and board_y_start <= y_click <= board_y_end:
            col = int((x_click - board_x_start) / square_width)
            row = int((y_click - board_y_start) / square_height)
            if row < board_size and col < board_size:
                return row, col
            else:
                return None
        else:
            return None  # kliknięcie poza planszą
        

    def get_square_index_new_fruits(x_click, y_click):
        size = screen.get_size()

        board_x_start = 95* (size[0]/BASE_W)
        board_x_end = (95 + size_on_board*11) * (size[0]/BASE_W)
        board_y_start = 1035 * (size[1]/BASE_H)
        board_y_end = (1020 + (size_on_board*3)) * (size[1]/BASE_H)

        cols = 11
        rows = 2
        square_width = (board_x_end - board_x_start) / cols
        square_height = (board_y_end - board_y_start) / rows

        if board_x_start <= x_click <= board_x_end and board_y_start <= y_click <= board_y_end:
            col = int((x_click - board_x_start) / square_width)
            row = int((y_click - board_y_start) / square_height)
            if row < 2 and col < 11:
                return row, col
            else:
                return None
        else:
            return None  #kliknięcie poza planszą


    board = np.zeros((board_size, board_size))

    init_time = False
    blink = 0
    blink_limit = 200
    blink_speed = 3

    mpos_on_fruit = []
    clicked_fruit = None


    while True:
        pygame.display.set_caption("Optimum")

        base_surface.fill("#1a88e2")
        base_surface.blit(plansza)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        mpos_on_fruit = [get_square_index_new_fruits(MENU_MOUSE_POS[0],MENU_MOUSE_POS[1])]


        for button in [AKCEPT_BUTTON, RESET_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(base_surface)

        x = 0
        y = 0 

        for x in range(0, 11):
            for y in range(0,2):
                if (y,x) in mpos_on_fruit and clicked_fruit != (x+y*11+1):
                    base_surface.blit(fruits_dict_img_BIGer[(x+y*11+1)], (95+size_on_board*x,1035+(size_on_board+25)*y))

                    if click:
                        clicked_fruit = (x+y*11+1)
                elif clicked_fruit != (x+y*11+1):
                    base_surface.blit(fruits_dict_img[(x+y*11+1)], (95+size_on_board*x,1035+(size_on_board+25)*y))

        if clicked_fruit:
            base_surface.blit(fruits_dict_img[clicked_fruit], (MENU_MOUSE_POS[0]-25,MENU_MOUSE_POS[1]-25))
        
        pos_in_board = get_square_index(MENU_MOUSE_POS[0],MENU_MOUSE_POS[1])

        if pos_in_board and clicked_fruit and click and board[pos_in_board[0],pos_in_board[1]] != clicked_fruit:
            board[pos_in_board[0],pos_in_board[1]] = clicked_fruit

            

        x = 0
        y = 0
        for x in range(0,board_size): 
            for y in range(0,board_size):
                if board[y][x]:
                    # if [y,x] in mpos_on_famili_fruit:
                    #     base_surface.blit(fruits_dict_img_BIGer[board[y][x]], (start_board_pixel_X-7+size_on_board*x,start_board_pixel_Y-7+size_on_board*y))
                    # elif [y,x] in best_famili_fruit_BF and len(best_famili_fruit_BF) > 1: 
                    #     if blink < blink_limit/2:
                    #         alfa_fuits = fruits_dict_img[board[y][x]].copy()
                    #         alfa_fuits.set_alpha(max(0, 255 - (blink)))
                    #         base_surface.blit(alfa_fuits, (start_board_pixel_X+size_on_board*x,start_board_pixel_Y+size_on_board*y))
                    #     elif blink >= blink_limit/2 and len(best_famili_fruit_BF) > 1:
                    #         alfa_fuits = fruits_dict_img[board[y][x]].copy()
                    #         alfa_fuits.set_alpha(max(0, 255 - blink_limit + (blink)))
                    #         base_surface.blit(alfa_fuits, (start_board_pixel_X+size_on_board*x,start_board_pixel_Y+size_on_board*y))
                    #         if blink >= blink_limit:
                    #             blink = 0

                    # else:
                    base_surface.blit(fruits_dict_img[board[y][x]], (start_board_pixel_X+size_on_board*x,start_board_pixel_Y+size_on_board*y))

        blink += blink_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False
            elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if AKCEPT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    optimalization(board=board) #TODO ZAMIENIĆ NA BOARD "TEST"
                if RESET_BUTTON.checkForInput(MENU_MOUSE_POS):
                    board = np.zeros((board_size, board_size))
                    clicked_fruit = None


        scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        clock.tick(60)
        pygame.display.flip()

def options():
    BASE_W, BASE_H = 1024, 1024
    font = pygame.font.Font("Czcionki\\ByteBounce.ttf", 40)


    base_surface = pygame.Surface((BASE_W, BASE_H))
    screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)

    image_board = pygame.image.load("Grafiki\\opcje.png").convert()
    clock = pygame.time.Clock()
    pygame.display.set_caption("OPTIONS")

    button = pygame.image.load("Grafiki\\button.png").convert_alpha()
    button = pygame.transform.scale(button, (button.get_width()/3 , button.get_height()/3))
    button2 = pygame.transform.scale(button, (button.get_width()/4 , button.get_height()/4))


    RETURN_BUTTON = Button(image=button, pos=(525,880), text_input="RETURN",
                        font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=100),
                        base_color="#d7fcd4", hovering_color="White") 
    
    STOP_START_BUTTON = Button(image=button2, pos=(450 + 125,350+150), text_input="START",
                        font=pygame.font.Font("Czcionki\\ByteBounce.ttf", size=35),
                        base_color="#d7fcd4", hovering_color="White") 
    

    #slider STEP
    slider1_x, slider1_y = 350, 250   # pozycja paska
    slider1_width, slider1_height = 300, 30

    min_val1 = 1
    max_val1 = 6
    value1 = 2 

    step1_size = slider1_width // (max_val1 - min_val1)

    #slider TOP
    slider2_x, slider2_y = 450, 350   # pozycja paska
    slider2_width, slider2_height = 300, 30

    min_val2 = 1
    max_val2 = 700
    value2 = 1

    step2_size = slider2_width / (max_val2 - min_val2)
    print(step2_size)




    def value_to_pos(slider_x,min_val,step_size,val):
        return slider_x + (val - min_val) * step_size

    def pos_to_value(slider_x,min_val,step_size,max_val,pos):
        idx = round((pos - slider_x) / step_size)
        return min_val + max(0, min(idx, max_val - min_val))

    knob1_x = value_to_pos(slider1_x,min_val1,step1_size,value1)
    dragging1 = False

    START = False
    graviti = 1
    knob2_y = value_to_pos(slider2_x,min_val2,step2_size,value2)
    
    while True:
        base_surface.blit(image_board, (0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in [RETURN_BUTTON, STOP_START_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(base_surface)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                knob1_rect = pygame.Rect(knob1_x-10, slider1_y-6, 20, slider1_height+12)  # taki sam jak rysujesz knob
                if knob1_rect.collidepoint(event.pos):
                    dragging1 = True

                if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    menu()

                if STOP_START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if STOP_START_BUTTON.text_input =="START":
                        STOP_START_BUTTON.text_input = "STOP"
                        STOP_START_BUTTON.base_color="#b94646"
                        STOP_START_BUTTON.hovering_color="#fa0101"

                        START = True
                    else:
                        STOP_START_BUTTON.text_input = "START"
                        START = False
                        STOP_START_BUTTON.base_color="#d7fcd4"
                        STOP_START_BUTTON.hovering_color="White"

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging1:
                    value1 = pos_to_value(slider1_x,min_val1,step1_size,knob1_x)       # oblicz najbliższą wartość
                    knob1_x = value_to_pos(slider1_x,min_val1,step1_size,value1)       # przesuń knob dokładnie na slot
                dragging1 = False

            elif event.type == pygame.MOUSEMOTION and dragging1:
                knob1_x = max(slider1_x, min(event.pos[0], slider1_x + slider1_width))
                value1 = pos_to_value(slider1_x,min_val1,step1_size,knob1_x)
                knob1_x = value_to_pos(slider1_x,min_val1,step1_size,value1)
               # przesuń knob dokładnie na slot

        if START:
            graviti+=3
            if graviti > max_val2:
                graviti = 0
            knob2_y = value_to_pos(slider2_y,min_val2,step2_size,graviti)
        
        
        # Rysowanie
        scaled_surface = pygame.transform.scale(base_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        # --- slider rysujemy NA screenie ---
        # w pętli rysowania zamiast okrągłego knoba:
        # --- pixel-art pasek --- STEP
        pygame.draw.rect(screen, "#0b6405", (slider1_x-2, slider1_y-2, slider1_width+4, slider1_height+4))  # obramówka
        pygame.draw.rect(screen, "#0D8F18", (slider1_x, slider1_y, slider1_width, slider1_height))       # wypełnienie
        # --- pixel-art pasek --- TOP
        pygame.draw.rect(screen, "#640505", (slider2_x-2, slider2_y-2, slider2_height+4, slider2_width+4))  # obramówka
        pygame.draw.rect(screen, "#5B0D8F", (slider2_x, slider2_y, slider2_height, slider2_width))       # wypełnienie


        # podziałka (kratki pixel-artowe)
        for i in range(min_val1, max_val1+1):
            px1 = value_to_pos(slider1_x,min_val1,step1_size,i)
            pygame.draw.rect(screen, "#0b6405", (px1-2, slider1_y-2, 4, slider1_height+4))

        # prostokątny knob STEP
        pygame.draw.rect(screen, "#108d07", (knob1_x-10, slider1_y-6, 21, slider1_height+13))
        pygame.draw.rect(screen, "#a5ff9e", (knob1_x-10, slider1_y-6, 20, slider1_height+12))
        # liczba obok
        text1 = font.render(f"Step = {value1}", True, (255, 255, 255))
        screen.blit(text1, (slider1_x+slider1_width/2 - 60, slider1_y-40))

        pygame.draw.rect(screen,  "#690808", (slider2_x-6,knob2_y-10, slider2_height+13,21))
        pygame.draw.rect(screen,"#3A065C", (slider2_x-6,knob2_y-10,slider2_height+12, 20))
        # liczba obok
        # liczba obok
        text2 = font.render(f"Step = {graviti}", True, (255, 255, 255))
        screen.blit(text2, (slider2_x+slider2_width/2 - 60, slider2_y-40))


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
                    options()
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
