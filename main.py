import os, sys, time
from scipy import signal
import numpy as np

import dataio 
import airmath

#LOGFOLDER = "~/docker/airMqttBroker/pyMqttLog/Logs"
LOGFOLDER = "./"
LOGFILE = "airlog_2.csv"

FPATH = os.path.join(LOGFOLDER,LOGFILE)

def main():
    
    
    Reader = dataio.Reader()

    d = Reader.read( FPATH, startTime=0, endTime=20 )
    
    Plot = dataio.Plot(d)
    AirMath = airmath.AirMath(d)
    
    #d.p *= 0.0174533  # Convert dps -> rad/s
    #d.q *= -1
    #d.r *= 0.0174533  # Convert dps -> rad/s
    
    #d.r = np.zeros_like(d.p)

    #b, a = signal.butter(2, 0.125)
    #d.p = signal.filtfilt(b, a, d.p, padlen=20)
    #d.q = signal.filtfilt(b, a, d.q, padlen=20)
    #d.r = signal.filtfilt(b, a, d.r, padlen=20)
    
    #d.q *= -1
    #d.r *= -1
    
    d.phi2, d.theta2 = integratePhiTheta(d.p, d.q, d.r, dt=0.05, phi0=d.phi[0], theta0=d.theta[0] )
    
    Plot.add(0, "phi")
    Plot.add(0, "phi2")
    Plot.add(0, "p", y2=True) 
    
    Plot.add(1, "theta")
    Plot.add(1, "theta2")
    Plot.add(1, "q", y2=True) 
    
    Plot.add(2, "ax")
    Plot.add(2, "ay")
    Plot.add(2, "az")
    
    Plot.add(3, "r")
    
    Plot.plot()  
    pass



def integratePhiTheta(p, q, r, dt=0.05, phi0=0, theta0=0):
    
    
    phi = phi0
    theta = theta0
    
    phiarr, thetaarr = [],[]
    for i in range(len(p)):
        
        phiarr.append( phi )
        thetaarr.append( theta )
    
        phidot = p[i] + q[i]*np.sin(phi)*np.tan(theta) + r[i]*np.cos(phi)*np.tan(theta)
        thetadot = q[i]*np.cos(phi) - r[i]*np.sin(phi)
        
        phi += phidot * dt
        theta += thetadot * dt 
    
    return np.array(phiarr), np.array(thetaarr)
    

        
    
     
    
    
    
    
    
    
    #return p + q*np.sin(phi)*np.tan(theta) + r*np.cos(phi)*np.tan(theta)



if __name__ == "__main__":
    main()