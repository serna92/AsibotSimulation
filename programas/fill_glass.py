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
cmd1.addString('bottle')
cmd1.addInt(1)

cmd2 = yarp.Bottle()

cmd2.addString('world')
cmd2.addString('grab')
cmd2.addString('obj')
cmd2.addString('bottle')
cmd2.addInt(0)  

#######################################

home=[0,0,1.4,0,0]

P1=[0.3,0.9,0.6,90,0]
P_botella=[0.6,0.4,0.5,90,0]
P_vaso=[0.3,0.9,0.4,90,0]

P2=[0.6,0.4,0.3,90,0]
P3=[0.7,0.5,0.3,90,0]

P4=[0.3,0.8,0.4,90,0]
P5=[0.3,0.8,0.37,90,0]
P6=[0.3,0.8,0.4,90,-75]

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
simCart.movj(P_botella)
simCart.wait()

simCart.movl(P2)
simCart.wait()
simCart.movl(P3)
simCart.wait()

rpc.write(cmd1, res)	# Agarrar la botella.

simCart.movl(P2)
simCart.wait()
simCart.movl(P_botella)
simCart.wait()

simCart.movj(P_vaso)
simCart.wait()

simCart.movl(P4)
simCart.wait()
simCart.movl(P5)
simCart.wait()

simCart.movl(P6)	# Rellenar vaso.
simCart.wait()
simCart.movl(P5)
simCart.wait()

simCart.movl(P4)
simCart.wait()
simCart.movl(P_vaso)
simCart.wait()

simCart.movj(P_botella)
simCart.wait()

simCart.movl(P2)
simCart.wait()
simCart.movl(P3)
simCart.wait()

rpc.write(cmd2, res)	# Soltar la botella.

simCart.movl(P2)
simCart.wait()
simCart.movl(P_botella)
simCart.wait()

simCart.movj(P1)
simCart.wait()
simCart.movj(home)
simCart.wait()

#######################################

print 'done!'
simCart.close()

