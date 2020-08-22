from js_parser.jsparser import JSParser
from mongo_cursor import MongoCursor
from parser_cli import ParserCLI
js_parser = JSParser()
m_cursor = MongoCursor()
parser_cli = ParserCLI(js_parser)
parser_cli.cmdloop()