import pickle
import pprint

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
 			'bestscore' : 0,
			'complvl1' : False,
			'complvl2' : False,
			'complvl3' : False,
			'badge1' : False,
			'badge2' : False,
			'badge3' : False,
			'badge4' : False
		}

	def add_login(self):
		self.userRecord = self.database[self.__userName] # defines the constant
		self.userRecord['logins'] += 1
		self.save_database()

	def add_attempt(self, gestureNum):
		digitString = 'digit'+str(gestureNum)+'attempts'

		self.userRecord[digitString] += 1

		# print 'Adding 1 to', digitString

		self.save_database()

	def add_time(self, gestureNum, currTime):
		timeString = 'digit'+str(gestureNum)+'time'

		if currTime < self.userRecord[timeString]:
			self.userRecord[timeString] = currTime
			# print 'New best gesture time'
		# else:
			# print 'Gesture time slower than prev gesture'

		self.save_database()

	def add_best_time(self, currTime):
		if currTime < self.userRecord['besttime']:
			self.userRecord['besttime'] = currTime
			# print 'New best run time'
		# else:
		# 	print 'Run time slower than prev run'

		self.save_database()

	def add_score(self, roundPoints):
		if roundPoints > self.userRecord['bestscore']:
			self.userRecord['bestscore'] = roundPoints
			# print 'New personal high score'
		# else:
			# print 'Round score lower than current high score'

		self.save_database()

	def completed_lvl1(self):
		print 'Completed Stage 1'
		self.userRecord['complvl1'] = True
		self.save_database()

	def completed_lvl2(self):
		print 'Completed Stage 2'
		self.userRecord['complvl2'] = True
		self.save_database()

	def completed_lvl3(self):
		print 'Completed Stage 3'
		self.userRecord['complvl3'] = True
		self.save_database()

	def latest_level(self):
		if self.userRecord['complvl1'] == False:
			return 1
		elif self.userRecord['complvl1'] == True:
			if self.userRecord['complvl2'] == False:
				return 2
			elif self.userRecord['complvl2'] == True:
				if self.userRecord['complvl3'] == False:
					return 3
				elif self.userRecord['complvl3'] == True:
					return 4

	def earn_badge1(self):
		print 'Achievement: Signed all gestures!'
		self.userRecord['badge1'] = True
		self.save_database()

	def earn_badge2(self):
		print 'Achievement: Memorized gestures!'
		self.userRecord['badge2'] = True
		self.save_database()

	def earn_badge3(self):
		print 'Achievement: Finished all the levels!'
		self.userRecord['badge3'] = True
		self.save_database()

	def earn_badge4(self):
		print 'Achievement: High score over 10!'
		self.userRecord['badge4'] = True
		self.save_database()

	def get_badge1(self):
		return self.userRecord['badge1']

	def get_badge2(self):
		return self.userRecord['badge2']

	def get_badge3(self):
		return self.userRecord['badge3']

	def get_badge4(self):
		return self.userRecord['badge4']

	def save_database(self):
		pickle.dump(self.database, open('userData/database.p','wb'))

	def get_leaderboard(self):
		leaderboard = []
		highest = -1
		highestUser = None
		nhighest = -1
		nhighestUser = None
		nnhighest = -1
		nnhighestUser = None

		for user in self.database:
			if self.database[user]['bestscore'] > highest:
				highest = self.database[user]['bestscore']
				highestUser = user
			else:
				if self.database[user]['bestscore'] > nhighest:
					nhighest = self.database[user]['bestscore']
					nhighestUser = user
				else:
					if self.database[user]['bestscore'] > nnhighest:
						nnhighest = self.database[user]['bestscore']
						nnhighestUser = user

		leaderboard.append(highestUser)
		leaderboard.append(str(highest))
		leaderboard.append(nhighestUser)
		leaderboard.append(str(nhighest))
		leaderboard.append(nnhighestUser)
		leaderboard.append(str(nnhighest))

		return leaderboard

	def display_profile(self):
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.userRecord)