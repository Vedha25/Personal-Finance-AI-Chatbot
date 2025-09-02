#!/usr/bin/env python3
"""
Startup script for Finance Tracker Application
"""

import uvicorn
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("🚀 Starting Finance Tracker Application...")
    print("📱 Frontend will be available at: http://localhost:8000")
    print("🔧 API documentation at: http://localhost:8000/docs")
    print("💚 Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
