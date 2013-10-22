with open('originals/dhcpd.conf', 'r') as f:
	data = f.read()

data = data.split('\n')

newdata = []
for line in data:
	try:
		if line[0] != '#':
			newdata.append(line)
	except:
		continue

print newdata
