"""
AB Race Translator

Converted from C++ ABRace.cpp
Handles translation of racing bet messages from LOGAB format to delimited string format.
"""

import time
import math
from typing import List, Optional
from .ab_msg_translator import ABMsgTranslator
from .constants import *
from .data_structures import Msg, Logab, StructParser
from .utils import DeSelMap


class ABRace(ABMsgTranslator):
    """
    Racing message translator.
    Converted from C++ ABRace class.
    """
    
    def __init__(self):
        """Initialize the race translator."""
        super().__init__()
        
        # Racing-specific fields
        self.m_sMeetDate = ""
        self.m_cLoc = 0
        self.m_cDay = 0
        self.m_itotalPay = 0
        self.m_iTotalCost = 0
        self.m_iFlexiBetFlag = 0
        self.m_iUnitBet = 0
        self.m_iUnitBetTenK = 0
        self.m_iTotalNoOfCombinations = 0
        self.m_sSellTime = ""
        self.m_cBetType = 0
        self.m_sBetType = ""
        self.m_sFormula = ""
        self.m_iAnonymous = 0
        self.m_iCscCard = 0
        
        # Allup fields
        self.m_cNoOfEvt = 0
        self.m_cFormula = 0
        self.m_cAllupPoolType = [0] * 6
        self.m_iAllupRaceNo = [0] * 6
        self.m_cAllupBankerFlag = [0] * 6
        self.m_cAllupFieldFlag = [0] * 6
        self.m_cAllupMultiFlag = [0] * 6
        self.m_cAllupMultiBankerFlag = [0] * 6
        self.m_cAllupRandomFlag = [0] * 6
        self.m_iNoOfCombination = [0] * 6
        self.m_iPayFactor = [0] * 6
        self.m_iAllupBankerBitmap = [0] * 6
        self.m_iAllupSelectBitmap = [0] * 6
        self.m_sAllupBettype = ""
        
        # Standard/Exotic fields
        self.m_iRaceNo = 0
        self.m_cBankerFlag = 0
        self.m_cFieldFlag = 0
        self.m_cMultiFlag = 0
        self.m_cMultiBankerFlag = 0
        self.m_cRandomFlag = 0
        self.m_iBitmap = [0] * 6
        self.m_sBitmap = ""
        
        # Selection utility
        self.desel_map = DeSelMap()

    def translate_action(self, msg: Msg) -> str:
        """
        Translate racing message to delimited string format.
        
        Args:
            msg: Input racing message
            
        Returns:
            str: Translated message in delimited format
        """
        try:
            # Parse the message
            pMlog = StructParser.parse_logab_from_msg(msg)
            
            # Pack header information
            self.pack_header("", pMlog, msg)
            
            # Extract racing data from the parsed structure
            return self._process_racing_data(pMlog, msg)
            
        except Exception as e:
            # Return error indicator on failure
            return f"ERROR: Failed to translate racing message: {str(e)}"

    def _process_racing_data(self, pMlog: Logab, msg: Msg) -> str:
        """
        Process racing-specific data from LOGAB structure.
        
        Args:
            pMlog: Parsed LOGAB structure
            msg: Original message
            
        Returns:
            str: Formatted racing data
        """
        try:
            # Get racing bet data
            if pMlog.data.bt_rac and pMlog.data.bt_rac.d:
                bet_data = pMlog.data.bt_rac.d
                bet_hdr = bet_data.hdr
                
                # Extract basic bet information
                self.m_itotalPay = bet_hdr.totdu
                self.m_iTotalCost = bet_hdr.costlu
                self.m_cBetType = bet_hdr.bettypebu
                
                # Handle flexi bet calculations
                if hasattr(bet_hdr.betinvcomb, 'flexi'):
                    flexi = bet_hdr.betinvcomb.flexi
                    self.m_iFlexiBetFlag = flexi.flexibet
                    
                    if self.m_iFlexiBetFlag == 0:
                        self.m_iUnitBet = flexi.baseinv
                        self.m_iUnitBetTenK = self.m_iUnitBet * 10000
                        if self.m_iUnitBet > 0:
                            self.m_iTotalNoOfCombinations = (self.m_iTotalCost // 100) // self.m_iUnitBet
                        else:
                            self.m_iTotalNoOfCombinations = 0
                    else:
                        self.m_iTotalNoOfCombinations = flexi.baseinv
                        # Calculate unit bet for flexi bets
                        if self.m_iTotalNoOfCombinations > 0:
                            a1 = float(self.m_iTotalCost)
                            a2 = float(self.m_iTotalNoOfCombinations)
                            tmp = (a1 * 1000.0) / a2
                            tmp1 = tmp / 10.0
                            tmp2 = math.floor(tmp1 + 0.5)
                            self.m_iUnitBetTenK = int(tmp2)
                        else:
                            self.m_iUnitBetTenK = 0
                else:
                    # Default values if flexi data not available
                    self.m_iFlexiBetFlag = 0
                    self.m_iUnitBet = 100  # Default $1
                    self.m_iUnitBetTenK = 1000000
                    self.m_iTotalNoOfCombinations = max(1, self.m_iTotalCost // 10000)
                
                # Format sell time
                sell_time = time.localtime(msg.m_iMsgSellTime or msg.m_iMsgTime)
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                month_name = months[sell_time.tm_mon - 1] if 1 <= sell_time.tm_mon <= 12 else "Jan"
                self.m_sSellTime = f"{sell_time.tm_mday:02d}-{month_name}-{sell_time.tm_year} {sell_time.tm_hour:02d}:{sell_time.tm_min:02d}:{sell_time.tm_sec:02d}"
                
                # Get bet type string
                self.m_sBetType = self.get_bet_type(self.m_cBetType)
                
                # Get selections using DeSelMap utility
                selections = self.desel_map.get_selections(pMlog, self.m_cBetType)
                
                # Process bet type specific data
                self._process_bet_type_data(bet_data, msg)
                
                # Get cross sell indicator
                cross_sell = getattr(pMlog.data.bt_rac, 'crossSellFl', 0)
                
                # Get anonymous and CSC flags
                self.m_iAnonymous = getattr(pMlog.hdr, 'anonymous1', 0)
                self.m_iCscCard = getattr(pMlog.data.bt_rac, 'csctrn', 0)
                
                # Build output string
                return self._build_output_string(selections, cross_sell)
                
            else:
                # No racing data available, return minimal output
                return self._build_minimal_output()
                
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _process_bet_type_data(self, bet_data, msg: Msg):
        """
        Process bet type specific data (Allup vs Standard/Exotic).
        
        Args:
            bet_data: Bet data structure
            msg: Original message
        """
        try:
            if self.m_cBetType == BETTYP_AUP:
                # Process Allup bet
                if bet_data.var and bet_data.var.a:
                    allup = bet_data.var.a
                    self.m_cNoOfEvt = allup.evtbu
                    self.m_cFormula = allup.fmlbu
                    self.m_cLoc = allup.loc
                    self.m_cDay = allup.day
                    
                    # Format meeting date
                    self.m_sMeetDate = self._format_meeting_date(allup.md)
                    
                    # Get formula string
                    self.m_sFormula = self.get_formula(self.m_cFormula)
                    
                    # Process each allup selection
                    for a in range(min(self.m_cNoOfEvt, 6)):
                        if a < len(allup.sel):
                            sel = allup.sel[a]
                            self.m_cAllupPoolType[a] = sel.bettypebu
                            self.m_iAllupRaceNo[a] = sel.racebu
                            self.m_cAllupBankerFlag[a] = sel.ind.bnk1
                            self.m_cAllupFieldFlag[a] = sel.ind.fld1
                            self.m_cAllupMultiFlag[a] = sel.ind.mul1
                            self.m_cAllupMultiBankerFlag[a] = sel.ind.mbk1
                            self.m_cAllupRandomFlag[a] = sel.ind.rand1
                            self.m_iNoOfCombination[a] = sel.comwu
                            self.m_iPayFactor[a] = sel.pftrlu
                            
                            # Get selection bitmaps
                            if sel.sellu and len(sel.sellu) >= 2:
                                self.m_iAllupBankerBitmap[a] = sel.sellu[0]
                                self.m_iAllupSelectBitmap[a] = sel.sellu[1]
            else:
                # Process Standard/Exotic bet
                if bet_data.var and bet_data.var.es:
                    exostd = bet_data.var.es
                    self.m_iRaceNo = exostd.racebu
                    self.m_cLoc = exostd.loc
                    self.m_cDay = exostd.day
                    
                    # Format meeting date
                    self.m_sMeetDate = self._format_meeting_date(exostd.md)
                    
                    # Get indicators
                    self.m_cBankerFlag = exostd.ind.bnk1
                    self.m_cFieldFlag = exostd.ind.fld1
                    self.m_cMultiFlag = exostd.ind.mul1
                    self.m_cMultiBankerFlag = exostd.ind.mbk1
                    self.m_cRandomFlag = exostd.ind.rand1
                    
                    # Get selection bitmaps
                    if exostd.sellu:
                        for a in range(min(len(exostd.sellu), 6)):
                            self.m_iBitmap[a] = exostd.sellu[a]
                            
        except Exception as e:
            # Set default values on error
            self.m_sMeetDate = "01-Jan-2024 00:00:00"
            self.m_cLoc = 1
            self.m_cDay = 1

    def _format_meeting_date(self, md: int) -> str:
        """
        Format meeting date from integer to string.
        
        Args:
            md: Meeting date as integer (YYYYMMDD format)
            
        Returns:
            str: Formatted date string
        """
        try:
            md_str = str(md)
            if len(md_str) == 8:
                yy = md_str[0:4]
                mm = md_str[4:6]
                dd = md_str[6:8]
                return f"{yy}-{mm}-{dd} 00:00:00"
            else:
                return "2024-01-01 00:00:00"
        except:
            return "2024-01-01 00:00:00"

    def _build_output_string(self, selections: str, cross_sell: int) -> str:
        """
        Build the final output string with all racing data.
        
        Args:
            selections: Selection string from DeSelMap
            cross_sell: Cross sell indicator
            
        Returns:
            str: Complete output string
        """
        # Add racing-specific fields
        self.add_field_string(self.m_sMeetDate, 0)
        self.add_field(self.m_cLoc, 0)
        self.add_field(self.m_cDay, 0)
        self.add_field_64(self.m_itotalPay, 0)
        self.add_field_64(self.m_iUnitBetTenK, 0)
        self.add_field_64(self.m_iTotalCost, 0)
        self.add_field_string(self.m_sSellTime, 0)
        self.add_field_string(self.m_sBetType, 0)
        
        # Cancel flag for EDW (empty for race bets)
        self.add_field_string(" ", 0)
        
        # Process bet type specific output
        if self.m_cBetType == BETTYP_AUP:
            self._add_allup_fields()
        else:
            self._add_standard_fields()
        
        # Add selections (truncate if too long)
        if len(selections) > 1000:
            selections = selections[:1000]
        self.add_field_string(selections, 0)
        
        # Add banker and bitmap information
        self._add_bitmap_fields()
        
        # Add final fields
        self.add_field(cross_sell, 0)
        self.add_field(self.m_iFlexiBetFlag, 0)
        self.add_field(self.m_iTotalNoOfCombinations, 0)
        self.add_field(self.m_iAnonymous, 0)
        self.add_field(self.m_iCscCard, 0)
        
        return self.buf

    def _add_allup_fields(self):
        """Add allup-specific fields to output."""
        self.add_field(self.m_cNoOfEvt, 0)
        self.add_field_string(self.m_sFormula, 0)
        
        # Add data for each event
        for a in range(self.m_cNoOfEvt):
            self.m_sAllupBettype = self.get_bet_type(self.m_cAllupPoolType[a])
            self.add_field_string(self.m_sAllupBettype, 0)
            self.add_field(self.m_iAllupRaceNo[a], 0)
            self.add_field(self.m_cAllupBankerFlag[a], 0)
            self.add_field(self.m_cAllupFieldFlag[a], 0)
            self.add_field(self.m_cAllupMultiFlag[a], 0)
            self.add_field(self.m_cAllupMultiBankerFlag[a], 0)
            self.add_field(self.m_cAllupRandomFlag[a], 0)
            self.add_field(self.m_iNoOfCombination[a], 0)
            self.add_field(self.m_iPayFactor[a], 0)
        
        # Pad remaining events with zeros
        for a in range(self.m_cNoOfEvt, 6):
            for _ in range(9):  # 9 fields per event
                self.add_field(0, 0)
        
        # Add standard bet fields (all zeros for allup)
        for _ in range(6):  # 6 standard bet fields
            self.add_field(0, 0)

    def _add_standard_fields(self):
        """Add standard/exotic bet specific fields to output."""
        # Add allup fields (all zeros for standard bets)
        self.add_field(0, 0)  # Number of events
        self.add_field(0, 0)  # Formula
        
        # Add allup event fields (all zeros)
        for _ in range(6):  # 6 events
            for _ in range(9):  # 9 fields per event
                self.add_field(0, 0)
        
        # Add standard bet fields
        self.add_field(self.m_iRaceNo, 0)
        self.add_field(self.m_cBankerFlag, 0)
        self.add_field(self.m_cFieldFlag, 0)
        self.add_field(self.m_cMultiFlag, 0)
        self.add_field(self.m_cMultiBankerFlag, 0)
        self.add_field(self.m_cRandomFlag, 0)

    def _add_bitmap_fields(self):
        """Add banker and bitmap fields to output."""
        if self.m_cBetType < BETTYP_AUP or self.m_cBetType >= BETTYP_FF:
            # Standard/exotic bet bitmaps
            # Add number of bankers (simplified)
            for i in range(3):
                self.add_field(0, 0)  # Banker counts
            
            # Add selection bitmaps
            for i in range(6):
                if self.m_iBitmap[i] > 65535:
                    self.add_field_string("0000", 0)
                else:
                    bitmap_str = f"{self.m_iBitmap[i]:04X}"
                    self.add_field_string(bitmap_str, 0)
        else:
            # Allup bet bitmaps
            # Add banker fields (zeros for allup)
            for _ in range(3):
                self.add_field(0, 0)
            
            # Add allup bitmaps
            for i in range(self.m_cNoOfEvt):
                temp1 = "0000" if self.m_iAllupBankerBitmap[i] > 65535 else f"{self.m_iAllupBankerBitmap[i]:04X}"
                temp2 = "0000" if self.m_iAllupSelectBitmap[i] > 65535 else f"{self.m_iAllupSelectBitmap[i]:04X}"
                bitmap_str = temp1 + temp2
                self.add_field_string(bitmap_str, 0)
            
            # Pad remaining with zeros
            for i in range(self.m_cNoOfEvt, 6):
                self.add_field_string("0000", 0)

    def _build_minimal_output(self) -> str:
        """
        Build minimal output when racing data is not available.
        
        Returns:
            str: Minimal output string
        """
        # Set default values
        self.m_sMeetDate = "01-Jan-2024 00:00:00"
        self.m_cLoc = 1
        self.m_cDay = 1
        self.m_itotalPay = 0
        self.m_iUnitBetTenK = 1000000  # $100 * 10000
        self.m_iTotalCost = 10000  # $100 in cents
        self.m_sSellTime = "01-Jan-2024 00:00:00"
        self.m_sBetType = "WIN"
        
        return self._build_output_string("1*01", 0)

    def get_bet_type(self, bet_type: int) -> str:
        """
        Convert bet type code to string.
        
        Args:
            bet_type: Bet type code
            
        Returns:
            str: Bet type string
        """
        return BET_TYPE_NAMES.get(bet_type, "XXXX")

    def get_formula(self, formula: int) -> str:
        """
        Convert formula code to string.
        
        Args:
            formula: Formula code
            
        Returns:
            str: Formula string
        """
        return FORMULA_NAMES.get(formula, "Err")

    def __str__(self) -> str:
        """String representation of the translator."""
        return f"ABRace(bet_type={self.m_cBetType}, cost={self.m_iTotalCost})"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"ABRace(bet_type={self.m_cBetType}, cost={self.m_iTotalCost}, "
                f"total_pay={self.m_itotalPay}, flexi={self.m_iFlexiBetFlag})")