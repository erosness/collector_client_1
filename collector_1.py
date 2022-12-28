import requests
import json
import time
import datetime
import serial

unit_serial = "001"
logger_id = "PC erik-gone-native"
timestamp = time.localtime

url_host = "http://collector.rosness.no:8001/" 
#url_host = "http://localhost:8001/" 
unit_url_path = "probaker/api/unit.php" 
session_url_path = "probaker/api/session.php" 
log_url_path = "probaker/api/log.php" 
unit_serial_parameter = "unit_serial=" + unit_serial
logger_id_parameter = "logger_id=" + logger_id

url_string = url_host + unit_url_path + "?" + logger_id_parameter
response_payload = requests.get(url_string)
unit_info = json.loads(response_payload.text)

unit_id = unit_info["unit_id"]
unit_id_parameter = "unit_id=" + unit_id

ser = serial.Serial('/dev/ttyUSB0', 921600 )
ser.reset_input_buffer()

while True:
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


    session_data = {
        "unit_id" : unit_id,
        "start_time" : st,
        "is_autoinitiated" : 1,
        "session_name" : ""
    }


    session_data_str = json.dumps(session_data)

    url_string = url_host + session_url_path + "?" + unit_id_parameter
    response_payload = requests.post(url_string, session_data_str)
    session_info = json.loads(response_payload.text)

    session_id = session_info["session_id"]
    session_id_parameter = "session_id=" + session_id

    new_session = False
    while not new_session:
        line = ser.readline()
        try:
            log_data = json.loads(line)
        except:
            print("JSON parse error")
            out_data = {
                "time" : 0
            }
        else:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            out_data = {"session_id" : session_id,
                        "log_time" : st,
                        "machine_time" : log_data["time"] }

            if("torque" in log_data):
                out_data["torque"] = log_data["torque"]

            if("state" in log_data):
                out_data["state"] = log_data["state"]
                if log_data["state"]["change"] & 1 and log_data["state"]["machine_state"]==1:
                    new_session = True

            if("input" in log_data):
                out_data["input"] = log_data["input"]

            out_data_str = json.dumps(out_data)

            url_string = url_host + log_url_path + "?" + session_id_parameter
            response_payload = requests.post(url_string, out_data_str)


        print("Etter  loop")

print ("end")


