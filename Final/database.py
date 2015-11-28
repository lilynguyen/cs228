import pickle

# =========================================
# DATABASE ================================
# =========================================

class Database():
	def __init__(self, userName, database):
		self.__userName = userName
		self.database = database

		self.userRecord = None

	def user_exists(self):
		if self.__userName in self.database:
			return True

		elif self.__userName not in self.database:
			return False

	def add_login(self):
		self.userRecord = self.database[self.__userName] # defines the constant
		self.userRecord['logins'] += 1
		self.save_database()

# {'lily': {'logins' : 0,								userRecord['logins'] = 0
# 					'digitAttempts' : {0 : 0,		userRecord['digitAttempts'][0] = 0
# 														 1 : 0,
# 														 2 : 0,
# 														 3 : 0,
# 														 4 : 0,
# 														 5 : 0,
# 														 6 : 0,
# 														 7 : 0,
# 														 8 : 0,
# 														 9 : 0},
# 					'digitTimes' : {0 : 0,
# 												 	1 : 0,
# 												 	2 : 0,
# 												 	3 : 0,
# 												 	4 : 0,
# 												 	5 : 0,
# 												 	6 : 0,
# 												 	7 : 0,
# 												 	8 : 0,
# 												 	9 : 0},
# 					'besttime' : 0,
# 					'completedLvls' : {1 : False,
# 														 2 : False,
# 														 3 : False}
# 				 }
# }

	def create_profile(self):
		self.database[self.__userName] = {'logins': 0, 
			'digit0attempts' : 0, 
			'digit1attempts' : 0, 
			'digit2attempts' : 0, 
			'digit3attempts' : 0, 
			'digit4attempts' : 0, 
			'digit5attempts' : 0, 
			'digit6attempts' : 0, 
			'digit7attempts' : 0, 
			'digit8attempts' : 0, 
			'digit9attempts' : 0,  
			'digit0attempts' : 0, 
			'digit0time' : 100, 
			'digit1time' : 100, 
			'digit2time' : 100, 
			'digit3time' : 100, 
			'digit4time' : 100, 
			'digit5time' : 100, 
			'digit6time' : 100, 
			'digit7time' : 100, 
			'digit8time' : 100, 
			'digit9time' : 100, 
			'besttime' : 100,
			'complvl1' : False,
			'complvl2' : False,
			'complvl3' : False
		}

	def add_attempt(self, gestureNum):
		digitString = 'digit'+str(gestureNum)+'attempts'
		self.userRecord[digitString] += 1

		print 'Adding 1 to', digitString
		self.save_database()

	def add_time(self, gestureNum, time):
		timeString = 'digit'+str(gestureNum)+'time'

		if time < self.userRecord[timeString]:
			self.userRecord[timeString] = time
			print 'New Time Record'
		else:
			print 'Time Slower than Prev Record'

		self.save_database()

	def save_database(self):
		pickle.dump(self.database, open('userData/database.p','wb'))