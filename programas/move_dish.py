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

   grab, release, add, delObjs, whereisObj, whereisRobot, whereisTCP = defineCommands('dish', 'asibot')

   res = yarp.Bottle()

   rpc.write(add, res)

   #######################################

   rpc.write(whereisObj, res)

   dish_position = []

   for i in range(0,3):
      dish_position.append(res.get(0).asList().get(i).asDouble())

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

   P_cajon=[0.05,0.5,0.8,90,0]

   #######################################

   simCart = CartesianClient()
   simCart.open('/ravebot')
   # use '/canbot' for real

   #######################################

   print ('\n' + 'Starting Simulation' + '\n')

   simCart.movl(home)  # defaults to 20 s
   simCart.wait()      # wait for movement

   targetpoint = calculateTargetpoint(dish_position, robot_base, 0.03, 0.3, 0.2)
   movj(targetpoint, axes, mode, pos, simCart, basemanip)

   movl(targetpoint, simCart, 0.02, 0.15, 0.08, dish_position, TCPPosition, rpc, grab, release, res, 1, 0)   # Grab dish

   movj(P_cajon, axes, mode, pos, simCart, basemanip)
   yarp.Time.delay(30)

   movl(P_cajon, simCart, 0, 0.38, 0.12, dish_position, TCPPosition, rpc, grab, release, res, 2, 0)   # Release dish

   movinitial(axes, mode, pos)

   simCart.wait()

   raw_input('Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################

   simCart.close()


if __name__ == '__main__':
   simulation()
