import paho.mqtt.client as mqtt

class Tally:
    client = mqtt.Client()
    state = "off"
    projectorState = False
    def __init__(self, name, mqttServer, mqttPort, mqttTopic, payloadOff ="?PL=1", payloadPreview = "?PL=2", payloadLive = "?PL=3"):
        self.name = name
        self.mqtt = mqttTopic
        self.payloadOff = payloadOff
        self.payloadPreview = payloadPreview
        self.payloadLive = payloadLive
        self.client.connect(mqttServer,mqttPort,60)

    def live(self):
        self.state = "live"

    def preview(self):
        self.state = "prev"

    def off(self):
        self.state = "off"

    def update(self):
        if self.projectorState:
            self.client.publish(self.mqtt, self.payloadLive)
            return
        if self.state == "live":
            self.client.publish(self.mqtt, self.payloadLive)
            return
        if self.state == "prev":
            self.client.publish(self.mqtt, self.payloadPreview)
            return
        self.client.publish(self.mqtt, self.payloadOff)

    def setProjector(self, pstate):
        self.projectorState = pstate
        return

    def getName(self):
        return self.name

    def callMQTTLoop(self):
        return self.client.loop()
