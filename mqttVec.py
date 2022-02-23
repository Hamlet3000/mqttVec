#!/usr/bin/env python3

import anki_vector
import paho.mqtt.client as mqtt
import time

###############################################################################
def main():
        
    voltage = 0
    batlevel = 0
    charging = 0
    docked = 0
    status = "error"
    ltime = time.strftime("%d.%m.%Y %H:%M:%S")
    
    try:
        # Connect to Vector and get battery info
        with anki_vector.Robot(behavior_control_level=None, 
                               cache_animation_lists=False) as robot:
            
            battery_state = robot.get_battery_state()
            voltage  = battery_state.battery_volts
            batlevel = battery_state.battery_level
            charging = battery_state.is_charging
            docked   = battery_state.is_on_charger_platform
            status   = get_status(robot)
    except:
        print("couldn't connect to Vector")

    # In the openHAB channel, use a jsonpath transform to get specific values like this: JSONPATH:$..voltage
    data = {}
    data['robots'] = []
    data['robots'].append({
       'name': 'Vector Green',
       'voltage': voltage,
       'batlevel': batlevel,
       'charging': charging,
       'docked': docked,
       'time': ltime,
       'status': status
    })
   
    # Configure and publish data to mqtt
    do_mqtt(data)

###############################################################################
def get_status(robot):
    
    status = "error"
    if robot.status.are_motors_moving:
        status = "Vector is moving"
    if robot.status.are_wheels_moving:
        status = "Vector's wheels are moving"
    if robot.status.is_animating:
        status = "Vector is animating"
    if robot.status.is_being_held:
        status = "Vector is being held"
    if robot.status.is_button_pressed:
        status = "Vector's button was button pressed"
    if robot.status.is_carrying_block:
        status = "Vector is carrying his block"
    if robot.status.is_charging:
        status = "Vector is currently charging"
    if robot.status.is_cliff_detected:
        status = "Vector has detected a cliff"
    if robot.status.is_docking_to_marker:
        status = "Vector has found a marker and is docking to it"
    if robot.status.is_falling:
        status = "Vector is falling"
    if robot.status.is_head_in_pos:
        status = "Vector's head is in position"
    if robot.status.is_in_calm_power_mode:
        status = "Vector is in calm power mode"
    if robot.status.is_lift_in_pos:
        status = "Vector's arm is in position"
    if robot.status.is_on_charger:
        status = "Vector is on the charger"
    if robot.status.is_pathing:
        status = "Vector is traversing a path"
    if robot.status.is_picked_up:
        status = "Vector is picked up"
    if robot.status.is_robot_moving:
        status = "Vector is in motion"

    return status

###############################################################################
def on_publish(client, userdata, mid):
    print("Message published to broker")

###############################################################################
def do_mqtt(data):
    
    # define variables for MQTT
    MQTT_HOST = "192.168.0.7"
    MQTT_TOPIC = "Vector"
    MQTT_PORT = 1883
    MQTT_KEEPALIVE_INTERVAL = 20
    MQTT_USER = "YOUR_MQTT_USER"
    MQTT_PW = "YOUR_MQTT_PW"

    # Convert it to text? Not sure why I did this but it works. Yay, 1am programming.
    MQTT_MSG = str(data)

    # Initiate MQTT Client
    mqttc = mqtt.Client()

    # Set username and password for the Broker
    mqttc.username_pw_set(MQTT_USER, MQTT_PW)
    
    # Register publish callback function
    #mqttc.on_publish = on_publish
    
    # Connect with MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    
    # Publish message to MQTT Broker
    mqttc.publish(MQTT_TOPIC,MQTT_MSG)
    
    # Disconnect from MQTT_Broker
    mqttc.disconnect()


###############################################################################
if __name__ == "__main__":
    main()

