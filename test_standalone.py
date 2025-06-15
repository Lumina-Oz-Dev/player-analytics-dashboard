#!/usr/bin/env python3
"""
Test the standalone app
"""

print("🔍 Testing standalone app...")

# Test imports
try:
    import flask
    print("✅ Flask available")
except ImportError:
    print("❌ Flask not available - run: pip install flask flask-cors")
    exit(1)

try:
    import flask_cors
    print("✅ Flask-CORS available")
except ImportError:
    print("❌ Flask-CORS not available - run: pip install flask-cors")
    exit(1)

print("🎉 All dependencies available!")
print("🚀 You can now run: python app_standalone.py")