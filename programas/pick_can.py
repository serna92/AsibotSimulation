# Miguel Serna Agudo
# NIA: 100285275

# Find (\n|^) as regular expression and replace \n   

#!/usr/bin/python

from common_functions import *

def simulation():

   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave()

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grab, release, add, delObjs, whereisObj, whereisRobot, whereisTCP = defineCommands('redCan', 'asibot')

   res = yarp.Bottle()

   rpc.write(add, res)

   #######################################

   rpc.write(whereisObj, res)

   redCan_position = []

   for i in range(0,3):
      redCan_position.append(res.get(0).asList().get(i).asDouble())

   rpc.write(whereisRobot, res)

   robot_base = []

   for i in range(0,3):
      robot_base.append(res.get(0).asList().get(i).asDouble())


   rpc.write(whereisTCP, res)

   TCPPosition = []

   for i in range(0,3):
      TCPPosition.append(res.get(0).asList().get(i).asDouble())

   #######################################

   home=[0,0,1.41,0,0]

   P_lips=[-0.2,0,0.62,90,0]

   #######################################

   simCart = CartesianClient()
   simCart.open('/ravebot')
   # use '/canbot' for real

   #######################################

   print ('\n' + 'Starting Simulation' + '\n')

   simCart.movl(home)  # defaults to 20 s
   simCart.wait()      # wait for movement

   targetpoint = calculateTargetpoint(redCan_position, robot_base, 0.03, 0.2, 0.2)
   movj(targetpoint, axes, mode, pos, simCart, basemanip)

   movl(targetpoint, simCart, 0.02, 0.15, 0.05, redCan_position, TCPPosition, rpc, grab, release, res, 1, 0)	# Grab red can

   movj(P_lips, axes, mode, pos, simCart, basemanip)
   yarp.Time.delay(20)

   tiltObj(P_lips, simCart, 20)		# Give drink

   movj(targetpoint, axes, mode, pos, simCart, basemanip)

   movl(targetpoint, simCart, 0.02, 0.15, 0.05, redCan_position, TCPPosition, rpc, grab, release, res, 2, 0)	# Release red can

   movinitial(axes, mode, pos)

   simCart.wait()

   print ('\n' + 'Done' + '\n')

   raw_input('Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################

   simCart.close()


if __name__ == '__main__':
   simulation()
