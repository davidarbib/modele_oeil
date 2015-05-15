import numpy as np
from fonctions import *

'''-----------------------------------------------------------
---Entite regroupant l'agent et ses effecteurs et la cible----
-----------------------------------------------------------'''

class Environnement:
  
  '''---------------------
  -------Attributs--------
  ---------------------'''
  
  #masse (systeme masse-ressort)
  m = 0
  
  #position et vitesse
  p_theta = 0.0
  v_theta = 0.0
  
  #angles max gauche et droite
  theta1 = np.pi/2.0
  theta2 = -1*np.pi/2.0
  
  #tension des ressorts (muscle gauche et muscle droit, respectivement)
  u1 = 0
  u2 = 0
  
  #amortissement
  a = 0
  
  #Tableau des etats  
  y = 0
      
  #position de l'agent dans l'environnement
  xA = 0
  yA = 0
  
  #position de la cible
  xS = 0
  yS = 0
      
  '''----------------------
  ------Constructeur-------
  ----------------------'''
  
  def __init__(self, nb_pts, duree_stim, ag_x, ag_y, cib_x, cib_y, eff_m = 0.05, eff_u1 = 1, eff_u2 = 1, eff_a = 2, p_theta = 0.0, v_theta = 0.0):
    '''Classe Environnement : entite qui regroupe l'agent, la cible et leurs proprietes
    (attention : certaines proprietes nexisteront plus en version de stimulation live)
    '''
    
    self.xA = ag_x
    self.yA = ag_y
    self.xS = cib_x
    self.yS = cib_y
    self.m  = eff_m
    self.u1 = eff_u1 
    self.u2 = eff_u2
    self.a  = eff_a
        
    self.y = np.zeros([nb_pts,2])
    
    #vecteur temporel
    self.time = np.linspace(0, duree_stim, nb_pts)
    
    self.nb_pts = nb_pts
    self.duree_stim = duree_stim
    self.dt = duree_stim/float(nb_pts)
    
    #init de la dynamique
    self.y[0,0] = p_theta
    self.y[0,1] = v_theta
  
  '''----------------------
  --------Methodes---------
  ----------------------'''
  
  #Forces (muscle gauche et muscle droit, respectivement)
  def _F1(self, theta):
    return (self.theta1 - theta)*self.u1
    
  def _F2(self, theta):
    return (self.theta2 - theta)*self.u2
  
  #Position angulaire de la cible
  def theta_etoile(self):
      ySA = self.yS-self.yA
      if ySA==0:
	ySA = 0.0000000000000000000000000000001
      return np.arctan((self.xA-self.xS)/ySA)
      
  #fct update de l'angle
  def _up_theta(self, state, t):
    g0 = state[1]
    g1 = (self._F1(state[0])+self._F2(state[0])-self.a*state[1])/self.m
    return np.array([g0, g1])
  
  #calcul du mouvement de l'oeil
  def _calcul(self, i):
    self.y[i+1] = rk4(self.y[i], self.time[i], self.dt, self._up_theta)
    return self.y 
  
  #update de l'environnement  
  def update(self, eff_u1, eff_u2, i):
    self.u1 = eff_u1
    self.u2 = eff_u2
    self._calcul(i)
    
 