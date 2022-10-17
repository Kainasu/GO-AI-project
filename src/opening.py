import json

with open('games.json') as mon_fichier:
    data = json.load(mon_fichier)
black_openings = []
white_openings =  []
for opening in data:
    if opening['winner'] == 'W':
        white_openings.append(opening["moves"])
    elif opening['winner'] == 'B':
        black_openings.append(opening["moves"])

print("Black openings")
print(black_openings)
print("##############################################")
print("White openings")
print(white_openings)
