from typing import Literal, List

ns = 10 ** (-9)
Ym: int
# 1:1 = [1] / 1:2 = [1, 2] / .* поэлементное умнож / в функции подставляется тольк один элемент
n: List[int]
nr: List[int]
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
t: Literal[0] = 0
H = "evs(Tr.Ya)"
Type: int
FacetN: int
vidDOR1: str = "G"
dH1: int
Kr1: int
DOR1: int
DOR2: int
dH2: int
Kr2: int
vidDOR2: str = "G"
DOR7: int
dH7: int
Kr7: int
vidDOR7: str = "G"
Ncr: int
DOR8: int
dH8: int
Kr8: int
vidDOR7: str = "1"
Step: int


class Rs:
    Nimp: str = "256"
    Polariz: str = "HH"
    Timp = "tauimp*Sqw"
    dtau = "tauimp/2"
    tauimp = "10*ns"
    AruType: int
    sh: int
    maxF: float
    Hmax: int
    Pz: str = "1"
    snr: str = "100"
    Tm_Pause: int
    Rmin: int
    Rmax: int
    GB: int
    Log: int
    Wnd: int
    Focus: int
    Logi: int
    Rmin: int
    Rmax: int
    GB: int
    Log: int
    Wnd: int
    Focus: int


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
    dnay: int  # по оси y
    dnaz: int  # по оси x


class test:
    figext: int
    Xcr: float
    Zcr: float
    Nadir: int
    SWT: int
    pF: int
    pN: int


class St:
    N: int
    Xs = "evs(Tr.Xa)+20"
    Ys = "evs(Tr.Ya)"
    Zs = "evs(Tr.Za)"
    Vx = "-evs(Tr.Vx)"
    Vy: str = "0"
    Vz: str = "0"
    tang: str = "0"
    kren: str = "0"
    psi: str = "0"
    Model: str = "0"
    Type: str = "1"
    wx: int
    wh: int
    wz: int
    RSC: int


class Tr:
    Xa: str = "0"
    Ya: str = "100"
    Za: str = "0"
    Vx: str = "100"
    Vy: str = "0"
    Vz: str = "0"
    tang: str = "30"
    kren: str = "0"
    psi: str = "0"


class Sf:
    Relief: str
    Kspot: float
    KspotN: float
    WindTh: int
    WindFi: int
    AirT: int
    TownD: int
    XZstep: int
    maxY: int
    Elev: int
    Dspot: int
    x: int
    z: int
    rad_mul: float
    x_size: int
    z_size: int
    med_shift: float


class Sea:
    rho: int
    WindV: int
    WaveL: int

    Shift: int
    depth: int
    nr: int


def evs():
    eval()


def Relief():
    pass
