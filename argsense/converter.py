import typing as t

from . import config
from .argparse import ParamType
from .parser.func_parser import T as T0

__all__ = ['name_2_cname', 'type_2_ctype']


class T:
    ParamType1 = T0.ParamType
    ParamType2 = ParamType
    Style = t.Literal['grp', 'cmd', 'arg', 'opt', 'ext']


def name_2_cname(name: str, style: T.Style = None) -> str:
    """ convert param name from python style to cli style. """
    name = name.lower().strip('_')
    if style == 'arg':
        style = config.ARG_NAME_STYLE
        if style == 'AAA_BBB':
            return name.upper()
        elif style == 'AAA-BBB':
            return name.upper().replace('_', '-')
        elif style == 'aaa_bbb':
            return name
        elif style == 'aaa-bbb':
            return name.replace('_', '-')
        elif style == 'AaaBbb':
            return name.replace('_', ' ').title().replace(' ', '')
        else:
            raise ValueError(f'unknown style: {style}')
    elif style == 'opt':
        return '--' + name.replace('_', '-')
    else:
        return name.replace('_', '-')


def type_2_ctype(t: T.ParamType1) -> T.ParamType2:
    """
    related:
        from: [./parser/func_parser.py : def parse_function()]
        to: [./argparse/parser.py : def parse_argv()]
    """
    return {
        'any'  : ParamType.ANY,
        'str'  : ParamType.TEXT,
        'float': ParamType.NUMBER,
        'flag' : ParamType.FLAG,
        'bool' : ParamType.BOOL,
        'int'  : ParamType.NUMBER,
        'list' : ParamType.LIST,
        'tuple': ParamType.LIST,
        'set'  : ParamType.LIST,
        'dict' : ParamType.DICT,
        'none' : ParamType.NONE,
    }.get(t, ParamType.ANY)
