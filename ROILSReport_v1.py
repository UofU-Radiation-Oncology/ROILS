import wx
import wx.adv
import datetime
import os
#https://github.com/ponty/pyscreenshot

#CheckComment(self,parent,label,test=True,widgetname=None,binding=None,entrylength=300):
#RadioComment(self,parent,label,test=True,choices=['Y','N'],widgetname=None,binding=None,entrylength=100):
#LabelRadioBox(self,parent,label,choices,test=True,widgetname=None,binding=None):
#CalendarBox(self,parent,label,time=False,widgetname=None,binding=None,timebinding=None):
#LabelCombo(self,parent,label,choices,readonly=True,widgetname=None,binding=None):
#LabelEntry(self,parent,label,test=True,returnLabel=False,widgetname=None,binding=None):
        
class InitialCheck(wx.Frame):

    def __init__(self,*args,**kwargs):
        super(InitialCheck, self).__init__(*args, **kwargs)
        self.start = datetime.datetime.now()
        self.path = 'X:/RadOnc/General Access/LO access/AutomatedNarrativeSummaries'
        self.frames = []
        self.index = 0
        self.name = None
        self.results = []
        self.numrx = None
        self.rxindex = None
        self.rxdone = []
        self.widgets = {}
        self.frames.append(self.DemoPanel())
        self.frames[-1].Show()
        self.validation_functions = []
        
        
    def OnQuit(self,event):
        for each in self.frames:
            each.Close()
        self.Close()


    def OnBack(self,event):
        self.frames[self.index].Hide()
        self.index -= 1
        self.frames[self.index].Show()


    def GetRadioChoice(self,widget):
        return widget.GetString(widget.GetSelection())



    def RadioComment(self,parent,label,test=True,choices=['Y','N'],widgetname=None,binding=None,entrylength=100):
        if test == False:
            self.widgets[widgetname] = None
            self.widgets[widgetname+'C'] = None
            return None,None,None
        box = wx.BoxSizer(wx.HORIZONTAL)
        standardpos = wx.ALIGN_CENTER|wx.ALL
        label = wx.StaticText(parent,-1,label=label)
        radio = wx.RadioBox(parent,-1,choices=choices)
        radio.SetSelection(1)
        entry = wx.TextCtrl(parent,-1,size=(entrylength,-1))
        if widgetname is not None:
            if widgetname in list(self.widgets.keys()): #Debugging - determine if overriding widget.
                print('Overriding widget %s!' %(widgetname))
            self.widgets[widgetname] = radio
            self.widgets[widgetname+'C'] = entry
        if binding is not None:
            radio.Bind(binding[0],binding[1])
        box.Add(label,0,standardpos,1)
        box.Add(radio,0,standardpos,1)
        box.Add(entry,0,standardpos,1)
        return box,radio,entry


    def LabelRadioBox(self,parent,label,choices,test=True,widgetname=None,binding=None,selection=None):
        if test == False:
            self.widgets[widgetname] = None
            return None,None,None
        box = wx.BoxSizer(wx.HORIZONTAL)
        standardpos = wx.ALIGN_CENTER|wx.ALL
        label = wx.StaticText(parent,-1,label=label)
        radio = wx.RadioBox(parent,-1,choices=choices)
        radio.SetSelection(0)
        if widgetname is not None:
            if widgetname in list(self.widgets.keys()): #Debugging - determine if overriding widget.
                print('Overriding widget %s!' %(widgetname))
            self.widgets[widgetname] = radio
        if binding is not None:
            radio.Bind(binding[0],binding[1])
        if selection is not None and type(selection) == type(int()) and selection < len(choices):
            radio.SetSelection(selection)
        box.Add(label,0,standardpos,1)
        box.Add(radio,0,standardpos,1)
        return box,radio,None

    def LabelCombo(self,parent,label,choices,readonly=True,widgetname=None,binding=None):
        standardpos = wx.ALIGN_CENTER|wx.ALL
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent,label=label)
        if readonly:
            combo = wx.ComboBox(parent,choices=choices,style=wx.CB_READONLY)
        else:
            combo = wx.ComboBox(parent,choices=choices)
        if widgetname is not None:
            if widgetname in list(self.widgets.keys()): #Debugging - determine if overriding widget.
                print('Overriding widget %s!' %(widgetname))
            self.widgets[widgetname] = combo
        if binding is not None:
            combo.Bind(binding[0],binding[1])
        box.Add(label,0,standardpos,1)
        box.Add(combo,0,standardpos,1)
        return box,combo,None
        

    def StandardButtons(self,parent,nextbind=None,prevbind=None,nextenable=True,prevenable=True,nexttitle=None,returnbuttons=False):
        standardpos = wx.ALIGN_CENTER|wx.ALL
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        quitbutton = wx.Button(parent,wx.ID_ANY,label='Quit')
        quitbutton.Bind(wx.EVT_BUTTON,self.OnQuit)
        previousbutton = wx.Button(parent,wx.ID_ANY,label='Back')
        if not prevenable:
            previousbutton.Enable(False)
        if prevbind is not None:
            previousbutton.Bind(wx.EVT_BUTTON,prevbind)
        if nexttitle is None:
            nextbutton = wx.Button(parent,wx.ID_ANY,label='Next')
        else:
            nextbutton = wx.Button(parent,wx.ID_ANY,label=nexttitle)
        if not nextenable:
            nextbutton.Enable(False)
        if nextbind is not None:
            nextbutton.Bind(wx.EVT_BUTTON,nextbind)
        buttonbox.Add(quitbutton,0,standardpos,1)
        buttonbox.Add(previousbutton,0,standardpos,1)
        buttonbox.Add(nextbutton,0,standardpos,1)
        if not returnbuttons:
            return buttonbox
        else:
            return buttonbox,quitbutton,previousbutton,nextbutton


    def LabelEntry(self,parent,label,test=True,widgetname=None,savelabelname=None,binding=None):
        if test == False:
            self.widgets[widgetname] = None
            if savelabelname is not None:
                self.widgets[savelabelname] = None
            return None, None, None
        standardpos = wx.ALIGN_CENTER|wx.ALL
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent,label=label)
        entry = wx.TextCtrl(parent)
        if widgetname is not None:
            if widgetname in list(self.widgets.keys()): #Debugging - determine if overriding widget.
                print('Overriding widget %s!' %(widgetname))
            self.widgets[widgetname] = entry
        if savelabelname is not None:
            if savelabelname in list(self.widgets.keys()):
                print('Overriding widget %s!' %(savelabelname))
            self.widgets[savelabelname] = label
        if binding is not None:
            entry.Bind(binding[0],binding[1])
        box.Add(label,0,standardpos,1)
        box.Add(entry,0,standardpos,1)
        return box, entry, label
    
    def NarLabelEntry(self,parent,label,test=True,widgetname=None,savelabelname=None,binding=None):
        if test == False:
            self.widgets[widgetname] = None
            if savelabelname is not None:
                self.widgets[savelabelname] = None
            return None, None, None
        standardpos = wx.ALIGN_CENTER|wx.ALL
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent,label=label)
        entry = wx.TextCtrl(parent,-1,size=(300,50), style = wx.TE_MULTILINE)
        if widgetname is not None:
            if widgetname in list(self.widgets.keys()): #Debugging - determine if overriding widget.
                print('Overriding widget %s!' %(widgetname))
            self.widgets[widgetname] = entry
        if savelabelname is not None:
            if savelabelname in list(self.widgets.keys()):
                print('Overriding widget %s!' %(savelabelname))
            self.widgets[savelabelname] = label
        if binding is not None:
            entry.Bind(binding[0],binding[1])
        box.Add(label,0,standardpos,1)
        box.Add(entry,0,standardpos,1)
        return box, entry, label

    def LabelBox(self,parent,label,test=True):
        if test == False:
            return None, None, None
        standardpos = wx.ALIGN_CENTER|wx.ALL
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(parent,-1,label=label)
        box.Add(label,0,standardpos,1)
        return box, None, None


    def WriteStandardLine(self,preface,widget,entry=None):
        cb = 'wxCheckBox'
        rb = 'wxRadioButton'
        rbox = 'wxRadioBox'
        cmb = 'wxComboBox'
        tc = 'wxTextCtrl'
        dp = 'wxDatePickerCtrl'
        tp = 'wxTimePickerCtrl'
        if widget is None:
            return ''
        if widget.ClassName == cb:
            if widget.IsChecked():
                result = 'Yes'
            else:
                result = 'No'
            st = preface+': '+result
            if entry is not None and entry.GetValue() != '':
                st += ', '+entry.GetValue()
        elif widget.ClassName == rb or widget.ClassName == rbox:
            result = self.GetRadioChoice(widget)
            if result == 'N':
                result = 'No'
            if result == 'Y':
                result = 'Yes'
            st = preface+': '+result
            if entry is not None and entry.GetValue() != '':
                st += ', '+entry.GetValue()
        elif widget.ClassName == cmb:
            result = widget.GetValue()
            st = preface+': '+result
            if entry is not None and entry.GetValue() != '':
                st += ', '+entry.GetValue()
        elif widget.ClassName == tc:
            result = widget.GetValue()
            st = preface+': '+result
            if entry is not None and entry.GetValue() != '':
                st += ', '+entry.GetValue()
        elif widget.ClassName == dp:
            result = widget.GetValue()
            st = preface+': '+'%i-%i-%i'%(result.year,result.month,result.day)
            if entry is not None and entry.GetValue() != '':
                st += ', '+entry.GetValue()
        elif widget.ClassName == tp:
            result = widget.GetValue()
            st = preface +': '+'%02i:%02i'%(result.hour,result.minute)
            if entry is not None and entry.GetValue() != '':
                st += ', '+entry.GetValue()
        else:
            print('Unknown Widget Type')
            print(widget.ClassName)
            print(widget)
            return ''
        st += '\n'
        return st




    #######
    ##   ##
    ## 1 ## 
    ##   ##
    #######

    def DemoPanel(self):
        """LO Entry."""

        #Geometry Initialization
        frame = wx.Frame(None,-1,'Initial Plan Check - Demographics')
        panel = wx.Panel(frame)
        vbox = wx.BoxSizer(wx.VERTICAL)

        #Widget Creation
 #       DemoBox = self.Demogbox(panel)
        un = self.LabelEntry(panel,'Patient MRN:',widgetname='UNum',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        name = self.LabelEntry(panel,'Patient Last Initial,First Initial:',widgetname='Name',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        MD = self.LabelEntry(panel,'MD initial:',widgetname='MDInit',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        Res = self.LabelEntry(panel,'Resident initial:',widgetname='ResInit',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        Dosi = self.LabelEntry(panel,'Dosi initial:',widgetname='DosInit',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        Phys = self.LabelEntry(panel,'Physicist initial:',widgetname='PhysInit',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        Ther = self.LabelEntry(panel,'Therapist initial:',widgetname='TherInit',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        When = self.LabelRadioBox(panel,'When:',['Before Tx','During Tx','After Tx Completion'],selection=2,widgetname='When',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        LocHap = self.LabelEntry(panel,'Where it Happened:',widgetname='LocHap',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        DateHap = self.LabelEntry(panel,'Date it Happened:',widgetname='DateHap',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        LocDis = self.LabelEntry(panel,'Where it was discovered:',widgetname='LocDis',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        DateDis = self.LabelEntry(panel,'Date it was discovered:',widgetname='DateDis',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        Dose = self.LabelEntry(panel,'Dose discrepancy?: YES(how much), NO, UNKNOWN',widgetname='Dose',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        NarSum = self.NarLabelEntry(panel,'Narrative Summary:',widgetname='NarSum',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        Why = self.NarLabelEntry(panel,'Why did it occur? (if known):',widgetname='why',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))

        for each in [un,name,MD,Res,Dosi,Phys,Ther,When,LocHap,DateHap,LocDis,DateDis,Dose,NarSum, Why]:
            vbox.Add(each[0],1,wx.ALL,1)

        #Standard Buttons
        vbox.Add(wx.StaticLine(panel,wx.ID_ANY,style=wx.LI_HORIZONTAL),0,wx.ALL|wx.EXPAND,2)
        buttonbox,quitbutton,prevbutton,nextbutton = self.StandardButtons(panel,nextbind=self.OnDemogNext,prevenable=False,nextenable=True,returnbuttons = True)
        vbox.Add(buttonbox)

        #Widget Recording
        self.widgets['DemNext'] = nextbutton
        
        panel.SetSizer(vbox)
        vbox.Fit(frame)
        return frame
    
    
    def Demogbox(self,frame):
        standardpos = wx.ALIGN_CENTER|wx.ALL
        demobox = wx.BoxSizer(wx.HORIZONTAL)
 #       un = self.LabelEntry(panel,'Patient MRN:',widgetname='UNum',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
 #       name = self.LabelEntry(panel,'Patient Last Initial,First Initial:',widgetname='Name',binding=(wx.EVT_KEY_UP,self.OnDemogValidate))
        unlabel = wx.StaticText(frame,label='Patient MRN:')
        un = wx.TextCtrl(frame,size=(60,-1))
        namelabel = wx.StaticText(frame,label='Patient Last Initial, First Initial:')
        name = wx.TextCtrl(frame,size=(40,-1))
        #rxtimes = wx.StaticText(frame,label='cGy x')
   #     rxfx = wx.TextCtrl(frame,size=(40,-1))
        #rxequal = wx.StaticText(frame,label='fractions =')
   #     rxtotal = wx.TextCtrl(frame,size=(60,-1))
   #     rxend = wx.StaticText(frame,label='cGy')
        for each in [unlabel, un, namelabel, name]:
            demobox.Add(each,0,standardpos,1)

        return demobox


    def OnDemogValidate(self,event):
  #placeholder.  may not need
        
        unum = self.widgets['UNum'].GetValue()
  #      name = self.widgets['Name'].GetValue()
        
  #      if  self.DemogValidateUnum(unum) and len(name)>0:
   #         self.widgets['DemNext'].Enable(True)
   #     else:
    #        self.widgets['DemNext'].Enable(False)


    def OnDemogNext(self,event):
   #     if len(self.frames) > self.index+1:
            self.WriteReport()
            self.OnQuit(None)

############################################################
    def Create_File(self,unum,path):
        candidate = '%s%s%s%s' %(path,os.sep,unum,'.txt')
        if os.path.isfile(candidate):
            i = 2
            while True:
                candidate = '%s%s%s (%i)' %(path,os.sep,unum,i)
                if os.path.isfile(candidate):
                    i += 1
                else:
                    break
        return candidate


    def WriteReport(self):
        fpath = self.Create_File(self.widgets['UNum'].GetValue(),self.path)
#        w = self.widgets
        with open(fpath,'w') as f:
            #def WriteStandardLine(preface,widget,entry=None):
            SL = self.WriteStandardLine
            f.write('DEMOGRAPHIC\n')
            f.write(SL('Patient',self.widgets['Name']))
            f.write(SL('U#',self.widgets['UNum']))
            f.write('\n')
            
            f.write('WHO\n')
            f.write(SL('MD Initial',self.widgets['MDInit']))
            f.write(SL('Resident Initial',self.widgets['ResInit']))
            f.write(SL('Dosi Initial',self.widgets['DosInit']))
            f.write(SL('Physicist Initial',self.widgets['PhysInit']))
            f.write(SL('Therapist Initial',self.widgets['TherInit']))
            f.write('\n')
            
          #  f.write('\nWHEN\n')
            f.write(SL('WHEN',self.widgets['When']))
            f.write('\n')
            
            f.write('WHERE\n')
            f.write(SL('Where it happened',self.widgets['LocHap']))
            f.write(SL('on',self.widgets['DateHap']))
            f.write(SL('Where it was realized',self.widgets['LocDis']))
            f.write(SL('on',self.widgets['DateDis']))
            f.write('\n')
            
       #     f.write('-'*25+'\n|  WHAT HAPPENED  |\n'+'-'*25+'\n\n')
            f.write(SL('WHAT HAPPENED',self.widgets['NarSum']))
            f.write('\n')
            
       #     f.write('-'*25+'\n|  DOSE DISCREPANCY  |\n'+'-'*25+'\n\n')
            f.write(SL('DOSE DISCREPANCY',self.widgets['Dose']))
            f.write('\n')
            
      #      f.write('-'*25+'\n|  WHY  |\n'+'-'*25+'\n\n')
            f.write(SL('WHY',self.widgets['why']))
            f.write('\n')

    
        return True

def main():
    app = wx.App()
    InitialCheck(None)
    app.MainLoop()

if __name__ == '__main__':
    main()
