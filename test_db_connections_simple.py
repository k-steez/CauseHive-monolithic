#!/usr/bin/env python3
"""
Simple database connection validation without actual network testing
"""
import os
from urllib.parse import urlparse
from pathlib import Path

try:
    import environ
    env = environ.Env()
    env_file = Path(__file__).parent / ".env"
    environ.Env.read_env(str(env_file))
    
    def get_env(key, default=''):
        return env(key, default=default)
except ImportError:
    def get_env(key, default=''):
        return os.environ.get(key, default)

def validate_connection_string(connection_string):
    """Validate connection string format without connecting"""
    try:
        parsed = urlparse(connection_string)
        
        # Check required components
        if not parsed.scheme or parsed.scheme != 'postgresql':
            return False, "Must start with 'postgresql://'"
        
        if not parsed.hostname:
            return False, "Missing hostname"
        
        if not parsed.username:
            return False, "Missing username"
        
        if not parsed.password:
            return False, "Missing password"
        
        if not parsed.path or parsed.path == '/':
            return False, "Missing database name"
        
        if 'your-password' in connection_string or 'your-project-ref' in connection_string:
            return False, "Contains placeholder values"
        
        return True, f"Valid format - Host: {parsed.hostname}, DB: {parsed.path.lstrip('/')}"
        
    except Exception as e:
        return False, f"Invalid format: {e}"

def main():
    print("🔍 Validating Supabase Connection String Format")
    print("=" * 50)
    print("Note: Skipping actual network connection due to IPv6 connectivity issues")
    print("This validation ensures your connection strings are properly formatted for Railway deployment.")
    print()
    
    connection_strings = [
        ('User Service (default)', get_env('USER_SERVICE_DATABASE_URL', '')),
        ('Cause Service', get_env('CAUSE_SERVICE_DATABASE_URL', '')),
        ('Donation Service', get_env('DONATION_SERVICE_DATABASE_URL', '')),
        ('Admin Service', get_env('ADMIN_SERVICE_DATABASE_URL', '')),
    ]
    
    all_valid = True
    
    for name, url in connection_strings:
        print(f"🔗 Validating {name}...")
        
        if not url:
            print("   ❌ Connection string not set in .env file")
            all_valid = False
            continue
        
        valid, message = validate_connection_string(url)
        
        if valid:
            print(f"   ✅ {message}")
        else:
            print(f"   ❌ {message}")
            all_valid = False
    
    print(f"\n{'='*50}")
    if all_valid:
        print("🎉 All connection strings are properly formatted!")
        print("✅ Ready for Railway deployment")
        print("\n💡 Note: Actual database connectivity will be tested during Railway deployment")
    else:
        print("⚠️  Some connection strings need fixing")
        print("📝 Please update your .env file with valid Supabase connection strings")
    
    return all_valid

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
