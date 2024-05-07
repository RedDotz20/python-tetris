
#* Updating Score
def update_score(nscore):
    score = max_score()
    with open('scores.txt', 'w', encoding="utf=8") as f:
        f.write(str(score) if int(score) > nscore else str(nscore))

#* Updating Max Scores
def max_score():
    with open('scores.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

#* Constant Scores per Milestones
def calculate_score(milestone):
    milestones = {1: 10, 2: 20, 3: 30, 4: 40}
    return milestones.get(milestone, 50)


#* Constant Fall Speed per Milestones
def calculate_fall_speed(milestone):
    fall_speeds = {1: 0.35, 2: 0.3, 3: 0.2, 4: 0.1}
    return fall_speeds.get(milestone, 0.08)
