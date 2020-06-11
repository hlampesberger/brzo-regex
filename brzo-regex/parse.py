from pyparsing import Literal, Word, OneOrMore, alphanums, alphas, printables, Optional, \
    Forward, ParseBaseException, Empty

from regex import *

def match(regex, strng):
    regex = regex.approximate()
    for a in strng:
        regex = regex.derivative(a)
        regex = regex.approximate()
    return regex.nullable()

symbol = Word(alphanums, exact=1)
symbol.leaveWhitespace()
symbol.setParseAction(lambda orig, loc, tok: Sym(tok[0]))

expression = Forward()

atom = symbol | Literal('(').suppress() + expression + Literal(')').suppress()
atom.leaveWhitespace()
# atom.setParseAction(lambda orig, loc, tok: Atom(tok[0]))

iteration = atom + Literal('*')
iteration.leaveWhitespace()
iteration.setParseAction(lambda orig, loc, tok: Rep(tok[0]))

factor = iteration | atom
factor.leaveWhitespace()
# factor.setParseAction(lambda orig, loc, tok: Factor(tok[0]))

term = Forward()

sequence = factor + term
sequence.leaveWhitespace()
sequence.setParseAction(lambda orig, loc, tok: Seq(tok[0], tok[1]))

term << (sequence | factor)
term.leaveWhitespace()
# term.setParseAction(lambda orig, loc, tok: Term(tok[0]))

choice = term + Literal('|') + expression
choice.leaveWhitespace()
choice.setParseAction(lambda orig, loc, tok: Alt(tok[0], tok[2]))

empty = Empty()
empty.leaveWhitespace()
empty.setParseAction(lambda orig, loc, tok: Epsilon())

expression << (choice | term | empty)
expression.leaveWhitespace()
# expression.setParseAction(lambda orig, loc, tok: Expression(tok[0]))


def parse(strng):
    return expression.parseString(strng, parseAll=True)[0]

