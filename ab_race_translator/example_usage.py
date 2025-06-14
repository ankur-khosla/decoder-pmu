"""
Example Usage for AB Race Translator

Demonstrates how to use the ab_race_translator package to process racing messages.
"""

import time
import os
from ab_race_translator import create_ab_race, Msg
from ab_race_translator.data_structures import create_sample_msg


def basic_usage_example():
    """
    Basic usage example showing how to translate a racing message.
    """
    print("=== Basic Usage Example ===")
    
    # Create a race translator instance
    translator = create_ab_race()
    
    # Create a sample racing message
    sample_data = b'\x00' * 200  # Sample binary data
    
    msg = Msg(
        m_cpBuf=sample_data,
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
    
    print(f"Original message size: {len(msg.m_cpBuf)} bytes")
    print(f"Translated result: {result[:200]}...")  # Show first 200 chars
    print(f"Result length: {len(result)} characters")
    
    return result


def win_bet_example():
    """
    Example for WIN bet translation.
    """
    print("\n=== WIN Bet Example ===")
    
    translator = create_ab_race()
    
    # Create WIN bet message
    msg = create_sample_msg()
    msg.m_iSysName = "AB"
    msg.m_iMsgCode = 6  # Racing bet
    
    result = translator.translate_action(msg)
    
    print(f"WIN bet translation: {result}")
    print("Expected fields: meet_date, location, day, total_pay, unit_bet, cost, sell_time, bet_type, etc.")


def allup_bet_example():
    """
    Example for Allup bet translation.
    """
    print("\n=== Allup Bet Example ===")
    
    translator = create_ab_race()
    
    # Create Allup bet message (simulated)
    msg = create_sample_msg()
    msg.m_iSysName = "AB"
    msg.m_iMsgCode = 6
    
    result = translator.translate_action(msg)
    
    print(f"Allup bet translation: {result}")
    print("Allup bets include formula and multiple event information")


def flexi_bet_example():
    """
    Example for Flexi bet translation with unit bet calculations.
    """
    print("\n=== Flexi Bet Example ===")
    
    translator = create_ab_race()
    
    # Simulate flexi bet processing
    msg = create_sample_msg()
    msg.m_iSysName = "AB"
    
    result = translator.translate_action(msg)
    
    print(f"Flexi bet translation: {result}")
    print("Flexi bets have special unit bet calculations")


def error_handling_example():
    """
    Example showing error handling with invalid data.
    """
    print("\n=== Error Handling Example ===")
    
    translator = create_ab_race()
    
    # Create message with error
    msg = Msg(
        m_cpBuf=b'invalid_data',
        m_iMsgErrwu=1,  # Error flag set
        m_iSysNo=1,
        m_iSysName="AB",
        m_iMsgTime=int(time.time()),
        m_iMsgDay=1,
        m_iMsgMonth=1,
        m_iMsgYear=2024
    )
    
    result = translator.translate_action(msg)
    
    print(f"Error case result: {result}")
    print("Translator handles errors gracefully")


def batch_processing_example():
    """
    Example of processing multiple racing messages in batch.
    """
    print("\n=== Batch Processing Example ===")
    
    translator = create_ab_race()
    
    # Process multiple messages
    messages = []
    for i in range(5):
        msg = create_sample_msg()
        msg.m_iSysName = f"AB{i+1}"
        msg.m_iMsgTime = int(time.time()) + i * 60  # Different times
        messages.append(msg)
    
    results = []
    for i, msg in enumerate(messages):
        result = translator.translate_action(msg)
        results.append(result)
        print(f"Message {i+1} processed: {len(result)} characters")
    
    print(f"Batch processing completed: {len(results)} messages")
    return results


def performance_test():
    """
    Performance test for message translation.
    """
    print("\n=== Performance Test ===")
    
    translator = create_ab_race()
    
    # Create test message
    msg = create_sample_msg()
    
    # Time multiple translations
    start_time = time.time()
    num_iterations = 1000
    
    for _ in range(num_iterations):
        result = translator.translate_action(msg)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"Processed {num_iterations} messages in {elapsed:.3f} seconds")
    print(f"Average time per message: {(elapsed/num_iterations)*1000:.3f} ms")
    print(f"Messages per second: {num_iterations/elapsed:.1f}")


def integration_example():
    """
    Example showing integration with external systems.
    """
    print("\n=== Integration Example ===")
    
    translator = create_ab_race()
    
    def process_message_from_queue(binary_data: bytes, metadata: dict) -> str:
        """Simulate processing message from message queue."""
        msg = Msg(
            m_cpBuf=binary_data,
            m_iMsgErrwu=metadata.get('error', 0),
            m_iSysNo=metadata.get('sys_no', 1),
            m_iSysName=metadata.get('sys_name', 'AB'),
            m_iMsgTime=metadata.get('msg_time', int(time.time())),
            m_iMsgDay=metadata.get('day', 1),
            m_iMsgMonth=metadata.get('month', 1),
            m_iMsgYear=metadata.get('year', 2024)
        )
        
        return translator.translate_action(msg)
    
    # Simulate messages from different sources
    test_messages = [
        (b'\x00' * 150, {'sys_name': 'AB_PROD', 'sys_no': 1}),
        (b'\x01' * 175, {'sys_name': 'AB_UAT', 'sys_no': 2}),
        (b'\x02' * 200, {'sys_name': 'AB_DEV', 'sys_no': 3, 'error': 1})
    ]
    
    for i, (data, metadata) in enumerate(test_messages):
        result = process_message_from_queue(data, metadata)
        print(f"Processed message from {metadata['sys_name']}: {len(result)} chars")
    
    print("Integration example completed")


def custom_configuration_example():
    """
    Example showing custom configuration of the translator.
    """
    print("\n=== Custom Configuration Example ===")
    
    # Create translator with custom settings
    translator = create_ab_race()
    
    # Set custom message order number
    translator.set_msg_key(tape_id=12345, msg_order_no=67890)
    
    # Create message with custom settings
    msg = create_sample_msg()
    msg.m_iSysName = "CUSTOM_AB"
    
    result = translator.translate_action(msg)
    
    print(f"Custom configured translation: {result[:100]}...")
    print("Translator configured with custom tape ID and message order")


def field_validation_example():
    """
    Example showing field validation and data quality checks.
    """
    print("\n=== Field Validation Example ===")
    
    translator = create_ab_race()
    
    def validate_translation_result(result: str) -> dict:
        """Validate the translated result."""
        fields = result.split("~|~")  # Split by delimiter
        
        validation_results = {
            'field_count': len(fields),
            'has_meet_date': len(fields) > 50 and fields[50] != "",
            'has_bet_type': len(fields) > 57 and fields[57] != "",
            'has_selections': len(fields) > 75 and fields[75] != "",
            'total_length': len(result)
        }
        
        return validation_results
    
    # Test with sample message
    msg = create_sample_msg()
    result = translator.translate_action(msg)
    validation = validate_translation_result(result)
    
    print("Validation Results:")
    for key, value in validation.items():
        print(f"  {key}: {value}")


def debugging_example():
    """
    Example showing debugging capabilities.
    """
    print("\n=== Debugging Example ===")
    
    translator = create_ab_race()
    
    # Create message for debugging
    msg = create_sample_msg()
    msg.m_iSysName = "DEBUG_AB"
    
    # Show translator state before processing
    print(f"Translator state before: bet_type={translator.m_cBetType}")
    
    result = translator.translate_action(msg)
    
    # Show translator state after processing
    print(f"Translator state after: bet_type={translator.m_cBetType}")
    print(f"Total cost: {translator.m_iTotalCost}")
    print(f"Total pay: {translator.m_itotalPay}")
    print(f"Flexi flag: {translator.m_iFlexiBetFlag}")
    print(f"Result preview: {result[:150]}...")


def file_processing_example():
    """
    Example showing file-based message processing.
    """
    print("\n=== File Processing Example ===")
    
    translator = create_ab_race()
    
    def process_binary_file(file_path: str) -> list:
        """Process binary messages from file."""
        results = []
        
        try:
            # Simulate reading binary file (in real scenario, you'd read actual binary data)
            # For demo, we'll create sample data
            sample_messages = [
                b'\x00' * 180,
                b'\x01' * 190, 
                b'\x02' * 200
            ]
            
            for i, binary_data in enumerate(sample_messages):
                msg = Msg(
                    m_cpBuf=binary_data,
                    m_iMsgErrwu=0,
                    m_iSysNo=1,
                    m_iSysName="FILE_AB",
                    m_iMsgTime=int(time.time()),
                    m_iMsgDay=1,
                    m_iMsgMonth=6,
                    m_iMsgYear=2024,
                    m_iMsgCode=6
                )
                
                result = translator.translate_action(msg)
                results.append(result)
                print(f"Processed message {i+1} from file: {len(result)} chars")
            
        except Exception as e:
            print(f"Error processing file: {e}")
        
        return results
    
    # Process sample file
    results = process_binary_file("sample_messages.bin")
    print(f"File processing completed: {len(results)} messages processed")


def main():
    """
    Main function to run all examples.
    """
    print("AB Race Translator - Example Usage")
    print("=" * 50)
    
    try:
        # Run all examples
        basic_usage_example()
        win_bet_example()
        allup_bet_example()
        flexi_bet_example()
        error_handling_example()
        batch_processing_example()
        performance_test()
        integration_example()
        custom_configuration_example()
        field_validation_example()
        debugging_example()
        file_processing_example()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()