''' 
In this example we solve the Poisson equation over an L-shaped domain 
with fixed boundary conditions. We use the multiquadratic RBF (*mq*) 
with a shape parameter that scales inversely with the average nearest 
neighbor distance.
'''
import numpy as np
from rbf.basis import mq
from rbf.geometry import contains
from rbf.nodes import menodes,neighbors
import matplotlib.pyplot as plt

# Define the problem domain with line segments.
vert = np.array([[0.0,0.0],[2.0,0.0],[2.0,1.0],
                 [1.0,1.0],[1.0,2.0],[0.0,2.0]])
smp = np.array([[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]])
N = 500 # total number of nodes
nodes,smpid = menodes(N,vert,smp) # generate nodes
edge_idx, = (smpid>=0).nonzero() # identify edge nodes
interior_idx, = (smpid==-1).nonzero() # identify interior nodes
dx = np.mean(neighbors(nodes,2)[1][:,1]) # avg. distance to nearest neighbor
eps = 0.5/dx  # shape parameter
# create "left hand side" matrix
A = np.empty((N,N))
A[interior_idx]  = mq(nodes[interior_idx],nodes,eps=eps,diff=[2,0])
A[interior_idx] += mq(nodes[interior_idx],nodes,eps=eps,diff=[0,2])
A[edge_idx] = mq(nodes[edge_idx],nodes,eps=eps)
# create "right hand side" vector
d = np.empty(N)
d[interior_idx] = -1.0 # forcing term
d[edge_idx] = 0.0 # boundary condition
# Solve for the RBF coefficients
coeff = np.linalg.solve(A,d) 
# interpolate the solution on a grid
xg,yg = np.meshgrid(np.linspace(-0.05,2.05,400),np.linspace(-0.05,2.05,400))
points = np.array([xg.flatten(),yg.flatten()]).T                    
u = mq(points,nodes,eps=eps).dot(coeff) # evaluate at the interp points
u[~contains(points,vert,smp)] = np.nan # mask outside points
ug = u.reshape((400,400)) # fold back into a grid
# make a contour plot of the solution
fig,ax = plt.subplots()
p = ax.contourf(xg,yg,ug,np.linspace(0.0,0.16,9),cmap='viridis')
ax.plot(nodes[:,0],nodes[:,1],'ko',markersize=4)
for s in smp:
  ax.plot(vert[s,0],vert[s,1],'k-',lw=2)

ax.set_aspect('equal')
fig.colorbar(p,ax=ax)
fig.tight_layout()
plt.savefig('../figures/basis.a.png')
plt.show()

