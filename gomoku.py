def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res




def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))



def is_empty(board):
    for i in board:
        for l in i:
            if l != " ":
                return False
    return True

def is_bounded(board, y_end,x_end, length,d_y,d_x):
    open_at_end = True
    open_at_start = True
    rows = len(board)
    cols = rows
    y_end_next = y_end + d_y   #the sequence one after the end
    x_end_next = x_end + d_x
    y_start = y_end
    x_start = x_end
    for i in range(length-1):
        y_start -= d_y
        x_start -= d_x
    y_start_before = y_start - d_y
    x_start_before = x_start - d_x #the sequebce one before the start
    if not (0 <= y_end_next <= rows-1 and 0 <= x_end_next <= cols-1):
        open_at_end = False
    elif board[y_end_next][x_end_next] == " ":
        open_at_end = True
    else:
        open_at_end = False

    if not (0 <= y_start_before <= rows-1 and 0 <= x_start_before <= cols-1):
        open_at_start = False
    elif board[y_start_before][x_start_before] == " ":
        open_at_start = True
    else:
        open_at_start = False

    if open_at_end and open_at_start:
        return "OPEN"
    elif open_at_end or open_at_start:
        return "SEMIOPEN"
    else:
        return "CLOSED"

def in_bounds(board, y, x):
    n = len(board)
    return 0 <= y < n and 0<=x<n

def detect_row(board,col,y_start,x_start,length,d_y,d_x):
    open_seq = 0
    semi_seq = 0
    y = y_start
    x = x_start
    seq_length = 0
    for i in range(len(board)):
        if not in_bounds(board,y,x):
            break
        if board[y][x] == col:
            seq_length += 1
        else:                              #if not same colour, the new sequence begins at length zero
            seq_length = 0
        next_in   = in_bounds(board, y + d_y, x + d_x)
        next_same = next_in and board[y + d_y][x + d_x] == col

        if seq_length == length and not next_same:  #next stone has to not be the same colour
            status = is_bounded(board, y,x, length,d_y,d_x)
            if status == "OPEN":
                open_seq +=1
            elif status == "SEMIOPEN":
                semi_seq +=1
        elif seq_length == length and next_same:  #if next stone is the same colour, must modify y and x until the stone is a different colour
            while in_bounds(board,y,x) and board[y][x]== col:
                y += d_y
                x += d_x
            seq_length = 0
            continue
        y += d_y
        x += d_x
    return (open_seq,semi_seq)


def detect_rows(board,col,length):
    b = len(board)
    open_num = 0
    semi_open_num = 0
    for i in range(b):
        open, semi_open = detect_row(board, col, i,0,length,0,1)
        open_num += open
        semi_open_num += semi_open
    for i in range(b):
        open,semi_open = detect_row(board, col, 0 , i , length, 1, 0)
        open_num += open
        semi_open_num += semi_open
    for i in range(b):
        open,semi_open = detect_row(board, col, 0,i,length,1,1)
        open_num += open
        semi_open_num += semi_open
    for i in range(1,b):
        open,semi_open = detect_row(board, col, i,0,length,1,1)
        open_num += open
        semi_open_num += semi_open
    for i in range(1,b):
        open,semi_open = detect_row(board, col, 0,i,length,1,-1)
        open_num += open
        semi_open_num += semi_open
    for i in range(b-1):
        open,semi_open = detect_row(board, col, i,b-1,length,1,-1)
        open_num += open
        semi_open_num += semi_open

    return (open_num,semi_open_num)


def empty_list(board):
    emp_list = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                emp_list.append((i,j))
    return emp_list

def search_max(board):
    new_board = []
    for i in board:
        new_board.append(i.copy())
    empty = empty_list(board)
    max_score = -100000000000000000000
    max_play = (0,0)
    for i in range(len(empty)):
        y,x = empty[i]
        new_board[y][x] = "b"
        if score(new_board) >= max_score:
            max_score = score(new_board)
            max_play = (y,x)
        new_board[y][x] = " "
    return max_play

def padded_board(board):
    n = len(board)
    empty_row = [" "]*(n+1)
    new_board = [empty_row.copy()]
    for row in board:
        new_board.append(row+ [" "])
    return new_board




def is_win(board):
    padded = padded_board(board)
    open_seq_white,semi_seq_white = detect_rows(padded,"w",5)
    white_win = open_seq_white + semi_seq_white
    open_seq_black,semi_seq_black = detect_rows(padded,"b",5)
    black_win = open_seq_black + semi_seq_black

    if white_win > 0:
        return "White won"
    elif black_win > 0:
        return "Black won"
    elif empty_list(board) == []:
        return "Draw"
    else:
        return "Continue playing"




def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    for i in range(length):
        if board[y_start][x_start] != col:
            return False
        y_start += d_y
        x_start += d_x
    return True


if __name__ == "__main__":
    board = make_empty_board(8)
    board[2][1]= "b"
    board[2][6] = "b"
    print_board(board)
    print(is_empty(board))
    put_seq_on_board(board, 2,2,0,1,4,"w")
    print_board(board)
    print(is_sequence_complete(board, "w",3, 4, 4, 0, 1))
    print(is_bounded(board,2,5,4,0,1))

    play_gomoku(8)















