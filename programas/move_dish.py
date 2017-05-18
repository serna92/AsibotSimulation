# Miguel Serna Agudo
# NIA: 100285275

#!/usr/bin/python

from AsibotPy import *
from openravepy import *

def simulation():

	env = Environment()
	env.SetViewer('qtcoin')
	env.Load('AsibotSimulation/entornoAsibot/asibot_kitchen.env.xml')

	dish = env.ReadKinBodyXMLFile('AsibotSimulation/entornoAsibot/dish.kinbody.xml')
	env.Add(dish)

	raw_input('\n' + 'Press Enter to close')

	rpc = yarp.RpcClient()

	rpc.open('/command/ravebot/world')

	yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

	#######################################

	res = yarp.Bottle()

	cmd1 = yarp.Bottle()

	cmd1.addString('world')
	cmd1.addString('grab')
	cmd1.addString('obj')
	cmd1.addString('dish')
	cmd1.addInt(1)

	cmd2 = yarp.Bottle()

	cmd2.addString('world')
	cmd2.addString('grab')
	cmd2.addString('obj')
	cmd2.addString('dish')
	cmd2.addInt(0)  

	#######################################

	home=[0,0,1.4,0,0]

	P1=[0.3,0.9,0.6,90,0]
	P2=[0.05,0.5,0.6,90,0]
	P3=[0.05,0.5,0.75,90,0]

	P_plato=[0.05,0.7,0.4,90,0]
	P_cajon=[0.05,0.8,0.75,90,0]

	P4=[0.05,0.7,0.25,90,0]
	P5=[0.05,0.75,0.25,90,0]

	P6=[0.05,0.95,0.75,90,0]
	P7=[0.05,0.95,0.68,90,0]

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
	simCart.movj(P_plato)
	simCart.wait()

	simCart.movl(P4)
	simCart.wait()
	simCart.movl(P5)
	simCart.wait()


	rpc.write(cmd1, res)	# Coger plato.


	simCart.movl(P4)
	simCart.wait()
	simCart.movl(P_plato)
	simCart.wait()

	simCart.movj(P2)
	simCart.wait()
	simCart.movj(P3)
	simCart.wait()
	simCart.movj(P_cajon)
	simCart.wait()

	simCart.movl(P6)
	simCart.wait()
	simCart.movl(P7)
	simCart.wait()


	rpc.write(cmd2, res)	# Dejar plato.


	simCart.movl(P6)
	simCart.wait()
	simCart.movl(P_cajon)
	simCart.wait()

	simCart.movj(P1)
	simCart.wait()
	simCart.movj(home)
	simCart.wait()

	#######################################

	print 'done!'
	simCart.close()

if __name__ == '__main__':
	simulation();
