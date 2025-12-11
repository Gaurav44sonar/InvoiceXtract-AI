"""
MODULE 1: Basic FastAPI Server
================================
This is the entry point of our Invoice OCR application.
Think of this as the main() function in ML - it starts everything.

What this does:
1. Creates a FastAPI application
2. Sets up basic routes (endpoints)
3. Configures CORS (allows frontend to connect)
4. Runs the server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI application instance
# This is like creating a model in ML - it's the main object
app = FastAPI(
    title="Invoice OCR System",
    description="Automated invoice data extraction using OCR and AI",
    version="1.0.0"
)

# Configure CORS - allows frontend (React) to talk to backend
# Think of this as removing barriers between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)


# ============================================
# TEST ENDPOINTS (to verify server is working)
# ============================================

@app.get("/")
async def root():
    """
    Root endpoint - Home page
    Like a welcome message when you visit the website
    
    Test it: http://localhost:8000/
    """
    return {
        "message": "Welcome to Invoice OCR System! 🚀",
        "status": "Server is running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "test": "/test"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint - verifies server is alive
    Like checking if your model is loaded and ready
    
    Test it: http://localhost:8000/health
    """
    return {
        "status": "healthy",
        "message": "Server is running perfectly! ✅"
    }


@app.get("/test")
async def test_endpoint():
    """
    Test endpoint - for debugging
    Returns sample invoice data to test frontend display
    
    Test it: http://localhost:8000/test
    """
    sample_invoice = {
        "invoice_number": "INV-2024-001",
        "invoice_date": "2024-01-15",
        "vendor_name": "Tech Solutions Pvt Ltd",
        "total_amount": 15000.00,
        "gst_amount": 2700.00,
        "grand_total": 17700.00,
        "items": [
            {
                "name": "Laptop",
                "quantity": 1,
                "unit_price": 45000.00,
                "total": 45000.00
            },
            {
                "name": "Mouse",
                "quantity": 2,
                "unit_price": 500.00,
                "total": 1000.00
            }
        ]
    }
    
    return {
        "status": "success",
        "message": "This is sample invoice data",
        "data": sample_invoice
    }


# ============================================
# SERVER STARTUP
# ============================================

if __name__ == "__main__":
    """
    This runs when you execute: python app/main.py
    Like running train.py in ML projects
    """
    print("=" * 50)
    print("🚀 Starting Invoice OCR Server...")
    print("=" * 50)
    print("📍 Server URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("=" * 50)
    print()
    
    # Run the server
    uvicorn.run(
        # app,
        "app.main:app",
        host="0.0.0.0",  # Makes server accessible from other devices
        port=8000,       # Port number
        reload=True      # Auto-reload on code changes (like hot-reload)
    )