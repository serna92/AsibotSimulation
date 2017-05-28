# Miguel Serna Agudo
# NIA: 100285275  

#!/usr/bin/python

from common_functions import *


def simulation(redCanCoords, robotCoords, wheelchairCoords):


   dd, pos, vel, enc, mode, axes = initRavebot()
   env, basemanip = initOpenRave(1, redCanCoords, [], wheelchairCoords, robotCoords)

   rpc = yarp.RpcClient()
   rpc.open('/command/ravebot/world')
   yarp.Network.connect('/command/ravebot/world', '/ravebot/world')

   grab, release, add, delObjs, whereisTCP, whereisObj, mvRobot, mvWheelchair, mvObj1, mvObj2, add2 = defineCommands(1, redCanCoords, [], wheelchairCoords, robotCoords)

   res = yarp.Bottle()

   rpc.write(add, res)

   rpc.write(mvWheelchair, res)
   rpc.write(mvRobot, res)
   rpc.write(mvObj1, res)

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
   targetpoint2.append(wheelchairCoords[1] - 1.17)	# respect to the position of the weelchair
   targetpoint2.append(wheelchairCoords[2] - 0.08)
   targetpoint2.append(90)
   targetpoint2.append(0)

   targetpoints = [targetpoint1, targetpoint2]

   if checkTargetPoints(targetpoints, 0, [], []) == True:

      movj(targetpoint1, axes, mode, pos, simCart, basemanip, env)

      print 'Grabbing red can'
      # Grab red can
      movl(targetpoint1, simCart, 0.02, 0.15, 0.05, rpc, grab, release, whereisTCP, whereisObj, res, 1, 'redCan', 0)
      refreshOpenrave(1, 1, rpc, res, whereisObj, env)

      movj(targetpoint2, axes, mode, pos, simCart, basemanip, env)

      print 'Giving drink'
      tiltObj(targetpoint2, simCart, 20)	# Give drink

      movj(targetpoint1, axes, mode, pos, simCart, basemanip, env)

      print 'Releasing red can'
      # Release red can
      movl(targetpoint1, simCart, 0.02, 0.15, 0.05, rpc, grab, release, whereisTCP, whereisObj, res, 2, 'redCan', 0)
      refreshOpenrave(1, 2, rpc, res, whereisObj, env)

      movinitial(axes, mode, pos)
      simCart.wait()

   raw_input('\n' + 'Press Enter to end simulation' + '\n')

   rpc.write(delObjs, res)

   #######################################
   env.Destroy()
   simCart.close()


if __name__ == '__main__':
   simulation()
