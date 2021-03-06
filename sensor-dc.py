#!/usr/bin/python
# Script by: Anggit M Ginanjar
#            anggit.ginanjar@merahputih.id
#            https://github.com/anggitmg

# Library ini digunakan untuk membaca output sensor 2302
import Adafruit_DHT as dht

# Import library mysql.connector yang telah di install menggunakan perintah
# "$python -m pip install mysql-connector"
# Library ini digunakan untuk melakukan koneksi antara script python dan database (Mysql)
import mysql.connector

# Import datetime library untuk menggunakan fungsi "Date and time" pada python
import datetime

# 1. Membuat variable kelembaban dan suhu
# 2. Sensor menggunakan tipe AM2302, maka function yang dipakai dht.AM2302
# 3. Pin yang digunakan pada GPIO Raspberry adalah 23
# 4. Maka parameter fungsi yang digunakan adalah:
#    dht.read_retry(jenis_sensor, pin_yang_digunakan)
kelembaban, suhu = dht.read_retry(dht.AM2302, 25)
suhu = '{0:0.1f}'.format(suhu)
kelembaban = '{0:0.1f}'.format(kelembaban)

# Variable "now" untuk menghasilkan waktu sekarang/saat sensor suhu aktif
log_time = datetime.datetime.now()

# Randomed ID for sensor_id on table
# bulan+jam+menit+detik
bulan = log_time.month
jam = log_time.hour
menit = log_time.minute
detik = log_time.second
sensor_id = str(bulan) + str(jam) + str(menit) + str(detik)

print(suhu, kelembaban, sensor_id)

# Database: sensor
# Table: sensor_dc_log
# Columns:
# | id | temperature | humidity | log_time |

# Inisialisasi koneksi ke database mysql
mydb = mysql.connector.connect(
	host="localhost",
	user="sensor",
	passwd="P4ssword",
	database="sensor"
)

## In order to put our new connnection to good use we need to create a cursor object. 
# The cursor object is an abstraction specified in the Python DB-API 2.0. 
# It gives us the ability to have multiple seperate working environments through the same connection to the database
mycursor = mydb.cursor()

# sql query untuk melakukan insert ke table sensor_dc_log database
sql = "INSERT INTO sensor_dc_log (id, temperature, humidity, log_time) VALUES (%s, %s, %s, %s)"
val = (sensor_id, suhu, kelembaban, log_time)
mycursor.execute(sql, val)

# Commit untuk melakukan perubahan pada table
mydb.commit()

# print jika berhasil ...
print("Data pada tanggal: " + str(log_time) + " telah dimasukan! :)")