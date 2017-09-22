# use a playfair crib to develop a possible grid

class Grid:
    def __init__(self):
        self.grid = {}
        
    def addLetter(self, letter, pos):
        if letter in self.grid:
            del self.grid[ self.grid[letter] ]
            del self.grid[ letter ]
        self.grid[letter] = pos
        self.grid[pos] = letter
    
    def decrypt(self, l1, l2):
        pass
        
# a complete grid comprises a bijective map between letters and grid positions.
# a partial grid is much the same, but with a restricted 