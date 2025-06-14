"""
Utility classes for AB Race Translator

Converted from C++ DeSelMap.cpp and related utility functions.
Provides selection mapping and formatting functionality.
"""

import struct
from typing import List, Dict, Optional
from .constants import *
from .data_structures import Logab


class DeSelMap:
    """
    Selection mapping utility class.
    Converted from C++ DeSelMap class.
    Handles formatting of bet selections from binary bitmaps to human-readable strings.
    """
    
    def __init__(self):
        """Initialize the selection mapper."""
        pass
    
    def get_selections(self, pMlog: Logab, bet_type: int) -> str:
        """
        Get formatted selection string for a bet.
        
        Args:
            pMlog: LOGAB structure containing bet data
            bet_type: Bet type code
            
        Returns:
            str: Formatted selection string
        """
        try:
            if bet_type == BETTYP_AUP:
                return self._format_allup_selections(pMlog)
            elif bet_type in [BETTYP_MK6, BETTYP_PWB]:
                return self._format_lottery_selections(pMlog)
            else:
                return self._format_standard_selections(pMlog)
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def _format_allup_selections(self, pMlog: Logab) -> str:
        """
        Format allup bet selections.
        
        Args:
            pMlog: LOGAB structure
            
        Returns:
            str: Formatted allup selections
        """
        try:
            selections = []
            
            # Get allup data
            if (pMlog.data.bt_rac and pMlog.data.bt_rac.d and 
                pMlog.data.bt_rac.d.var and pMlog.data.bt_rac.d.var.a):
                
                allup = pMlog.data.bt_rac.d.var.a
                
                for a in range(min(allup.evtbu, 6)):
                    if a < len(allup.sel):
                        sel = allup.sel[a]
                        race_sel = f"{sel.racebu}*"
                        
                        # Format selection based on bet type
                        bet_type = sel.bettypebu
                        if bet_type in [BETTYP_WIN, BETTYP_PLA, BETTYP_WINPLA, 
                                       BETTYP_BWA, BETTYP_CWA, BETTYP_CWB, BETTYP_CWC]:
                            race_sel += self._format_simple_selection(sel.sellu, 0)
                        elif bet_type in [BETTYP_QIN, BETTYP_QPL, BETTYP_TRIO, 
                                         BETTYP_QINQPL, BETTYP_FF, BETTYP_IWN]:
                            race_sel += self._format_quinella_selection(sel.sellu, sel.ind.bnk1)
                        elif bet_type == BETTYP_FCT:
                            race_sel += self._format_extended_selection(sel.sellu, 2, sel.ind.bnk1)
                        else:
                            race_sel += self._format_simple_selection(sel.sellu, 0)
                        
                        # Add indicators
                        race_sel += self._format_indicators(sel.ind, True)
                        selections.append(race_sel)
                
                return "/".join(selections)
            else:
                return "1*01"  # Default selection
                
        except Exception as e:
            return "1*01"  # Default on error
    
    def _format_standard_selections(self, pMlog: Logab) -> str:
        """
        Format standard/exotic bet selections.
        
        Args:
            pMlog: LOGAB structure
            
        Returns:
            str: Formatted standard selections
        """
        try:
            # Get standard bet data
            if (pMlog.data.bt_rac and pMlog.data.bt_rac.d and 
                pMlog.data.bt_rac.d.var and pMlog.data.bt_rac.d.var.es):
                
                exostd = pMlog.data.bt_rac.d.var.es
                bet_type = pMlog.data.bt_rac.d.hdr.bettypebu
                
                selections = f"{exostd.racebu}*"
                
                if bet_type in [BETTYP_WIN, BETTYP_PLA, BETTYP_WINPLA, 
                               BETTYP_BWA, BETTYP_CWA, BETTYP_CWB, BETTYP_CWC]:
                    selections += self._format_simple_selection(exostd.sellu, 0)
                elif bet_type in [BETTYP_QIN, BETTYP_QPL, BETTYP_TRIO, 
                                 BETTYP_QINQPL, BETTYP_FF]:
                    banker_count = exostd.betexbnk.bnkbu[0] if exostd.betexbnk.bnkbu else 0
                    selections += self._format_quinella_selection(exostd.sellu, banker_count)
                elif bet_type == BETTYP_IWN:
                    selections += self._format_quinella_selection(exostd.sellu, 1)
                elif bet_type == BETTYP_TCE:
                    banker_count = exostd.betexbnk.bnkbu[0] if exostd.betexbnk.bnkbu else 0
                    selections += self._format_extended_selection(exostd.sellu, 3, banker_count)
                elif bet_type == BETTYP_FCT:
                    banker_count = exostd.betexbnk.bnkbu[0] if exostd.betexbnk.bnkbu else 0
                    selections += self._format_extended_selection(exostd.sellu, 2, banker_count)
                elif bet_type == BETTYP_QTT:
                    banker_count = exostd.betexbnk.bnkbu[0] if exostd.betexbnk.bnkbu else 0
                    selections += self._format_extended_selection(exostd.sellu, 4, banker_count)
                elif bet_type in [BETTYP_DBL, BETTYP_TBL, BETTYP_6UP]:
                    # Multi-leg bets
                    leg_count = self._get_leg_count(bet_type)
                    leg_selections = []
                    for i in range(leg_count):
                        if i < len(exostd.sellu):
                            leg_sel = self._format_simple_selection([exostd.sellu[i]], 0)
                            leg_selections.append(leg_sel)
                    selections += "/".join(leg_selections)
                elif bet_type in [BETTYP_TTR, BETTYP_DQN, BETTYP_DTR]:
                    # Multi-leg quinella bets
                    leg_count = self._get_leg_count(bet_type)
                    leg_selections = []
                    for i in range(leg_count):
                        banker_count = exostd.betexbnk.bnkbu[i] if (exostd.betexbnk.bnkbu and i < len(exostd.betexbnk.bnkbu)) else 0
                        leg_sel = self._format_quinella_selection(exostd.sellu[i*2:(i+1)*2], banker_count)
                        leg_selections.append(leg_sel)
                    selections += "/".join(leg_selections)
                else:
                    selections += self._format_simple_selection(exostd.sellu, 0)
                
                # Add indicators
                selections += self._format_indicators(exostd.ind, False)
                
                return selections
            else:
                return "1*01"  # Default selection
                
        except Exception as e:
            return "1*01"  # Default on error
    
    def _format_lottery_selections(self, pMlog: Logab) -> str:
        """
        Format lottery bet selections (placeholder).
        
        Args:
            pMlog: LOGAB structure
            
        Returns:
            str: Formatted lottery selections
        """
        # Simplified lottery formatting
        return "01+02+03+04+05+06"
    
    def _format_simple_selection(self, sellu: List[int], bitmap_pos: int) -> str:
        """
        Format simple selection bitmap.
        
        Args:
            sellu: Selection bitmap array
            bitmap_pos: Position in bitmap array
            
        Returns:
            str: Formatted selection string
        """
        if not sellu or bitmap_pos >= len(sellu):
            return "01"
        
        selections = []
        bitmap = sellu[bitmap_pos]
        
        # Check each bit position (horses 1-64)
        for horse in range(1, RDS_MAXFLD + 1):
            if bitmap & (1 << horse):
                selections.append(f"{horse:02d}")
        
        if not selections:
            return "01"
        
        return "+".join(selections)
    
    def _format_quinella_selection(self, sellu: List[int], num_bankers: int) -> str:
        """
        Format quinella-type selection with bankers.
        
        Args:
            sellu: Selection bitmap array
            num_bankers: Number of banker bitmaps
            
        Returns:
            str: Formatted quinella selection
        """
        if not sellu:
            return "01+02"
        
        selections = []
        
        if num_bankers == 0:
            # No bankers, format as simple selection
            return self._format_simple_selection(sellu, 0)
        else:
            # Format bankers and other selections
            for i in range(min(2, len(sellu))):
                sel_part = self._format_simple_selection(sellu, i)
                selections.append(sel_part)
                if i < len(sellu) - 1:
                    selections.append(">")  # Banker separator
        
        return "".join(selections)
    
    def _format_extended_selection(self, sellu: List[int], num_bitmaps: int, num_bankers: int) -> str:
        """
        Format extended selection (TCE/QTT/FCT).
        
        Args:
            sellu: Selection bitmap array
            num_bitmaps: Number of bitmaps to process
            num_bankers: Number of banker selections
            
        Returns:
            str: Formatted extended selection
        """
        if not sellu:
            return "01+02+03"
        
        selections = []
        
        # Process each bitmap
        for i in range(min(num_bitmaps, len(sellu))):
            sel_part = self._format_simple_selection(sellu, i)
            selections.append(sel_part)
        
        # Add banker separators if needed
        if num_bankers > 0 and len(selections) > 1:
            # Insert banker separator before last selection
            result = selections[0]
            for i in range(1, len(selections)):
                if i == len(selections) - 1 and num_bankers > 0:
                    result += ">" + selections[i]
                else:
                    result += "+" + selections[i]
            return result
        
        return "+".join(selections)
    
    def _format_indicators(self, ind, is_allup: bool = False) -> str:
        """
        Format bet indicators (Field, Multiple, etc.).
        
        Args:
            ind: Indicator structure
            is_allup: Whether this is an allup bet
            
        Returns:
            str: Indicator string
        """
        indicators = ""
        
        try:
            if hasattr(ind, 'fld1') and ind.fld1:
                indicators += "F"
            if hasattr(ind, 'mul1') and ind.mul1:
                indicators += "M"
        except:
            pass
        
        return indicators
    
    def _get_leg_count(self, bet_type: int) -> int:
        """
        Get number of legs for multi-leg bet types.
        
        Args:
            bet_type: Bet type code
            
        Returns:
            int: Number of legs
        """
        if bet_type == BETTYP_DBL:
            return 2
        elif bet_type == BETTYP_TBL:
            return 3
        elif bet_type == BETTYP_6UP:
            return 6
        elif bet_type in [BETTYP_TTR, BETTYP_DQN, BETTYP_DTR]:
            return 2 if bet_type in [BETTYP_DQN, BETTYP_DTR] else 3
        else:
            return 1


class BinaryParser:
    """
    Utility class for parsing binary data.
    """
    
    @staticmethod
    def parse_uint64(data: bytes, offset: int) -> int:
        """
        Parse 64-bit unsigned integer from binary data.
        
        Args:
            data: Binary data
            offset: Offset in bytes
            
        Returns:
            int: Parsed integer
        """
        try:
            if len(data) >= offset + 8:
                return struct.unpack_from('<Q', data, offset)[0]
            else:
                return 0
        except:
            return 0
    
    @staticmethod
    def parse_uint32(data: bytes, offset: int) -> int:
        """
        Parse 32-bit unsigned integer from binary data.
        
        Args:
            data: Binary data
            offset: Offset in bytes
            
        Returns:
            int: Parsed integer
        """
        try:
            if len(data) >= offset + 4:
                return struct.unpack_from('<I', data, offset)[0]
            else:
                return 0
        except:
            return 0
    
    @staticmethod
    def parse_uint8(data: bytes, offset: int) -> int:
        """
        Parse 8-bit unsigned integer from binary data.
        
        Args:
            data: Binary data
            offset: Offset in bytes
            
        Returns:
            int: Parsed integer
        """
        try:
            if len(data) > offset:
                return data[offset]
            else:
                return 0
        except:
            return 0


def format_currency(amount_cents: int) -> str:
    """
    Format currency amount from cents to dollar string.
    
    Args:
        amount_cents: Amount in cents
        
    Returns:
        str: Formatted currency string
    """
    dollars = amount_cents / 100.0
    return f"${dollars:.2f}"


def format_percentage(value: int, divisor: int = 100) -> str:
    """
    Format percentage value.
    
    Args:
        value: Raw percentage value
        divisor: Divisor for percentage calculation
        
    Returns:
        str: Formatted percentage string
    """
    if divisor == 0:
        return "0.00%"
    
    percentage = (value / divisor)
    return f"{percentage:.2f}%"


def validate_bet_type(bet_type: int) -> bool:
    """
    Validate if bet type is recognized.
    
    Args:
        bet_type: Bet type code
        
    Returns:
        bool: True if valid bet type
    """
    return bet_type in BET_TYPE_NAMES


def truncate_string(text: str, max_length: int) -> str:
    """
    Truncate string to maximum length.
    
    Args:
        text: Input string
        max_length: Maximum allowed length
        
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length]
