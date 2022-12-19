import requests
import json
import time
import datetime

unit_serial = "A"
logger_id = "10.0.0.111"
timestamp = time.localtime

url_host = "http://localhost:8001/" 
unit_url_path = "probaker/api/unit/" 
session_url_path = "probaker/api/session/" 
torque_url_path = "probaker/api/torque/" 
unit_serial_parameter = "unit_serial=" + unit_serial
logger_id_parameter = "logger_id=" + logger_id

url_string = url_host + unit_url_path + "?" + logger_id_parameter
response_payload = requests.get(url_string)
unit_info = json.loads(response_payload.text)

unit_id = unit_info["unit_id"]

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


session_data = {
    "unit_id" : unit_id,
    "start_time" : st,
    "is_autoinitiated" : 1,
    "session_name" : "Initial test session"
}


session_data_str = json.dumps(session_data)

url_string = url_host + session_url_path + unit_id
response_payload = requests.post(url_string, session_data_str)
session_info = json.loads(response_payload.text)

session_id = session_info["session_id"]



#print(y["unit_id"])


for loopcnt in range(9):
    print("Før -Loopcnt=", loopcnt)

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    torque_data = {
        "session_id" : session_id,
        "log_time" : st,
        "machine_time" : 50000
    }

    torque_data_str = json.dumps(torque_data)

    url_string = url_host + torque_url_path + session_id
    response_payload = requests.post(url_string, torque_data_str)
    log_info = json.loads(response_payload.text)


    print("Etter - Loopcnt=", loopcnt, " data: ", log_info)
    time.sleep(1.1)

print ("end")


