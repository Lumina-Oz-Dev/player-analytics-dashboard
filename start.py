#!/usr/bin/env python3
"""
Smart Launcher for Player Analytics Dashboard
Automatically detects available configuration and runs appropriate version
"""

import os
import sys
import subprocess
from pathlib import Path

def check_google_cloud_credentials():
    """Check if Google Cloud credentials are available"""
    # Check for service account file
    creds_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_file and os.path.exists(creds_file):
        return True, f"Found credentials file: {creds_file}"
    
    # Check for gcloud default credentials
    try:
        result = subprocess.run(['gcloud', 'auth', 'list', '--filter=status:ACTIVE'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            return True, "Found gcloud default credentials"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return False, "No Google Cloud credentials found"

def check_local_setup():
    """Check if local SQLite setup is available"""
    required_files = [
        'app_standalone.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        return False, f"Missing local files: {', '.join(missing_files)}"
    
    return True, "Local setup available"

def check_local_dependencies():
    """Check if local dependencies are installed"""
    try:
        import flask
        import flask_cors
        return True, "Local dependencies available"
    except ImportError as e:
        return False, f"Missing dependencies: {e}. Run: pip install flask flask-cors python-dotenv"

def run_cloud_version():
    """Run the cloud version with Firestore"""
    print("☁️  Starting Cloud Version (Firestore)")
    print("=" * 40)
    try:
        # Set environment to use original app
        os.environ['FLASK_APP'] = 'app.py'
        subprocess.run([sys.executable, 'app.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting cloud version: {e}")
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def run_local_version():
    """Run the local version with SQLite"""
    print("💻 Starting Local Version (SQLite)")
    print("=" * 40)
    
    # Check local dependencies first
    deps_ok, deps_msg = check_local_dependencies()
    if not deps_ok:
        print(f"❌ {deps_msg}")
        return
    
    try:
        # Set environment to use standalone app
        os.environ['FLASK_APP'] = 'app_standalone.py'
        subprocess.run([sys.executable, 'app_standalone.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting local version: {e}")
        print("💡 Try running: pip install flask flask-cors python-dotenv")
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def show_menu():
    """Show configuration menu"""
    print("🏀 Player Analytics Dashboard - Configuration")
    print("=" * 50)
    
    # Check configurations
    has_cloud, cloud_msg = check_google_cloud_credentials()
    has_local, local_msg = check_local_setup()
    has_local_deps, local_deps_msg = check_local_dependencies()
    
    print(f"☁️  Cloud Setup: {'✅' if has_cloud else '❌'} {cloud_msg}")
    print(f"💻 Local Setup: {'✅' if has_local else '❌'} {local_msg}")
    print(f"📦 Local Dependencies: {'✅' if has_local_deps else '❌'} {local_deps_msg}")
    print()
    
    if has_cloud and has_local and has_local_deps:
        print("Both configurations available. Choose your preference:")
        print("1. Run with Google Cloud Firestore (recommended for production)")
        print("2. Run with local SQLite database (recommended for development)")
        print("3. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice == '1':
                run_cloud_version()
                break
            elif choice == '2':
                run_local_version()
                break
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    elif has_cloud and not has_local_deps:
        print("✅ Running with Google Cloud Firestore")
        print("💡 Install local dependencies for development: pip install flask flask-cors python-dotenv")
        input("Press Enter to continue with cloud version...")
        run_cloud_version()
    
    elif has_local and has_local_deps:
        print("✅ Running with local SQLite database")
        if not has_cloud:
            print("💡 For production: Set up Google Cloud credentials")
        input("Press Enter to continue with local version...")
        run_local_version()
    
    elif has_local and not has_local_deps:
        print("❌ Local dependencies missing!")
        print("Run this command to install:")
        print("pip install flask flask-cors python-dotenv")
        
    else:
        print("❌ No valid configuration found!")
        print("\nTo set up:")
        print("• For cloud: Set GOOGLE_APPLICATION_CREDENTIALS or run 'gcloud auth login'")
        print("• For local: Run 'pip install flask flask-cors python-dotenv'")

def main():
    """Main launcher function"""
    # Quick check for direct arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['cloud', 'firestore']:
            run_cloud_version()
            return
        elif arg in ['local', 'sqlite']:
            run_local_version()
            return
        elif arg in ['help', '-h', '--help']:
            print("Usage: python start.py [cloud|local|help]")
            print("  cloud/firestore: Force cloud version")
            print("  local/sqlite: Force local version")
            print("  help: Show this message")
            return
    
    # Interactive menu
    show_menu()

if __name__ == "__main__":
    main()