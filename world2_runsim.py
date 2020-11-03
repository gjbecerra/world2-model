# This is a translation of the World2 model from R to Python, based on the source
# code found in https://github.com/amignan/hist_gc_sysdyn
# Original ref.: Forrester JW (1971) World Dynamics. Wright-Allen Press, Inc., 
# Cambridge, 144 pp.
# The World2 model can be considered the first computer-based doomsday model. It is
# a 5th-order differential equation model with population, natural resource, capital 
# investment, capital-investment-in-agriculture fraction, and pollution as main 
# variables.

# LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# FUNCTIONS
# logical function used as time switch to change parameter value
def CLIP(FUNCT1, FUNCT2, THRESH, VAL):
  if THRESH >= VAL:
    return FUNCT1
  else: 
    return FUNCT2

## (3) Birth-rate-from-material multiplier BRMM ##
def BRMM(MSL):
  # MSL_p   = MATERIAL STANDARD OF LIVING ()
  # BRMMT_p = BIRTH-RATE-FROM-MATERIAL MULTIPLIER TABLE
  MSL_p = np.arange(0, 6, 1)
  BRMMT_p = [1.2, 1., .85, .75, .7, .7]
  return np.interp(MSL, MSL_p, BRMMT_p)


## (6) Natural-Resource-Extraction Multiplier NREM ##
def NREM(NRFR):
  # NRFR_p  = NATURAL-RESOURCE FRACTION REMAINING ()
  # NREMT_p = NATURAL-RESOURCE-EXTRACTION-MULTIPLIER TABLE
  NRFR_p = np.arange(0, 1.25, 0.25)
  NREMT_p = [0, .15, .5, .85, 1]
  return np.interp(NRFR, NRFR_p, NREMT_p)

## (11) Death-Rate-from-Material Multiplier DRMM ##
def DRMM(MSL):
  # DRMMT = DEATH-RATE-FROM-MATERIAL MULTIPLIER TABLE
  MSL_p = np.arange(0, 5.5, 0.5)
  DRMMT_p = [3, 1.8, 1, .8, .7, .6, .53, .5, .5, .5, .5]
  return np.interp(MSL, MSL_p, DRMMT_p)


## (12) Death-Rate-from-Pollution Multiplier DRPM ##
def DRPM(POLR):
  # POLR  = POLLUTION RATIO ()
  # DRPMT = DEATH-RATE-FROM-POLLUTION MULTIPLIER TABLE
  POLR_p = np.arange(0, 70, 10)
  DRPMT_p = [.92, 1.3, 2, 3.2, 4.8, 6.8, 9.2]
  return np.interp(POLR, POLR_p, DRPMT_p)

## (13) Death-Rate-from-Food Multiplier DRFM ##
def DRFM(FR):
  # FR  = FOOD RATIO ()
  # DRFMT = DEATH-RATE-FROM-FOOD MULTIPLIER TABLE
  FR_p = np.arange(0, 2.25, .25)
  DRFMT_p = [30, 3, 2, 1.4, 1, .7, .6, .5, .5]
  return np.interp(FR, FR_p, DRFMT_p)

## (14) Death-Rate-from-Crowding Multiplier DRCM ##
def DRCM(CR):
  # CR  = CROWDING RATIO ()
  # DRCMT = DEATH-RATE-FROM-CROWDING MULTIPLIER TABLE
  CR_p = np.arange(0, 6, 1)
  DRCMT_p = [.9, 1, 1.2, 1.5, 1.9, 3]
  return np.interp(CR, CR_p, DRCMT_p)

## (16) Birth-Rate-from_Crowding Multiplier BRCM ##
def BRCM(CR):
  # BRCMT = BIRTH-RATE-FROM-CROWDING MULTIPLIER TABLE
  CR_p = np.arange(0, 6, 1)
  BRCMT_p = [1.05, 1, .9, .7, .6, .55]
  return np.interp(CR, CR_p, BRCMT_p)

## (17) Birth-Rate-from-Food Multiplier BRFM ##
def BRFM(FR):
  # BRFMT = BIRTH-RATE-FROM-FOOD MULTIPLIER TABLE
  FR_p = np.arange(0, 5, 1)
  BRFMT_p = [0, 1, 1.6, 1.9, 2]
  return np.interp(FR, FR_p, BRFMT_p)

## (18) Birth-Rate-from-Pollution Multiplier BRPM ##
def BRPM(POLR):
  # BRPMT = BIRTH-RATE-FROM-POLLUTION MULTIPLIER TABLE
  POLR_p = np.arange(0, 70, 10)
  BRPMT_p = [1.02, .9, .7, .4, .25, .15, .1]
  return np.interp(POLR, POLR_p, BRPMT_p)

## (20) Food-from-Crowding Multiplier FCM ##
def FCM(CR):
  # FCMT = FOOD-FROM-CROWDING MULTIPLIER TABLE
  # CR   = CROWDING RATIO ()
  CR_p = np.arange(0, 6, 1)
  FCMT_p = [2.4, 1, .6, .4, .3, .2]
  return np.interp(CR, CR_p, FCMT_p)

## (21) Food from Capital Investment FPCI ##
def FPCI(CIRA):
  # FPCIT = FOOD-FROM-CAPITAL-INVESTMENT TABLE
  # CIRA  = CAPITAL-INVESTMENT RATIO IN AGRICULTURE (CAPITAL UNITS/PERSON)
  CIRA_p = np.arange(0, 7, 1) 
  FPCIT_p = [.5, 1., 1.4, 1.7, 1.9, 2.05, 2.2]
  return np.interp(CIRA, CIRA_p, FPCIT_p)

## (26) Capital-Investment Multiplier CIM ##
def CIM(MSL):
  # CIMT = CAPITAL-INVESTMENT-MULTIPLIER TABLE
  MSL_p = np.arange(0, 6, 1) 
  CIMT_p = [.1, 1, 1.8, 2.4, 2.8, 3]
  return np.interp(MSL, MSL_p, CIMT_p)

## (28) Food-from-Pollution Multiplier FPM ##
def FPM(POLR):
  # FPMT = FOOD-FROM-POLLUTION-MULTIPLIER TABLE
  POLR_p = np.arange(0, 70, 10)
  FPMT_p = [1.02, .9, .65, .35, .2, .1, .05]
  return np.interp(POLR, POLR_p, FPMT_p)

## (32) Pollution-from-Capital Multiplier POLCM ##
def POLCM(CIR):
  # POLCMT = POLLUTION-FROM-CAPITAL-MULTIPLIER TABLE
  CIR_p = np.arange(0, 6, 1) 
  POLCMT_p = [.05, 1, 3, 5.4, 7.4, 8]
  return np.interp(CIR, CIR_p, POLCMT_p)

## (34) Pollution-Absorption Time POLAT
def POLAT(POLR):
  # POLATT = POLLUTION-ABSORPTION-TIME TABLE
  POLR_p = np.arange(0, 70, 10)
  POLATT_p = [.6, 2.5, 5, 8, 11.5, 15.5, 20]
  return np.interp(POLR, POLR_p, POLATT_p)

## (36) Capital Fraction Indicated by Food Ratio CFIFR ##
def CFIFR(FR):
  # POLATT = POLLUTION-ABSORPTION-TIME TABLE
  FR_p = np.arange(0, 2.5, .5)
  CIFRT_p = [1, .6, .3, .15, .1]
  return np.interp(FR, FR_p, CIFRT_p)

## (38) Quality of Life from Material QLM ##
def QLM(MSL):
  # QLMT = QUALITY-OF-LIFE-FROM-MATERIAL TABLE
  MSL_p = np.arange(0, 6, 1)
  QLMT_p = [.2, 1, 1.7, 2.3, 2.7, 2.9]
  return np.interp(MSL, MSL_p, QLMT_p)

## (39) Quality of Life from Crowding QLC ##
def QLC(CR):
  # QLCT = QUALITY-OF-LIFE-FROM-CROWDING TABLE
  CR_p = np.arange(0, 5.5, .5)
  QLCT_p = [2, 1.3, 1, .75, .55, .45, .38, .3, .25, .22, .2]
  return np.interp(CR, CR_p, QLCT_p)

## (40) Quality of Life from Food QLF ##
def QLF(FR):
  # QLFT = QUALITY-OF-LIFE-FROM-FOOD TABLE
  FR_p = np.arange(0, 5, 1) 
  QLFT_p = [0, 1, 1.8, 2.4, 2.7]
  return np.interp(FR, FR_p, QLFT_p)

## (41) Quality of Life from Pollution QLP ##
def QLP(POLR):
  # QLPT = QUALITY-OF-LIFE-FROM-POLLUTION TABLE
  POLR_p = np.arange(0, 70, 10) 
  QLPT_p = [1.04, .85, .6, .3, .15, .05, .02]
  return np.interp(POLR, POLR_p, QLPT_p)

## (42) Natural-Resource-from-Material Multiplier NRMM ##
def NRMM(MSL):
  # NRMMT = NATURAL-RESOURCE-FROM-MATERIAL-MULTIPLIER TABLE
  MSL_p = np.arange(0, 11, 1) 
  NRMMT_p = [0, 1, 1.8, 2.4, 2.9, 3.3, 3.6, 3.8, 3.9, 3.95, 4]
  return np.interp(MSL, MSL_p, NRMMT_p)

## (43) Capital-Investment-from-Quality Ratio CIQR ##
def CIQR(QLM_QFL):
  # CIQRT = CAPITAL-INVESTMENT-FROM-QUALITY-RATIO TABLE
  # QLM   = QUALITY OF LIFE FROM MATERIAL ()
  # QFL   = QUALITY OF LIFE FROM FOOD ()
  QLM_QFL_p = np.arange(0, 2.5, .5) 
  CIQRT_p = [.7, .8, 1, 1.5, 2]
  return np.interp(QLM_QFL, QLM_QFL_p, CIQRT_p)

def world2_run(BRN1, NRUN1, DRN1, FC1, POLN1):
    DT = 0.2
    TIME = np.arange(1900, 2100, DT)    # CALENDAR TIME (YEARS)
    n = len(TIME)

    ## (1) Population P ##
    # P = P.J + DT (BR.JK - DR.JK)
    # BR = BIRTH RATE (PEOPLE/YEAR)
    # DR = DEATH RATE (PEOPLE/YEAR)
    # PI = POPULATION INITIAL (PEOPLE)
    P = np.zeros(n)     # POPULATION (PEOPLE)
    PI = 1.65e9         # in YEAR = 1900

    ## (2) Birth rate BR ##
    # BRL = P CLIP(BRN, BRN1, SWT1, TIME) BRFM BRMM BRCM BRPM
    # BRFM = BIRTH-RATE-FROM-FOOD MULTIPLIER ()
    # BRMM = BIRTH-RATE-FROM-MATERIAL MULTIPLIER ()
    # BRCM = BIRTH-RATE-FROM-CROWDING MULTIPLIER ()
    # BRPM = BIRTH-RATE-FROM-POLLUTION MULTIPLIER ()
    BR = np.zeros(n)    # BIRTH RATE (PEOPLE/YEAR)
    BRN = 0.04          # BIRTH RATE NORMAL (FRACTION/YEAR)
    # BRN1 = 0.04         # BIRTH RATE NORMAL no. 1 (FRACTION/YEAR)
    SWT1 = 1970         # SWITCH TIME no. 1 FOR BRN (YEARS)
    
    ## (4) Material standard of living MSL ##
    # MSL = ECIR / ECIRN
    # ECIR = EFFECTIVE-CAPITAL-INVESTMENT RATIO (CAPITAL UNITS/PERSON)
    # ECIRN = EFFECTIVE-CAPITAL-INVESTMENT RATIO NORMAL (CAPITAL UNITS/PERSON)
    MSL = np.zeros(n)   # MATERIAL STANDARD OF LIVING
    ECIRN = 1

    ## (5) Effective-Capital-Investment Ratio ECIR ##
    # ECIR = CIR (1 - CIAF) NREM / (1 - CIAFN)
    # CIR   = CAPITAL-INVESTMENT RATIO (CAPITAL UNITS/PERSON)
    # CIAF  = CAPITAL-INVESTMENT-IN-AGRICULTURE FRACTION ()
    # CIAFN = CAPITAL-INVESTMENT-IN-AGRICULTURE FRACTION NORMAL ()
    # NREM  = NATURAL-RESOURCE-EXTRACTION MULTIPLIER ()
    ECIR = np.zeros(n)  # EFFECTIVE-CAPITAL-INVESTMENT RATIO


    ## (7) Natural-Resource Fraction Remaining NRFR ##
    # NRFR = NR / NRI
    # NR  = NATURAL RESOURCES (NATURAL RESOURCE UNITS)
    # NRI = NATURAL RESOURCES INITIAL (NATURAL RESOURCE UNITS)
    NRFR = np.zeros(n)  # NATURAL RESOURCES FRACTION REMAINING
    NRI = 900e9

    ## (8) Natural Resource NR ##
    # NR = NR.J + DT (-NRUR.JK)
    # NRUR = NATURAL-RESOURCE-USAGE RATE (NATURAL RESOURCE UNITS/YEAR)
    NR = np.zeros(n)    # NATURAL RESOURCES

    ## (9) Natural-Resource-Usage Rate NRUR ##
    # NRURL = P CLIP(NRUN, NRUN1, SWT2, TIME) NRMM
    # NRUN  = NATURAL-RESOURCE USAGE NORMAL (NATURAL RESOURCE UNITS/PERSON/YEAR)
    # NRUN1 = NATURAL-RESOURCE USAGE NORMAL no. 1 (NATURAL RESOURCE UNITS/PERSON/YEAR)
    # SWT2  = SWITCH TIME no. 2 FOR NRUN (YEARS)
    # NRMM  = NATURAL-RESOURCE-FROM-MATERIAL MULTIPLIER ()
    NRUR = np.zeros(n)  # NATURAL-RESOURCE USAGE RATE
    NRUN = 1
    # NRUN1 = 1
    SWT2 = 1970

    ## (10) DEATH RATE DR ##
    # DRL = P CLIP(DRN, DRN1, SWT3, TIME) DRMM DRPM DRFM DRCM
    # DRN  = DEATH RATE NORMAL (FRACTION/YEAR)
    # DRN1 = DEATH RATE NORMAL no. 1 (FRACTION/YEAR)
    # SWT3 = SWITCH TIME no. 3 FOR DRN (YEARS)
    # DRMM = DEATH-RATE-FROM-MATERIAL MULTIPLIER ()
    # DRPM = DEATH-RATE-FROM-POLLUTION MULTIPLIER ()
    # DRFM = DEATH-RATE-FROM-FOOD MULTIPLIER ()
    # DRCM = DEATH-RATE-FROM-CROWDING MULTIPLIER ()
    DR = np.zeros(n)    # DEATH RATE (PEOPLE/YEAR)
    DRN = 0.028
    # DRN1 = 0.028
    SWT3 = 1970

    ## (15) Crowding Ratio CR ##
    # CR = P / (LA * PDN)
    # LA  = LAND AREA (SQUARE KILOMETERS)
    # PDN = POPULATION DENSITY NORMAL (PEOPLE/SQUARE KILOMETER)
    CR = np.zeros(n)    # CROWDING RATIO
    LA = 135e6
    PDN = 26.5

    ## (19) Food Ratio FR ##
    # FR = FPCI FCM FPM CLIP(FC, FC1, SWT7, TIME) / FN
    # FPCI = FOOD POTENTIAL FROM CAPITAL INVESTMENT (FOOD UNITS/PERSON/YEAR)
    # FCM  = FOOD-FROM-CROWDING MULTIPLIER ()
    # FPM  = FOOD-FROM-POLLUTION MULTIPLIER ()
    # FC   = FOOD COEFFICIENT ()
    # FC1  = FOOD COEFFICIENT no. 1 ()
    # SWT7 = SWITCH TIME no. 7 FOR FC (YEARS)
    # FN   = FOOD NORMAL (FOOD UNITS/PERSON/YEAR)
    FR = np.zeros(n)    # FOOD RATIO
    FC = 1
    # FC1 = 1
    FN = 1
    SWT7 = 1970

    ## (22) Capital-Investment Ratio in Agriculture CIRA ##
    # CIRA = CIR CIAF / CIAFN
    # CIR   = CAPITAL-INVESTMENT RATIO (CAPITAL UNITS/PERSON)
    # CIAF  = CAPITAL-INVESTMENT-in-AGRICULTURE FRACTION ()
    # CIAFN = CAPITAL-INVESTMENT-in-AGRICULTURE FRACTION NORMAL ()
    CIRA = np.zeros(n)  # CAPITAL-INVESTMENT RATIO IN AGRICULTURE
    CIAFN = .3

    ## (23) Capital-Investment Ratio CIR ##
    # CIR = CI / P
    # CI = CAPITAL-INVESTMENT (CAPITAL UNITS)
    CIR = np.zeros(n)   # CAPITAL-INVESTMENT RATIO

    ## (24) Capital Investment CI ##
    # CI = CI.J + DT (CIG.JK - CID.JK)
    # CIG = CAPITAL-INVESTMENT GENERATION (CAPITAL UNITS/YEAR)
    # CID = CAPITAL-INVESTMENT DISCARD (CAPITAL UNITS/YEAR)
    # CII = CAPITAL-INVESTMENT INITIAL (CAPITAL UNITS)
    CI = np.zeros(n)    # CAPITAL-INVESTMENT
    CII = .4e9

    ## (25) Capital-Investment Generation CIG ##
    # CIG = P CIM CLIP(CIGN, CIGN1, SWT4, TIME)
    # CIM   = CAPITAL-INVESTMENT MULTIPLIER ()
    # CIGN  = CAPITAL-INVESTMENT GENERATION NORMAL (CAPITAL UNITS/PERSON/YEAR)
    # CIGN1 = CAPITAL-INVESTMENT GENERATION NORMAL no. 1 (CAPITAL UNITS/PERSON/YEAR)
    # SWT4  = SWITCH TIME no. 4 FOR CIGN (YEARS)
    CIG = np.zeros(n)   # CAPITAL-INVESTMENT GENERATION
    CIGN1 = .05
    CIGN = .05
    SWT4 = 1970

    ## (27) Capital-Investment Discard CID ##
    # CIDL = CI CLIP(CIDN, CIDN1, SWTS, TIME)
    # CIDN  = CAPITAL-INVESTMENT DISCARD NORMAL (FRACTION/YEAR)
    # CIDN1 = CAPITAL-INVESTMENT DISCARD NORMAL no. 1 (FRACTION/YEAR)
    # SWT5  = SWITCH TIME no. 5 FOR CIDN (YEARS)
    CID = np.zeros(n)   # CAPITAL-INVESTMENT DISCARD
    CIDN1 = .025
    CIDN = .025
    SWT5 = 1970

    ## (29) Pollution Ratio POLR ##
    # POLR = POL / POLS
    # POL  = POLLUTION (POLLUTION UNITS)
    # POLS = POLLUTION STANDARD (POLLUTION UNITS)
    POLR = np.zeros(n)  # POLLUTION RATIO
    POLS = 3.6e9

    ## (30) Pollution POL ##
    # POL = POL.J + DT (POLG.JK - POLA.JK)
    # POLG = POLLUTION GENERATION (POLLUTION UNITS/YEAR)
    # POLA = POLLUTION ABSORPTION (POLLUTION UNITS/YEAR)
    # POLI = POLLUTION INITIAL (POLLUTION UNITS)
    POL = np.zeros(n)   # POLLUTION
    POLI = .2e9

    ## (31) Pollution Generation POLG ##
    # POLGL = P CLIP(POLN, POLN1, SWT6, TIME) POLCM
    # POLN  = POLLUTION NORMAL (POLLUTION UNITS/PERSON/YEAR)
    # POLN1 = POLLUTION NORMAL no. 1 (POLLUTION UNITS/PERSON/YEAR)
    # SWT6  = SWITCH TIME no. 6 FOR POLN (YEARS)
    # POLCM = POLLUTION-FROM-CAPITAL MULTIPLIER ()
    POLG = np.zeros(n)  # POLLUTION GENERATION
    # POLN1 = 1
    POLN = 1
    SWT6 = 1970

    ## (35) Capital-Investment-in-Agriculture Fraction CIAF ##
    # CIAF = CIAF.J + (DT / CIAFT) (CFIFR.J * CIQR.J - CIAF.J)
    # CIAFT = CAPITAL-INVESTMENT-IN-AGRICULTURE-FRACTION ADJUSTMENT TIME (YEARS)
    # CIAFI = CAPITAL-INVESTMENT-IN-AGRICULTURE-FRACTION INITIAL ()
    # CFIFR = CAPITAL FRACTION INDICATED BY FOOD RATIO ()
    # CIQR  = CAPITAL-INVESTMENT-FROM-QUALITY RATIO ()
    CIAF = np.zeros(n)  # CAPITAL-INVESTMENT-IN-AGRICULTURE FRACTION
    CIAFI = .2
    CIAFT = 15

    ## (33) Pollution Absorption POLA ##
    # POLAL = POL / POLAT
    # POLA  = POLLUTION ABSORPTION (POLLUTION UNITS/YEAR)
    # POLAT - POLLUTION-ABSORPTION TIME (YEARS)
    POLA = np.zeros(n)  # POLLUTION ABSORPTION

    ## (37) Quality of Life QL ##
    # QL = QLS QLM QLC QLF QLP
    # QL  = QUALITY OF LIFE (SATISFACTION UNITS)
    # QLS = QUALITY-OF-LIFE STANDARD (SATISFACTION UNITS)
    # QLM = QUALITY OF LIFE FROM MATERIAL ()
    # QLC = QUALITY OF LIFE FROM CROWDING ()
    # QLF = QUALITY OF LIFE FROM FOOD ()
    # QLP = QUALITY OF LIFE FROM POLLUTION ()
    QL = np.zeros(n)    # QUALITY OF LIFE
    QLS = 1

    ## RUNS SIMULATION
    P[0] = PI
    NR[0] = NRI
    CI[0] = CII
    POL[0] = POLI
    CIAF[0] = CIAFI

    CIR[0] = CI[0] / P[0]
    POLG[0] = P[0] * CLIP(POLN, POLN1, SWT6, TIME[0]) * POLCM(CIR[0])
    POLR[0] = POL[0] / POLS
    POLA[0] = POL[0] / POLAT(POLR[0])
    CR[0] = P[0] / (LA * PDN)
    NRFR[0] = NR[0] / NRI
    ECIR[0] = CIR[0] * (1 - CIAF[0]) * NREM(NRFR[0]) / (1 - CIAFN)
    MSL[0] = ECIR[0] / ECIRN
    CIRA[0] = CIR[0] * CIAF[0] / CIAFN
    FR[0] = FPCI(CIRA[0]) * FCM(CR[0]) * FPM(POLR[0]) * CLIP(FC, FC1, SWT7, TIME[0]) / FN


    CID[0] = np.NAN
    CIG[0] = np.NAN
    BR[0] = np.NAN
    DR[0] = np.NAN
    QL[0] = np.NAN

    for k in range(1,n):
        j = k - 1

        BR[k] = P[j] * CLIP(BRN, BRN1, SWT1, TIME[j]) * BRMM(MSL[j]) * BRCM(CR[j]) * BRFM(FR[j]) * BRPM(POLR[j])  # (2-3,16-18)
        DR[k] = P[j] * CLIP(DRN, DRN1, SWT3, TIME[j]) * DRMM(MSL[j]) * DRPM(POLR[j]) * DRFM(FR[j]) * DRCM(CR[j])  # (10-14)
        P[k] = P[j] + DT * (BR[k] - DR[k])    # (1)
        
        NRUR[k] = P[j] * CLIP(NRUN, NRUN1, SWT2, TIME[j]) * NRMM(MSL[j])   # (9,42)
        NR[k] = NR[j] + DT * (-NRUR[k])   # (8)
        NRFR[k] = NR[k] / NRI     # (7)
        
        POLG[k] = P[j] * CLIP(POLN, POLN1, SWT6, TIME[j]) * POLCM(CIR[j])  # (31-32)
        POLA[k] = POL[j] / POLAT(POLR[j])   # (33-34)
        POL[k] = POL[j] + DT * (POLG[k] - POLA[k])   # (30)
        POLR[k] = POL[k] / POLS   # (29)
        
        CIAF[k] = CIAF[j] + (DT / CIAFT) * (CFIFR(FR[j]) * CIQR(QLM(MSL[j]) / QLF(FR[j])) - CIAF[j])  # (35-36,43)

        CID[k] = CI[j] * CLIP(CIDN, CIDN1, SWT5, TIME[j])   # (27)
        CIG[k] = P[j] * CIM(MSL[j]) * CLIP(CIGN, CIGN1, SWT4, TIME[j])  # (25-26)
        CI[k] =  CI[j] + DT * (CIG[k] - CID[k])    # (24)
        CR[k] = P[k] / (LA * PDN)  # (15)
        CIR[k] = CI[k] / P[k]    # (23)
        
        CIRA[k] = CIR[k] * CIAF[k] / CIAFN   # (22)
        FR[k] = FCM(CR[k]) * FPCI(CIRA[k]) * FPM(POLR[k]) * CLIP(FC, FC1, SWT7, TIME[k]) / FN   # (19-21, 28)
        
        ECIR[k] = CIR[k] * (1 - CIAF[k]) * NREM(NRFR[k]) / (1 - CIAFN)  # (5,6)
        MSL[k] = ECIR[k] / ECIRN   # (4)
        
        QL[k] = QLS * QLM(MSL[k]) * QLC(CR[k]) * QLF(FR[k]) * QLP(POLR[k])   # (37-41)

    # This removes NAN values that make plotting library fail
    CID[0] = CID[1]
    CIG[0] = CIG[1]
    BR[0]  = BR[1]
    DR[0]  = DR[1]
    QL[0]  = QL[1]
    
    return np.around(TIME,1), np.around(P,0), np.around(POLR,5), np.around(CI,5), np.around(QL,5), np.around(NR,5)