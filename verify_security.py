"""
Security Setup Verification Script
This script checks if your YouTube Bot is configured securely.
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    print("🔍 Checking .env file...")
    
    if not env_example_path.exists():
        print("  ❌ .env.example not found!")
        return False
    else:
        print("  ✅ .env.example exists")
    
    if not env_path.exists():
        print("  ❌ .env file not found!")
        print("  💡 Create it with: copy .env.example .env")
        return False
    else:
        print("  ✅ .env file exists")
    
    # Check if .env has the token
    with open(env_path, 'r') as f:
        content = f.read()
        if 'TELEGRAM_BOT_TOKEN=' in content:
            if 'your_token_here' in content or 'your_actual_token_here' in content:
                print("  ⚠️  .env file has placeholder token - please update it!")
                return False
            else:
                print("  ✅ TELEGRAM_BOT_TOKEN is set")
                return True
        else:
            print("  ❌ TELEGRAM_BOT_TOKEN not found in .env")
            return False

def check_gitignore():
    """Check if .env is in .gitignore"""
    gitignore_path = Path('.gitignore')
    
    print("\n🔍 Checking .gitignore...")
    
    if not gitignore_path.exists():
        print("  ⚠️  .gitignore not found")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
        if '.env' in content:
            print("  ✅ .env is gitignored")
            return True
        else:
            print("  ❌ .env is NOT gitignored!")
            return False

def check_python_dotenv():
    """Check if python-dotenv is installed"""
    print("\n🔍 Checking python-dotenv...")
    
    try:
        import dotenv
        print("  ✅ python-dotenv is installed")
        return True
    except ImportError:
        print("  ❌ python-dotenv not installed")
        print("  💡 Install with: pip install python-dotenv")
        return False

def check_no_hardcoded_tokens():
    """Check that no tokens are hardcoded in scripts"""
    print("\n🔍 Checking for hardcoded tokens in scripts...")
    
    files_to_check = ['run.bat', 'run_agent.bat', 'run_agent.sh']
    token_pattern = r'[0-9]{10}:AA[A-Za-z0-9_-]{33}'
    
    import re
    found_tokens = []
    
    for filename in files_to_check:
        filepath = Path(filename)
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Check for uncommented tokens
                for line in content.split('\n'):
                    if not line.strip().startswith(('REM', '#', '//')):
                        if re.search(token_pattern, line):
                            found_tokens.append(filename)
                            break
    
    if found_tokens:
        print(f"  ❌ Found hardcoded tokens in: {', '.join(found_tokens)}")
        return False
    else:
        print("  ✅ No hardcoded tokens found in scripts")
        return True

def check_config_file():
    """Check if config.yaml exists"""
    print("\n🔍 Checking config.yaml...")
    
    config_path = Path('config.yaml')
    config_example_path = Path('config.example.yaml')
    
    if not config_example_path.exists():
        print("  ⚠️  config.example.yaml not found")
    else:
        print("  ✅ config.example.yaml exists")
    
    if not config_path.exists():
        print("  ⚠️  config.yaml not found")
        print("  💡 Create it with: copy config.example.yaml config.yaml")
        return False
    else:
        print("  ✅ config.yaml exists")
        return True

def main():
    print("=" * 60)
    print("🔐 YouTube Bot Security Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        check_env_file(),
        check_gitignore(),
        check_python_dotenv(),
        check_no_hardcoded_tokens(),
        check_config_file()
    ]
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ All checks passed! ({passed}/{total})")
        print("\n🎉 Your setup is secure and ready to use!")
        print("\n💡 Next step: Run the agent with:")
        print("   python -m yt_agent.cli --config config.yaml")
    else:
        print(f"⚠️  {total - passed} check(s) failed ({passed}/{total} passed)")
        print("\n💡 Please fix the issues above before running the agent.")
    
    print("\n" + "=" * 60)
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
