from krita import *

class SwitchBrushAlternative(Extension):

    shareOpacity = False
    shareSize = False
    lastestPresetGroup = ""
    latestOpacity = None
    latestSize = None

    def __init__ (self,parent):
        super().__init__(parent)

    def setup(self) :
        if Application.readSetting("sb_alternative", "shareOpacity", "true") == "true":
            self.shareOpacity = True
        if Application.readSetting("sb_alternative", "shareSize", "true") == "true":
            self.shareSize = True

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
        ss = currentPreset.name().replace(" ","_")
        ss = ss.split("[")[0]

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
    
    def switchToAlternate(self,pi) :
        # if nextpresetgroup == latestgroup
        #     if current shareOpacity
        #         save Opacity
            
        #     changepreset
        #     if check opacity parameter
        #             change opaciy to globalsavedopacity
        #     latest = currentperst

        # else
        #   change preset
        #   set latest = preset
        #   Opacity = nan
        ###########################

        # w = Application.activeWindow()
        # w.views()[0].activateResource(self.alternateBrush()[pi])
        
        v = Application.activeWindow().views()[0]
        p = self.alternateBrush()[pi]

        
        np = p.name().replace(" ","_").split("[")
        if np[0].endswith("_") : np[0] = np[0][:-1]
        li = len(np)
        while li < 3 :
            np.append("_")
            li = len(np)
        cp = v.currentBrushPreset().name().replace(" ","_").split("[")
        if cp[0].endswith("_") : cp[0] = cp[0][:-1]
        li = len(cp)
        while li < 3 :
            cp.append("_")
            li = len(cp)

        ddbug = 0
        
        if np[0] != self.lastestPresetGroup :
            self.latestOpacity = None
            self.latestSize = None

        if cp[2].find("o") == -1 :
            self.latestOpacity = v.paintingOpacity()
        if cp[2].find("s") == -1 :
            self.latestSize = v.brushSize()

        v.activateResource(p)

        if self.shareOpacity & (np[2].find("o") == -1) :
            if self.latestOpacity != None :
                v.setPaintingOpacity(self.latestOpacity)
        if self.shareSize & (np[2].find("s") == -1) :
            if self.latestSize != None :
                v.setBrushSize(self.latestSize)

        self.lastestPresetGroup = np[0]

        
        
    
    def createActions(self,window):
        self.sb_alternative_next = window.createAction("sb_alternative_next", "Switch Next Alternate Brush")
        self.sb_alternative_prev = window.createAction("sb_alternative_prev", "Switch Previous Alternate Brush")

        # Create visibility toggle action
        self.sb_alternative_op = window.createAction("sb_alternative_op", "SB Share Opacity")
        #action.toggled.connect(self.pad.toggleWidgetVisible)
        self.sb_alternative_op.setCheckable(True)
        self.sb_alternative_op.setChecked(self.shareOpacity)

        # Create visibility toggle action
        self.sb_alternative_sz = window.createAction("sb_alternative_sz", "SB Share Size")
        #action.toggled.connect(self.pad.toggleWidgetVisible)
        self.sb_alternative_sz.setCheckable(True)
        self.sb_alternative_sz.setChecked(self.shareOpacity)

        @self.sb_alternative_op.toggled.connect
        def on_sb_alternative_op_toggled(toggled):
            Application.writeSetting("sb_alternative", "shareOpacity", str(toggled).lower())
            self.shareOpacity = toggled

        @self.sb_alternative_sz.toggled.connect
        def on_sb_alternative_sz_toggled(toggled):
            Application.writeSetting("sb_alternative", "shareSize", str(toggled).lower())
            self.shareSize = toggled

        @self.sb_alternative_next.triggered.connect
        def on_sb_alternative_next_trigger():
            self.switchToAlternate(1)
            
        @self.sb_alternative_prev.triggered.connect
        def on_sb_alternative_prev_trigger():
            self.switchToAlternate(0)
    
    

Krita.instance().addExtension(SwitchBrushAlternative(Krita.instance()))