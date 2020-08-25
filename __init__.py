from js_parser.jsparser import JSParser
from mongo_cursor import MongoCursor
from parser_cli import ParserCLI
from parser_controller import ParserController
js_parser = JSParser()
m_cursor = MongoCursor()
parser_controller = ParserController()
parser_cli = ParserCLI(js_parser, m_cursor, parser_cli)
parser_cli.cmdloop()
