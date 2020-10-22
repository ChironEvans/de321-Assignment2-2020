from abc import ABCMeta, abstractmethod
from re import sub, findall, search, split


class SearcherTemplate(metaclass=ABCMeta):
    def __init__(self, search_string, clean_string=''):
        self.search_criteria = search_string
        self.js_input = ''
        self.matches = []
        self.clean_string = clean_string

    def find_matches(self, input_str):
        self.matches = []
        self.js_input = input_str
        self.remove_comments_blocks_fixed()
        self.get_matches_override()
        if len(self.matches) > 0:
            return self.matches
        return None

    def remove_comments_blocks_fixed(self):
        self.js_input = sub("/\*(.|\n)*\*/", '', self.js_input)
        self.js_input = sub("#.*", '', self.js_input)

    @abstractmethod
    def get_matches_override(self):
        raise NotImplementedError()
