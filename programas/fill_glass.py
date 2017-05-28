# Miguel Serna Agudo
# NIA: 100285275  

#!/usr/bin/python

from common_functions import *


def simulation(glassCoords, bottleCoords, robotCoords, wheelchairCoords):


   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave(2, bottleCoords, glassCoords, wheelchairCoords, robotCoords)

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grab, release, add, delObjs, whereisTCP, whereisObj, mvRobot, mvWheelchair, mvObj1, mvObj2, add2 = defineCommands(2, bottleCoords, glassCoords, wheelchairCoords, robotCoords)

   res = yarp.Bottle()

   rpc.write(add, res)
   rpc.write(add2, res)

   rpc.write(mvWheelchair, res)
   rpc.write(mvRobot, res)
   rpc.write(mvObj1, res)
   rpc.write(mvObj2, res)

   #######################################

   home=[0,0,1.4,0,0]

   #######################################

   simCart = CartesianClient()
   simCart.open('/ravebot')
   # use '/canbot' for real

   #######################################

   print ('\n' + 'Starting Simulation' + '\n')

   simCart.movl(home)  # defaults to 20 s
   simCart.wait()      # wait for movement

   targetpoints = []

   targetpoint1 = calculateTargetpoint(bottleCoords, robotCoords, 0.03, 0.2, 0.2)

   targetpoint2 = []
   targetpoint2.append(glassCoords[0] - 0.18)		# Targetpoint desired to be at the right of the glass
   targetpoint2.append(glassCoords[1] - 0.1)
   targetpoint2.append(glassCoords[2] + 0.03)
   targetpoint2 = calculateTargetpoint(targetpoint2, robotCoords, 0.03, 0.2, 0.2)

   targetpoints = [targetpoint1, targetpoint2]

   if checkTargetPoints(targetpoints, 1, glassCoords, bottleCoords) == True:

      movj(targetpoint1, axes, mode, pos, simCart, basemanip, env)

      print 'Grabbing bottle'
      # Grab bottle
      movl(targetpoint1, simCart, 0.02, 0.15, 0.05, rpc, grab, release, whereisTCP, whereisObj, res, 1, 'bottle', 0)
      refreshOpenrave(2, 1, rpc, res, whereisObj, env)

      movj(targetpoint2, axes, mode, pos, simCart, basemanip, env)
      
      print 'Filling glass'
      tiltObj(targetpoint2, simCart, 75)	# Fill glass

      movj(targetpoint1, axes, mode, pos, simCart, basemanip, env)

      print 'Releasing bottle'
      # Release bottle
      movl(targetpoint1, simCart, 0.02, 0.15, 0.05, rpc, grab, release, whereisTCP, whereisObj, res, 2, 'bottle', 0)
      refreshOpenrave(2, 2, rpc, res, whereisObj, env)

      movinitial(axes, mode, pos)
      simCart.wait()

   raw_input('\n' + 'Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################
   env.Destroy()
   simCart.close()


if __name__ == '__main__':
   simulation()
