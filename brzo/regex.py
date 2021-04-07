from abc import abstractmethod, ABCMeta

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class Regex(metaclass=ABCMeta):
    @abstractmethod
    def derivative(self, char): pass
    @abstractmethod
    def nullable(self): pass
    def __repr__(self):
        return f"{self.__cls_.__name__}()"
    def approximate(self):
        return self
    
class Terminal(Regex):
    def __init__(self, value):
        self.value = value
    def __hash__(self):
        return hash(self.value)
    def __repr__(self):
        return f"{self.__cls_.__name__}({repr(self.value)})"
    def __eq__(self, other):
        if isinstance(other, Terminal):
            return self.value == other.value
        else:
            return False

class UnaryRegex(Regex):
    def __init__(self, child):
        self.child = child
    def __hash__(self):
        return hash(self.child)
    def __repr__(self):
        return f"{self.__cls_.__name__}({repr(self.child)})"
    def __eq__(self, other):
        if isinstance(other, UnaryRegex):
            return self.child == other.child
        else:
            return False        

class BinaryRegex(Regex):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __hash__(self):
        return hash((self.left, self.right))
    def __repr__(self):
        return f"{self.__cls_.__name__}({repr(self.left)}, {repr(self.right)})"
    def __eq__(self, other):
        if isinstance(other, BinaryRegex):
            return self.left == other.left and self.right == other.right
        else:
            return False    
    
    
class EmptySet(Singleton, Regex):
    def derivative(self, char):
        return EmptySet()
    def nullable(self):
        return False
    def __str__(self):
        return "∅"
    
class Epsilon(Singleton, Regex):
    def derivative(self, char):
        return EmptySet()
    def nullable(self):
        return True
    def __str__(self):
        return "ε"
    
class Sym(Terminal):
    def derivative(self, char):
        if char == self.value:
            return Epsilon()
        else:
            return EmptySet()
    
    def nullable(self):
        return False
    def __str__(self):
        return self.value

    
class Alt(BinaryRegex):
    def derivative(self, char):
        return Alt(self.left.derivative(char), self.right.derivative(char))
    
    def nullable(self):
        return self.left.nullable() or self.right.nullable()
    
    def approximate(self): # simplify
        left = self.left.approximate()
        right = self.right.approximate()
        if left == right:
            return left
        if left is EmptySet():
            return right
        if right is EmptySet():
            return left
        return Alt(left, right)
    
    def __str__(self):
        return f"({self.left}|{self.right})"
        

    
class Seq(BinaryRegex):
    def derivative(self, char):
        if self.left.nullable():
            return Alt(Seq(self.left.derivative(char), self.right), self.right.derivative(char))
        else:
            return Seq(self.left.derivative(char), self.right)
    
    def nullable(self):
        return self.left.nullable() and self.right.nullable()

    def approximate(self):
        left = self.left.approximate()
        right = self.right.approximate()
        if left is EmptySet() or right is EmptySet():
            return EmptySet()
        if left is Epsilon(): return right
        if right is Epsilon(): return left
        return Seq(left, right)
    
    def __str__(self):
        return f"{str(self.left)}{str(self.right)}"
    
    
class Rep(UnaryRegex):
    def derivative(self, char):
        return Seq(self.child.derivative(char), Rep(self.child))
    
    def nullable(self):
        return True   

    def approximate(self):
        if isinstance(self.child, Rep):
            return self.child.approximate()
        else:
            return Rep(self.child.approximate())

    def __str__(self):
        if isinstance(self.child, Terminal):
            return f"{str(self.child)}*"
        else:
            return f"({str(self.child)})*"

