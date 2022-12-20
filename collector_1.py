import requests
import json
import time
import datetime
import serial

unit_serial = "A"
logger_id = "10.0.0.111"
timestamp = time.localtime

#url_host = "http://collector.rosness.no:8001/" 
url_host = "http://localhost:8001/" 
unit_url_path = "probaker/api/unit.php" 
session_url_path = "probaker/api/session.php" 
torque_url_path = "probaker/api/torque.php" 
unit_serial_parameter = "unit_serial=" + unit_serial
logger_id_parameter = "logger_id=" + logger_id

url_string = url_host + unit_url_path + "?" + logger_id_parameter
response_payload = requests.get(url_string)
unit_info = json.loads(response_payload.text)

unit_id = unit_info["unit_id"]
unit_id_parameter = "unit_id=" + unit_id

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


session_data = {
    "unit_id" : unit_id,
    "start_time" : st,
    "is_autoinitiated" : 1,
    "session_name" : "Initial test session"
}


session_data_str = json.dumps(session_data)

url_string = url_host + session_url_path + "?" + unit_id_parameter
response_payload = requests.post(url_string, session_data_str)
session_info = json.loads(response_payload.text)

session_id = session_info["session_id"]
session_id_parameter = "session_id=" + session_id



#print(y["unit_id"])


ser = serial.Serial('/dev/ttyUSB0', 921600 )
ser.reset_input_buffer()
machine_time_counter = 50000


for loopcnt in range(99):
#    print("Før -Loopcnt=", loopcnt)

    line = ser.readline()
    try:
        torque_data = json.loads(line)
    except:
        print("JSON parse error")
        torque_data = {
            "torque":"nothing",
            "time" : 0
        }
    else:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        torque_log = {
            "session_id" : session_id,
            "log_time" : st,
            "machine_time" : torque_data["time"],
            "torque" : torque_data["torque"]
        }

        machine_time_counter+=50
        torque_data_str = json.dumps(torque_log)

        url_string = url_host + torque_url_path + "?" + session_id_parameter
        response_payload = requests.post(url_string, torque_data_str)
#        log_info = json.loads(response_payload.text)


    print("Etter - Loopcnt=", loopcnt, " data: ")
#    time.sleep(1.1)

print ("end")


