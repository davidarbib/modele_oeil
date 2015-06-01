import numpy as np
'''----------------------
------configuration------
----------------------'''

#param de simulation
nb_pts = 500
duree_sim = 2.0
dt = duree_sim/float(nb_pts-1)

#nombre de neurones
N = 200

#position agent
xA = 0
yA = 0

#position cible
xS = -5
yS = 0

#Masse
m = 0.05

#Frottement
a = 1

#constante de raideur
k = 2.0

#bornes angulaires
theta1 = np.pi/2.0
theta2 = -1*np.pi/2.0

#tension de depart
u1 = 1.0
u2 = 1.0

#pos et vitesse de depart
p_theta = 0.0
v_theta = 0.0

#scaling
skl = 100

'''------------------------
--------fonctions----------
------------------------'''

#integration selon Euler
def euler(y, t, dt, derivs):
  y_next = y + derivs(y,t) * dt
  return y_next

#integration Runge Kutta d'ordre 4
def rk4(y, t, dt, derivs):
  k0 = dt * derivs(y, t)
  k1 = dt * derivs(y+0.5*k0, t+0.5*dt)
  k2 = dt * derivs(y+0.5*k1, t+0.5*dt)
  k3 = dt * derivs(y+k2, t*dt)
  y_next = y + (k0 + 2*k1 + 2*k2 + k3)/6
  return y_next

def add(x):
  return x[0]+x[1]

def multlist(a, k):
  for i in range(len(a)):
    a[i] = a[i]*k
  return a
  
#calcul des valeurs A, B, C et D
def A(x):
  return (-1*k/(theta2-theta1))*x
    
def B(x):
  return (-1*k/(theta1-theta2))*x
      
def C(x):
  return (k/(theta2-theta1))*x

def D(x):
  return (k/(theta1-theta2))*x
  
def Y(x):
  return (k*theta2/(theta2-theta1))*x
  
def Z(x):
  return (k*theta1/(theta1-theta2))*x