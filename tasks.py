import os
from time import sleep
from datetime import datetime
import tinytuya
from pyModbusTCP.client import ModbusClient
from w1thermsensor import W1ThermSensor

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def modbus_read_loop():
    bulb_01 = tinytuya.OutletDevice(dev_id=os.getenv("B1_ID"), address=os.getenv("B1_IP"),
                                    local_key=os.getenv("B1_KEY"), version=3.3)  # NOQA
    bulb_02 = tinytuya.OutletDevice(dev_id=os.getenv("B2_ID"), address=os.getenv("B2_IP"),
                                    local_key=os.getenv("B2_KEY"), version=3.3)  # NOQA
    bulb_03 = tinytuya.OutletDevice(dev_id=os.getenv("B3_ID"), address=os.getenv("B3_IP"),
                                    local_key=os.getenv("B3_KEY"), version=3.3)  # NOQA
    bulb_04 = tinytuya.OutletDevice(dev_id=os.getenv("B4_ID"), address=os.getenv("B4_IP"),
                                    local_key=os.getenv("B4_KEY"), version=3.3)  # NOQA
    bulb_05 = tinytuya.OutletDevice(dev_id=os.getenv("B5_ID"), address=os.getenv("B5_IP"),
                                    local_key=os.getenv("B5_KEY"), version=3.3)  # NOQA
    bulb_06 = tinytuya.OutletDevice(dev_id=os.getenv("B6_ID"), address=os.getenv("B6_IP"),
                                    local_key=os.getenv("B6_KEY"), version=3.3)  # NOQA
    bright = 10
    temperature = 0
    last_loop_sec = 0

    while True:

        try:
            c = ModbusClient(host=os.getenv("PLC_IP"), auto_open=True, auto_close=True)
            modbus_input_map = c.read_discrete_inputs(1025, 255)
            outputs = []
            for pk, val in enumerate(modbus_input_map):
                if val:
                    #                     print(pk)
                    #                     print(datetime.datetime.now())
                    outputs.append(pk)
            if datetime.now().second != last_loop_sec:
                last_loop_sec = datetime.now().second
                outputs.append(datetime.now())
                print(outputs)
            if modbus_input_map[138]:
                bright += 99
                bright = check_limit(bright)
                print('lighter', bright)
                set_light_value(bright, 22, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
            elif modbus_input_map[137]:
                bright -= 99
                bright = check_limit(bright)
                print('darker', bright)
                set_light_value(bright, 22, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
            elif modbus_input_map[136]:
                temperature += 99
                temperature = check_limit(temperature)
                print('colder', temperature)
                set_light_value(temperature, 23, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
            elif modbus_input_map[135]:
                temperature -= 99
                temperature = check_limit(temperature)
                print('hotter', temperature)
                set_light_value(temperature, 23, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
            else:
                sleep(0.1)
        except TypeError:
            print("PLC disconnected")
            sleep(0.5)


def set_light_value(value, index, b1, b2, b3, b4, b5, b6):
    sleep(0.02)
    b1.set_value(value=value, index=index)
    b2.set_value(value=value, index=index)
    b3.set_value(value=value, index=index)
    b4.set_value(value=value, index=index)
    b5.set_value(value=value, index=index)
    b6.set_value(value=value, index=index)


def check_limit(value):
    if value > 999:
        value = 999
    if value < 10:
        value = 10
    return value


@app.task
def modbus_xy_read():
    start = datetime.timestamp(datetime.now())
    i = 0
    trig_y = False
    while True:

        #     try:
        c = ModbusClient(host=os.getenv("PLC_IP"), auto_open=True, auto_close=True)
        modbus_input_map = c.read_discrete_inputs(1024, 255)
        modbus_output_map = c.read_discrete_inputs(1280, 16)

        if not trig_y and modbus_output_map[3]:
            print("trig on")
            trig_y = True
        if trig_y and not modbus_output_map[3]:
            print("trig off")
            trig_y = False

        for pk, val in enumerate(modbus_input_map):
            if val and pk == 72:
                i += 1
                if i == 2:
                    print(pk, f"TIMER: {round(datetime.timestamp(datetime.now()) - start, 3)}")
                sleep(0.3)
                if i >= 3:
                    end = datetime.timestamp(datetime.now()) - start
                    print(pk, f"TIMER: {round(end, 3)}", f"Actual consumption: {3600.0 / end}")
                    start = datetime.timestamp(datetime.now())
                    i = 1
    #     except:
    #         print("error")
    #         sleep(1)


@app.task
def read_1wire_sensors():
    amount = 0
    tries = 0
    while True:
        list = []
        tries += 1
        try:
            for sensor in W1ThermSensor.get_available_sensors():
                list.append(sensor.id)
                list.append("Actual temp: ")
                list.append(round(sensor.get_temperature(), 1))
            print(list, f'No of Errors: {amount}', f'No of tries: {tries}')
            sleep(1)
        except:
            amount += 1
            print(amount, 'sensor error')
            sleep(0.2)


@app.task
def read_bt_xiaomi():
    from lywsd03mmc import Lywsd03mmcClient

    client = Lywsd03mmcClient("A4:C1:38:8B:12:55")

    data = client.data
    print('Gabinet: ', "A4:C1:38:8B:12:55", '- Battery: ', str(data.battery))
    print('Temperature: ', str(data.temperature), '- Humidity: ', str(data.humidity))
    print('   ')

    client = Lywsd03mmcClient("A4:C1:38:2E:47:5A")

    data = client.data
    print('Antresola: ', "A4:C1:38:2E:47:5A", '- Battery: ', str(data.battery))
    print('Temperature: ', str(data.temperature), '- Humidity: ', str(data.humidity))
