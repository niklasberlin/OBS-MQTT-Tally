# OBS-MQTT-Tally
Small script that will connect to OBS via Websockets and set the State of Tally-Light according to the visibility of sources.

## Setup/Configuration
at the top of the script you can find some variables to configure the script (IP-Adresses for OBS and MQTT-Broker), you can also set up any amount of Tally Lights there, just create more Tally Objects and append them to the tallyList. Each Tally-Object takes the following parameters: OBS Source Name, mqttServer, mqttPort, mqtt-adress, mqtt-payload-off, mqtt-payload-preview, mqtt-payload-live 

## Tally Setup
For our Setup we used some ESP8266 with WLED Firmware and set up three scenes (1 - off, 2 - preview and 3 - live), we then configured the controller to connect to our MQTT Broker (see WLED Documentation for Details)

## Licence
This Script is licenced unter the MIT Licence. The used MQTT Library is licenced under the Eclipse Public License 2.0 (https://github.com/eclipse/paho.mqtt.python). The used OBS Webcoket Library is licensed under the MIT License. 
