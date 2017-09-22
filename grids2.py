# playfair grid generator from crib

class Grid:
    def __init__(self):
        self.positions = {} 
        self.letters = {}
    
    def getPositionOf(self, letter):
        if letter in self.positions:
            return self.positions[letter]
        else:
            return None # raise?
    
    def getLetterAt(self, position):
        if position in self.letters:
            return self.letters[position]
        else:
            return "?"
    
    def addLetterAt(self, letter, position):
        if letter in self.positions:
            del self.positions[letter]
        if position in self.letters:
            del self.letters[position]
        
        self.letters[position] = letter # sanity check on bounds?
        self.positions[letter] = position
        
    def decryptPair(self, p):
        p1, p2 = p

        if p1 in self.positions:
            x1, y1 = self.positions[p1]
        else:
            return "??"
        if p2 in self.positions:
            x2, y2 = self.positions[p2]
        else:
            return "??"
        if x1 == x2:
            return self.getLetterAt((x1,(y1+1)%5)) + self.getLetterAt ((x2,(y2+1)%5))
        elif y1 == y2:
            return self.getLetterAt(((x1+1)%5, y1)) + self.getLetterAt (((x2+1)%5, y2))
        else:
            return self.getLetterAt( (x2, y1)) + self.getLetterAt((x1, y2))
        
    def decrypt(self, s):
        s = s.replace(" ", "") 
        out = ""
        while s:
            out += self.decryptPair(s[:2])
            s = s[2:]
        
        
    
        