class Scene:
    def __init__(self, name = ""):
        #print("new Scene Object created")
        self.srcs = [] #all sources with visible state of this scene, including srcs from nested scenes
        self.scenes = [] #list of all nested scenes
        self.name = name
