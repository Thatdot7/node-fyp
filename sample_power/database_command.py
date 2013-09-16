import sqlite3
import sys
from crontab import CronTab

def setup():
        cron = CronTab()
	cron.remove_all("")
	cron.write()
        job = cron.new(command='python /home/pi/node-fyp/sample_power/database_command.py hourly')
        job.minute.on(0)
        job = cron.new(command='python /home/pi/node-fyp/sample_power/database_command.py daily')
        job.minute.on(0)
	job.hour.on(0)
        cron.write()
        
	conn = sqlite3.connect('/home/pi/node-fyp/sample_power/test.db')

	conn.execute("PRAGMA journal_mode = WAL;")

	# Forming row_counters table
	#
	# This will keep track of the entry it will next write to in the
	# given table
	print "Creating and filling table 'row_counters'"
	conn.execute("DROP TABLE IF EXISTS row_counters;")
	conn.execute("CREATE TABLE IF NOT EXISTS row_counters ( \
		table_name TEXT PRIMARY KEY,\
		counter INTEGER);")

	conn.execute("INSERT INTO row_counters VALUES ('real_time_record', 1)")

	# Forming real time record
	#
	# This will keep track of energy used and real power every second
	print "Creating 'real_time_record' and filling it with 10000 dummy rows"
	conn.execute("DROP TABLE IF EXISTS real_time_record;")
	conn.execute("CREATE TABLE real_time_record (\
		rowID INTEGER,\
		time TIMESTAMP,\
		real_power REAL,\
		energy REAL);")

	for i in range(10000):
		conn.execute("INSERT INTO real_time_record VALUES (\
			" + str(i+1) + ", datetime(CURRENT_TIMESTAMP),\
                         0, 0 );")

	# Hourly
	#
	# This will keep track of energy used in hourly blocks
	print "Creating 'hourly_record'"
	conn.execute("DROP TABLE IF EXISTS hourly_record;")
	conn.execute("CREATE TABLE IF NOT EXISTS hourly_record (\
		time TIMESTAMP,\
		energy REAL);")

	conn.commit()

	# Daily
	#
	# This will keep track of energy used in daily blocks
	print "Creating 'daily_record'"
	conn.execute("DROP TABLE IF EXISTS daily_record;")
	conn.execute("CREATE TABLE IF NOT EXISTS daily_record (\
		time TIMESTAMP,\
		energy REAL);")

	conn.commit()
	conn.close()


def hourly():
	conn = sqlite3.connect('/home/pi/node-fyp/sample_power/test.db')

        cur = conn.cursor()
        cur.execute("SELECT TOTAL(energy) FROM real_time_record WHERE (time > datetime(CURRENT_TIMESTAMP, '-1 hour'));")

        energy_total = cur.fetchone()[0]
	if not energy_total:
		energy_total = 0

        conn.execute("INSERT INTO hourly_record VALUES (datetime(CURRENT_TIMESTAMP), " + str(energy_total) + ");")
        conn.commit()
        conn.close()

def daily():
	conn = sqlite3.connect('/home/pi/node-fyp/sample_power/test.db')

        cur = conn.cursor()
        cur.execute("SELECT TOTAL(energy) FROM hourly_record WHERE (time > datetime(CURRENT_TIMESTAMP, '-1 day'));")

        energy_total = cur.fetchone()[0]
	if not energy_total:
		energy_total = 0

        conn.execute("INSERT INTO daily_record VALUES (datetime(CURRENT_TIMESTAMP), " + str(energy_total) + ");")
        conn.commit()
        conn.close()


if __name__ == "__main__":
	if sys.argv[1] == "setup":
		setup()
        elif sys.argv[1] == "hourly":
                hourly()
	elif sys.argv[1] == "daily":
		daily()
