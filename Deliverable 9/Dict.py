try:
	import pickle
except ImportError:
	print 'ERR: Package "pickle" doesn\'t exist'
else:
	try:
		database = pickle.load(open('userData/database.p','rb'))

		userName = raw_input('Please enter your name: ')
		userName = userName.lower()
		formattedName = userName[0].upper() + userName[1:]

		if userName in database:
			userRecord = database[userName]#['logins'] += 1
			userRecord['logins'] += 1
			print 'Welcome back ' + formattedName + '!'

		elif userName not in database:
			database[userName] = {}
			database[userName] = {'logins': 1}
			print 'Welcome ' + formattedName + '!'

		print database

		pickle.dump(database, open('userData/database.p','wb'))
		
	except IOError:
		print 'ERR: File "database.p" doesn\'t exist'
finally:
	print 'Terminating Program'