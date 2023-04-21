"""
TODO:
    currently, the following options are defined but not used:
        ALIGN_ARGS_AND_OPTS_FIELD_WIDTH
        FALLBACK_TO_HELP_IF_ARGPARSE_FAILED
        FALLBACK_TYPE
        PRETTY_ERROR
        USE_RICH_MARKUP
"""


class T:
    from typing import Literal
    ArgNameStyle = Literal['AAA_BBB', 'AAA-BBB', 'aaa_bbb', 'aaa-bbb', 'AaaBbb']
    FallbackType = Literal['any', 'str']
    OverwrittenScheme = Literal['first', 'last']
    TitleHeadStyle = Literal['system_dependent', 'fixed']


# appearance style
ALIGN_ARGS_AND_OPTS_FIELD_WIDTH = False
ARG_NAME_STYLE: T.ArgNameStyle = 'aaa-bbb'
PRETTY_ERROR = True
TITLE_HEAD_STYLE: T.TitleHeadStyle = 'system_dependent'
''' the difference:
        system      system_dependent    fixed
        ------      ----------------    -----
        unix        python3             python
        unix        python3 -m          python -m
        windows     py                  python
        windows     py -m               python -m
        windows     xxx.exe             xxx.exe
'''
USE_RICH_MARKUP = True

# fallback
BARE_NONE_MEANS_ANY = False
FALLBACK_TYPE: T.FallbackType = 'str'
#   see [./parser/func_parser.py : def parse_function()]
FALLBACK_DESC = '[dim]no description[/]'
''' suggested:
        <empty string>
        [dim]no description[/]
        [dim]there is no description provided.[/]
    see also: [./cli.py : def show2() : def show()]
'''
FALLBACK_TO_HELP_IF_ARGPARSE_FAILED = False
#   see [./argparse/argv.py : class ArgvVendor : def report()]
OVERWRITTEN_SCHEME: T.OverwrittenScheme = 'last'

# console related
WARNING_IF_RUNNING_ON_PYCHARM_CONSOLE = False
CONSOLE_WIDTH: int = 0


# dynamic settings
class Dynamic:
    PREFERRED_FIELD_WIDTH_OF_NAME = 0
    PREFERRED_FIELD_WIDTH_OF_TYPE = 6  # the length of 'NUMBER'


def apply_changes():
    if CONSOLE_WIDTH == 0:
        from .console import console
        rulers = (80, 100, 120, 200)
        for x in reversed(rulers):
            if console.width > x:
                console.width = x
                break
