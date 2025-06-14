"""
Constants for AB Race Translator

Converted from C++ header files including:
- bettypdef.h  
- ABMsgDef.h
- LOGDEF_AB.h
"""

# Bet Type Constants (from bettypdef.h)
BETTYP_WINPLA = 0
BETTYP_WIN = 1
BETTYP_PLA = 2
BETTYP_QIN = 3
BETTYP_QPL = 4
BETTYP_DBL = 5
BETTYP_TCE = 6
BETTYP_QTT = 7
BETTYP_DQN = 8
BETTYP_TBL = 9
BETTYP_TTR = 10
BETTYP_6UP = 11
BETTYP_DTR = 12
BETTYP_TRIO = 13
BETTYP_QINQPL = 14
BETTYP_CV = 15
BETTYP_MK6 = 16
BETTYP_PWB = 17
BETTYP_AUP = 18
BETTYP_SB = 19
BETTYP_SB_FO = 20
BETTYP_SB_EXO = 21
BETTYP_SB_AUP_PM = 22
BETTYP_SB_AUP_FO_CTL = 23
BETTYP_SB_AUP_FO_NON = 24
BETTYP_SB_SCT_FO = 25
BETTYP_SB_MIX_FO = 26
BETTYP_FF = 27
BETTYP_BWA = 28
BETTYP_CWA = 29
BETTYP_CWB = 30
BETTYP_CWC = 31
BETTYP_IWN = 33
BETTYP_FCT = 34

# Allup variants (from work file definitions)
BETTYP_AWP = 18  # Allup Win/Place
BETTYP_AWN = 19  # Allup Win
BETTYP_APL = 20  # Allup Place
BETTYP_AQN = 21  # Allup Quinella
BETTYP_AQP = 22  # Allup Quinella Place
BETTYP_ATR = 23  # Allup Trio
BETTYP_AQQP = 24 # Allup Quinella/Quinella Place
BETTYP_ATC = 25  # Allup Trifecta
BETTYP_AQT = 26  # Allup Quartet

# Message Codes (from ABMsgDef.h and LOGDEF_AB.h)
LOGAB_CODE_SGN = 1    # sign on
LOGAB_CODE_SGF = 2    # sign off
LOGAB_CODE_ACA = 3    # account access via voice
LOGAB_CODE_ACR = 4    # account release
LOGAB_CODE_WTW = 5    # withdrawal
LOGAB_CODE_RAC = 6    # racing bet
LOGAB_CODE_LOT = 7    # lottery bet
LOGAB_CODE_CAN = 8    # cancel
LOGAB_CODE_RCL = 9    # recall
LOGAB_CODE_OLS = 10   # on-line statement
LOGAB_CODE_DEP = 11   # deposit/deposit cit
LOGAB_CODE_SB = 15    # soccer bet
LOGAB_CODE_ERR = 50001 # custom error code

# Store Type Constants
STORE_TYPE_STRING = 1
STORE_TYPE_INTEGER = 2
STORE_TYPE_CHAR = 3

# Delimiters
DELIMITER = "~|~"
DELIMITER_SIM_SEL = "@|@"  # for simple selection

# Error Constants
NO_TRANSLATE_ERR = "NO_TRANSLATE_ERR"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
TRANSLATE_ERR = "TRANSLATE_ERR"

# Buffer Size
BUF_SIZE = 8192

# Formula Constants (from DeSelMap.cpp)
FORMULA_NAMES = {
    0: "2x1", 1: "2x3", 2: "3x1", 3: "3x3", 4: "3x4", 5: "3x6", 6: "3x7",
    7: "4x1", 8: "4x4", 9: "4x5", 10: "4x6", 11: "4x10", 12: "4x11",
    13: "4x14", 14: "4x15", 15: "5x1", 16: "5x5", 17: "5x6", 18: "5x10",
    19: "5x15", 20: "5x16", 21: "5x20", 22: "5x25", 23: "5x26", 24: "5x30",
    25: "5x31", 26: "6x1", 27: "6x6", 28: "6x7", 29: "6x15", 30: "6x20",
    31: "6x21", 32: "6x22", 33: "6x35", 34: "6x41", 35: "6x42", 36: "6x50",
    37: "6x56", 38: "6x57", 39: "6x62", 40: "6x63", 41: "7x1", 42: "7x7",
    43: "7x8", 44: "7x21", 45: "7x28", 46: "7x29", 47: "7x35", 48: "7x56",
    49: "7x63", 50: "7x64", 51: "7x70", 52: "7x91", 53: "7x98", 54: "7x99",
    55: "7x112", 56: "7x119", 57: "7x120", 58: "7x126", 59: "7x127", 60: "8x1"
}

# Bet Type Names Mapping
BET_TYPE_NAMES = {
    BETTYP_WINPLA: "W-P",
    BETTYP_WIN: "WIN",
    BETTYP_PLA: "PLA", 
    BETTYP_QIN: "QIN",
    BETTYP_QPL: "QPL",
    BETTYP_DBL: "DBL",
    BETTYP_TCE: "TCE",
    BETTYP_FCT: "FCT",
    BETTYP_QTT: "QTT",
    BETTYP_DQN: "D-Q",
    BETTYP_TBL: "TBL",
    BETTYP_TTR: "T-T",
    BETTYP_6UP: "6UP",
    BETTYP_DTR: "D-T",
    BETTYP_TRIO: "TRI",
    BETTYP_QINQPL: "QQP",
    BETTYP_CV: "CV",
    BETTYP_MK6: "MK6",
    BETTYP_PWB: "PWB",
    BETTYP_AWP: "ALUP",
    BETTYP_FF: "F-F",
    BETTYP_BWA: "BWA",
    BETTYP_CWA: "CWA",
    BETTYP_CWB: "CWB",
    BETTYP_CWC: "CWC",
    BETTYP_IWN: "IWN"
}

# Source Type Constants
LOGAB_SRC_VOICE = 1
LOGAB_SRC_CIT = 2
LOGAB_SRC_MAT = 3
LOGAB_SRC_CB_BT = 4
LOGAB_SRC_EWIN = 5
LOGAB_SRC_OLD = 6
LOGAB_SRC_BAT_DEP = 7
LOGAB_SRC_EFT_CB = 8
LOGAB_SRC_EFT_CIT = 9
LOGAB_SRC_EFT_EWIN = 16
LOGAB_SRC_POL = 14
LOGAB_SRC_MAT = 3
LOGAB_SRC_CB_EWAL = 19

# Device Type Constants
DEV_TYP_MPB = 1
DEV_TYP_CIT3 = 2
DEV_TYP_CIT3A = 3
DEV_TYP_CIT5 = 4
DEV_TYP_CIT6 = 5
DEV_TYP_TWM = 6
DEV_TYP_CITPDA = 7
DEV_TYP_ESC = 8
DEV_TYP_INET = 9
DEV_TYP_CIT8 = 10
DEV_TYP_JCBW = 11
DEV_TYP_AMBS = 12
DEV_TYP_WLPDA = 13
DEV_TYP_IPPHONE = 14
DEV_TYP_JCBWEKBA = 17
DEV_TYP_MBSN = 19
DEV_TYP_IOSBS = 20
DEV_TYP_JCMOW = 21
DEV_TYP_IBT = 22
DEV_TYP_AOSBS = 23
DEV_TYP_APISMC = 24
DEV_TYP_APITD = 25
DEV_TYP_IBUT = 26
DEV_TYP_API3HK = 27
DEV_TYP_IBUA = 28
DEV_TYP_WOSBS = 29
DEV_TYP_MASBAI = 30
DEV_TYP_MASBAA = 31

# CIT Type Names
CIT_TYPE_NAMES = [
    "MPB", "CIT-3", "CIT-3A", "CIT-5", "CIT-6", "TWM", "CIT-PDA", "ESC", 
    "EWIN", "CIT-8", "JCBW", "AMBS", "WLPDA", "IP-PHONE", "ITV", "WLPDA",
    "JCBWEKBA", "ITV", "APINOW", "IOSBS", "JCMOW", "IBT", "AOSBS", "APISMC",
    "APITD", "IBUT", "APIWC", "IBUA", "WOSBS", "MASBAI", "MASBAA"
] + [""] * 68 + ["ECBPCC"]  # Index 99 = ECBPCC

# Maximum field size for race
RDS_MAXFLD = 64
