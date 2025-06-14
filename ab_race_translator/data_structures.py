"""
Data Structures for AB Race Translator

Converted from C++ structures in LOGDEF_AB.h and related headers.
These classes represent the binary message format used in the AB racing system.
"""

import struct
import time
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Msg:
    """
    Main message structure containing the binary buffer and metadata.
    Equivalent to C++ Msg structure.
    """
    m_cpBuf: bytes
    m_iMsgErrwu: int
    m_iSysNo: int
    m_iSysName: str
    m_iMsgTime: int
    m_iMsgDay: int
    m_iMsgMonth: int
    m_iMsgYear: int
    m_iMsgSellTime: int = 0
    m_iMsgCode: int = 0


@dataclass
class LogabHdr:
    """
    LOGAB header structure.
    Corresponds to C++ struct LOGAB_HDR.
    """
    sizew: int
    codewu: int
    errorwu: int
    trapcodebu: int
    stafflu: int
    ltnlu: int
    acclu: int
    filebu: int
    blocklu: int
    overflowlu: int
    offwu: int
    tranwu: int
    timelu: int
    lgslu: int
    msnlu: int
    anonymous1: int = 0
    custSessIdd: int = 0


@dataclass 
class BetFlexiCombo:
    """Flexi bet combination structure"""
    baseinv: int  # 31 bits
    flexibet: int  # 1 bit


@dataclass
class BetInvestCombo:
    """Investment combination union"""
    flexi: BetFlexiCombo


@dataclass
class BetHdr:
    """
    Bet header structure.
    Corresponds to C++ struct BETHDR.
    """
    totdu: int  # total payout in cents
    betinvcomb: BetInvestCombo
    costlu: int  # total cost in cents
    sellTime: int
    businessDate: int
    bettypebu: int


@dataclass
class BetInd:
    """
    Bet indicator structure.
    Corresponds to C++ struct BETIND.
    """
    bnk1: int  # banker
    fld1: int  # field
    mul1: int  # multiple
    mbk1: int  # multiple banker
    rand1: int  # randomly generated
    twoentry: int


@dataclass
class BetAupSel:
    """
    Allup selection structure.
    Corresponds to C++ struct BETAUPSEL.
    """
    racebu: int
    bettypebu: int
    ind: BetInd
    pid: List[int]  # pool id array
    fdsz: int  # field size
    sellu: List[int]  # selection bitmap array
    comwu: int
    pftrlu: int


@dataclass
class BetAup:
    """
    Allup bet structure.
    Corresponds to C++ struct BETAUP.
    """
    loc: int
    day: int
    md: int  # meeting date
    evtbu: int
    fmlbu: int
    sel: List[BetAupSel]  # array of selections


@dataclass
class BetExBnk:
    """
    Extended banker structure.
    Can be either selection bitmap or banker counts.
    """
    sellu: Optional[List[int]] = None  # selection bitmap
    bnkbu: Optional[List[int]] = None  # banker counts


@dataclass
class BetExoStd:
    """
    Exotic/Standard bet structure.
    Corresponds to C++ struct BETEXOSTD.
    """
    loc: int
    day: int
    md: int
    racebu: int
    ind: BetInd
    pid: List[int]  # pool id array
    fdsz: List[int]  # field size array
    sellu: List[int]  # selection bitmap array
    betexbnk: BetExBnk


@dataclass
class BetVar:
    """
    Variable part of bet structure.
    Union representing different bet types.
    """
    a: Optional[BetAup] = None  # allup
    es: Optional[BetExoStd] = None  # exotic/standard


@dataclass
class BetData:
    """
    Bet data structure.
    Corresponds to C++ struct BETDATA.
    """
    hdr: BetHdr
    var: BetVar


@dataclass
class LogabRac:
    """
    Racing bet log structure.
    Corresponds to C++ struct LOGAB_RAC.
    """
    srcbu: int  # source of sell
    blc1: int  # BLC flag
    csctrn: int  # CSC transaction
    crossSellFl: int  # cross sell flag
    d: BetData  # bet data


@dataclass
class LogabData:
    """
    LOGAB data union.
    Contains the actual transaction data.
    """
    bt_rac: Optional[LogabRac] = None


@dataclass
class Logab:
    """
    Complete LOGAB structure.
    Corresponds to C++ struct LOGAB.
    """
    hdr: LogabHdr
    data: LogabData


class StructParser:
    """
    Utility class for parsing binary structures from byte buffers.
    Handles the conversion from C++ packed structures to Python objects.
    """
    
    @staticmethod
    def parse_logab_header(data: bytes, offset: int = 0) -> LogabHdr:
        """
        Parse LOGAB header from binary data.
        
        Args:
            data: Binary data buffer
            offset: Starting offset in buffer
            
        Returns:
            LogabHdr: Parsed header structure
        """
        try:
            # Simplified parsing - adjust format string based on actual C++ struct layout
            fmt = '<HHHBIIIBIII'  # Example format, adjust as needed
            if len(data) < offset + struct.calcsize(fmt):
                raise ValueError("Insufficient data for LOGAB header")
                
            values = struct.unpack_from(fmt, data, offset)
            
            return LogabHdr(
                sizew=values[0],
                codewu=values[1], 
                errorwu=values[2],
                trapcodebu=values[3],
                stafflu=values[4],
                ltnlu=values[5],
                acclu=values[6],
                filebu=values[7],
                blocklu=values[8],
                overflowlu=values[9],
                offwu=values[10] if len(values) > 10 else 0,
                tranwu=values[11] if len(values) > 11 else 0,
                timelu=int(time.time()),  # Default to current time
                lgslu=0,
                msnlu=0
            )
        except (struct.error, IndexError, ValueError) as e:
            # Return default header on parse error
            return LogabHdr(
                sizew=len(data),
                codewu=6,  # LOGAB_CODE_RAC
                errorwu=0,
                trapcodebu=0,
                stafflu=0,
                ltnlu=0,
                acclu=0,
                filebu=0,
                blocklu=0,
                overflowlu=0,
                offwu=0,
                tranwu=0,
                timelu=int(time.time()),
                lgslu=0,
                msnlu=0
            )
    
    @staticmethod
    def parse_bet_header(data: bytes, offset: int) -> BetHdr:
        """
        Parse bet header from binary data.
        
        Args:
            data: Binary data buffer
            offset: Starting offset in buffer
            
        Returns:
            BetHdr: Parsed bet header
        """
        try:
            # Simplified bet header parsing
            fmt = '<QQI'  # totdu, cost, bettypebu
            if len(data) < offset + struct.calcsize(fmt):
                raise ValueError("Insufficient data for bet header")
                
            values = struct.unpack_from(fmt, data, offset)
            
            # Create flexi combo structure
            flexi = BetFlexiCombo(baseinv=100, flexibet=0)  # Default values
            betinvcomb = BetInvestCombo(flexi=flexi)
            
            return BetHdr(
                totdu=values[0],
                betinvcomb=betinvcomb,
                costlu=values[1],
                sellTime=int(time.time()),
                businessDate=20240101,  # Default business date
                bettypebu=values[2] if len(values) > 2 else 1
            )
        except (struct.error, IndexError, ValueError):
            # Return default bet header on parse error
            flexi = BetFlexiCombo(baseinv=100, flexibet=0)
            betinvcomb = BetInvestCombo(flexi=flexi)
            
            return BetHdr(
                totdu=0,
                betinvcomb=betinvcomb,
                costlu=0,
                sellTime=int(time.time()),
                businessDate=20240101,
                bettypebu=1  # Default WIN bet
            )
    
    @staticmethod
    def parse_logab_from_msg(msg: Msg) -> Logab:
        """
        Parse complete LOGAB structure from message.
        
        Args:
            msg: Input message containing binary data
            
        Returns:
            Logab: Parsed LOGAB structure
        """
        try:
            # Parse header
            header = StructParser.parse_logab_header(msg.m_cpBuf)
            
            # For racing messages, parse racing data
            if header.codewu == 6:  # LOGAB_CODE_RAC
                # Parse bet header (simplified)
                bet_hdr = StructParser.parse_bet_header(msg.m_cpBuf, 50)  # Estimated offset
                
                # Create simplified racing structure
                bet_var = BetVar()
                bet_data = BetData(hdr=bet_hdr, var=bet_var)
                
                logab_rac = LogabRac(
                    srcbu=0,
                    blc1=0,
                    csctrn=0,
                    crossSellFl=0,
                    d=bet_data
                )
                
                logab_data = LogabData(bt_rac=logab_rac)
            else:
                logab_data = LogabData()
            
            return Logab(hdr=header, data=logab_data)
            
        except Exception as e:
            # Return minimal valid structure on any error
            header = LogabHdr(
                sizew=len(msg.m_cpBuf),
                codewu=msg.m_iMsgCode or 6,
                errorwu=msg.m_iMsgErrwu,
                trapcodebu=0,
                stafflu=0,
                ltnlu=0,
                acclu=0,
                filebu=0,
                blocklu=0,
                overflowlu=0,
                offwu=0,
                tranwu=0,
                timelu=msg.m_iMsgTime,
                lgslu=0,
                msnlu=0
            )
            
            return Logab(hdr=header, data=LogabData())


def create_sample_msg() -> Msg:
    """
    Create a sample message for testing.
    
    Returns:
        Msg: Sample message with test data
    """
    # Create sample binary data
    sample_data = b'\x00' * 200  # 200 bytes of zeros
    
    return Msg(
        m_cpBuf=sample_data,
        m_iMsgErrwu=0,
        m_iSysNo=1,
        m_iSysName="AB",
        m_iMsgTime=int(time.time()),
        m_iMsgDay=1,
        m_iMsgMonth=1,
        m_iMsgYear=2024,
        m_iMsgSellTime=int(time.time()),
        m_iMsgCode=6  # LOGAB_CODE_RAC
    )
