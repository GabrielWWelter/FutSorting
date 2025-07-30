
from pathlib import Path
from typing import List
from player import player 
from player import team
from itertools import combinations, product


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


def sort_teams(goalkeepers, strikers, mids, cbs, top_n=5):

    if len(goalkeepers) < 2:
        raise ValueError("Precisam existir ao menos 2 goleiros.")
    gk_best, gk_worst = goalkeepers[1], goalkeepers[0]
   
    def split_by_count(pos_list):
        n = len(pos_list)
        k_opts = {n // 2, n // 2 + (n % 2)}  
        for k in k_opts:
            for idxs in combinations(range(n), k):
                t1 = [pos_list[i] for i in idxs]
                t2 = [p for i, p in enumerate(pos_list) if i not in idxs]
                yield t1, t2

    splits_str = list(split_by_count(strikers))
    splits_mid = list(split_by_count(mids))
    splits_cb  = list(split_by_count(cbs))

    solutions = []
    for (t1_st, t2_st), (t1_mid, t2_mid), (t1_cb, t2_cb) in product(
            splits_str, splits_mid, splits_cb):

        team1 = team(); team2 = team()
        team1.add(gk_best,  *t1_st, *t1_mid, *t1_cb)
        team2.add(gk_worst, *t2_st, *t2_mid, *t2_cb)

        diff = abs(team1.mean - team2.mean)
        solutions.append((diff, team1, team2))

    solutions.sort(key=lambda x: x[0])
    return solutions[:top_n]
    





players_list = get_players("app/players.txt")
goalkeepers,strikers,midfielders,centerbacks = distribute_postion(players_list)
best_solution = sort_teams(goalkeepers,strikers,midfielders,centerbacks)
for diff, t1, t2 in best_solution:
    print(f"\nDiferença entre médias de times = {diff:.3f}")
    print("T1:", t1)
    print("T2:", t2)