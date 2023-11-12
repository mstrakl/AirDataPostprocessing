import numpy as np


class AirMath:
    
    def __init__(self, d):
        self.__d = d
        self.trel = self.__d.trel
    
    
    def integrateEuler( self, x, initValue=0.0 ):
        

        dt = (self.trel[-1] - self.trel[0]) / len(self.trel)
        print("dt=", dt)
        
        u, uarr = initValue, []
        for i in range(len(x)):
            
            u += x[i] * dt
            uarr.append( u )
        
        return np.array( uarr )
        
            