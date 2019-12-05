# if no points are within travelling distance of that timestep
# they become free agents and are assigned to a longer task

# manages the robots
import numpy as np

class _Robot():
	def __init__(self, position = [0,0]):
		self.position = position
		self.assigned = False
		self.goal = position
		self.speed = 0.05
		self.direction = [0,0]

	def step(self):
		# timestep defaults to 1
		if np.linalg.norm([x - y for x, y in zip(self.goal, self.position)]) > 0.05:
			increment = [self.speed * x for x in self.direction]
			self.position[0] = self.position[0] + increment[0]
			self.position[1] = self.position[1] + increment[1]
		return self.position

	def updateGoal(self, point):
		self.goal = point
		diff = [x1 - x2 for (x1, x2) in zip(self.goal, self.position)]
		self.direction = diff/(np.linalg.norm(diff))

	def __repr__(self):
		return 'Robot: pos [%.3f, %3f] goal:[%.3f, %.3f]' % (self.position[0], self.position[1], self.goal[0], self.goal[1])


class RobotManager():
	def __init__(self, num = 10):
		self.size = num
		self.robots = [None] * num
		for i in range(num):
			self.robots[i] = _Robot([2, i/2])

	def assignRobots(self, hullset):
		# hull is a list of NUMPY ARRAYS
		# DOES NOT HANDLE HAVING DIFFERENT NUMBER OF HULL VS ROBOTS
		# NEED TO CHANGE SO IT REMOVES the undone ones
		#flatten hullset
		flat = []
		for hull in hullset:
			for p in hull:
				flat.append(p)

		for i, robot in enumerate(self.robots):
			if i < len(flat):
				robot.updateGoal([flat[i][0], flat[i][1]])
			else:
				break

	def smartAssignRobots(self, hullset):
		flat = []
		for hull in hullset:
			for p in hull:
				flat.append([p[0], p[1]])
		flat = sorted(flat, key=lambda x: x[0])
		for robot in self.robots:
			newgoal = self.bruteForce(flat, robot)
			#newgoal = self.closest(flat, robot)
			#if robot.goal[0] != newgoal[0] and robot.goal[1] != newgoal[1]:
			#	print("removing flat goal")
			flat.remove(flat[flat.index(newgoal)])
			robot.updateGoal([newgoal[0], newgoal[1]])
			if len(flat) == 0:
				print("out of spots to assign")
				break

	def dist(self, point1, point2):
		diff = [p1 - p2 for p1, p2 in zip(point1, point2)]
		return np.linalg.norm(diff)

	def closest(self, points, robot):
		# replace with binary search if you have time
		# find index of where the xcoords are strictly larger than cpos.x
		n = self.findSplitIndex(points, robot.position)
		d = np.linalg.norm([a - b for a, b in zip(robot.position, robot.goal)])
		subarray = [points[n]]
		i = 1
		while n - i >= 0:
			dL = np.linalg.norm([a - b for a, b in zip(points[n-i], robot.position)])
			if dL < d:
				testpoint = points[n-i]
				subarray.append(testpoint)
				i += 1
			else:
				break

		i = 1
		while n + i < len(points):
			dR = np.linalg.norm([a - b for a, b in zip(points[n+i], robot.position)])
			if dR < d:
				testpoint = points[n+i]
				subarray.append(testpoint)
				i += 1
			else:
				break
		subarray = sorted(subarray, key=lambda x: x[1])

		minimum_d = np.linalg.norm([(a-b) for a, b in zip(subarray[0], robot.position)])
		newgoal = subarray[0]
		mindex = 0
		for index, sub in enumerate(subarray):
			diff = [(a-b) for a, b in zip(sub, robot.position)]
			newmin = np.linalg.norm(diff)
			if newmin < minimum_d:
				minimum_d = newmin
				minpoint = index
				newgoal = sub
		print("new goal found", newgoal, "previous goal", robot.goal)
		#print("||| new points |||", points)
		return newgoal


	def findSplitIndex(self, points, pos):
		for i, p in enumerate(points):
			if p[0] > pos[0]:
				return i-1
		return len(points) -1

	def stepRobots(self):
		for r in self.robots:
			r.step()

	def bruteForce(self, flat, robot):
		minimum = np.linalg.norm([a-b for a, b in zip(robot.goal, flat[0])])
		mindex = 0
		newgoal = flat[0]
		for i, p in enumerate(flat):
			check = np.linalg.norm([a-b for a, b in zip(robot.goal, p)])
			if check < minimum:
				mindex = i
				newgoal = p
				minimum = check
		return newgoal


if __name__ == '__main__':
	manager = RobotManager(num = 7)
	hull = [np.array([[3, 3], [10, 10], [2, 2], [1, 1], [0, 4]])]
	manager.assignRobots(hull)
	manager.smartAssignRobots(hull)

	for i in range(5):
		manager.stepRobots()


