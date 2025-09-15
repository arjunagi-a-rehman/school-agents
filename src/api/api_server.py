"""
School Agents API Server

Simple FastAPI-based REST API for the school agents system.
Provides a single endpoint for interacting with StudyBuddy agent.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import asyncio
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Check if Google API key is available
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Warning: GOOGLE_API_KEY not found in environment variables")
    print("💡 Make sure you have a .env file with GOOGLE_API_KEY set")
else:
    print("✅ Google API key loaded successfully")

# Import the StudyBuddy agent
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agents.studdy_buddy.agent import root_agent

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Simple Request Model
class QueryRequest(BaseModel):
    """Request model for querying the StudyBuddy agent"""
    query: str  # Only mandatory field
    session_id: Optional[str] = None  # Optional - for session continuation
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "query": "Can you help me solve this quadratic equation: x² + 5x + 6 = 0?"
                },
                {
                    "query": "Explain photosynthesis in simple terms",
                    "session_id": "session_123"
                }
            ]
        }

# Create FastAPI app
app = FastAPI(
    title="School Agents API",
    description="Simple API for interacting with StudyBuddy agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the StudyBuddy agent runner
runner = Runner(
    app_name="School Agents API",
    agent=root_agent,
    session_service=InMemorySessionService()
)

@app.post("/query", 
          summary="Query StudyBuddy Agent",
          description="Send a query to the StudyBuddy AI agent and get educational assistance.",
          response_description="Complete agent response with session information")
@limiter.limit("25/day")
async def process_query(request: Request, query_request: QueryRequest):
    """Process query with StudyBuddy agent"""
    
    # Proper session management for context continuity
    # Use single consistent user_id for all students since this is educational API
    user_id = "student"
    
    if not query_request.session_id:
        # First request - create new session and return session_id for future requests
        session = await runner.session_service.create_session(
            app_name="School Agents API",
            user_id=user_id,
            state={}
        )
        session_id = session.id
        is_new_session = True
    else:
        # User provided session_id - check if it exists before using it
        try:
            # Check if session exists by trying to get it
            existing_session = await runner.session_service.get_session(
                app_name="School Agents API",
                user_id=user_id,
                session_id=query_request.session_id
            )
            if existing_session:
                session_id = query_request.session_id
                is_new_session = False
            else:
                raise ValueError("Session returned None")
        except Exception as e:
            # Session doesn't exist, create new one
            print(f"Session {query_request.session_id} not found, creating new one")
            session = await runner.session_service.create_session(
                app_name="School Agents API",
                user_id=user_id,
                state={}
            )
            session_id = session.id
            is_new_session = True
    
    # Create message content
    message = types.Content(
        role='user',
        parts=[types.Part.from_text(text=query_request.query)]
    )
    
    # Collect all events from the StudyBuddy agent
    response_parts = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text is not None:
                    response_parts.append(str(part.text))
    
    # Filter and join response
    response_parts = [part for part in response_parts if part and part.strip()]
    response_text = " ".join(response_parts) if response_parts else "I'm ready to help with your studies! Please ask me any question."
    
    return {
        "response": response_text,
        "session_id": session_id,
        "new_session": is_new_session,
        "message": "Use this session_id in your next request to maintain conversation context" if is_new_session else "Continuing conversation with existing context"
    }

# Root endpoint - serve chat UI
@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    """Serve the StudyBuddy chat interface"""
    try:
        # Get the path to the HTML template
        template_path = Path(__file__).parent / "templates" / "index.html"
        
        # Read and return the HTML content
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        # Fallback API info if template not found
        return HTMLResponse(
            content="""
            <html>
                <head><title>StudyBuddy API</title></head>
                <body>
                    <h1>StudyBuddy API</h1>
                    <p>Chat interface template not found.</p>
                    <p><a href="/docs">View API Documentation</a></p>
                </body>
            </html>
            """,
            status_code=200
        )

# API info endpoint
@app.get("/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "School Agents API",
        "version": "1.0.0", 
        "description": "Simple API for interacting with StudyBuddy agent",
        "agent": "StudyBuddy - Your AI Learning Companion",
        "docs": "/docs",
        "endpoints": {
            "chat": "/ - StudyBuddy chat interface",
            "query": "/query - Main API endpoint to interact with StudyBuddy",
            "health": "/health - Health check",
            "info": "/info - This endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "StudyBuddy"}

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8080))
    
    print("🎓 Starting School Agents API with StudyBuddy")
    print(f"🚀 Server running on port {port}")
    print(f"💬 Chat Interface: http://localhost:{port}/")
    print(f"📖 API Documentation: http://localhost:{port}/docs")
    print(f"🤖 Agent: StudyBuddy - Your AI Learning Companion")
    print(f"🔗 API Endpoint: http://localhost:{port}/query")
    print(f"⚡ Rate Limit: 50 requests per day per IP")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
