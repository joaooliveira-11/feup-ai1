class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for -: 'Position' and '{}'".format(type(other).__name__))
        
    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +: 'Position' and '{}'".format(type(other).__name__))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError("Unsupported operand type for ==: 'Position' and '{}'".format(type(other).__name__))
        
    def __hash__(self):
        return hash((self.x, self.y))