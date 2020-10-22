from abc import ABCMeta, abstractmethod
from re import sub, findall, search, split

from js_parser.searcher_template import SearcherTemplate


class Searcher(SearcherTemplate):
    def __init__(self, search_string, clean_string=''):
        super().__init__(search_string, clean_string)

    def find_matches(self, input_str):
        self.matches = []
        self.js_input = input_str
        self.remove_comments_blocks_fixed()
        self.get_matches_override()
        if len(self.matches) > 0:
            return self.matches
        return None

    def get_matches_override(self):
        matches_raw = findall(self.search_criteria, self.js_input)
        matches_cleaned = set([])
        for match in matches_raw:
            matches_cleaned.add(match.replace(self.clean_string, ''))
        for cleaned_match in matches_cleaned:
            self.matches.append(cleaned_match)


