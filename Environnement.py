import numpy as np
from v_f_global import *

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
  
  def __init__(self, ag_x, ag_y, dt, eff_m, eff_u1, eff_u2, eff_a, p_theta, v_theta):
    '''Classe Environnement : entite qui regroupe l'agent, la cible et leurs proprietes
    (attention : certaines proprietes nexisteront plus en version de stimulation live)
    '''
    
    self.xA = ag_x
    self.yA = ag_y
    self.m  = eff_m
    self.u1 = eff_u1 
    self.u2 = eff_u2
    self.a  = eff_a
        
    self.y= np.zeros([1,2])   #variable d'etat de la dynamique

    self.dt = dt
    
    #init de la dynamique
    self.y[0, 0] = p_theta
    self.y[0, 1] = v_theta
    
    self.psitheta = []
    self.tab_vtheta = []
  
  '''----------------------
  --------Methodes---------
  ----------------------'''
  
  #Forces (muscle gauche et muscle droit, respectivement)
  def _F1(self, theta):
    return (theta1 - theta)*self.u1
    
  def _F2(self, theta):
    return (theta2 - theta)*self.u2
  
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
  
  #fct appelee par rna
  def step(self, t, x):
    self.u1 = x[0]*skl
    self.u2 = x[1]*skl
    self.xS = x[2]
    self.yS = x[3]
    
    #print "avant :", self.y[0]
    self.y[0] = list(euler(self.y[0], t, self.dt, self._up_theta))
    #print "apres :", self.y[0]
    
    psi = self.theta_etoile() - self.y[0, 0]    
    theta = self.y[0, 0]
    vtheta = self.y[0, 1]
    
    self.tab_vtheta.append(vtheta)
    print [t, self.theta_etoile(), theta, vtheta]
    #self.psitheta.append([psi, theta])
    
    return [psi/skl, theta/skl]


class Cible:
  
  xS = 0
  yS = 0
  dt = 0
  
  def __init__(self, xS, yS, dt):
    self.xS = xS
    self.yS = yS
    
  
  def posCible(self, t):
    '''
    if t >= duree_sim/2:  #au milieu de la simulation : cible droit devant
      self.xS = 0
      self.yS = 2
    '''
    return [self.xS, self.yS]
 