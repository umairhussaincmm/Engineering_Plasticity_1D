import numpy as np
import matplotlib.pyplot as pt

# Material data
E=200.0
K=0 #E/4.0
H=0.2*E
sigy=1e-3*E
n=2000 # no of steps

# Initialising data storage vectors
e=np.zeros(n) #total strain
t=np.zeros(n) #time step
sig=np.zeros(n) #stress
epn=np.zeros(n) #plastic strain
alp=np.zeros(n) #back stress
de=np.zeros(n) # change in strain
#sigt=np.zeros(n)
#alpt=np.zeros(n)
dp=np.zeros(n) #dissipated energy

#Initial conditions
e[0]=t[0]=sig[0]=alp[0]=epn[0]=0.0

#Sgn function
def sgn(f):
	if f<0:
		return -1
	else:
		return 1

t=np.linspace(0,10,n) #initialising time steps to t=10
e=0.002*np.sin(2*np.pi*t) #initialising strain at each time step


for i in range(len(t)-1):
	dlam=0.0
	de[i]=e[i+1]-e[i] # total strain increment
	dsigt=E*de[i] # trial stress increment
	sigt=sig[i]+dsigt # trial stress
	alpt=alp[i] #trial back stress (same as last step)
	bett=sigt-alpt # trial effective stress
	# checking yield criteria
	if abs(bett)-sigy<=0: # not yielded
		sig[i+1]=sigt
		alp[i+1]=alpt
		epn[i+1]=epn[i]
		depn=epn[i+1]-epn[i]
		dp[i+1]=sig[i+1]*depn
	if abs(bett)-sigy>0: # yielded
		dlam=(abs(sigt-alpt)-sigy)/(E+K+H) # change in plastic arc length
		depn=dlam*sgn(bett) # change in plastic strain
		epn[i+1]=epn[i]+depn
		dsig=dsigt-E*depn
		sig[i+1]=sig[i]+dsig
		dp[i+1]=sig[i+1]*depn
		sigy=sigy+H*dlam
		alp[i+1]= K*epn[i+1]


enrg=[0.0]*10
#adding energy in a cycle
for j in range(10+1):
	for i in range(len(t)):
		if t[i]<=j+1 and t[i]>j:
			enrg[j]=enrg[j]+dp[i]


pt.plot(t,sig)
pt.ylabel("Stress")
pt.xlabel("Time")
pt.title("$\sigma_{y}$ = $\sigma_{y0}$ + 0.2Es")
pt.show()		

pt.plot(t,epn)
pt.ylabel("Plastic strain")
pt.xlabel("Time")
pt.title("$\sigma_{y}$ = $\sigma_{y0}$ + 0.2Es")
pt.show()

pt.plot(e,sig)
pt.ylabel("Stress")
pt.xlabel("Strain")
pt.title("$\sigma_{y}$ = $\sigma_{y0}$ + 0.2Es")
pt.show()

pt.plot(range(10), enrg)
pt.ylabel("Energy per cycle")
pt.xlabel("Cycle")
pt.title("$\sigma_{y}$ = $\sigma_{y0}$ + 0.2Es")
pt.show()
