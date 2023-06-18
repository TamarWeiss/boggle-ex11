from pprint import pprint
from typing import Generator, Iterable, Optional

from boggle_board_randomizer import BOARD_SIZE
from consts import Board, Path, Point, FILENAME

def is_neighbor(point1: Point, point2: Point) -> bool:
    y1, x1 = point1
    y2, x2 = point2
    return point1 != point2 and abs(y2 - y1) < 2 and abs(x2 - x1) < 2

def get_word(board: Board, path: Path) -> str:
    return ''.join(board[y][x] for y, x in path)

def load_words(filename) -> list[str]:
    with open(filename) as file:
        return file.read().splitlines()

def board_coords(board: Board) -> Path:
    return [(i, j) for i, row in enumerate(board) for j in range(len(row))]

def get_neighbors(point: Point):
    in_bounds = lambda num: -1 < num < BOARD_SIZE
    y, x = point
    return [
        (i, j)
        for i in [y - 1, y, y + 1]
        for j in [x - 1, x, x + 1]
        if (i, j) != point and in_bounds(i) and in_bounds(j)
    ]

def path_combinations(board: Board, n=1) -> Generator[Path, any, any]:
    if n < 2:
        return ([point] for point in board_coords(board))
    return (
        curr_path + [point]
        for curr_path in path_combinations(board, n - 1)
        for point in get_neighbors(curr_path[-1])
        if point not in curr_path
    )

def word_combinations(board: Board, n=1):
    paths = [[]]
    for i in range(n):
        new_paths = []
        for curr_path in paths:
            curr_word = get_word(board, curr_path)
            if len(curr_word) == n:
                new_paths.append(curr_path)
                continue

            for point in get_neighbors(curr_path[-1]) if i else board_coords(board):
                next_path = curr_path + [point]
                next_word = get_word(board, next_path)
                if len(next_word) > n or point in curr_path:
                    continue
                new_paths.append(next_path)

            if paths == new_paths:
                break
        paths = new_paths
    return paths

# -----------------------------------------------------------------------------------

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    word = ''
    for i in range(len(path)):  # check if the path is consecutive
        if i != len(path) - 1 and not is_neighbor(path[i], path[i + 1]):
            return
        y, x = path[i]
        word += board[y][x]

    if word in set(words):  # check if the word is valid
        return word

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> list[Path]:
    words = set(words)
    return [
        path for path in path_combinations(board, n)
        if get_word(board, path) in words
    ]

def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> list[Path]:
    words = set(words)
    return [
        path for path in word_combinations(board, n)
        if get_word(board, path) in words
    ]

# rough draft. HIGHLY unoptimised and slow. has yet to filter out paths with the same word.
def max_score_paths(board: Board, words: Iterable[str]) -> list[Path]:
    cell_num = sum(len(row) for row in board)
    max_word_len = max(len(word) for word in words)
    n = min(cell_num, max_word_len)
    for i in range(n, 0, -1):
        print(i)  # here just to keep track of how long it takes
        paths = find_length_n_paths(i, board, words)
        if paths:
            return list({get_word(board, path): path for path in paths}.values())

# much faster in execution. relies on a wonky assumption that there are words of len i for all the range
def max_score_paths2(board: Board, words: Iterable[str]) -> list[Path]:
    cell_num = sum(len(row) for row in board)
    max_word_len = max(len(word) for word in words)
    min_word_len = min(len(word) for word in words)
    n = min(cell_num, max_word_len)
    max_paths = []
    for i in range(min_word_len, n):
        paths = find_length_n_paths(i, board, words)
        if not paths: break
        max_paths = paths
    return list({get_word(board, path): path for path in max_paths}.values())

# TEMPORARY. for debug purposes only.
if __name__ == '__main__':
    words = load_words(FILENAME)
    board = [
        ['T', 'H', 'Y', 'H'],
        ['H', 'I', 'L', 'T'],
        ['T', 'B', 'O', 'E'],
        ['B', 'A', 'N', 'QU']
    ]
    pprint(board)
    paths = [(get_word(board, path), path) for path in find_length_n_paths(6, board, words)]
    print(len(paths), paths)
    paths2 = [(get_word(board, path), path) for path in find_length_n_words(7, board, words)]
    print(len(paths2), paths2)
    max_paths = [(get_word(board, path), path) for path in max_score_paths2(board, words)]
    print(len(max_paths), max_paths)