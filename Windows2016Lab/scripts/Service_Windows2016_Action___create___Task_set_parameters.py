username = 'user-{}'.format(_construct_random_password(8,numDigits=4, numLetters=4, numPuncs=0, numCaps=0).lower())
password = _construct_random_password(10,upper=14, numDigits=4)
print('ACCESS_USERNAME={}'.format(username))
print('ACCESS_PASSWORD={}'.format(password))

calm_index = int('@@{calm_array_index}@@')
email_list = '''@@{EMAIL_LIST}@@'''
clean_list = [x for x in email_list.splitlines() if x.strip(' ')]
if calm_index < len(clean_list):
    print('EMAIL={}'.format(clean_list[calm_index]))
else:
	print('EMAIL={}'.format(clean_list[0]))
