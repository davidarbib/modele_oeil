import matplotlib.pyplot as plt
from Environnement import *
from v_f_global import *
from nengo import *

'''-----------------------------------
-------Fichier main du projet---------
-----------------------------------'''

'''-------------------'''
'''
#debut de la simulation
env = Environnement(nb_pts, duree_stim, xA, yA, xS, yS)
agent = Controleur(k, dt)

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
'''


  
modele = Network(label = 'Modele_oeil')

with modele:
  #---Groupes de neurones---
  THETA = Ensemble(N, dimensions=1)
  PSI = Ensemble(N, dimensions=1)
  U1 = Ensemble(N, dimensions=1)
  U2 = Ensemble(N, dimensions=1)
  postA = Ensemble(N, dimensions=1)
  postB = Ensemble(N, dimensions=1)
  postC = Ensemble(N, dimensions=1)
  postD = Ensemble(N, dimensions=1)
  
  #---Entrees et fonctions---
  cib = Cible(xS, yS, dt)
  env = Environnement(xA, yA, dt)
  
  
  ENVIRONNEMENT = Node(env.step, size_in = 4, size_out = 2)
  CIBLE = Node(cib.posCible, size_out = 2)
  
  
  #---Connectique---
  Connection(ENVIRONNEMENT[0], PSI)
  Connection(ENVIRONNEMENT[1], THETA)
  
  Connection(U1, ENVIRONNEMENT[0])
  Connection(U2, ENVIRONNEMENT[1])
  
  Connection(PSI, postC, function=C)
  Connection(PSI, postD, function=D)
  Connection(THETA, postA, function=A)
  Connection(THETA, postB, function=B)
  
  Connection(postA, U1)
  Connection(postC, U1)
  Connection(postB, U2)
  Connection(postD, U2)
  
  Connection(CIBLE[0], ENVIRONNEMENT[2])
  Connection(CIBLE[1], ENVIRONNEMENT[3])
  
  test_probe = Probe(ENVIRONNEMENT[0])
  test_probe2 = Probe(ENVIRONNEMENT[1]) 

sim = Simulator(modele, dt)

sim.run(duree_sim)


#---Affichage---
plt.plot(sim.trange(), sim.data[test_probe])
plt.plot(sim.trange(), sim.data[test_probe2])
plt.ylim(-np.pi, np.pi)
plt.show()


