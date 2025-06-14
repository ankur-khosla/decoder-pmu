"""
Base AB Message Translator

Converted from C++ ABMsgTranslator.cpp
Provides base functionality for message translation with field formatting.
"""

import time
from typing import List, Optional, Union
from .constants import *
from .data_structures import Msg, Logab, StructParser


class ABMsgTranslator:
    """
    Base class for AB message translation.
    Converted from C++ ABMsgTranslator class.
    """
    
    def __init__(self):
        """Initialize the translator."""
        self.buf = ""
        self.m_iCount = 0
        self.m_iLoggerMsgOrderNo = 1
        self.m_lLoggerTapeId = 1
        self.m_iTerminalType = 0
        
        # Header fields
        self.m_iSysNo = 0
        self.m_iMsgOrderNo = 0
        self.m_sSysName = ""
        self.m_sSellingDate = ""
        self.m_iMsgSize = 0
        self.m_iMsgCode = 0
        self.m_iErrCode = 0
        self.m_iTrapCode = 0
        self.m_iStaffNo = 0
        self.m_iLogTermNo = 0
        self.m_iAcctNo = 0
        self.m_iFileNo = 0
        self.m_iBlockNo = 0
        self.m_iOverflowNo = 0
        self.m_iOffsetUnit = 0
        self.m_iTranNo = 0
        self.m_sTime = ""
        self.m_iLastLogSeq = 0
        self.m_iMsnNo = 0
        self.m_iExtSysType = 0
        self.m_iCatchUp = 0
        self.m_iBtExcept = 0
        self.m_iOtherSys = 0
        self.m_iPreLog = 0
        self.m_iTimeout = 0
        self.m_iLateReply = 0
        self.m_iBcsMsg = 0
        self.m_iRcvMsg = 0
        self.m_iOverFlow = 0
        self.m_iEscRel = 0
        self.m_iNoFlush = 0
        self.m_iTrainAcct = 0
        self.m_iSessionInfo = 0
        self.m_iSourceType = 0
        self.m_cVoiceFENo = 0
        self.m_sTerminalNo = ""
        self.m_iVoiceLocId = 0
        self.m_iDidCitNo = 0
        self.m_cDidPseTermNo = 0
        self.m_cDidFENo = 0
        self.m_sDidCitType = ""
        self.m_iCBCenterNo = 0
        self.m_iCBWindowNo = 0
        self.m_iCBLogTermNo = 0
        self.m_cCBSysNo = 0
        self.m_iOldCenterNo = 0
        self.m_iOldWindowNo = 0
        self.m_iOldChanNo = 0
        self.m_cOldSysNo = 0
        self.m_cPolFileNo = 0
        self.m_iPolOffsetNo = 0
        self.m_cMatNo = ""
        self.m_iBatchDep = 0
        self.m_iCallSeq = 0

    def translate_header(self, msg: Msg) -> str:
        """
        Translate message header.
        
        Args:
            msg: Input message
            
        Returns:
            str: Translated header or error message
        """
        try:
            pMlog = StructParser.parse_logab_from_msg(msg)
            
            if (msg.m_iMsgErrwu != 0) and (pMlog.hdr.codewu != LOGAB_CODE_ACA):
                self.get_error(pMlog, msg)
            else:
                if (pMlog.hdr.errorwu != 0 or 
                    getattr(pMlog.hdr, 'prelog1', 0) != 0 or
                    getattr(pMlog.hdr, 'laterpy1', 0) != 0 or 
                    getattr(pMlog.hdr, 'timeout1', 0) != 0 or
                    getattr(pMlog.hdr, 'train1', 0) != 0):
                    self.get_error(pMlog, msg)
            
            return self.buf
        except Exception as e:
            return ""

    def translate_action(self, msg: Msg) -> str:
        """
        Virtual method for translating message action.
        Should be overridden by derived classes.
        
        Args:
            msg: Input message
            
        Returns:
            str: NOT_IMPLEMENTED for base class
        """
        hdr_err = self.translate_header(msg)
        
        if hdr_err and DELIMITER in hdr_err:
            return hdr_err  # Error message
        
        return NOT_IMPLEMENTED

    def translate(self, msg_type: int, msg: Msg) -> str:
        """
        Main translation method.
        
        Args:
            msg_type: Message type code
            msg: Input message
            
        Returns:
            str: Translated message
        """
        hdr_err = self.translate_header(msg)
        
        if hdr_err and DELIMITER in hdr_err:
            return hdr_err  # Error message
            
        buf_msg = self.translate_action(msg)
        return buf_msg

    def pack_header(self, store_proc_name: str, pMlog: Logab, msg: Msg):
        """
        Pack message header into output buffer.
        
        Args:
            store_proc_name: Stored procedure name
            pMlog: LOGAB structure
            msg: Input message
        """
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        self.m_iSysNo = msg.m_iSysNo
        self.m_iMsgOrderNo = self.m_iLoggerMsgOrderNo
        self.m_sSysName = msg.m_iSysName
        
        self.m_sSellingDate = f"{msg.m_iMsgDay:02d}-{months[msg.m_iMsgMonth]}-{msg.m_iMsgYear}"
        
        self.m_iMsgSize = pMlog.hdr.sizew
        self.m_iMsgCode = pMlog.hdr.codewu
        self.m_iErrCode = msg.m_iMsgErrwu
        if self.m_iErrCode != 0:
            self.m_iErrCode = 1
            
        self.m_iTrapCode = pMlog.hdr.trapcodebu
        self.m_iStaffNo = pMlog.hdr.stafflu
        self.m_iLogTermNo = pMlog.hdr.ltnlu
        self.m_iAcctNo = pMlog.hdr.acclu
        self.m_iFileNo = pMlog.hdr.filebu
        self.m_iBlockNo = pMlog.hdr.blocklu
        self.m_iOverflowNo = pMlog.hdr.overflowlu
        self.m_iOffsetUnit = pMlog.hdr.offwu
        self.m_iTranNo = pMlog.hdr.tranwu
        self.m_iLastLogSeq = pMlog.hdr.lgslu
        self.m_iMsnNo = pMlog.hdr.msnlu
        
        # Format time
        tm_time = time.localtime(msg.m_iMsgTime)
        month_name = months[tm_time.tm_mon] if tm_time.tm_mon < len(months) else "Jan"
        self.m_sTime = f"{tm_time.tm_mday:02d}-{month_name}-{tm_time.tm_year} {tm_time.tm_hour:02d}:{tm_time.tm_min:02d}:{tm_time.tm_sec:02d}"
        
        # Initialize source-specific fields
        self.m_iSourceType = getattr(pMlog.hdr, 'srcTypebu', 0)
        self.m_sTerminalNo = ""
        self.m_sDidCitType = ""
        self.m_cMatNo = ""
        
        # Handle different source types (simplified)
        if self.m_iSourceType == LOGAB_SRC_CIT or self.m_iSourceType == LOGAB_SRC_EFT_CIT:
            self.m_sDidCitType = "CIT"
        elif self.m_iSourceType == LOGAB_SRC_EWIN or self.m_iSourceType == LOGAB_SRC_EFT_EWIN:
            self.m_sDidCitType = "EWIN"
        
        self.m_iCallSeq = getattr(pMlog.hdr, 'custSessIdd', 0)
        
        # Add header fields to output
        self.add_field(0, 0)  # Record separator
        self.add_field(self.m_iMsgCode, 0)  # Message code
        self.add_field_string(self.m_sSysName, 0)  # System name
        self.add_field(self.m_iMsgOrderNo, 0)  # Message order
        self.add_field_string(self.m_sSellingDate, 0)  # Selling date
        self.add_field(self.m_iMsgSize, 0)  # Message size
        self.add_field(self.m_iMsgCode, 0)  # Message code (again)
        self.add_field(self.m_iErrCode, 0)  # Error code
        self.add_field(self.m_iTrapCode, 0)  # Trap code
        self.add_field(self.m_iStaffNo, 0)  # Staff number
        self.add_field(self.m_iLogTermNo, 0)  # Log terminal number
        self.add_field(self.m_iAcctNo, 0)  # Account number
        self.add_field(self.m_iFileNo, 0)  # File number
        self.add_field(self.m_iBlockNo, 0)  # Block number
        self.add_field(self.m_iOverflowNo, 0)  # Overflow number
        self.add_field(self.m_iOffsetUnit, 0)  # Offset unit
        self.add_field(self.m_iTranNo, 0)  # Transaction number
        self.add_field_string(self.m_sTime, 0)  # Time
        self.add_field(self.m_iLastLogSeq, 0)  # Last log sequence
        self.add_field(self.m_iMsnNo, 0)  # MSN number
        self.add_field(self.m_iExtSysType, 0)  # External system type
        self.add_field(self.m_iCatchUp, 0)  # Catch up
        self.add_field(self.m_iBtExcept, 0)  # BT exception
        self.add_field(self.m_iOtherSys, 0)  # Other system
        self.add_field(self.m_iPreLog, 0)  # Pre log
        self.add_field(self.m_iTimeout, 0)  # Timeout
        self.add_field(self.m_iLateReply, 0)  # Late reply
        self.add_field(self.m_iBcsMsg, 0)  # BCS message
        self.add_field(self.m_iRcvMsg, 0)  # Receive message
        self.add_field(self.m_iOverFlow, 0)  # Overflow
        self.add_field(self.m_iEscRel, 0)  # ESC release
        self.add_field(self.m_iNoFlush, 0)  # No flush
        self.add_field(self.m_iTrainAcct, 0)  # Training account
        self.add_field(self.m_iSessionInfo, 0)  # Session info
        self.add_field(self.m_iSourceType, 0)  # Source type
        self.add_field(self.m_cVoiceFENo, 0)  # Voice FE number
        self.add_field_string(self.m_sTerminalNo, 0)  # Terminal number
        self.add_field(self.m_iVoiceLocId, 0)  # Voice location ID
        self.add_field(self.m_iDidCitNo, 0)  # DID CIT number
        self.add_field(self.m_cDidPseTermNo, 0)  # DID pseudo terminal
        self.add_field(self.m_cDidFENo, 0)  # DID FE number
        self.add_field_string(self.m_sDidCitType, 0)  # DID CIT type
        self.add_field(self.m_iCBCenterNo, 0)  # CB center number
        self.add_field(self.m_iCBWindowNo, 0)  # CB window number
        self.add_field(self.m_iCBLogTermNo, 0)  # CB log terminal
        self.add_field(self.m_cCBSysNo, 0)  # CB system number
        self.add_field(self.m_iOldCenterNo, 0)  # Old center number
        self.add_field(self.m_iOldWindowNo, 0)  # Old window number
        self.add_field(self.m_iOldChanNo, 0)  # Old channel number
        self.add_field(self.m_cOldSysNo, 0)  # Old system number
        self.add_field(self.m_cPolFileNo, 0)  # POL file number
        self.add_field(self.m_iPolOffsetNo, 0)  # POL offset number
        self.add_field_string(self.m_cMatNo, 0)  # MAT number
        self.add_field(self.m_iBatchDep, 0)  # Batch deposit
        
        # Add call sequence
        if self.m_iErrCode == 0:
            self.add_field_64(self.m_iCallSeq, 0)
        else:
            self.add_field(0, 0)
            
        # Add terminal type
        if self.m_iMsgCode == 202:
            self.add_field(0, 0)
        else:
            self.add_field(self.m_iTerminalType, 0)

    def add_field(self, val: Union[int, str], output: int):
        """
        Add integer field to output buffer.
        
        Args:
            val: Value to add
            output: Output flag (unused)
        """
        if isinstance(val, str):
            self.add_field_string(val, output)
            return
            
        # Handle integer values
        r_val = val
        if val > 2147483647:
            r_val = 2147483647
        elif val < -2147483647:
            r_val = -2147483647
            
        self.add_field_string(str(r_val), output)

    def add_field_64(self, val: int, output: int):
        """
        Add 64-bit integer field to output buffer.
        
        Args:
            val: 64-bit value to add
            output: Output flag (unused)
        """
        self.add_field_string(str(val), output)

    def add_field_string(self, val: str, output: int):
        """
        Add string field to output buffer.
        
        Args:
            val: String value to add
            output: Output flag (unused)
        """
        if self.m_iCount == 2:
            self.buf += DELIMITER_SIM_SEL
        elif self.m_iCount > 2:
            self.buf += DELIMITER
            
        if self.m_iCount >= 1:
            self.buf += val
            
        self.m_iCount += 1

    def get_error(self, pMlog: Logab, msg: Msg):
        """
        Handle error conditions in message processing.
        
        Args:
            pMlog: LOGAB structure
            msg: Input message
        """
        # Simplified error handling
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        self.m_iSysNo = msg.m_iSysNo
        self.m_iMsgOrderNo = self.m_iLoggerMsgOrderNo
        self.m_sSysName = msg.m_iSysName
        self.m_sSellingDate = f"{msg.m_iMsgDay:02d}-{months[msg.m_iMsgMonth]}-{msg.m_iMsgYear}"
        
        # Add error fields
        self.add_field(0, 0)
        self.add_field(LOGAB_CODE_ERR, 0)  # Error code
        self.add_field_string(self.m_sSysName, 0)
        self.add_field(self.m_iMsgOrderNo, 0)
        self.add_field_string(self.m_sSellingDate, 0)

    def set_msg_key(self, tape_id: int, msg_order_no: int):
        """
        Set message key parameters.
        
        Args:
            tape_id: Tape ID
            msg_order_no: Message order number
        """
        self.m_lLoggerTapeId = tape_id
        self.m_iLoggerMsgOrderNo = msg_order_no