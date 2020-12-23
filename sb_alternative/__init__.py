from krita import *

class SwitchBrushAlternative(Extension):
    def __init__ (self,parent):
        super().__init__(parent)

    def alternateBrush(self):
        window = Application.activeWindow()
        allPresets = Application.resources("preset")
        currentPreset = window.views()[0].currentBrushPreset()
        prevPreset = None
        nextPreset = None
        firstPreset = None
        lastPreset = None
        presetFound = False
        sp = None
        ss = currentPreset.name().split("[")[0]
        ss =ss.replace(" ","_")

        if ss.endswith("_") : ss = ss[:-1]

        for pp in allPresets:

            if pp != currentPreset.name():
                
                sp = pp.replace(" ","_")
                sp = sp.split("[")[0]
                if sp.endswith("_") : sp = sp[:-1]

                if sp == ss :
                    if firstPreset == None : firstPreset = pp
                    if presetFound == False :
                        prevPreset = pp
                    else :
                        if nextPreset == None : nextPreset = pp
                    lastPreset = pp
                
            else:
                if firstPreset == None : firstPreset = pp
                lastPreset = pp
                presetFound = True

        if nextPreset == None : nextPreset = firstPreset
        if prevPreset == None : prevPreset = lastPreset
        rr = [allPresets[prevPreset], allPresets[nextPreset]]
        return rr
    
    def createActions(self,window):
        self.sb_alternative_next = window.createAction("sb_alternative_next", "Switch Next Alternate Brush")
        self.sb_alternative_prev = window.createAction("sb_alternative_prev", "Switch Previous Alternate Brush")

        @self.sb_alternative_next.triggered.connect
        def on_sb_alternative_next_trigger():
            w = Application.activeWindow()
            w.views()[0].activateResource(self.alternateBrush()[1])
        
        @self.sb_alternative_prev.triggered.connect
        def on_sb_alternative_prev_trigger():
            w = Application.activeWindow()
            w.views()[0].activateResource(self.alternateBrush()[0])
    
    def setup(self):
        pass

Krita.instance().addExtension(SwitchBrushAlternative(Krita.instance()))