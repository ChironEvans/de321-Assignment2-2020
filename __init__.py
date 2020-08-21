from js_parser.jsparser import JSParser
from parser_cli import ParserCLI
js_parser = JSParser()
parser_cli = ParserCLI(js_parser)
parser_cli.cmdloop()
