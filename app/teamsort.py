
from pathlib import Path
from typing import List
from player import Player 
from player import Team
from player import Match
from itertools import combinations

def get_players(file_path: str | Path, *, has_header: bool = True) -> List[Player]:
   
    players: List[Player] = []

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
            players.append(Player(name, score_str, pos))
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


def split_by_count(pos_list):
        n = len(pos_list)
        k_opts = {n // 2, n // 2 + (n % 2)}  
        for k in k_opts:
            for idxs in combinations(range(n), k):
                t1 = [pos_list[i] for i in idxs]
                t2 = [p for i, p in enumerate(pos_list) if i not in idxs]
                yield t1, t2
    

def best_possible(gks, sts, mids, cbs):

    if len(gks) < 2:
        raise ValueError("Precisam existir ao menos 2 goleiros.")
    solution = []
    splits_str = list(split_by_count(sts))
    splits_mid = list(split_by_count(mids))
    splits_cb  = list(split_by_count(cbs))
    sort_teams(gks,splits_str,splits_mid,splits_cb,solution)
    solution.sort(key=lambda m: m.delta_m)
    return solution

 
def sort_teams(gks,splits_str,splits_mid,splits_cb,solution):
    
    for(t1st,t2st) in splits_str:
        for(t1mid,t2mid) in splits_mid:
            for(t1cb,t2cb) in splits_cb:
                team1 = Team(); team2 = Team()
                team1.add(gks[1],*t1st, *t1mid, *t1cb)
                team2.add(gks[0],*t2st, *t2mid, *t2cb)
                team1.calculate_pos()  
                team2.calculate_pos()
                delta_m = abs(team1.mean - team2.mean)
                delta_std = abs(team1.stdDevasion - team2.stdDevasion)
                current_match = Match(team1,team2,delta_m,delta_std)
                if (current_match.can_match_happen()):
                    solution.append(current_match)
    


players_list = get_players("app/players.txt")
goalkeepers,strikers,midfielders,centerbacks = distribute_postion(players_list)
solution = best_possible(goalkeepers,strikers,midfielders,centerbacks)
for matches in solution:
    print(f"\nΔμ = {matches.delta_m:.5f}")
    print(f"\nΔσ = {matches.delta_std:.5f}")
    print("\nT1:", matches.team1)
    print("\nT2:", matches.team2)