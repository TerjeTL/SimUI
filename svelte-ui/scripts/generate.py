#!/usr/bin/env python
"""Generate simdata.ts from sim_ui/simdata.py — called by npm prebuild."""
import importlib.util
import typing
from pathlib import Path
from typing import Any

_root = Path(__file__).parent.parent.parent
TS_OUT = Path(__file__).parent.parent / 'src' / 'simdata.ts'

_spec = importlib.util.spec_from_file_location('simdata', _root / 'sim_ui' / 'simdata.py')
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]
Frame = _mod.Frame


def to_ts(tp: Any) -> str:
    if tp is str:           return 'string'
    if tp is bool:          return 'boolean'
    if tp in (int, float):  return 'number'
    if getattr(tp, '__name__', None) == 'ndarray': return 'number[]'
    origin = typing.get_origin(tp)
    args   = typing.get_args(tp)
    if origin is tuple:
        return '[' + ', '.join(to_ts(a) for a in args) + ']'
    if origin is list:
        return f'{to_ts(args[0])}[]'
    if origin is typing.Union:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return f'{to_ts(non_none[0])} | undefined'
    if origin is typing.Literal:
        return ' | '.join(f"'{a}'" for a in args)
    return 'unknown'


def generate() -> str:
    hints = typing.get_type_hints(Frame)
    fields = '\n'.join(f'  {name}: {to_ts(tp)}' for name, tp in hints.items())
    return f'// auto-generated from Frame — do not edit\nexport interface SimData {{\n{fields}\n}}\n'


if __name__ == '__main__':
    TS_OUT.write_text(generate())
    print(f'generated {TS_OUT.relative_to(_root)}')
