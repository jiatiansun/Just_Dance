class Panel(object):

    def __init__(self, background, buttonMap):
        self.img = background
        self.itemDict = buttonMap
        # print self.itemDict.keys()

    def addItem(self, itemKey, itemRef):
        self.itemDict[itemKey] = itemRef

    def getBackground(self):
        return self.img

    def setBackground(self, newImg):
        self.img = newImg

    def getItem(self,key):
        return self.itemDict[key]

    def setItem(self,key,val):
        self.itemDict[key] = val

    def show(self):
        self.img.show()
        for item in self.itemDict:
            self.itemDict[item].show()

    def hide(self):
        self.img.hide()
        for item in self.itemDict:
            self.itemDict[item].hide()

    def destroy(self):
        self.img.destroy()
        for item in self.itemDict:
            self.itemDict[item].destroy()

    def __str__(self):
        return self.itemDict.keys()[0]