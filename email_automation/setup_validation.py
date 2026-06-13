"""
Setup and Test Validation Script
Verifies the email automation system is properly configured and working.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_file_structure():
    """Check if all required files exist."""
    print("\n" + "=" * 60)
    print("Checking File Structure...".center(60))
    print("=" * 60)
    
    required_files = [
        'email_sender.py',
        'main.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'config/settings.py',
        'utils/validators.py',
        'utils/logger.py',
        'utils/exceptions.py',
        'examples/single_email.py',
        'examples/bulk_email.py',
        'examples/email_with_attachment.py',
        'examples/html_email.py',
    ]
    
    all_exist = True
    for file in required_files:
        filepath = os.path.join(os.path.dirname(__file__), file)
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if required Python packages are installed."""
    print("\n" + "=" * 60)
    print("Checking Dependencies...".center(60))
    print("=" * 60)
    
    required_packages = ['dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (not installed)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_configuration():
    """Check if .env file is configured."""
    print("\n" + "=" * 60)
    print("Checking Configuration...".center(60))
    print("=" * 60)
    
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file):
        print("✗ .env file not found")
        print("  Create from .env.example: copy .env.example .env")
        return False
    
    print("✓ .env file exists")
    
    # Check configuration
    try:
        from config.settings import EmailConfig
        
        required_fields = ['SENDER_EMAIL', 'SENDER_PASSWORD']
        missing_fields = []
        
        for field in required_fields:
            value = getattr(EmailConfig, field, None)
            if not value or value.startswith('your_'):
                missing_fields.append(field)
                print(f"⚠ {field}: Not configured (placeholder value)")
            else:
                print(f"✓ {field}: Configured")
        
        if missing_fields:
            print(f"\n⚠ Missing configuration: {', '.join(missing_fields)}")
            print("  Edit .env file and fill in your SMTP credentials")
            return False
        
        return True
    
    except Exception as e:
        print(f"✗ Error checking configuration: {e}")
        return False

def check_imports():
    """Check if all imports work correctly."""
    print("\n" + "=" * 60)
    print("Checking Imports...".center(60))
    print("=" * 60)
    
    modules = [
        'config.settings',
        'utils.validators',
        'utils.logger',
        'utils.exceptions',
        'email_sender',
    ]
    
    all_import = True
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except Exception as e:
            print(f"✗ {module}: {str(e)}")
            all_import = False
    
    return all_import

def run_validation():
    """Run all validation checks."""
    print("\n" + "#" * 60)
    print("  EMAIL AUTOMATION SYSTEM - SETUP VALIDATION".center(60))
    print("#" * 60)
    
    results = {
        'Files': check_file_structure(),
        'Dependencies': check_dependencies(),
        'Imports': check_imports(),
        'Configuration': check_configuration(),
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY".center(60))
    print("=" * 60)
    
    all_pass = True
    for check, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check}")
        if not result:
            all_pass = False
    
    print("=" * 60)
    
    if all_pass:
        print("\n✓ All checks passed! System is ready to use.\n")
        print("Next steps:")
        print("1. Run: python main.py           (Interactive CLI)")
        print("2. Or: python examples/single_email.py   (Test example)")
        print("3. Or: python examples/bulk_email.py     (Bulk example)")
        print("")
    else:
        print("\n✗ Some checks failed. Please address the issues above.")
        print("")
    
    return all_pass

if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
