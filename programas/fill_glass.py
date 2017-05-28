# Miguel Serna Agudo
# NIA: 100285275  

#!/usr/bin/python

from common_functions import *

def simulation(glassCoords, bottleCoords, robotCoords, wheelchairCoords):

   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave(robotCoords, wheelchairCoords)

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grab, release, add, delObjs, whereisTCP, mvRobot, mvWheelchair, mvObj1, mvObj2, add2 = defineCommands(2, bottleCoords, glassCoords, wheelchairCoords, robotCoords)

   res = yarp.Bottle()

   rpc.write(add, res)
   rpc.write(add2, res)

   rpc.write(mvWheelchair, res)
   rpc.write(mvRobot, res)
   rpc.write(mvObj1, res)
   rpc.write(mvObj2, res)

   #######################################

   rpc.write(whereisTCP, res)

   TCPPosition = []

   for i in range(0,3):
      TCPPosition.append(res.get(0).asList().get(i).asDouble())

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

   if checkTargetPoints(targetpoints) == True:

      movj(targetpoint1, axes, mode, pos, simCart, basemanip)

      print 'Grabbing bottle'
      movl(targetpoint1, simCart, 0.02, 0.15, 0.05, bottleCoords, TCPPosition, rpc, grab, release, res, 1, 0)	# Grab bottle

      movj(targetpoint2, axes, mode, pos, simCart, basemanip)
      
      print 'Filling glass'
      tiltObj(targetpoint2, simCart, 75)	# Fill glass

      movj(targetpoint1, axes, mode, pos, simCart, basemanip)

      print 'Releasing bottle'
      movl(targetpoint1, simCart, 0.02, 0.15, 0.05, bottleCoords, TCPPosition, rpc, grab, release, res, 2, 0)	# Release bottle

      movinitial(axes, mode, pos)
      simCart.wait()

   raw_input('\n' + 'Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################

   simCart.close()


if __name__ == '__main__':
   simulation()
