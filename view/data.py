
MainWindow = None
def initMainWindow(win):
    global MainWindow
    MainWindow = win

def gMainWindow():
    global MainWindow
    return MainWindow

class MenuBarData:
    def __init__(self, name, actions):
        self.name = name
        self.actions = actions

