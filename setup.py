#!/usr/bin/env python3
"""
Enhanced Scrapy-AI-Contact-Finder Setup Script
Automates installation and initial configuration
"""

import os
import sys
import subprocess
import platform

def run_command(command, check=True):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return None

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        run_command(f"{sys.executable} -m pip install -r requirements.txt")
        print("✅ Dependencies installed successfully")
    else:
        print("❌ requirements.txt not found")
        print("Installing core dependencies manually...")
        
        core_deps = [
            "streamlit>=1.28.0",
            "requests>=2.31.0",
            "pandas>=2.0.0",
            "validators>=0.22.0",
            "python-dotenv>=1.0.0",
            "openpyxl>=3.1.0",
            "whois>=0.9.27",
            "beautifulsoup4>=4.12.0"
        ]
        
        for dep in core_deps:
            run_command(f"{sys.executable} -m pip install {dep}")
        
        print("✅ Core dependencies installed")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        print("📄 Creating .env configuration file...")
        
        env_content = """# Enhanced Scrapy-AI-Contact-Finder Configuration
# Get your API key from https://openrouter.ai/

# OpenRouter API Key (Required)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Default settings
DEFAULT_MODEL=perplexity/llama-3-sonar-large-online
DEFAULT_COUNTRY=Germany
DEFAULT_SEARCH_METHODS=AI Research,WHOIS Lookup

# Optional: Advanced settings
MAX_BATCH_SIZE=100
REQUEST_TIMEOUT=120
RATE_LIMIT_DELAY=1
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ .env file created")
        print("🔐 Please edit .env file and add your OpenRouter API key")
    else:
        print("✅ .env file already exists")

def create_sample_csv():
    """Create sample CSV for batch processing"""
    if not os.path.exists("sample_companies.csv"):
        print("📊 Creating sample CSV file...")
        
        csv_content = """company,website,country,industry
BBW Berufsbildungswerk Hamburg,bbw.de,Germany,Education
Microsoft Corporation,microsoft.com,USA,Technology
SAP SE,sap.com,Germany,Software
Siemens AG,siemens.com,Germany,Manufacturing
Tesla Inc,tesla.com,USA,Automotive
"""
        
        with open("sample_companies.csv", "w") as f:
            f.write(csv_content)
        
        print("✅ Sample CSV created: sample_companies.csv")

def check_streamlit():
    """Check if Streamlit is working"""
    print("🔧 Testing Streamlit installation...")
    result = run_command("streamlit --version", check=False)
    if result:
        print(f"✅ Streamlit version: {result}")
        return True
    else:
        print("❌ Streamlit test failed")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print()
    print("📝 NEXT STEPS:")
    print()
    print("1. 🔐 Get OpenRouter API Key:")
    print("   - Visit: https://openrouter.ai/")
    print("   - Sign up for an account")
    print("   - Generate an API key")
    print("   - Add credits to your account")
    print()
    print("2. ⚙️ Configure your API key:")
    print("   - Edit the .env file")
    print("   - Replace 'your_openrouter_api_key_here' with your actual key")
    print()
    print("3. 🚀 Run the application:")
    print("   streamlit run scrapy_email_finder.py")
    print()
    print("4. 📊 For batch processing:")
    print("   - Use sample_companies.csv as a template")
    print("   - Add your companies and upload via the web interface")
    print()
    print("💡 TIPS:")
    print("   - Use Web Search models for best results")
    print("   - Start with single company searches to test")
    print("   - Check the README.md for detailed instructions")
    print()
    print("🆘 NEED HELP?")
    print("   - Check README.md for troubleshooting")
    print("   - Verify your API key has sufficient credits")
    print("   - Test with the sample companies first")
    print()

def main():
    """Main setup function"""
    print("🔍 Enhanced Scrapy-AI-Contact-Finder Setup")
    print("="*50)
    print()
    
    # Check system compatibility
    print("🔍 Checking system compatibility...")
    check_python_version()
    
    print(f"💻 Operating System: {platform.system()} {platform.release()}")
    print()
    
    # Install dependencies
    install_requirements()
    print()
    
    # Create configuration files
    create_env_file()
    create_sample_csv()
    print()
    
    # Test installation
    if check_streamlit():
        print("✅ Installation verification passed")
    else:
        print("⚠️ Installation verification failed - but you can still try running the app")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        print("Please check the error message and try again")
        sys.exit(1)
