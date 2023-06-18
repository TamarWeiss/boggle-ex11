from typing import Iterable, Generator

from consts import Path, Board, PathDict
from ex11_utils import board_coords, get_neighbors, get_word

class PathFinder:
    """create a class which will include the word sets and path dict"""

    def __init__(self, board: Board, words: Iterable[str]):
        # get words as a set, and subset of length 5 and 10 to filter useless paths
        self.board = board
        self.words = set(words)
        self.word_sets = self.check_set()
        self.words5, self.words10 = self.word_sets
        self.paths_dict: PathDict = {}

    def check_set(self) -> tuple[set[str], set[str]]:
        set5, set10 = set(), set()
        for word in self.words:
            if len(word) >= 10:
                set10.add(word[:10])
            if len(word) >= 5:
                set5.add(word[:5])
        return set5, set10

    def path_combinations(self, n=1) -> Generator[Path, any, any]:
        """for each step, get the current word, word checks if it is in the word set.
        if so, check if the word is already in my paths_dict, and if so, add the current path to its key
        as a list of tuples: {'word_1' : [[(location),(location)],[(location),location)]]}.
        so ultimately the values will be tuples, which contain tuples of tuples representing paths.
        also, if the current word is of length 5 or 10, check if its substring is in th e5 or 10 substring set.
        if not - that path ends. otherwise - carry on
        """
        if n < 2:
            for point in board_coords(self.board):
                yield [point]
        else:
            for curr_path in self.path_combinations(n - 1):
                for point in get_neighbors(curr_path[-1]):
                    if point not in curr_path:
                        new_path = curr_path + [point]
                        word = get_word(self.board, new_path)
                        if word in self.words:
                            curr_paths = self.paths_dict.get(word, [])
                            if new_path not in new_path:
                                curr_paths.append(new_path)
                            self.paths_dict[word] = curr_paths
                        if len(new_path) != 5 or word[:5] in self.words5 \
                                and len(new_path) != 10 or word[:10] in self.words10:
                            yield new_path

    def get_paths_dict(self) -> PathDict:
        return self.paths_dict