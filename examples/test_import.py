#!/usr/bin/env python3
"""
Test script to verify ab_race_translator installation and basic functionality.
"""

def test_import():
    """Test package import."""
    try:
        import ab_race_translator
        print("✅ ab_race_translator imported successfully")
        
        from ab_race_translator import create_ab_race, Msg
        print("✅ Main classes imported successfully")
        
        # Test translator creation
        translator = create_ab_race()
        print("✅ Translator created successfully")
        
        # Test with sample data
        from ab_race_translator.data_structures import create_sample_msg
        msg = create_sample_msg()
        print("✅ Sample message created successfully")
        
        # Test translation
        result = translator.translate_action(msg)
        print(f"✅ Translation successful: {len(result)} characters")
        
        print("\n🎉 All tests passed! Package is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_import()
