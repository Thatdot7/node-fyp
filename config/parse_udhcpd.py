f = open('node-fyp/config/originals/udhcpd.conf','r')

output = f.read()

f.close()

output = output.split('\n')

filtered = []

for lines in output:
	if '#' in lines:
		continue
	elif lines is '':
		continue
	else:
		lines = lines.split(' ')
		filtered.append(lines)

print filtered

f = open('temp_udhcpd', 'w')

file_content = ''

for lines in filtered:
	for items in lines:
		file_content = file_content + items + " "

	file_content = file_content + '\n'	

f.write(file_content)
f.close()
