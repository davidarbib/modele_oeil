import numpy as np
from nengo import *
from fonctions import *

'''-----------------------------------
-----Entite etat mental de l'agent----
-----------------------------------'''

class Controleur :
  
  '''----------------------
  --------Attributs--------
  ----------------------'''
  input_psi   = 0
  input_theta = 0
  
  output_u1 = 0
  output_u2 = 0
  
  k = 0
  theta1 = np.pi/2.0
  theta2 = -1*np.pi/2.0
  
  #Neural config
  net = 0
  N = 1000
  
  #simulation
  dt = 0
  sim = 0
  
  #recup valeurs
  probe_u1 = 0
  probe_u2 = 0
  
  #calcul des valeurs A, B, C et D
  def _A(self,x):
    return (self.k*self.theta2)/(2*(self.theta2-self.theta1)) - self.k*(x/(self.theta2-self.theta1))
    
  def _B(self,x):
    return (self.k*self.theta1)/(2*(self.theta1-self.theta2)) - self.k*(x/(self.theta1-self.theta2))
      
  def _C(self,x):
    return (self.k*self.theta2)/(2*(self.theta2-self.theta1)) - self.k*(x/(self.theta2-self.theta1))
  
  def _D(self,x):
    return (self.k*self.theta1)/(2*(self.theta1-self.theta2)) - self.k*(x/(self.theta1-self.theta2)) 
      
  '''--------------------------
  --------Constructeur---------
  --------------------------'''
  def __init__(self, k, dt):
    self.k = k
    self.dt = dt
    
    #creation du reseau de neurones
    self.net = Network(label = 'agent')     
    with self.net:
      self.THETA = Ensemble(self.N, dimensions=1)
      self.PSI = Ensemble(self.N, dimensions=1)
      self.U1 = Ensemble(self.N, dimensions=1)
      self.U2 = Ensemble(self.N, dimensions=1)
      self.postA = Ensemble(self.N, dimensions=1)
      self.postB = Ensemble(self.N, dimensions=1)
      self.postC = Ensemble(self.N, dimensions=1)
      self.postD = Ensemble(self.N, dimensions=1)
      self.AC = Ensemble(self.N*2, dimensions=2)
      self.BD = Ensemble(self.N*2, dimensions=2)	
      self.input_THETA = Node(self.input_theta)
      self.input_PSI = Node(self.input_psi)
      Connection(self.input_THETA, self.THETA)
      Connection(self.input_PSI, self.PSI)
      
      Connection(self.PSI,self.postC,function=self._C)
      Connection(self.PSI,self.postD,function=self._D)
      Connection(self.THETA,self.postA,function=self._A)
      Connection(self.THETA,self.postB,function=self._B)
      
      Connection(self.postA,self.AC[0])
      Connection(self.postB,self.BD[0])
      Connection(self.postC,self.AC[1])
      Connection(self.postD,self.BD[1])
      
      Connection(self.AC,self.U1,function=add)
      Connection(self.BD,self.U2,function=add)
      
      self.probe_u1 = Probe(self.U1)
      self.probe_u2 = Probe(self.U2)
      
      self.sim = Simulator(self.net, self.dt) 
      
    
    
    '''--------------------
    --------Methodes-------
    --------------------'''
    '''
    #calcul des valeurs A, B, C et D
    def _ABCD(self):
    a = (self.k*self.theta2)/(2*(self.theta2-self.theta1)) - self.k*(self.input_theta/(self.theta2-self.theta1))
    b = (self.k*self.theta1)/(2*(self.theta1-self.theta2)) - self.k*(self.input_theta/(self.theta1-self.theta2))
    c = (self.k*self.theta2)/(2*(self.theta2-self.theta1)) - self.k*(self.input_psi/(self.theta2-self.theta1))
    d = (self.k*self.theta1)/(2*(self.theta1-self.theta2)) - self.k*(self.input_psi/(self.theta1-self.theta2))
    return [a, b, c, d]
    
    #MaJ de l'agent (version de base)
    def update(self, theta, theta_etoile):
    self.input_psi = theta_etoile - theta
    self.input_theta = theta
    self.output_u1 = self._ABCD()[0] + self._ABCD()[2]
    self.output_u2 = self._ABCD()[1] + self._ABCD()[3]
    '''
   
  #MaJ de l'agent (version avec nengo)
  def update(self, theta, theta_etoile):
    self.input_psi = theta_etoile - theta
    self.input_theta = theta
    
    self.sim.run_steps(1, False)
    
    temp_u1= self.sim.data[self.probe_u1]
    temp_u2= self.sim.data[self.probe_u2]
    self.output_u1 = temp_u1[0]
    print temp_u1
    self.output_u2 = temp_u2[0]