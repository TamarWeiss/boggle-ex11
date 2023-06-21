from typing import Iterable, Optional, Generator

from boggle_board_randomizer import BOARD_SIZE
from consts import Board, Path, Point, FILENAME, PathDict

def is_neighbor(point1: Point, point2: Point) -> bool:
    """checks whether two points are neighbors on a grid. returns true if so"""
    y1, x1 = point1
    y2, x2 = point2
    # check that different but that their coordinates within 1 of each other
    return point1 != point2 and abs(y2 - y1) < 2 and abs(x2 - x1) < 2

def get_word(board: Board, path: Path) -> str:
    """converts a path on the board to a word according to the letters at each location along the path.
    returns the word as a string"""
    return ''.join(board[y][x] for y, x in path)

def load_words(filename) -> list[str]:
    """load the word list from a file. return a list of strings representing the lines"""
    with open(filename) as file:
        return file.read().splitlines()

def board_coords(board: Board) -> Path:
    """create a list of tuples representing a list of all coordinates on the board"""
    return [(i, j) for i, row in enumerate(board) for j in range(len(row))]

def get_neighbors(point: Point) -> Path:
    """return a list of tuples of all neighbors within bounds"""
    in_bounds = lambda num: -1 < num < BOARD_SIZE
    y, x = point
    return [
        (i, j)
        for i in [y - 1, y, y + 1]
        for j in [x - 1, x, x + 1]
        if (i, j) != point and in_bounds(i) and in_bounds(j)  # don't add coordinates out of bounds
    ]

def path_combinations(board: Board, n=1) -> Generator[Path, any, any]:
    """returns a list of tuples representing all the possible paths of length n on a Boggle board."""
    # base: return all the points on the board
    if n < 2:
        return ([point] for point in board_coords(board))
    # adds every possible neighbor except those already in the path
    return (
        curr_path + [point]
        for curr_path in path_combinations(board, n - 1)
        for point in get_neighbors(curr_path[-1])
        if point not in curr_path
    )

def word_combinations(board: Board, n=1) -> list[Path]:
    """returns a list of tuples representing all the paths which give a word of length n in the dict."""
    paths: list[Path] = [[]]
    for i in range(n):
        new_paths = []
        for curr_path in paths:
            curr_word = get_word(board, curr_path)
            if len(curr_word) == n:
                new_paths.append(curr_path)
                continue

            # If not at the first iteration, get neighbors of the last point in the current path.
            # Otherwise, get all points from the board
            for point in get_neighbors(curr_path[-1]) if i else board_coords(board):
                next_path = curr_path + [point]
                next_word = get_word(board, next_path)

                # If this new word is too long or the point is already in the current path, continue
                if len(next_word) > n or point in curr_path:
                    continue
                new_paths.append(next_path)

            # If no new paths were added on this iteration, break the loop
            if paths == new_paths:
                break
        paths = new_paths
    return paths

def find_all_words(board: Board, words: Iterable[str]) -> PathDict:
    """write a generator comprehension which goes through the entire board"""
    # call the pathfinder object
    from path_finder import PathFinder
    cell_num = sum(len(row) for row in board)
    max_word_len = max(len(word) for word in words)
    # run until exhausted the board or all words in dict
    n = min(cell_num, max_word_len)
    finder = PathFinder(board, words)
    # Iterate over the generator to generate all paths
    for _ in finder.path_combinations(n):
        pass
    return finder.get_paths_dict()

# -----------------------------------------------------------------------------------

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """ checks if a word based on a path in Boggle board is in a list of words.
    if so, returns the word as string, otherwise returns None."""
    word = ''
    my_coords = board_coords(board)
    for i in range(len(path)):  # check if the path is consecutive
        # ensure the location in the path exists on the board
        if i != len(path) - 1 and not is_neighbor(path[i], path[i + 1]) or path[i] not in my_coords:
            return
        y, x = path[i]
        word += board[y][x]

    if word in set(words):  # check if the word is valid
        return word

def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> list[Path]:
    """returns a list of tuples representing all the
    possible paths of length n on a Boggle board, which represent words
    in the word list"""
    from path_finder import PathFinder
    path_finder = PathFinder(board, words)
    words = set(words)
    return [
        path for path in path_finder.path_combinations(n)
        if get_word(board, path) in words
    ]

def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> list[Path]:
    """returns a list of tuples representing all the possible paths of on a Boggle board,
    which represent words of length n in the word list"""
    words = set(words)
    return [
        path for path in word_combinations(board, n)
        if get_word(board, path) in words
    ]

def max_score_paths(board: Board, words: Iterable[str]) -> list[Path]:
    """get dict of all words and paths."""
    paths_dict = find_all_words(board, words)
    max_paths_dict = {word: max(paths, key=len) for word, paths in paths_dict.items()}
    return list(max_paths_dict.values())

# TEMPORARY. for debug purposes only.
if __name__ == '__main__':
    words = load_words(FILENAME)
    board = [
        ['T', 'H', 'Y', 'H'],
        ['H', 'I', 'L', 'T'],
        ['T', 'B', 'O', 'E'],
        ['B', 'A', 'N', 'QU']
    ]
    print(max_score_paths(board, words))