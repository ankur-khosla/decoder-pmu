import pytest


import time
from ab_race_translator import create_ab_race, Msg

header_fields = [
    "headerSystemID",
    "headerBusinessDate",
    "headerActivityID",
    "headerEnquiryStatus",
    "headerActivityNature",
    "headerErrorCode",
    "headerMessageCode"
]

value_fields = [
    "oltp_id",
    "msg_order_no",
    "selling_date",
    "msg_size",
    "msg_code",
    "err_code",
    "bcs_trap_msg_code",
    "staff_no",
    "logical_term_no",
    "acct_no",
    "acct_file_file_no",
    "acct_file_block_no",
    "overflow_block_no",
    "offset_to_acct_unit",
    "ac_tran_no",
    "time_stamp",
    "last_log_seq",
    "msn",
    "ext_req_type",
    "prev_txn_catch_up",
    "bt_exception",
    "msg_to_other_system",
    "pre_logon_flag",
    "ext_req_timeout_flag",
    "late_reply_flag",
    "upd_bcsmsg_flag",
    "upd_rcvmsg_flag",
    "overflow_required_flag",
    "cb_local_acct_release_flag",
    "no_flush_acct_release_flag",
    "training_acct",
    "acct_sess_info_append",
    "source_type",
    "front_end_no",
    "v_term_no",
    "v_location_id",
    "d_cit_no",
    "d_pseudo_term_no",
    "d_frontend_no",
    "cit_type",
    "cbbt_centre_no",
    "cbbt_window_no",
    "cbbt_logical_term_no",
    "cbbt_system_no",
    "old_cb_centre_no",
    "old_cb_window_no",
    "old_cb_channel_no",
    "old_cb_system_no",
    "pol_file_no",
    "pol_offset_no",
    "mat_no",
    "batch_deposit",
    "call_seq",
    "opt_mode",
    "meeting_date",
    "meeting_loc",
    "meeting_day",
    "ttl_pay",
    "unit_bet",
    "ttl_cost",
    "sell_time",
    "bet_type",
    "cancel_flag",
    "allup_event_no",
    "allup_formula",
    "allup_pool_type1",
    "allup_race_no1",
    "allup_banker_flag1",
    "allup_field_flag1",
    "allup_multi_flag1",
    "allup_multi_banker_flag1",
    "allup_random_flag1",
    "allup_no_of_combination1",
    "allup_pay_factor1",
    "allup_pool_type2",
    "allup_race_no2",
    "allup_banker_flag2",
    "allup_field_flag2",
    "allup_multi_flag2",
    "allup_multi_banker_flag2",
    "allup_random_flag2",
    "allup_no_of_combination2",
    "allup_pay_factor2",
    "allup_pool_type3",
    "allup_race_no3",
    "allup_banker_flag3",
    "allup_field_flag3",
    "allup_multi_flag3",
    "allup_multi_banker_flag3",
    "allup_random_flag3",
    "allup_no_of_combination3",
    "allup_pay_factor3",
    "allup_pool_type4",
    "allup_race_no4",
    "allup_banker_flag4",
    "allup_field_flag4",
    "allup_multi_flag4",
    "allup_multi_banker_flag4",
    "allup_random_flag4",
    "allup_no_of_combination4",
    "allup_pay_factor4",
    "allup_pool_type5",
    "allup_race_no5",
    "allup_banker_flag5",
    "allup_field_flag5",
    "allup_multi_flag5",
    "allup_multi_banker_flag5",
    "allup_random_flag5",
    "allup_no_of_combination5",
    "allup_pay_factor5",
    "allup_pool_type6",
    "allup_race_no6",
    "allup_banker_flag6",
    "allup_field_flag6",
    "allup_multi_flag6",
    "allup_multi_banker_flag6",
    "allup_random_flag6",
    "allup_no_of_combination6",
    "allup_pay_factor6",
    "race_no",
    "banker_flag",
    "field_flag",
    "multiple_flag",
    "multi_banker_flag",
    "random_flag",
    "sb_selection",
    "no_banker_bitmap1",
    "no_banker_bitmap2",
    "no_banker_bitmap3",
    "bitmap1",
    "bitmap2",
    "bitmap3",
    "bitmap4",
    "bitmap5",
    "bitmap6",
    "cross_selling_flag",
    "flexi_bet_flag",
    "no_of_combinations",
    "is_anonymous_acc",
    "is_csc_card"
]

def fetch_result(input_data):
    """
    Basic usage example showing how to translate a racing message.
    """
    print("=== Basic Usage Example ===")
    
    # Create a race translator instance
    translator = create_ab_race()
    
    
    msg = Msg(
        m_cpBuf=bytes.fromhex(input_data),
        m_iMsgErrwu=0,
        m_iSysNo=1,
        m_iSysName="AB",
        m_iMsgTime=int(time.time()),
        m_iMsgDay=15,
        m_iMsgMonth=6,
        m_iMsgYear=2024,
        m_iMsgSellTime=int(time.time()),
        m_iMsgCode=6  # LOGAB_CODE_RAC
    )
    
    # Translate the message
    result = translator.translate_action(msg)
    print(result)
    exit(0)
    return result


def test_method_output_case1():
    # INPUT (hex string or binary blob)
    input_data = "14000000D3B334010029470902000000428A143F01000000000000000005001C001E0000002C0A5F6500000000CC000000000000002C0A5F6500000000D3B33401ED000600000000B0650300E90600002C45F2000000000000000000000000CC002C0A5F65FE284709020000004F6E000005000000009B5F140000000120D3B33401000000000000000000009210190001000000428A143F0100000000000000000000000000E906000000000000000000000000000000000000010000FE0500000500000000000000001E0000007017000000000000D3B334010400080505D3B334010201FC8FAEA41E01000000000000000000000F0000000000004000000000000020040000000000000000000000000000000000000000000000000000000000000000000000000000010000"

    # EXPECTED output string
    expected_output = (
        "20@|@20231123@|@8745593088@|@0@|@0@|@0@|@6@|@ACP01~|~0~|~23-Nov-2023~|~237~|~6~|~0~|~0~|~222640~|~1769~|~15877420~|~0~|~0~|~0~|~0~|~204~|~23-Nov-2023 16:15:40~|~155658494~|~28239~|~0~|~1~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~5~|~0~|~~|~0~|~0~|~155~|~95~|~IOSBS~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~~|~0~|~5353278018~|~0~|~2023-11-23 00:00:00~|~5~|~5~|~0~|~300000~|~6000~|~23-Nov-2023 16:15:40~|~QPL~|~ ~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~0~|~2~|~1~|~0~|~0~|~0~|~0~|~2*14>05+10~|~1~|~0~|~0~|~4000~|~0420~|~0000~|~0000~|~0000~|~0000~|~0~|~0~|~2~|~0~|~0"
    )

    header_fields_count_matched = False
    value_fields_count_matched = False
    header_fields_matching = 0
    header_fields_not_matching = 0
    hdr_fields_matching = []
    hdr_fields_not_matching = []
    value_fields_matching = 0
    value_fields_not_matching = 0
    val_fields_matching = []
    val_fields_not_matching = []

    # Assume this is your method under test
    actual_output = fetch_result(input_data)
    header_fields_count = 7
    delimiter = "@|@"
    sub_delimiter = "~|~"

    expected_parts = expected_output.split(delimiter)
    actual_parts = actual_output.split(delimiter)
    errors = []
    try:
        assert len(expected_parts) == len(actual_parts), (
            f"Mismatch in total number of fields: expected {len(expected_parts)}, got {len(actual_parts)}"
        )
        header_fields_count_matched = True
    except AssertionError as e:
            print(f"Assertion failed: {e}")
            errors.append(str(e))

    # Split header and value fields
    expected_header = expected_parts[:header_fields_count]
    actual_header = actual_parts[:header_fields_count]

        # 1. Check Header Fields
    min_len = min(len(expected_header), len(actual_header))
    for i in range(min_len):
        try:
            if '~|~' in expected_header[i]:
                 expected_hdr = expected_header[i].split('~|~')[0]
            else:
                 expected_hdr = expected_header[i]
            if '~|~' in actual_header[i]:
                 actual_hdr = actual_header[i].split('~|~')[0]
            else:
                 actual_hdr = actual_header[i]

            assert expected_hdr == actual_hdr, (
                f"Header field '{header_fields[i]}' mismatch: expected '{expected_hdr}', got '{actual_hdr}'"
            )
            header_fields_matching = header_fields_matching + 1
            hdr_fields_matching.append(header_fields[i])
        except AssertionError as e:
                print(f"Assertion failed: {e}")
                errors.append(str(e))
                header_fields_not_matching = header_fields_not_matching + 1
                hdr_fields_not_matching.append(header_fields[i])
    expected_value_parts = expected_output.split(sub_delimiter)
    actual_value_parts = actual_output.split(sub_delimiter)
    try:
        assert len(expected_value_parts) == len(actual_value_parts), (
            f"Mismatch in total number of value fields: expected {len(expected_value_parts)}, got {len(actual_value_parts)}"
        )
        value_fields_count_matched = True
    except AssertionError as e:
            print(f"Assertion failed: {e}")
            errors.append(str(e))
    
    # Split header and value fields
    expected_value = expected_value_parts
    actual_value = actual_value_parts

        # 1. Check Header Fields
    min_len_value = min(len(expected_value), len(actual_value))
    
    for i in range(min_len_value):
        try:
            if '@|@' in expected_value[i]:
                 expected_val = expected_value[i].split('@|@')[len(expected_value[i].split('@|@'))-1]
            else:
                 expected_val = expected_value[i]
            if '@|@' in actual_value[i]:
                 actual_val = actual_value[i].split('~|~')[0]
            else:
                 actual_val = actual_value[i].split('@|@')[len(actual_value[i].split('@|@'))-1]

            assert expected_val == actual_val, (
                f"Value field '{value_fields[i]}' mismatch: expected '{expected_val}', got '{actual_val}'"
            )
            value_fields_matching = value_fields_matching + 1
            val_fields_matching.append(value_fields[i])
        except AssertionError as e:
                print(f"Assertion failed: {e}")
                errors.append(str(e))
                value_fields_not_matching = value_fields_not_matching + 1
                val_fields_not_matching.append(value_fields[i])
    
    print(f"""
    header_fields_count_matched = {header_fields_count_matched}
    value_fields_count_matched = {value_fields_count_matched}
    header_fields_matching = {header_fields_matching}
    hdr_fields_matching = {hdr_fields_matching}
    header_fields_not_matching = {header_fields_not_matching}
    hdr_fields_not_matching = {hdr_fields_not_matching}
    value_fields_matching = {value_fields_matching}
    val_fields_matching = {val_fields_matching}
    value_fields_not_matching = {value_fields_not_matching}
    val_fields_not_matching = {val_fields_not_matching}""")
    if errors:
        raise AssertionError(f"\n{len(errors)} assertions failed:\n" + "\n".join(errors))
        