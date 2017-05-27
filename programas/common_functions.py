#!/usr/bin/python

from AsibotPy import *
from openravepy import *
import math


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


def mvKinbody(kinBodyName, coords, env):


   objPtr = env.GetKinBody(kinBodyName)
   T = objPtr.GetTransform()
   T[0][3] = coords[0]
   T[1][3] = coords[1]
   T[2][3] = coords[2]
   objPtr.SetTransform(T)


def addKinbody(kinBodyFile, env):

   objKinBody = env.ReadKinBodyXMLFile(kinBodyFile)
   env.Add(objKinBody, True)


def grabKinbody(objKinBody, env):


   robot = env.GetRobots()[0]
   with env:
      robot.Grab(env.GetKinBody(objKinBody))


def releaseKinbody(objKinBody, env):


   robot = env.GetRobots()[0]
   with env:
      robot.Release(env.GetKinBody(objKinBody))


def refreshOpenrave(task, action, rpc, res, whereisObj, env):


   if task == 1:

      objname = 'redCan'   
   
   elif task == 2:

      objname = 'bottle'

   else:

      objname = 'dish'

   rpc.write(whereisObj,res)

   objPosition = []

   for i in range(0,3):
      objPosition.append(res.get(0).asList().get(i).asDouble())

   mvKinbody(objname, objPosition, env)

   if action == 1:

      grabKinbody(objname, env)
   else:
      releaseKinbody(objname, env)


def initOpenRave(task, objCoords, objCoords2, wheelchairCoords, robotCoords):


   env = Environment()
   env.Load('AsibotSimulation/entornoAsibot/asibot_kitchen.env.xml')
   env.SetViewer('qtcoin')
   mvKinbody('asibot', robotCoords, env)
   mvKinbody('wheelchair', wheelchairCoords, env)

   if task == 1:

      addKinbody('AsibotSimulation/entornoAsibot/redCan.kinbody.xml', env)
      mvKinbody('redCan', objCoords, env)
   elif task == 2:
 
      addKinbody('AsibotSimulation/entornoAsibot/bottle.kinbody.xml', env)
      addKinbody('AsibotSimulation/entornoAsibot/glass.kinbody.xml', env)
      mvKinbody('bottle', objCoords, env)
      mvKinbody('glass', objCoords2, env)
   else:

      addKinbody('AsibotSimulation/entornoAsibot/dish.kinbody.xml', env)
      mvKinbody('dish', objCoords, env)

   robot = env.GetRobots()[0]
   basemanip = interfaces.BaseManipulation(robot, plannername = 'BiRRT')

   return env, basemanip


def defineCommands(task, ObjCoords, ObjCoords2, wheelchairCoords, robotCoords):

   grab = yarp.Bottle()
   release = yarp.Bottle()
   add = yarp.Bottle()
   add2 = yarp.Bottle()
   delObjs = yarp.Bottle()
   whereisTCP = yarp.Bottle()
   whereisObj = yarp.Bottle()
   mvRobot = yarp.Bottle()
   mvWheelchair = yarp.Bottle()
   mvObj1 = yarp.Bottle()
   mvObj2 = yarp.Bottle()

   if task == 1:

      objname = 'redCan'   
   
   elif task == 2:

      objname = 'bottle'
      objname2 = 'glass'

   else:

      objname = 'dish'


   grab.addString('world')
   grab.addString('grab')
   grab.addString('obj')
   grab.addString(objname)
   grab.addInt(1)

   release.addString('world')
   release.addString('grab')
   release.addString('obj')
   release.addString(objname)
   release.addInt(0)

   add.addString('world')
   add.addString('mk')
   add.addString('obj')
   add.addString('AsibotSimulation/entornoAsibot/' + objname + '.kinbody.xml')

   delObjs.addString('world')
   delObjs.addString('del')
   delObjs.addString('all')

   whereisTCP.addString('world')
   whereisTCP.addString('whereis')
   whereisTCP.addString('tcp')

   whereisObj.addString('world')
   whereisObj.addString('whereis')
   whereisObj.addString('obj')
   whereisObj.addString(objname)

   mvRobot.addString('world')
   mvRobot.addString('mv')
   mvRobot.addString('asibot')
   mvRobot.addDouble(robotCoords[0])
   mvRobot.addDouble(robotCoords[1])
   mvRobot.addDouble(robotCoords[2])

   mvWheelchair.addString('world')
   mvWheelchair.addString('mv')
   mvWheelchair.addString('wheelchair')
   mvWheelchair.addDouble(wheelchairCoords[0])
   mvWheelchair.addDouble(wheelchairCoords[1])
   mvWheelchair.addDouble(wheelchairCoords[2])

   mvObj1.addString('world')
   mvObj1.addString('mv')
   mvObj1.addString(objname)
   mvObj1.addDouble(ObjCoords[0])
   mvObj1.addDouble(ObjCoords[1])
   mvObj1.addDouble(ObjCoords[2])

   if task == 2:

      mvObj2.addString('world')
      mvObj2.addString('mv')
      mvObj2.addString(objname2)
      mvObj2.addDouble(ObjCoords2[0])
      mvObj2.addDouble(ObjCoords2[1])
      mvObj2.addDouble(ObjCoords2[2])

      add2.addString('world')
      add2.addString('mk')
      add2.addString('obj')
      add2.addString('AsibotSimulation/entornoAsibot/' + objname2 + '.kinbody.xml')

   return grab, release, add, delObjs, whereisTCP, whereisObj, mvRobot, mvWheelchair, mvObj1, mvObj2, add2


def movinitial(axes, mode, pos):


   for i in range(0,axes): mode.setPositionMode(i)

   for j in range(0, axes):
      pos.positionMove(j,0)

   while True:
      yarp.Time.delay(0.5)
      if pos.checkMotionDone():
         break


def movj(targetpoint, axes, mode, pos, simCart, basemanip, env):


   goal = []
   simCart.inv(targetpoint, goal)

   for i in range (0, len(goal)):
      goal[i] = goal[i] / 360 * 2 * 3.141593	# Change degrees --> radians

   # Get a valid trajectory

   traj = basemanip.MoveManipulator(goal = goal, execute = False, maxiter = 3000, steplength = 0.15, maxtries = 3, outputtrajobj = True)
   robot = env.GetRobots()[0]
   # basemanip.VerifyTrajectory(traj, samplingstep = 0.002)
   robot.GetController().SetPath(traj)

   n = traj.GetNumWaypoints()

   print ('INFO: Trajectory has %d waypoints'%(traj.GetNumWaypoints()))

   for i in range(0,axes): mode.setPositionMode(i)

   for i in range(0,n):

      waypoint = []
      for j in range(0, axes):
         waypoint.append(traj.GetWaypoint(i)[j] / 2 / 3.141593 * 360)	# Change radians --> degrees
      pos.positionMove(4,waypoint[4])
      pos.positionMove(3,waypoint[3])
      pos.positionMove(2,waypoint[2])
      pos.positionMove(1,waypoint[1])
      pos.positionMove(0,waypoint[0])
      
   while True:
      yarp.Time.delay(0.5)
      if pos.checkMotionDone():
         break


def movl(targetpoint, simCart, distance_offset_x, distance_offset_y, height_offset, objPosition, TCPPosition, rpc, grab, release, res, action, objKinbody, degrees):


   if ((TCPPosition[0] - objPosition[0]) < -0.02):

      targetpoint[0] -= distance_offset_x
      targetpoint[1] += distance_offset_y

      simCart.movl(targetpoint)
      simCart.wait()

      targetpoint[2] -= height_offset

      simCart.movl(targetpoint)
      simCart.wait()

      if (action == 1): rpc.write(grab, res)	# Grab object
      elif (action == 2): rpc.write(release, res)	# Release object
      elif (action == 3):   tiltObj(targetpoint, simCart, degrees)	# Tilt object

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
      targetpoint.append(robotPosition[0] - objPosition[0])
      targetpoint.append(robotPosition[1] - objPosition[1] - distance_offset_y)

   else:
      targetpoint.append(robotPosition[0] - objPosition[0] - distance_offset_x)
      targetpoint.append(robotPosition[1] - objPosition[1] - distance_offset_y)

   

   targetpoint.append(objPosition[2] - robotPosition[2] + height_offset)

   targetpoint += [90,0]

   return targetpoint


def checkTargetPoints(targetpoints):

   for i in range (0, len(targetpoints)):
      for j in range (0, len(targetpoints[i])):
         if math.isnan(targetpoints[i][j]):
            print ('\n' + 'ERROR: Targetpoint' + str(i) + 'is out of range' + '\n')
            return False

   return True


if __name__ == '__main__':
   initRavebot()
