import numpy as np
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

  '''--------------------------
  --------Constructeur---------
  --------------------------'''
  def __init__(self, k):
    self.k = k

  '''--------------------
  --------Methodes-------
  --------------------'''

  #calcul des valeurs A, B, C et D
  def _ABCD(self):
    a = (self.k*self.theta2)/(2*(self.theta2-self.theta1)) - self.k*(self.input_theta/(self.theta2-self.theta1))
    b = (self.k*self.theta1)/(2*(self.theta1-self.theta2)) - self.k*(self.input_theta/(self.theta1-self.theta2))
    c = (self.k*self.theta2)/(2*(self.theta2-self.theta1)) - self.k*(self.input_psi/(self.theta2-self.theta1))
    d = (self.k*self.theta1)/(2*(self.theta1-self.theta2)) - self.k*(self.input_psi/(self.theta1-self.theta2))
    return [a, b, c, d]
  
  def update(self, theta, theta_etoile):
    self.input_psi = theta_etoile - theta
    self.input_theta = theta
    self.output_u1 = self._ABCD()[0] + self._ABCD()[2]
    self.output_u2 = self._ABCD()[1] + self._ABCD()[3]