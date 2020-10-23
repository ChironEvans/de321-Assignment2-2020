from re import sub, findall, search, split
from js_parser.searcher_template import SearcherTemplate


class Splitter(SearcherTemplate):
    def __init__(self, search_string, split_string):
        super().__init__(search_string)
        self.split = []
        self.split_string = split_string

    def find_matches(self, input_str):
        self.matches = []
        self.split = []
        self.js_input = input_str
        self.remove_comments_blocks_fixed()
        self.get_matches_override()
        if len(self.split) > 0:
            return self.split
        return None

    def get_matches_override(self):
        js_match_raw = findall(self.search_criteria, self.js_input)
        for match in js_match_raw:
            match = search(self.search_criteria, match)
            s = match.start()
            e = match.end()
            match = match.string[s:e]
            match = match.split(" ")[1]
            if match not in self.matches:
                self.matches.append(match)
        js_file_for_split = sub(self.search_criteria, f"filjjndfs789er45jkngdrijouerga890e4jndr{self.split_string}",
                                self.js_input)
        js_file_split = split("filjjndfs789er45jkngdrijouerga890e4jndr", js_file_for_split)
        for item in js_file_split:
            if item[0:5] == "class":
                self.split.append(item)
