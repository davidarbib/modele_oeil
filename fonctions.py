#---fonctions utiles---



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
  
