import pygame

# UPDATING SCORES
def update_score(nscore):
    score = max_score()
    with open('scores.txt', 'w', encoding="utf=8") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

# UPDATING MAX SCORE
def max_score():
    with open('scores.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score