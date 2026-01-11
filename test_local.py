"""
Quick test script to verify your environment variables are set correctly
Run this before deploying to Cloudflare
"""
import os
import sys

def test_environment():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment variables...\n")
    
    required_vars = {
        'CF_ACCOUNT_ID': 'Cloudflare Account ID',
        'CF_API_TOKEN': 'Cloudflare API Token',
        'WEATHER_API_KEY': 'Weather API Key (OpenWeatherMap)'
    }
    
    all_set = True
    
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Show partial value for security
            masked = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '***'
            print(f"✅ {var}: {masked}")
            print(f"   ({description})")
        else:
            print(f"❌ {var}: NOT SET")
            print(f"   ({description})")
            all_set = False
        print()
    
    if all_set:
        print("✨ All environment variables are set!")
        print("\nYou can now run the application with:")
        print("   python app.py")
        return True
    else:
        print("⚠️  Some environment variables are missing.")
        print("\nTo set them (Windows PowerShell):")
        print('   $env:CF_ACCOUNT_ID="your-value"')
        print('   $env:CF_API_TOKEN="your-value"')
        print('   $env:WEATHER_API_KEY="your-value"')
        print("\nTo set them (Linux/Mac):")
        print('   export CF_ACCOUNT_ID="your-value"')
        print('   export CF_API_TOKEN="your-value"')
        print('   export WEATHER_API_KEY="your-value"')
        return False

if __name__ == '__main__':
    success = test_environment()
    sys.exit(0 if success else 1)
