from markdown.preprocessors import Preprocessor
from collections import OrderedDict
import re

STYLE_COMMAND = 'style'
REGEX_COMMAND = 'regex'
MATCH_COMMAND = 'match'
FORMAT_COMMAND = 'format'
DEFAULT_COMMANDS = [REGEX_COMMAND, MATCH_COMMAND, STYLE_COMMAND, FORMAT_COMMAND, 'new_line', 'whitespace', 'wildcard']

class StylePreprocessor(Preprocessor):
    '''
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Markdown parser class.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'style'
        self.pattern = self.processors]['pattern']
        self.strings = self.processors]['strings']
        self.rules = StylePreprocessor.compile_rules(self.processors]['rules'])
        #self.extension = ext

    def test(self, lines):
        '''All documents always need to be processed.

        Args:
            lines: A string of Markdown text.
        Returns:
            True
        '''
        return True

    def run(self, lines):
        doc = '\n'.join(lines)

        for rule, commands in self.rules.items():
            command, args = commands[0], commands[1:]
            if command == STYLE_COMMAND:
                q = []
                for command in commands[1:]:
                    pass

    @staticmethod
    def apply_rule(rule, input):
        pass

    @staticmethod
    def compile_rules(rules):
        # NTS: Needs ordering of rules
        rules = OrderedDict()

        new_line_command = re.compile('\n')
        whitespace_command = re.compile('[\s]+')
        wildcard_command = re.compile('.', flags=re.DOTALL)

        rules['new_line'] = ['match', lambda string: new_line_command.match(string)]
        rules['whitespace'] = ['match', lambda string: whitespace_command.match(string)]
        rules['wildcard'] = ['match', lambda string: wildcard_command.match(string)]

        'regex': lambda args: lambda string: re.compile(args[0]).match(string) is not None

        for rule, command_string in rules.items():
            if rule.startswith('_'):
                raise("Rule names cannot start with underscore, reserved for match enforcing.")

            # NTS: Future add support for many brackets
            commands = break_up_source(command_string)
            rules[rule] = compile_rule(commands)

        # Validate rules

        return rules

    @staticmethod
    def compile_rule(commands):
        command, args = commands[0], commands[1:]

        if isinstance(command, list):
            raise Exception("First argument must be a command.")

        # Compile Arguments too

        if command == STYLE_COMMAND:
            return commands
        elif command == REGEX_COMMAND:
            if isinstance(args[0], list):
                # Compile rest of list
                rules[rule] = commands
            compiled_command = lambda string: re.compile(string).match(string) is not None
        else:
            raise Exception("Command not recognised, {0} must be either {1} or {2}.". format(command, REGEX_COMMAND, STYLE_COMMAND))

    @staticmethod
    def break_up_source(command_string):
        commands = []
        previous = []
        current = commands

        i = 0
        opening_parentheses = 0
        close_parentheses = 0

        if command_string[0] != '(' and command_string[-1] != ')':
            raise Exception('Missing opening and closing parentheses.')
        command_string = command_string[1:-1]

        while i < len(command_string):
            if command_string[i] == '(':
                opening_parentheses += 1
                current.append([])
                previous.append(current)
                current = current[-1]
                i += 1
            elif command_string[i] == ')':
                close_parentheses += 1
                if len(previous) == 0:
                    raise Exception('Close parenthesis before opening.')
                current = previous.pop()
                i += 1
            elif command_string[i] != ' ':
                string = ''
                in_literal = False
                while i < len(command_string) and (in_literal or command_string[i] not in ' ()'):
                    if not in_literal and command_string[i] == '"':
                        in_literal = True
                    elif in_literal and command_string[i] == '"' and command_string[i-1] != '\\':
                        in_literal = False
                    else:
                        string += command_string[i]
                    i += 1
                current.append(string)
            else:
                i += 1

        if opening_parentheses != close_parentheses:
            extra = "More opening than closing." if opening_parentheses > close_parentheses else "More closing than opening."
            raise Exception('Parentheses don\'t match. {0}'.format(extra))
        return commands
