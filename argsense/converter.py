import os
import re
import typing as t

from . import config
from .parser.args_parser import ParamType
from .parser.func_parser import T as T0


class T:
    ParamType1 = T0.PlainParamType  # literal
    ParamType2 = ParamType  # enum
    Style = t.Literal['grp', 'cmd', 'arg', 'opt', 'ext']


def args_2_cargs(*args, **kwargs) -> t.List[str]:
    """
    example:
        args_2_cargs(
            123, 'abc', True, False, None,
            aaa=456, bbb=True, ccc=False, ddd=None, eee='hello')
        -> ['123', 'abc', ':true', ':false', ':none', '--aaa', '456', '--bbb',
            '--not-ccc', '--ddd', ':none', '--eee', 'hello']
    """
    
    def value_2_cvalue(value: t.Any) -> str:
        if value is None:
            return ':none'
        elif value is True:
            return ':true'
        elif value is False:
            return ':false'
        else:
            return str(value)
    
    out = []
    for value in args:
        out.append(value_2_cvalue(value))
    for name, value in kwargs.items():
        out.append(name_2_cname(name, style='opt'))
        if isinstance(value, bool):
            if value is False:
                out[-1] = '--not-' + out[-1][2:]
        else:
            out.append(value_2_cvalue(value))
    return out


def name_2_cname(name: str, style: T.Style = None) -> str:
    """
    convert param name from python style to cli style.
    
    style   input       output (default)
    -----   ----------  ----------------
    arg     aaa_bbb     aaa-bbb
    arg     _aaa_bbb    aaa-bbb
    arg     __aaa_bbb   aaa-bbb
    arg     aaa_bbb_    aaa-bbb
    arg     aaa_bbb__   aaa-bbb
    opt     aaa_bbb     --aaa-bbb
    opt     _aaa_bbb    --aaa-bbb
    opt     __aaa_bbb   --aaa-bbb  # FIXME: maybe we should not show it in CLI?
    opt     ___aaa_bbb  --aaa-bbb
    opt     aaa_bbb_    --aaa-bbb
    opt     _aaa_bbb_   --aaa-bbb
    
    other styles follow the same rule with `arg`.
    
    note:
        the output is forced lower case, no matter what the case of `name` is.
    
    TODO:
        be careful using `xxx_`, `_xxx`, etc. in the same function. it produces
        duplicate cnames and causes unexpected behavior!
        we will add a checker in future version.
    """
    if name in ('*', '**'):
        return name
    name = name.lower().strip('_')
    if style == 'arg':
        style = config.ARG_NAME_STYLE
        if style == 'AAA_BBB':
            return name.upper()
        elif style == 'AAA-BBB':
            return name.upper().replace('_', '-')
        elif style == 'aaa_bbb':
            return name
        elif style == 'aaa-bbb':  # the default
            return name.replace('_', '-')
        elif style == 'AaaBbb':
            return name.replace('_', ' ').title().replace(' ', '')
        else:
            raise ValueError(f'unknown style: {style}')
    elif style == 'opt':
        return '--' + name.replace('_', '-')
    else:  # follow 'aaa-bbb' style
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


# -----------------------------------------------------------------------------

def cname_to_name(name: str) -> str:
    return name.replace('-', '_')


PYTHON_ACCEPTABLE_NUMBER_PATTERN = re.compile(
    r'^ *-?'
    r'(?:[0-9]+'
    r'|[0-9]*\.[0-9]+'
    r'|0b[01]+'
    r'|0x[0-9a-fA-F]+'
    r') *$'
)

SPECIAL_ARGS = {
    ':true' : True,
    ':false': False,
    # ':t': True,
    # ':f': False,
    ':none' : None,
    ':cwd'  : os.getcwd(),
}


def cval_to_val(value: str, type: ParamType) -> t.Any:
    if value in SPECIAL_ARGS:
        value = SPECIAL_ARGS[value]
    
    # print(':v', arg, type(arg), type, type(type))
    if isinstance(value, str):
        assert type in (
            ParamType.TEXT, ParamType.NUMBER, ParamType.ANY
        )
        if type == ParamType.TEXT:
            return value
        elif type == ParamType.NUMBER:
            assert PYTHON_ACCEPTABLE_NUMBER_PATTERN.match(value)
            return eval(value)
        else:
            if PYTHON_ACCEPTABLE_NUMBER_PATTERN.match(value):
                return eval(value)
            else:
                return value
    elif isinstance(value, bool):
        # warning: bool type is also an "int" type. so
        # `isinstance(True, int)` returns True.
        # to avoid this weird behavior, we must check
        # `isinstance(arg, bool)` before `isinstance(arg, int)`.
        assert type in (
            ParamType.FLAG, ParamType.BOOL, ParamType.ANY
        )
    elif isinstance(value, (int, float)):
        assert type in (
            ParamType.NUMBER, ParamType.ANY
        )
    elif value is None:
        assert type in (
            ParamType.ANY,
        )
    
    return value
