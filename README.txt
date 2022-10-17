Auteurs: Nicalos Do, Youness Dkhissi


Les points forts du joueur:
--------------------------
Ouvertures :
Les premiers coups de notre joueur se basent sur une bibliothèque d'ouverture issue du fichier games.json fourni sur Moodle.
Nous avons séparé les données de ce fichier en fonction du vainqueurs des parties et nous avons défini deux listes d'ouverture, une pour le côté blanc et une pour le côté noir.
Le joueur commence par choisir un coup parmi ceux proposés par la bibliothèque et il supprime de la bibliothèque toutes les parties qui ne commencent pas par ce coup.
Après que l'adversaire joue son coup, notre joueur enlève toutes les parties qui ne suivent pas la meme ouverture que le jeu actuel.
Ensuite, il  va répéter la meme procédure faite au premier coups jusqu'à ce que notre bibliothèque devient vide. 
Dans ce cas, le joueur va utiliser la méthode Iterative Deepening en se basant sur l'heuristique implémentée pour choisir son coups.

IterativeDeepening :
La méthode IterativeDeepening nous assure que le joueur ne va pas dépasser une certaine durée qu'on a choisi dans chaque coups.
La durée utilisée est de 15 secondes par tour, nous avons constaté que la majorité des parties que nous jouions ne dépassait pas plus de 60 coups par joueur.
L'avantage de cette méthode est qu'on explore progressivement des profondeurs avec alpha-beta si le temps nous le permet tout en ayant en permanence un coup de prêt à être joué.

L'heuristique :
Pour l'heuristique qu'on a choisi, on a essayé de faire en sorte qu'elle donne de l'importance au nombre de pièces de notre joueur, le nombre de pièces de l'adversaire qu'il a capturé
et donner plus d'importance au libertés des pièces.
Donc avec cette heuristique, notre joueur essaie de limiter la liberté des pieces du joueur adverse et augmenter la liberté de ses pièces. 
Aussi, notre heuristique pousse le joueur à capturer les pieces d'adversaire et essayer de protéger ses pièces.
On a donné plus d'importance au liberté des pièces dans l'heuristique parce qu'elle est un critère crucial pour gagner une partie de jeu GO.


Les points faibles du joueur:
--------------------------
La fonction d'évaluation utilisé est un peu trop coûteuse à cause de l'appel à count_area, ce qui nous empêche d'explorer très profond en début de partie (lorsque le nombre de coup légal est assez important).
De ce fait, la recherche de coup avec MiniMax est assez lente. Elle l'est moins avec alpha-beta puisqu'elle élague des parties de l'arbre des possibilités mais cela reste lent (d'où l'utilisation de IterativeDeepening).

