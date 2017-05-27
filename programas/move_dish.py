# Miguel Serna Agudo
# NIA: 100285275

#!/usr/bin/python

from common_functions import *

def simulation(dishCoords, robotCoords, wheelchairCoords):

   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave(3, dishCoords, [], wheelchairCoords, robotCoords)

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grab, release, add, delObjs, whereisTCP, whereisObj, mvRobot, mvWheelchair, mvObj1, mvObj2, add2 = defineCommands(3, dishCoords, [], wheelchairCoords, robotCoords)

   res = yarp.Bottle()

   rpc.write(add, res)

   rpc.write(mvWheelchair, res)
   rpc.write(mvRobot, res)
   rpc.write(mvObj1, res)

   #######################################

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

   targetpoints = []

   targetpoint1 = calculateTargetpoint(dishCoords, robotCoords, 0.03, 0.3, 0.2)
   targetpoint2 = P_cajon

   targetpoints = [targetpoint1, targetpoint2]

   if checkTargetPoints(targetpoints) == True:

      movj(targetpoint1, axes, mode, pos, simCart, basemanip, env)

      print 'Grabbing dish'
      movl(targetpoint1, simCart, 0.01, 0.15, 0.08, dishCoords, TCPPosition, rpc, grab, release, res, 1, 'dish', 0)    # Grab dish
      refreshOpenrave(1, 1, rpc, res, whereisObj, env) 

      movj(targetpoint2, axes, mode, pos, simCart, basemanip, env)

      print 'Releasing dish'
      movl(targetpoint2, simCart, 0, 0.38, 0.12, dishCoords, TCPPosition, rpc, grab, release, res, 2, 'dish', 0)    # Release dish
      refreshOpenrave(1, 2, rpc, res, whereisObj, env)

      movinitial(axes, mode, pos)

      simCart.wait()

   raw_input('\n' + 'Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################

   simCart.close()


if __name__ == '__main__':
   simulation()
