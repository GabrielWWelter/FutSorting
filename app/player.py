import numpy as np;

MEAN_LIMIT = 0.1
STD_DEV_LIMIT = 0.3


class Player:
    
    def __init__(self, name,score:np.float64,position):
        self.name = name
        self.score = np.float64(str(score))
        self.position = position
    
    def editScore(self,new_score:np.float64):
        self.score = new_score
    
    def editPosition(self,new_Position):
        self.position = new_Position
    
class Team:
    def __init__(self):
        self.players = []
        self.scores = []
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
        return np.mean(self.scores)

    @property
    def median(self):
        return np.median(self.scores)
    
    @property
    def stdDevasion(self):
        return np.std(self.scores)
    
    @property
    def clear(self):
        self.players.clear()
        self.scores.clear()
        self.sts = 0
        self.mids = 0
        self.cbs = 0

    def add(self, *players: Player):
        for p in players:
            self.players.append(p)
            self.scores.append(p.score)
        

    def __repr__(self):
        
        names_scores = ", ".join(f"{p.name} {p.score:.2f}" for p in self.players)
        return f"Team(μ={self.mean:.2f}, σ={self.stdDevasion:.2f},players=[{names_scores}])"

class Match:
    #tira esse estrutura de dados e coloca o can_match_happen pro teamsort
    def __init__(self, team1:Team,team2:Team,delta_m:np.float64,delta_std:np.float64):
        self.team1 = team1
        self.team2 = team2
        self.delta_m = delta_m
        self.delta_std = delta_std

    def can_match_happen(self):
        if(self.delta_m <= MEAN_LIMIT and self.delta_std <= STD_DEV_LIMIT and (len(self.team1.players) == len(self.team2.players))):
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