import matplotlib.pyplot as plt
from Environnement import *
from Controleur import *
from fonctions import *

'''-----------------------------------
-------Fichier main du projet---------
-----------------------------------'''


'''----------------------
------configuration------
----------------------'''

nb_pts = 500
duree_stim = 20.0
dt = duree_stim/float(nb_pts-1)

#position agent
xA = 0
yA = 0

#position cible
xS = -5
yS = 0

#constante raideur
k = 3.0
'''-------------------'''

#debut de la simulation
env = Environnement(nb_pts, duree_stim, xA, yA, xS, yS)
agent = Controleur(k)

#boucle de simulation
for i in range(nb_pts-1): 
  agent.update(env.y[i,0], env.theta_etoile()) #en parametres, respectivement : theta, theta etoile(deplacement angulaire desire)
  env.update(agent.output_u1, agent.output_u2, i)

#affichage
somme = 0
for i in range(nb_pts):
  somme += env.y[i,1]
  moyV = somme / float(nb_pts)


xdata = [env.y[i,0] for i in range(nb_pts)]

plt.plot(env.time, xdata)
plt.xlabel("temps (en s.)")
plt.ylabel("angle (en rad.)")

plt.show()




