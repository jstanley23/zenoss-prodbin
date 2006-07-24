# Begin -- grammar generated by Yapps
import sys, re
import yapps.yappsrt as yappsrt

class WhereClauseScanner(yappsrt.Scanner):
    patterns = [
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ("'not'", re.compile('not')),
        ("'like'", re.compile('like')),
        ('"or"', re.compile('or')),
        ('"and"', re.compile('and')),
        ('[ \r\t\n]+', re.compile('[ \r\t\n]+')),
        ('END', re.compile('$')),
        ('NUM', re.compile('[0-9]+')),
        ('VAR', re.compile('[a-zA-Z0-9_]+')),
        ('BIN', re.compile('>=|<=|==|=|<|>|!=|<>')),
        ('STR', re.compile('"([^\\\\"]+|\\\\.)*"')),
        ('STR2', re.compile("'([^\\\\']+|\\\\.)*'")),
    ]
    def __init__(self, str):
        yappsrt.Scanner.__init__(self,None,['[ \r\t\n]+'],str)

class WhereClause(yappsrt.Parser):
    Context = yappsrt.Context
    def goal(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'goal', [])
        andexp = self.andexp(_context)
        END = self._scan('END')
        return andexp

    def andexp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'andexp', [])
        orexp = self.orexp(_context)
        e = orexp
        while self._peek('"and"', 'END', '"\\\\)"') == '"and"':
            self._scan('"and"')
            orexp = self.orexp(_context)
            e = ('and', e, orexp)
        if self._peek() not in ['"and"', 'END', '"\\\\)"']:
            raise yappsrt.SyntaxError(charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(['"and"', 'END', '"\\\\)"']))
        return e

    def orexp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'orexp', [])
        binary = self.binary(_context)
        e = binary
        while self._peek('"or"', '"and"', 'END', '"\\\\)"') == '"or"':
            self._scan('"or"')
            binary = self.binary(_context)
            e = ('or', e, binary)
        if self._peek() not in ['"or"', '"and"', 'END', '"\\\\)"']:
            raise yappsrt.SyntaxError(charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(['"or"', '"and"', 'END', '"\\\\)"']))
        return e

    def binary(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'binary', [])
        term = self.term(_context)
        e = term
        while self._peek('BIN', "'like'", "'not'", '"or"', '"and"', 'END', '"\\\\)"') in ['BIN', "'like'", "'not'"]:
            _token = self._peek('BIN', "'like'", "'not'")
            if _token == 'BIN':
                BIN = self._scan('BIN')
                term = self.term(_context)
                e = (BIN, e, term)
            elif _token == "'like'":
                self._scan("'like'")
                term = self.term(_context)
                e = ('like', e, term)
            else: # == "'not'"
                self._scan("'not'")
                self._scan("'like'")
                term = self.term(_context)
                e = ('not like', e, term)
        if self._peek() not in ['BIN', "'like'", "'not'", '"or"', '"and"', 'END', '"\\\\)"']:
            raise yappsrt.SyntaxError(charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(['BIN', "'like'", "'not'", '"or"', '"and"', 'END', '"\\\\)"']))
        return e

    def term(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'term', [])
        _token = self._peek('NUM', 'VAR', 'STR', 'STR2', '"\\\\("')
        if _token == 'NUM':
            NUM = self._scan('NUM')
            return int(NUM)
        elif _token == 'VAR':
            VAR = self._scan('VAR')
            return VAR
        elif _token == 'STR':
            STR = self._scan('STR')
            return STR
        elif _token == 'STR2':
            STR2 = self._scan('STR2')
            return STR2
        else: # == '"\\\\("'
            self._scan('"\\\\("')
            andexp = self.andexp(_context)
            self._scan('"\\\\)"')
            return andexp


def parse(rule, text):
    P = WhereClause(WhereClauseScanner(text))
    return yappsrt.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
