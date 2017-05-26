# Miguel Serna Agudo
# NIA: 100285275  

#!/usr/bin/python

from common_functions import *

def simulation(redCanCoords, robotCoords, wheelchairCoords):

   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave(robotCoords, wheelchairCoords)

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grab, release, add, delObjs, whereisTCP, mvRobot, mvWheelchair, mvObj1, mvObj2, add2 = defineCommands(1, redCanCoords, [], wheelchairCoords, robotCoords)

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

   #######################################

   simCart = CartesianClient()
   simCart.open('/ravebot')
   # use '/canbot' for real

   #######################################

   print ('\n' + 'Starting Simulation' + '\n')

   simCart.movl(home)  # defaults to 20 s
   simCart.wait()      # wait for movement

   targetpoints = []

   targetpoint1 = calculateTargetpoint(redCanCoords, robotCoords, 0.03, 0.2, 0.2)

   targetpoint2 = []
   targetpoint2.append(wheelchairCoords[0] - 1.48)	# Targetpoint desired to be near user lips
   targetpoint2.append(wheelchairCoords[1] - 0.45)	# respect to the position of the weelchair
   targetpoint2.append(wheelchairCoords[2] - 0.08)
   targetpoint2.append(90)
   targetpoint2.append(0)

   targetpoints = [targetpoint1, targetpoint2]

   if checkTargetPoints(targetpoints) == True:

      movj(targetpoint, axes, mode, pos, simCart, basemanip)

      print 'Grabbing red can'
      movl(targetpoint, simCart, 0.02, 0.15, 0.05, redCanCoords, TCPPosition, rpc, grab, release, res, 1, 0)	# Grab red can

      movj(targetpoint2, axes, mode, pos, simCart, basemanip)

      print 'Giving drink'
      tiltObj(targetpoint2, simCart, 20)	# Give drink

      movj(targetpoint, axes, mode, pos, simCart, basemanip)

      print 'Releasing red can'
      movl(targetpoint, simCart, 0.02, 0.15, 0.05, redCanCoords, TCPPosition, rpc, grab, release, res, 2, 0)	# Release red can

      movinitial(axes, mode, pos)
      simCart.wait()

   raw_input('\n' + 'Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################

   simCart.close()


if __name__ == '__main__':
   simulation()
