import random
import pygame
import sys
import math

field = [['.' for x in range(8)] for y in range(8)]
field[3][3] = field[4][4] = 1
field[3][4] = field[4][3] = 2
player = 0
turn = 1
column_char_index = {
                     "a": 1, "b": 2, "c": 3,
                     "d": 4, "e": 5, "f": 6,
                     "g": 7, "h": 8
                    }

placesAroundPieces = [
    (2, 2), (2, 3), (2, 4),
    (2, 5), (3, 2), (4, 2),
    (5, 2), (5, 3), (5, 4),
    (5, 5), (4, 5), (3, 5)
]
ADJACENT = [
    (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)
]
possibleMoves = []


def initialization():
    global field, player, column_char_index, placesAroundPieces, possibleMoves, turn

    field = [['.' for x in range(8)] for y in range(8)]
    field[3][3] = field[4][4] = 1
    field[3][4] = field[4][3] = 2
    player = 1
    turn = 1
    column_char_index = {
        "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8
    }
    placesAroundPieces = [
        (2, 2), (2, 3), (2, 4),
        (2, 5), (3, 2), (4, 2),
        (5, 2), (5, 3), (5, 4),
        (5, 5), (4, 5), (3, 5)
    ]
    possibleMoves = []


def print_field():
    print('   a_b_c_d_e_f_g_h')
    for x in range(len(field)):
        print((x + 1), '| ', sep='', end='')
        for y in range(len(field[0])):
            print(field[x][y], end=' ')
        print('')


def opponent():
    if player == 1:
        return 2
    else:
        return 1


def move_is_valid(row, column, current_player):
    if field[row][column] == 1 or field[row][column] == 2:
        return False
    for i in range(8):
        enemies_pieces_count = 0
        next_piece_row_i = ADJACENT[i][0] + row
        next_piece_col_i = ADJACENT[i][1] + column

        if (next_piece_row_i < 0 or next_piece_row_i > 7
                or next_piece_col_i < 0 or next_piece_col_i > 7):
            continue
        if (field[next_piece_row_i][next_piece_col_i] == current_player
                or field[next_piece_row_i][next_piece_col_i] == '.'
                or field[next_piece_row_i][next_piece_col_i] == '*'
                or field[next_piece_row_i][next_piece_col_i] == 'P'):
            continue

        while not (next_piece_row_i < 0 or next_piece_row_i > 7
                   or next_piece_col_i < 0 or next_piece_col_i > 7
                   or field[next_piece_row_i][next_piece_col_i] == '.'
                   or field[next_piece_row_i][next_piece_col_i] == '*'
                   or field[next_piece_row_i][next_piece_col_i] == 'P'):
            if field[next_piece_row_i][next_piece_col_i] == opponent():
                enemies_pieces_count += 1
                next_piece_row_i += ADJACENT[i][0]
                next_piece_col_i += ADJACENT[i][1]
            else:
                return True
    return False


def update_places_around_pieces(row_index, col_index):
    for i in range(8):
        adj_cell_row = ADJACENT[i][0] + row_index
        adj_cell_col = ADJACENT[i][1] + col_index
        if (0 <= adj_cell_row < 8
            and 0 <= adj_cell_col < 8
                and field[adj_cell_row][adj_cell_col] == '.'):
            field[adj_cell_row][adj_cell_col] = '*'
            placesAroundPieces.append((adj_cell_row, adj_cell_col))
    print(placesAroundPieces)


def highlight_border_pieces():
    for i in range(len(placesAroundPieces)):
        field[placesAroundPieces[i][0]][placesAroundPieces[i][1]] = '*'


count = 0


def highlight_possible_moves():
    global count

    for i in range(len(placesAroundPieces)):
        count = count + 1
        if move_is_valid(placesAroundPieces[i][0], placesAroundPieces[i][1], player):
            field[placesAroundPieces[i][0]][placesAroundPieces[i][1]] = 'P'
            possibleMoves.append((placesAroundPieces[i][0], placesAroundPieces[i][1]))
        elif field[placesAroundPieces[i][0]][placesAroundPieces[i][1]] == 'P':
            field[placesAroundPieces[i][0]][placesAroundPieces[i][1]] = '*'


def clear_possible_moves_list():
    possibleMoves.clear()


def make_move(row, column, current_player):
    all_pieces_to_flip = []

    for i in range(8):
        enemies_pieces_count = 0
        next_piece_row_i = ADJACENT[i][0] + row
        next_piece_col_i = ADJACENT[i][1] + column
        pieces_in_line_to_flip = []
        flip_line = False

        if (next_piece_row_i < 0 or next_piece_row_i > 7
                or next_piece_col_i < 0 or next_piece_col_i > 7):
            continue
        if (field[next_piece_row_i][next_piece_col_i] == current_player
                or field[next_piece_row_i][next_piece_col_i] == '.'
                or field[next_piece_row_i][next_piece_col_i] == '*'
                or field[next_piece_row_i][next_piece_col_i] == 'P'):
            continue

        while not (next_piece_row_i < 0 or next_piece_row_i > 7
                   or next_piece_col_i < 0 or next_piece_col_i > 7
                   or field[next_piece_row_i][next_piece_col_i] == '.'
                   or field[next_piece_row_i][next_piece_col_i] == '*'
                   or field[next_piece_row_i][next_piece_col_i] == 'P'):
            if field[next_piece_row_i][next_piece_col_i] == opponent():
                enemies_pieces_count += 1

                pieces_in_line_to_flip.append((next_piece_row_i, next_piece_col_i))

                next_piece_row_i += ADJACENT[i][0]
                next_piece_col_i += ADJACENT[i][1]
            else:
                flip_line = True
                break

        if flip_line:
            for i in range(len(pieces_in_line_to_flip)):
                all_pieces_to_flip.append(pieces_in_line_to_flip[i])

    for i in range(len(all_pieces_to_flip)):
        field[all_pieces_to_flip[i][0]][all_pieces_to_flip[i][1]] = current_player

    field[row][column] = player


def end_game():
    first_player_score = 0
    second_player_score = 0

    for x in range(8):
        for y in range(8):
            if field[x][y] == 1: first_player_score += 1
            elif field[x][y] == 2: second_player_score += 1

    print("Score: player one - ", first_player_score, ", player two - ", second_player_score, ".")

    if first_player_score > second_player_score:
        print("FIRST PLAYER WON!!!")
    elif second_player_score > first_player_score:
        print("SECOND PLAYER WON!!!")
    else:
        print("ITS A TIE")


def ai_random_move():
    ai_move = random.randint(0, len(possibleMoves) - 1)
    placesAroundPieces.remove((possibleMoves[ai_move][0], possibleMoves[ai_move][1]))
    update_places_around_pieces(possibleMoves[ai_move][0], possibleMoves[ai_move][1])
    make_move(possibleMoves[ai_move][0], possibleMoves[ai_move][1], player)

pygame.init()

GRAY = (200,200,200)
DARK_GRAY = (128,128,128)
RED = (178,23,23)
BLACK = (0,0,0)

ROW_COUNT = 8
COLUMN_COUNT = 8

SQUARESIZE = 60

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT) * SQUARESIZE

size = (width, height)

def draw_board(board):

    # Прорисовка самой доски
    for c in range(ROW_COUNT):
        for r in range(COLUMN_COUNT):
            pygame.draw.rect(screen, GRAY,
                (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, DARK_GRAY,
                (int(c * SQUARESIZE + SQUARESIZE / 2),
                 int(r * SQUARESIZE + SQUARESIZE / 2)),
                RADIUS)

    # Прорисовка фишек
    for c in range(ROW_COUNT):
        for r in range(COLUMN_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(field)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

col, row = 0, 0


def play():
    global player, col, row, turn
    previous_player_cant_move = False

    while True:
        highlight_border_pieces()
        highlight_possible_moves()
        # print_field()
        # print("Ходит игрок ", player)
        for event in pygame.event.get():
            draw_board(field)

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                # pygame.draw.rect(screen, DARK_GRAY, (0, 0, width, SQUARESIZE))
                col = int(math.floor((event.pos[0]) / SQUARESIZE))
                row = int(math.floor(event.pos[1] / SQUARESIZE))
                posx = col * SQUARESIZE + (SQUARESIZE / 2)
                posy = row * SQUARESIZE + (SQUARESIZE / 2)
                if player == 1:
                    pygame.draw.circle(screen, RED, (posx, posy), RADIUS)
                else:
                    pygame.draw.circle(screen, BLACK, (posx, posy), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("\n======================\n\nСледующий ход:", turn)
                print("Ходит игрок №", player)

                print_field()
                if len(possibleMoves) > 0:
                    previous_player_cant_move = False
                    print(row, ' ', col)
                    if move_is_valid(row, col, player):
                        placesAroundPieces.remove((row, col))
                        update_places_around_pieces(row, col)
                        make_move(row, col, player)
                        print("Сходил игрок №", player)
                        clear_possible_moves_list()
                        highlight_border_pieces()
                        print_field()
                        turn = turn + 1
                        player = opponent()
                else:
                    if previous_player_cant_move:
                        end_game()
                        break
                    previous_player_cant_move = True
                    print("Player ", player, " does not have any possible moves")


        if player == 2:
            clear_possible_moves_list()
            highlight_border_pieces()
            highlight_possible_moves()
            print("\nСледующий ход:", turn)
            print("Ходит игрок №", player)
            print_field()
            if len(possibleMoves) > 0:
                previous_player_cant_move = False
                ai_random_move()
                print("Сходил игрок №", player)
                clear_possible_moves_list()
                highlight_border_pieces()
                print_field()
                turn = turn + 1
                player = opponent()
            else:
                if previous_player_cant_move:
                    end_game()
                    break
                previous_player_cant_move = True
                print("Player ", player, " does not have any possible moves")

            #draw_board(field)

        pygame.display.update()
        clear_possible_moves_list()

for x in range(1):
    initialization()
    play()
