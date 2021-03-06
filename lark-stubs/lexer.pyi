# -*- coding: utf-8 -*-

from typing import (
    TypeVar, Type, Tuple, List, Dict, Iterator, Collection, Callable, Optional,
    Pattern as REPattern,
)
from abc import abstractmethod, ABC

_T = TypeVar('_T')


class Pattern(ABC):
    value: str
    flags: Collection[str]

    def __init__(self, value: str, flags: Collection[str] = ...):
        ...

    @property
    @abstractmethod
    def type(self) -> str:
        ...

    @abstractmethod
    def to_regexp(self) -> str:
        ...

    @property
    @abstractmethod
    def min_width(self) -> int:
        ...

    @property
    @abstractmethod
    def max_width(self) -> int:
        ...


class PatternStr(Pattern):
    type: str = ...

    def to_regexp(self) -> str:
        ...

    @property
    def min_width(self) -> int:
        ...

    @property
    def max_width(self) -> int:
        ...


class PatternRE(Pattern):
    type: str = ...

    def to_regexp(self) -> str:
        ...

    @property
    def min_width(self) -> int:
        ...

    @property
    def max_width(self) -> int:
        ...


class TerminalDef:
    name: str
    pattern: Pattern
    priority: int

    def __init__(self, name: str, pattern: Pattern, priority: int = ...):
        ...


class Token(str):
    type: str
    pos_in_stream: int
    value: str
    line: int
    column: int
    end_line: int
    end_column: int
    end_pos: int

    def update(self, type_: Optional[str] = None, value: Optional[str] = None) -> Token:
        ...

    @classmethod
    def new_borrow_pos(cls: Type[_T], type_: str, value: str, borrow_t: Token) -> _T:
        ...


_Callback = Callable[[Token], Token]


class Lexer(ABC):
    lex: Callable[..., Iterator[Token]]


class TraditionalLexer(Lexer):
    terminals: Collection[TerminalDef]
    ignore_types: List[str]
    newline_types: List[str]
    user_callbacks: Dict[str, _Callback]
    callback: Dict[str, _Callback]
    mres: List[Tuple[REPattern, Dict[int, str]]]

    def __init__(
        self,
        terminals: Collection[TerminalDef],
        ignore: Collection[str] = ...,
        user_callbacks: Dict[str, _Callback] = ...
    ):
        ...

    def build(self) -> None:
        ...

    def match(self, stream: str, pos: int) -> Optional[Tuple[str, str]]:
        ...

    def lex(self, stream: str) -> Iterator[Token]:
        ...


class ContextualLexer(Lexer):
    lexers: Dict[str, TraditionalLexer]
    root_lexer: TraditionalLexer

    def __init__(
        self,
        terminals: Collection[TerminalDef],
        states: Dict[str, Collection[str]],
        ignore: Collection[str] = ...,
        always_accept: Collection[str] = ...,
        user_callbacks: Dict[str, _Callback] = ...
    ):
        ...

    def lex(self, stream: str, get_parser_state: Callable[[], str]) -> Iterator[Token]:
        ...
