
from pathlib import Path
from typing import List
from player import player 
from player import team
from player import match
from itertools import combinations, product
import copy 

def get_players(file_path: str | Path, *, has_header: bool = True) -> List[player]:
   
    players: List[player] = []

    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    if has_header:
        lines = lines[1:]  

    for n, line in enumerate(lines, start=2 if has_header else 1):
       
        parts = line.strip().split()
        if len(parts) != 3:
            print(f"  Linha {n} ignorada (esperava 3 colunas): {line.rstrip()}")
            continue

        name, score_str, pos = parts
        try:
            players.append(player(name, score_str, pos))
        except Exception as e:
            print(f"  Erro na linha {n}: {e} -> {line.rstrip()}")

    return players

def distribute_postion(players_list:list):
    goalkeepers = []
    strikers = []
    midfielders = []
    centerbacks = []
    
    for p in players_list:
        if p.position == "GOL":
            goalkeepers.append(p)
        elif p.position == "ATA":
            strikers.append(p)
        elif p.position == "MEIO":
            midfielders.append(p)
        elif p.position == "ZAG":
            centerbacks.append(p)

    goalkeepers = sorted(goalkeepers, key=lambda p: p.score)
    strikers = sorted(strikers, key=lambda p: p.score)
    midfielders = sorted(midfielders, key=lambda p: p.score)
    centerbacks = sorted(centerbacks, key=lambda p: p.score)
    return goalkeepers,strikers,midfielders,centerbacks

    
def best_possible(gks, sts, mids, cbs):

    if len(gks) < 2:
        raise ValueError("Precisam existir ao menos 2 goleiros.")
    gk_best, gk_worst = gks[1], gks[0]
    t1 = team()
    t2 = team()
    t1.add(gk_best)
    t2.add(gk_worst)
    players1 = 0
    players2 = 0
    solution = []
    
    for i in range (0,len(sts)):
        if i % 2 == 0:
            t1.add(sts[i])
            players1+=1
        else: 
            t2.add(sts[i])
            players2+=1
    
    if(players1>players2):
        for i in range (0,len(mids)):
            if i % 2 == 0:
                t2.add(mids[i])
                players1+=1
            else: 
                t1.add(mids[i])
                players2+=1
    else:
        for i in range (0,len(mids)):
            if i % 2 == 0:
                t1.add(mids[i])
                players1+=1
            else: 
                t2.add(mids[i])
                players2+=1
    if(players1>players2):
        for i in range (0,len(cbs)):
            if i % 2 == 0:
                t2.add(cbs[i])
                players1+=1
            else: 
                t1.add(cbs[i])
                players2+=1
    else:
        for i in range (0,len(cbs)):
            if i % 2 == 0:
                t1.add(cbs[i])
                players1+=1
            else: 
                t2.add(cbs[i])
                players2+=1

    delta_m = abs(t1.mean - t2.mean)
    solution.append(match(t1,t2,delta_m))  
    sort_teams(t1,t2,solution)
    solution.sort(key=lambda m: m.delta_m)
    return solution

 
def sort_teams(tbase1:team,tbase2:team,solution):
    size_of_team = 7
    
    for i in range(1,size_of_team):
        for j in range(1,size_of_team):
            team1 = copy.deepcopy(tbase1)
            team2 = copy.deepcopy(tbase2)
            pt1 = team1.players[i]
            pt2 = team2.players[j]
            team1.players[i] = pt2
            team2.players[j] = pt1
            team1.calculate_pos()
            team2.calculate_pos()
            delta_m = abs(team1.mean - team2.mean)
            current_match = match(team1,team2,delta_m)
            if (current_match.can_match_happen()):
                solution.append(match(team1,team2,delta_m))


                
    
            
            


players_list = get_players("app/players.txt")
goalkeepers,strikers,midfielders,centerbacks = distribute_postion(players_list)
solution = best_possible(goalkeepers,strikers,midfielders,centerbacks)
for matches in solution:
    print(f"\nDiferença entre médias de times = {matches.delta_m}")
    print("T1:", matches.team1)
    print("T2:", matches.team2)
