#!/usr/bin/python
#     Math Magic!
#     Copyright 2015 Abram Hindle
#     
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#     
#         http://www.apache.org/licenses/LICENSE-2.0
#     
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License
# .
import scipy
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib
import argparse




WINDOWNAME="Function"

class F(object):
    def __init__(self,W,H):
        self.W = W
        self.H = H
        x = np.linspace(0,1,W)
        y = np.linspace(0,1,H)
        xv, yv = np.meshgrid(x,y)
        self.xv = xv
        self.yv = yv
    
    def apply(self,**kwargs):
        h = self.xv * 0.0
        return (h,h,h)

class Mine(F):
    def apply(self,**kwargs):
        t = kwargs.get("t",1.0)
        h = np.sin(3.15 * self.xv * self.yv)
        # s = np.tan(9.6)
        # s = xv*0 + np.tan(9.6)
        s = np.tan(self.xv*self.yv*(20.0*t/100.0))
        v = self.xv * self.yv
        return (h,s,v)

class Evaler(F):
    def __init__(self,W,H,h="0*xv",s="0*xv",v="0*xv"):
        super(Evaler, self).__init__(W,H)
        self.heq = h
        self.seq = s
        self.veq = v
        self.zeros = np.zeros((H,W))
        self.ones = self.zeros + 1.0

    def apply(self,**kwargs):
        t = kwargs.get("t",1.0)
        x = self.xv
        y = self.yv
        xv = self.xv
        yv = self.yv
        zeros = self.zeros
        ones = self.ones
        oldh = kwargs.get("oldh",zeros)
        olds = kwargs.get("olds",zeros)
        oldv = kwargs.get("oldv",zeros)
        oldh = zeros if oldh is None else oldh
        olds = zeros if olds is None else olds
        oldv = zeros if oldv is None else oldv
        sin = np.sin
        cos = np.cos
        tan = np.tan
        exp = np.exp
        h = eval(self.heq)
        s = eval(self.seq)
        v = eval(self.veq)
        h = h if isinstance(h,np.ndarray) else h * ones
        s = s if isinstance(s,np.ndarray) else s * ones
        v = v if isinstance(v,np.ndarray) else v * ones
        return (h,s,v)
    
        

def animate(f,H,W,frames=1000):
    h = None
    s = None
    v = None
    for i in xrange(0,frames):
        print i
        (h,s,v) = f.apply(t=i,frame=i,oldh=h,olds=s,oldv=v)                
        hsv = np.dstack([h,s,v],)
        rgb = matplotlib.colors.hsv_to_rgb(hsv)
        cv2.imshow(WINDOWNAME,rgb)
        key = cv2.waitKey(33) & 0xFF
        if key == 27:
            cv2.destroyAllWindows()
            return
        

if __name__ == "__main__":
    description = '''
    Draw Math Magic!
    from 0..1 and 0..1 in x and y
    available variables
        x = x positions
        y = y positions
        oldh = last h
        olds = last s
        oldv = last v
    available functions:
        sin
        tan
        

    Any numpy functions are available as np.sum etc.
    
    This program is NOT SAFE.

    Try:
    python mathmagic.py -H "(x+(t%100)/100.0)/2.0" -S "y" -V "(t%100)/100.0"
    python mathmagic.py -H "x" -S "y" -V "x*y*t"
    python mathmagic.py -H "x" -S "y" -V "(t%100)/100.0"
    python mathmagic.py -H "x/3" -S '5*y*x' -V "t%10"
    python mathmagic.py -H "t%2" -S 't%5' -V "t%3"
    python mathmagic.py -H "x*t%2" -S 'y*t%5' -V "x*y*t%3"
    python mathmagic.py -H "y" -S "x" -V "np.log(0.1+t%10*x)"
    python mathmagic.py -H "x + 0.5*(olds*x + t%100/100.0)" -S "oldv*y + t%66/66.0" -V "oldh*(t%10)"

    Inspired by/Stolen from Ashley Mills https://www.youtube.com/watch?v=OIlJVH99yIk

    (C) 2015 Abram Hindle 

    License: Apache 2.0



    Copyright 2015 Abram Hindle
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.


    '''
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-f', default=1024,help="Number of frames")
    parser.add_argument('-width', default=320, help='Width')
    parser.add_argument('-height', default=240, help='Height')
    parser.add_argument('-H', default="x", help='H equation from HSV')
    parser.add_argument('-S', default="y", help='S equation from HSV')
    parser.add_argument('-V', default="(t%100)/100.0", help='V equation from HSV')
    args = parser.parse_args()


    cv2.namedWindow(WINDOWNAME, cv2.WND_PROP_FULLSCREEN)     
    H = int(args.height)
    W = int(args.width)
    # f = Mine(320,240)
    # f = Evaler(W,H,"x","tan((t%100)/100.0*9.6*y)","x*y")
    f = Evaler(W,H,h=args.H,s=args.S,v=args.V)
    animate(f,W,H,frames=int(args.f))
    
