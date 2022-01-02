#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from obswebsocket import obsws, events, requests  # noqa: E402

from tally import Tally
from Scene import Scene


#OBS Settings
host = "localhost"
port = 4444
password = "xhainavx"

#MQTT Settings
mqttServer = "localhost"
mqttport = 1883


tallyList = []
tallyList.append(Tally("BM Port 1 - PTZ", mqttServer, mqttport, "wled/tally2/api", "?PL=1", "?PL=2", "?PL=3"))
tallyList.append(Tally("BM Port 2 - S1",mqttServer,mqttport,"wled/tally3/api", "?PL=1", "?PL=2", "?PL=3"))
projectorScene = "Projector AUX"


############################

ws = obsws(host, port, password)

scene_Live = []
scene_Prev = []
current_Live = ""
current_Prev = ""

###
#  Initialize lokal Cache to speedup 
###

sceneList = [] #list off scene objects with info about sources

nestedScenes = []  #list off all scenes that are used as sources somewhere

tallySrcs = [] #list to hold all srources that are used to trigger a tally light

def getSrcVisibility(sceneName, srcName):#
    global tallySrcs
    global sceneList
    global tallyList
    #loop thru all scenes until we find the scene we are looking for
    for scene in sceneList:
        if scene.name == sceneName:
            #loop thru all src in this scene and check if it is the src we are looking for and if it is visible
            for src in scene.srcs:
                if src["name"] == srcName and src["visible"]:
                    return True
            #if this does not return a True lets check all scenes in this scene
            for nestedscene in scene.scenes:
                if nestedscene["visible"]: #only check for scenes that are visible
                    if getSrcVisibility(nestedscene["name"], srcName):
                        return True
    return False
            

def setTallys():
    #this will set the tallys acording to to the cached lists
    global scene_Prev
    global scene_Live
    global current_Live
    global current_Prev
    global projectorScene
    global tallySrcs
    global sceneList
    global tallyList
    for tally in tallyList:
        tally.off() #set default state
        if getSrcVisibility(current_Prev, tally.getName()):
            tally.preview()
        if getSrcVisibility(current_Live, tally.getName()):
            tally.live()
        tally.setProjector(getSrcVisibility(projectorScene, tally.getName()))
        tally.update()
    return

def on_event(message):
    return

def on_preview(message):
    global scene_Prev
    global current_Prev 
    current_Prev = message.getSceneName()
    setTallys()

def on_visibilityChanged(message):
    global sceneList
    global nestedScenes
    for scene in sceneList:
        if (scene.name == message.getSceneName()):
            #we found the correct scene in that the visibility change happend, lets find the src element (remeber, this could also be a scene)
            for src in scene.srcs:
                if src["name"] == message.getItemName():
                    src["visible"] = message.getItemVisible()
            for tmpScene in scene.scenes:
                if tmpScene["name"] == message.getItemName():
                    tmpScene["visible"] = message.getItemVisible()
    setTallys()
    return

def on_switch(message):
    global scene_Live
    global current_Live
    current_Live = message.getSceneName()
    setTallys()
    

ws.register(on_event)
ws.register(on_preview, events.PreviewSceneChanged)
ws.register(on_visibilityChanged, events.SceneItemVisibilityChanged)
ws.register(on_switch, events.SwitchScenes)
ws.connect()
current_Prev = ws.call(requests.GetPreviewScene()).getName()
current_Live = ws.call(requests.GetCurrentScene()).getName()


#populate SceneList
result = ws.call(requests.GetSceneList())
for scene in result.getScenes():
    temp = Scene(scene["name"])
    for src in scene["sources"]:
        if src["type"] == "scene":
            nestedScenes.append(src["name"])
            temp.scenes.append({"name":src["name"],"visible":src["render"]})
        else:
            temp.srcs.append({"name":src["name"], "visible":src["render"]})
    sceneList.append(temp)

nestedScenes = list(dict.fromkeys(nestedScenes))

#populate TallySrcList
for tally in tallyList:
    tallySrcs.append(tally.getName())

tallySrcs = list(dict.fromkeys(tallySrcs))

setTallys()

print("OBS Tally script started")

while True:
    try:
        time.sleep(.1)
        for tally in tallyList:
            tally.callMQTTLoop()


    except KeyboardInterrupt:
        ws.disconnect()
        break

