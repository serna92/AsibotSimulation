# Miguel Serna Agudo
# NIA: 100285275

from AsibotPy import *

rpc = yarp.RpcClient()

rpc.open('/command/ravebot/world')

yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

#######################################

res = yarp.Bottle()

cmd1 = yarp.Bottle()

cmd1.addString('world')
cmd1.addString('grab')
cmd1.addString('obj')
cmd1.addString('redCan')
cmd1.addInt(1)

cmd2 = yarp.Bottle()

cmd2.addString('world')
cmd2.addString('grab')
cmd2.addString('obj')
cmd2.addString('redCan')
cmd2.addInt(0)  

#######################################

home=[0,0,1.4,0,0]

P1=[0.3,0.9,0.6,90,0]
P_lata=[-0.15,0.7,0.5,90,0]
P_labios=[-0.2,0,0.6,90,0]

P2=[-0.15,0.7,0.25,90,0]
P3=[-0.15,0.8,0.25,90,0]

#P4=
#P5=

#######################################

simCart = CartesianClient()
simCart.open('/ravebot')
# use '/canbot' for real

#######################################

print 'hello, robot!'
simCart.movl(home)  # defaults to 20 s
simCart.wait()      # wait for movement

simCart.movj(P1)
simCart.wait()
simCart.movj(P_lata)
simCart.wait()

simCart.movl(P2)
simCart.wait()
simCart.movl(P3)
simCart.wait()

rpc.write(cmd1, res)	# Agarrar lata.

simCart.movl(P2)
simCart.wait()
simCart.movj(P_lata)
simCart.wait()

simCart.movj(P_labios)
simCart.wait()

	# Mov. cartesiano para dar de beber.
	# Problemas con el limite de movimiento
	# maximo de los ejes.

simCart.movj(P_lata)
simCart.wait()

simCart.movl(P2)
simCart.wait()
simCart.movl(P3)
simCart.wait()

rpc.write(cmd2, res)	# Soltar lata.

simCart.movl(P2)
simCart.wait()
simCart.movj(P_lata)
simCart.wait()

simCart.movj(P1)
simCart.wait()
simCart.movj(home)
simCart.wait()

#######################################

print 'done!'
simCart.close()