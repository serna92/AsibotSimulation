#!/usr/bin/python

from AsibotPy import *
from openravepy import *


def initRavebot():


   options = yarp.Property()  # create an instance of Property, a nice YARP class for storing name-value (key-value) pairs
   options.put('device','remote_controlboard')  # we add a name-value pair that indicates the YARP device
   options.put('remote','/ravebot')  # we add info on to whom we will connect
   options.put('local','/testRemoteRavebot')  # we add info on how we will call ourselves on the YARP network
   dd = yarp.PolyDriver(options)  # create a YARP multi-use driver with the given options

   pos = dd.viewIPositionControl()  # make a position controller object we call 'pos'
   vel = dd.viewIVelocityControl()  # make a velocity controller object we call 'vel'
   enc = dd.viewIEncoders()  # make an encoder controller object we call 'enc'
   mode = dd.viewIControlMode()  # make a mode controller object we call 'mode'

   axes = enc.getAxes()

   return dd, pos, vel, enc, mode, axes


def initOpenRave():


   env = Environment()
   env.Load('AsibotSimulation/entornoAsibot/asibot_kitchen.env.xml')
   robot = env.GetRobots()[0]
   basemanip = interfaces.BaseManipulation(robot, plannername = 'BiRRT')

   return env, basemanip


def defineCommands(objname, robotname):

   grab = yarp.Bottle()

   grab.addString('world')
   grab.addString('grab')
   grab.addString('obj')
   grab.addString(objname)
   grab.addInt(1)

   release = yarp.Bottle()

   release.addString('world')
   release.addString('grab')
   release.addString('obj')
   release.addString(objname)
   release.addInt(0)

   add = yarp.Bottle()

   add.addString('world')
   add.addString('mk')
   add.addString('obj')
   add.addString('AsibotSimulation/entornoAsibot/' + objname + '.kinbody.xml')

   delObjs = yarp.Bottle()

   delObjs.addString('world')
   delObjs.addString('del')
   delObjs.addString('all')

   whereisObj = yarp.Bottle()

   whereisObj.addString('world')
   whereisObj.addString('whereis')
   whereisObj.addString('obj')
   whereisObj.addString(objname)

   whereisRobot = yarp.Bottle()

   whereisRobot.addString('world')
   whereisRobot.addString('whereis')
   whereisRobot.addString('obj')
   whereisRobot.addString(robotname)

   whereisTCP = yarp.Bottle()

   whereisTCP.addString('world')
   whereisTCP.addString('whereis')
   whereisTCP.addString('tcp')

   return grab, release, add, delObjs, whereisObj, whereisRobot, whereisTCP


def movinitial(axes, mode, pos):

   for i in range(0,axes): mode.setPositionMode(i)

   for j in range(0, axes):
      pos.positionMove(j,0)


def movj(targetpoint, axes, mode, pos, simCart, basemanip):


   goal = []

   simCart.inv(targetpoint, goal)

   for i in range (0, len(goal)):
      goal[i] = goal[i] / 360 * 2 * 3.141593	# Change degrees --> radians

   # Get a valid trajectory

   traj = basemanip.MoveManipulator(goal = goal, execute = False, maxiter = 3000, steplength = 0.15, maxtries = 3, outputtrajobj = True)

   n = traj.GetNumWaypoints()

   raveLogInfo('traj has %d waypoints, last waypoint is: %s'%(traj.GetNumWaypoints(),repr(traj.GetWaypoint(-1)[0:5])))

   for i in range(0,axes): mode.setPositionMode(i)

   for i in range(0,n):

      waypoint = []
      for j in range(0, axes):
         waypoint.append(traj.GetWaypoint(i)[j] / 2 / 3.141593 * 360)	# Change radians --> degrees
      pos.positionMove(0,waypoint[0])
      pos.positionMove(1,waypoint[1])
      pos.positionMove(2,waypoint[2])
      pos.positionMove(3,waypoint[3])
      pos.positionMove(4,waypoint[4])


def movl(targetpoint, simCart, distance_offset_x, distance_offset_y, height_offset, objPosition, TCPPosition, rpc, grab, release, res, action, degrees):


   if ((TCPPosition[0] - objPosition[0]) < -0.02):

      targetpoint[0] -= distance_offset_x
      targetpoint[1] += distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[2] -= height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      if (action == 1):  rpc.write(grab, res)	# Grab object
      elif (action == 2):   rpc.write(release, res)		# Release object
      elif (action == 3):   tiltObj(targetpoint, simCart, degrees)	# Tilt object
      else:
         pass

      targetpoint[2] += height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[0] += distance_offset_x
      targetpoint[1] -= distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()

   elif ((TCPPosition[0] - objPosition[0]) <= 0.02 and (TCPPosition[0] - objPosition[0]) >= -0.02):

      targetpoint[1] += distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[2] -= height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      if (action == 1):  rpc.write(grab, res)	# Grab object
      elif (action == 2):   rpc.write(release, res)		# Release object
      elif (action == 3):   tiltObj(targetpoint, simCart, degrees)	# Tilt object
      else:
         pass

      targetpoint[2] += height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[1] -= distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()

   else:

      targetpoint[0] += distance_offset_x
      targetpoint[1] += distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[2] -= height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      if (action == 1):  rpc.write(grab, res)	# Grab object
      elif (action == 2):   rpc.write(release, res)		# Release object
      elif (action == 3):   tiltObj(targetpoint, simCart, degrees)	# Tilt object
      else:
         pass

      targetpoint[2] += height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[0] -= distance_offset_x
      targetpoint[1] -= distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()


def tiltObj(targetpoint, simCart, degrees):


   targetpoint[4] -= degrees		# Tilt object
   simCart.movl(targetpoint)
   simCart.wait()

   targetpoint[4] += degrees
   simCart.movl(targetpoint)
   simCart.wait()


def calculateTargetpoint(objPosition, robotPosition, distance_offset_x, distance_offset_y, height_offset):


   targetpoint = []

   if ((robotPosition[0] - objPosition[0]) < -0.02):
      targetpoint.append(robotPosition[0] - objPosition[0] + distance_offset_x)
      targetpoint.append(robotPosition[1] - objPosition[1] - distance_offset_y)

   elif ((robotPosition[0] - objPosition[0]) <= 0.02 and (robotPosition[0] - objPosition[0]) >= -0.02):
      targetpoint.append(robotPosition[1] - objPosition[1] - distance_offset_y)

   else:
      targetpoint.append(robotPosition[0] - objPosition[0] - distance_offset_x)
      targetpoint.append(robotPosition[1] - objPosition[1] - distance_offset_y)

   

   targetpoint.append(objPosition[2] - robotPosition[2] + height_offset)

   targetpoint += [90,0]

   return targetpoint


if __name__ == '__main__':
   initRavebot()
