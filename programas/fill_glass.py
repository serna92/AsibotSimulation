# Miguel Serna Agudo
# NIA: 100285275  

#!/usr/bin/python

from common_functions import *

def simulation():

   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave()

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grabObj1, releaseObj1, addObj1, delObjs, whereisObj1, whereisRobot, whereisTCP = defineCommands('glass', 'asibot')
   grabObj2, releaseObj2, addObj2, delObjs, whereisObj2, whereisRobot, whereisTCP = defineCommands('bottle', 'asibot')

   res = yarp.Bottle()

   rpc.write(addObj1, res)
   rpc.write(addObj2, res)

   #######################################

   rpc.write(whereisObj1, res)

   glass_position = []

   for i in range(0,3):
      glass_position.append(res.get(0).asList().get(i).asDouble())

   rpc.write(whereisObj2, res)

   bottle_position = []

   for i in range(0,3):
      bottle_position.append(res.get(0).asList().get(i).asDouble())

   rpc.write(whereisRobot, res)

   robot_base = []

   for i in range(0,3):
      robot_base.append(res.get(0).asList().get(i).asDouble())


   rpc.write(whereisTCP, res)

   TCPPosition = []

   for i in range(0,3):
      TCPPosition.append(res.get(0).asList().get(i).asDouble())

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

   print ('\n' + 'Starting Simulation' + '\n')

   simCart.movl(home)  # defaults to 20 s
   simCart.wait()      # wait for movement

   print bottle_position

   targetpoint = calculateTargetpoint(bottle_position, robot_base, 0.03, 0.2, 0.2)
   movj(targetpoint, axes, mode, pos, simCart, basemanip)

   movl(targetpoint, simCart, 0.02, 0.15, 0.05, bottle_position, TCPPosition, rpc, grabObj2, releaseObj2, res, 1, 0)	# Grab bottle

   glass_position[0] -= 0.18	# Targetpoint desired to be at the right of the glass
   glass_position[1] -= 0.1
   glass_position[2] += 0.03

   targetpoint2 = calculateTargetpoint(glass_position, robot_base, 0.03, 0.2, 0.2)
   movj(targetpoint2, axes, mode, pos, simCart, basemanip)

   tiltObj(targetpoint2, simCart, 75)	# Fill glass

   movj(targetpoint, axes, mode, pos, simCart, basemanip)

   movl(targetpoint, simCart, 0.02, 0.15, 0.05, bottle_position, TCPPosition, rpc, grabObj2, releaseObj2, res, 2, 0)	# Release bottle

   movinitial(axes, mode, pos)

   simCart.wait()

   raw_input('Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################

   simCart.close()


if __name__ == '__main__':
   simulation()
