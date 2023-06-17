from typing import Generator, Iterable, Optional

from boggle_board_randomizer import BOARD_SIZE

Board = list[list[str]]
Point = tuple[int, int]
Path = list[Point]

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
    paths = [[point] for point in board_coords(board)]

    for iteration in range(n):
        new_paths = []
        for curr_path in paths:
            curr_word = get_word(board, curr_path)
            if len(curr_word) == n:
                new_paths.append(curr_path)
                continue

            for point in get_neighbors(curr_path[-1]):
                next_path = curr_path + [point]
                next_word = get_word(board, next_path)
                if len(next_word) > n or point in curr_path:
                    continue
                new_paths.append(next_path)
            if paths == new_paths:
                break
        paths = new_paths
    return paths

def find_all_words(board: Board, words: Iterable[str]):
    """write a generator comprehension which does through board (4 by 4)."""
    from path_finder import PathFinder
    cell_num = sum(len(row) for row in board)
    max_word_len = max(len(word) for word in words)
    n = min(cell_num, max_word_len)
    finder = PathFinder(board, words)
    for _ in finder.path_combinations(n):  # Iterate over the generator to generate all paths
        pass
    return finder.get_paths_dict()

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

def max_score_paths(board: Board, words: Iterable[str]) -> list[Path]:
    """
    get dict of all words and paths.
    for each word, find the longest path (filter? reduce?)
    then add the path to the final list and add the word to a set
    """
    paths_dict = find_all_words(board, words)

    max_paths_dict = {
        word: max(paths, key=len) for word, paths in paths_dict.items()
    }
    return [list(path) for path in max_paths_dict.values()]

# TEMPORARY. for debug purposes only.
if __name__ == '__main__':
    words = load_words('boggle_dict.txt')
    board = [
        ['T', 'H', 'Y', 'E'],
        ['H', 'I', 'L', 'T'],
        ['T', 'Q', 'U', 'O'],
        ['B', 'A', 'N', 'QU']
    ]
    # pprint(board)
    # paths = [(get_word(board, path), path) for path in find_length_n_paths(7, board, words)]
    # print(len(paths), paths)
    # paths2 = [(get_word(board, path), path) for path in find_length_n_words(7, board, words)]
    # print(len(paths2), paths2)
    # TODO: Does not return the expected paths. Try again
    print(max_score_paths(board, words))