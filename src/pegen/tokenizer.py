import token
import tokenize
from typing import Dict, Iterator, List, Set

Mark = int  # NewType('Mark', int)


def shorttok(tok: tokenize.TokenInfo) -> str:
    return "%-25.25s" % f"{tok.start[0]}.{tok.start[1]}: {token.tok_name[tok.type]}:{tok.string!r}"


class Tokenizer:
    """Caching wrapper for the tokenize module.

    This is pretty tied to Python's syntax.
    """

    _tokens: List[tokenize.TokenInfo]

    def __init__(self, tokengen: Iterator[tokenize.TokenInfo], *, verbose: bool = False):
        self.exact_token_types = token.EXACT_TOKEN_TYPES.copy()
        self._tokengen = tokengen
        self._tokens = []
        self._index = 0
        self._verbose = verbose
        self._keywords: Dict[str, int] = dict()
        if verbose:
            self.report(False, False)

    def getnext(self) -> tokenize.TokenInfo:
        """Return the next token and updates the index."""
        cached = True
        while self._index == len(self._tokens):
            tok = next(self._tokengen)
            if tok.type in (tokenize.NL, tokenize.COMMENT):
                continue
            if tok.type == token.ERRORTOKEN and tok.string.isspace():
                continue
            self._tokens.append(self.update_token_type(tok))
            cached = False
        tok = self._tokens[self._index]
        self._index += 1
        if self._verbose:
            self.report(cached, False)
        return tok

    def peek(self) -> tokenize.TokenInfo:
        """Return the next token *without* updating the index."""
        while self._index == len(self._tokens):
            tok = next(self._tokengen)
            if tok.type in (tokenize.NL, tokenize.COMMENT):
                continue
            if tok.type == token.ERRORTOKEN and tok.string.isspace():
                continue
            self._tokens.append(self.update_token_type(tok))
        return self._tokens[self._index]

    def diagnose(self) -> tokenize.TokenInfo:
        if not self._tokens:
            self.getnext()
        return self._tokens[-1]

    def mark(self) -> Mark:
        return self._index

    def install_keyword_handling(self, keywords: Dict[str, int]) -> None:
        self._keywords = keywords
        self.exact_token_types.update(keywords)

    def update_token_type(self, tok: tokenize.TokenInfo) -> tokenize.TokenInfo:
        if tok.type == tokenize.NAME and tok.string in self._keywords:
            tok = tokenize.TokenInfo(
                type=self._keywords[tok.string],
                string=tok.string,
                start=tok.start,
                end=tok.end,
                line=tok.line
            )
        return tok

    def reset(self, index: Mark) -> None:
        if index == self._index:
            return
        assert 0 <= index <= len(self._tokens), (index, len(self._tokens))
        old_index = self._index
        self._index = index
        if self._verbose:
            self.report(True, index < old_index)

    def report(self, cached: bool, back: bool) -> None:
        if back:
            fill = "-" * self._index + "-"
        elif cached:
            fill = "-" * self._index + ">"
        else:
            fill = "-" * self._index + "*"
        if self._index == 0:
            print(f"{fill} (Bof)")
        else:
            tok = self._tokens[self._index - 1]
            print(f"{fill} {shorttok(tok)}")
