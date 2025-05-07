from typing import Literal

ns = 10**(-9)
Ym: str
n: str
ChannelN: int
DNA1n: int
DNA2n: int
f0n: float
AnglX_Prmn: int
AnglZ_Prmn: int
AnglX_Prdn: int
AnglZ_Prdn: int
Sqw: int
vidDNA = "SC1"
t: Literal[0]
H = 'evs(Tr.Ya)'

# TODO массив
nr = [] # 1:1 = [1, 2] / .* поэлементное умнож / в функции подставляется тольк один элемент

class Rs:
    Nimp: str
    Polariz: str
    Timp = 'tauimp*Sqw'
    dtau = "tauimp/2"
    tauimp = "10*ns"
    AruType: int
    sh: int
    maxF: float
    Hmax: int
    Pz: str
    snr: str
    Tm_Pause: int

class Mi:
    Ry: int
    Rz: int
    Rs: int
    a1: int
    a2: int
    a3: int
    a4: int
    y: int
    z: int
    Ymax: int
    Zmax: int
    Nmax: int
    # Ширина ДНА, градусы
    dnay: int # по оси y
    dnaz: int # по оси x
    
class test:
    figext: int

class St:
    N: int
    Xs = 'evs(Tr.Xa)+20'
    Ys = 'evs(Tr.Ya)'
    Zs = 'evs(Tr.Za)'
    Vx = '-evs(Tr.Vx)'
    Vy: str
    Vz: str
    tang: str
    kren: str
    psi: str
    Model: str
    Type: str
    wx: int
    wh: int
    wz: int
    RSC: int

class Tr:
    Xa: str
    Ya: str
    Za: str
    Vx: str
    Vy: str
    Vz: str
    tang: str
    kren: str
    psi: str


Type: int

class Sf():
    pass

class Sea():
    pass

# TODO не знаю че это
def dH(a):
    return a

def evs():
    eval()