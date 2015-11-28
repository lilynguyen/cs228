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

	def save_database(self):
		pickle.dump(self.database, open('userData/database.p','wb'))

	# def get_leaderboard(self): #leaderboard appended in order
		# leaderboard = []

		# iterate through dictionary, grab usernames and their 'besttime'
		# append these to TWO LISTS, one for names one for their time MAKE SURE INDICES MATCH
		# find max of score list, set to highest
		# get index of that, retrieve username
		# delete both of these from each list
		# finx max of new list without the TOP highest...do again until get TOP THREE

		# problem with this is that what if one person has multiple GREAT RUNS that beat everyone else
		# it's as if the user can only have one best score...how do you keep track of all the top scores.
		# ADD THEM AS THEY COME IN...KEEP TRACK OF ALL THE BEST SCORES TOTAL EVER?
		# PUT THAT INTO A DB? JUST FOR SCORES?

		# return leaderboard