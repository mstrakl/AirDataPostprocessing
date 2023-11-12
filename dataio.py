import pandas as pd
import numpy as np

from cycler import cycler
from matplotlib import pyplot as plt
from plum import dispatch


TIMETAG = "TimeRel"

class Data:
    
    def __init__(self, df, startTime=0, endTime=0):
        
        self.__df = df
        self.initTimes(startTime, endTime)
    
    
    def initTimes(self, startTime, endTime):
        
        t = np.array( self.__df[TIMETAG] )
        dt = ( t[-1] - t[0] ) / len(t)
        
        self.__istart = 0
        self.__iend = -1
        
        if dt > 0:
        
            if startTime > 0:
                self.__istart = int( startTime / dt )
            
                if endTime > startTime:
                    self.__iend = int( endTime / dt )

            #print("Cutting time:")
            #print("start index:", self.__istart)
            #print("end index:", self.__iend)

    def getRawDataFrame(self):
        return self.__df
    
    
    def readByTag(self, tag):
        
        try:
            x = np.array( self.__df[tag] )[ self.__istart : self.__iend ]
        except:
            print("Error, cannot read tag:", tag)
            x = None

        return x 
    
    
class Reader:
    
    def __init__(self):
        pass

    
    def read(self, fname, startTime=0, endTime=0) -> Data:
        
        data = Data( pd.read_csv(fname, sep=","), startTime=startTime, endTime=endTime )
        
        data.trel = data.readByTag(TIMETAG)
        
        data.ax = data.readByTag("xacc") / 1000.0   # g  
        data.ay = data.readByTag("yacc") / 1000.0   # g
        data.az = data.readByTag("zacc") / 1000.0   # g
        
        data.p = data.readByTag("xgyro") / 1000.0   # rad/s  
        data.q = data.readByTag("ygyro") / 1000.0   # rad/s
        data.r = data.readByTag("zgyro") / 1000.0   # rad/s
        
        data.phi = data.readByTag("phi")  # rad
        data.theta = data.readByTag("theta")  # rad
        
        data.ch1 = data.readByTag("ch1")
        data.ch2 = data.readByTag("ch2")
        data.ch3 = data.readByTag("ch3")
        data.ch4 = data.readByTag("ch4")
        data.ch5 = data.readByTag("ch5")
        data.ch6 = data.readByTag("ch6")
        data.ch7 = data.readByTag("ch7")
        data.ch8 = data.readByTag("ch8")
        data.ch9 = data.readByTag("ch9")
        data.ch10 = data.readByTag("ch10")
        data.ch11 = data.readByTag("ch11")
        data.ch12 = data.readByTag("ch12")
        
        data.servo1 = data.readByTag("servo1")
        data.servo2 = data.readByTag("servo2")
        data.servo3 = data.readByTag("servo3")
        data.servo4 = data.readByTag("servo4")
        data.servo5 = data.readByTag("servo5")
        data.servo6 = data.readByTag("servo6")
        data.servo7 = data.readByTag("servo7")
        data.servo8 = data.readByTag("servo8")
        data.servo9 = data.readByTag("servo9")
        data.servo10 = data.readByTag("servo10")
        data.servo11 = data.readByTag("servo11")
        data.servo12 = data.readByTag("servo12")
        
        
        return data
    
    

    
    
    
class Plot:
    
    def __init__(self, d):
        
        self.fig = None
        self.ax = None
        
        self.__d = d
        self.__y = []

    
    def reset(self): 
        self.__y = []

    
    @dispatch
    def add( self, plotnum:int, y:str, y2=False ):
        
        try:
            obj = getattr( self.__d, y )

        except:
            print(f"Error::Plot:: Cannot read {y} parameter")
            return
        
        dct = {
            "ax": plotnum,
            "y": obj,
            "label": y,
            "isy2": y2,
        }
        
        self.__y.append( dct )

    
    def plot(self):
        
        numplots = 0 
        
        for dct in self.__y:
            if (dct["ax"]+1) > numplots:
                numplots = (dct["ax"]+1)

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        clr1 = colors[0:5]
        clr2 = colors[5:10]        
        
        fig, ax = plt.subplots( numplots )
        
        try:
            ax[0]
        except:
            ax = [ ax ]
         
        ax2 = [ None for i in range(len(ax)) ]
        
        for pdct in self.__y:
            
            i = pdct["ax"]
            
            if not pdct["isy2"]:
                
                ax[i].plot( self.__d.trel, 
                            pdct["y"], 
                            label=pdct["label"],
                            color=clr1[len(ax[i].lines)] )
            
            else:
                
                if ax2[i] is None:
                    ax2[i] = ax[i].twinx()
                    
                ax2[i].plot( self.__d.trel, 
                             pdct["y"], 
                             label=pdct["label"],
                             color=clr2[len(ax2[i].lines)] )
            

                    
        for i in range(len(ax)):
            ax[i].grid()
            ax[i].set_prop_cycle(cycler('color', ['c', 'm', 'y', 'k']))
            ax[i].legend(loc="upper left")
            ax[i].sharex( ax[0] )
            
            try:
                ax2[i].set_prop_cycle(cycler('color', ['r', 'r', 'g', 'y']))
                ax2[i].legend(loc="upper right")
            except: pass
            
      
        
        plt.show() 
        
    #@dispatch
    #def add( self, x:str, y:str, y2=False ):
        
        