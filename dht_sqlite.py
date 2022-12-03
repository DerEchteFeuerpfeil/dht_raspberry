import time
import board
import adafruit_dht as ad
import csv
from datetime import datetime
import sqlite3

# sleep interval in seconds between measurements 
INTERVAL = 60

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
		return conn
	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()
	

def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def insert_measurement(conn, measurement_tuple):
	sql = """INSERT INTO room(datetime,temperature,humidity) VALUES(?,?,?)"""
	cur = conn.cursor()
	cur.execute(sql, measurement_tuple)
	conn.commit()
	
	return cur.lastrowid

if __name__ == "__main__":
	sql_create_table = """CREATE TABLE IF NOT EXISTS room (
							datetime integer PRIMARY KEY,
							temperature real,
							humidity real);"""
	
	database = "~/Desktop/tempdata.db"
	
	# create a database connection
	conn = create_connection(database)
	
	# create tables
	if(conn is not None):
		create_table(conn, sql_create_table)
	else:
		print("Error! Cannot create db connection.")
		
	# measure loop
	
	
		
	

dht_device = ad.DHT22(board.D4, use_pulseio=False)
todate = datetime.now().strftime("%d_%m_%Y")
filename = f"{todate}_temp_log.csv"
f = open(filename, "w+")
f.write("datetime,temperature,humidity\n")

#temp_writer = csv.writer(f, delimiter=",", quotechar="'")
#temp_writer.writerow(["time", "temperature", "humidity"])
while True:
	try:
		temp = dht_device.temperature
		humidity = dht_device.humidity
		data = [datetime.now().strftime("%d.%m.%Y %H:%M:%S"), str(temp), str(humidity)]
		f.write(",".join(data)+"\n")
		print(" ".join(data))
	except RuntimeError as er:
		print(er)
		time.sleep(2.0)
		continue
	except KeyboardInterrupt:
		f.close()
		print("INTERRUPTED")
		break
	except Exception as er:
		f.close()
		dht_device.exit()
		raise er
	time.sleep(2.0)

