from decimal import Decimal
from collections import Counter

class player:
    
    def __init__(self, name,score:Decimal,position):
        self.name = name
        self.score = Decimal(str(score))
        self.position = position
    
    def editScore(self,new_score:Decimal):
        self.score = new_score
    
    def editPosition(self,new_Position):
        self.position = new_Position
    
class team:
    def __init__(self):
        self.players = []
        self.sts = 0
        self.mids = 0
        self.cbs = 0

    def calculate_pos(self):
        
        for p in self.players:
            if p.position == "ATA":
                self.sts+=1
            elif p.position == "MEIO":
                self.mids+=1
            elif p.position == "ZAG":
                self.cbs+=1
        
    @property
    def score_sum(self):
        return sum(p.score for p in self.players)

    @property
    def mean(self):
        return self.score_sum / len(self.players) if self.players else Decimal(0)

    @property
    def counts(self):
        return Counter(p.position for p in self.players)

    def add(self, *players: player):
        self.players.extend(players)

    def __repr__(self):
        names = ", ".join(p.name for p in self.players)
        return f"Team(mean={self.mean:.2f}, players=[{names}])"

class match:
    
    def __init__(self, team1:team,team2:team,delta_m:Decimal):
        self.team1 = team1
        self.team2 = team2
        self.delta_m = Decimal(str(delta_m))

    def can_match_happen(self):
        if(self.delta_m <= 0.3):
            return True
        else:
            return False
                
"""

t1 = team()
t2 = team()
t1.add_player(p1)
t1.add_player(p2)
t1.add_player(p3)
t1.add_player(p4)
t2.add_player(p5)
t2.add_player(p6)
t2.add_player(p7)
t2.add_player(p8)

"""