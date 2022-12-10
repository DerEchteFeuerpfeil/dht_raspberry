import time
import board
import adafruit_dht as ad
import sqlite3

# sleep interval in seconds between measurements 
INTERVAL = 20

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print("Version: ",sqlite3.version)
		return conn
	except sqlite3.Error as e:
		print("ERROR ",e)
	

def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except sqlite3.Error as e:
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
	
	database = "tempdata.db"
	
	# create a database connection
	conn = create_connection(database)
	
	# create tables
	if(conn is not None):
		create_table(conn, sql_create_table)
	else:
		print("Error! Cannot create db connection.")
		
	dht_device = ad.DHT22(board.D4, use_pulseio=False)

	# measure loop
	while True:
		try:
			temp = dht_device.temperature
			humidity = dht_device.humidity
			measure_time = time.time()
			data = [int(measure_time), float(temp), float(humidity)]
			insert_measurement(conn, data)
		except RuntimeError as er:
			print(er)
			time.sleep(INTERVAL)
			continue
		except KeyboardInterrupt:
			conn.close()
			dht_device.exit()
			print("INTERRUPTED")
			break
		except Exception as er:
			conn.close()
			dht_device.exit()
			raise er
		time.sleep(INTERVAL)
	
		
	



