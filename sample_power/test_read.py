import sqlite3

conn = sqlite3.connect('/home/pi/node-fyp/sample_power/test.db')

cur = conn.execute('select strftime("%s", time), real_power from real_time_record order by time desc limit 10;')
data = cur.fetchall()

print data
