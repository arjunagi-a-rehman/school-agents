# Deploying Your StudyBuddy Agent: From Code to Production

Previously, we used tool calls to equip our Study Buddy agent with the right capabilities. Now we'll look at how to deploy it so it's accessible to the world through a REST API.

## Deployment Approaches

There are two common ways to achieve this:
1. **Google ADK–supported**: Leverage AI Engine, Cloud Run, or GKE (Google Kubernetes Engine)
2. **Custom FastAPI Deployment**: Build your own REST API wrapper

For Google ADK–supported deployment, please refer to the official docs: https://google.github.io/adk-docs/deploy/

In this section, I'll demonstrate our **custom FastAPI deployment** with detailed implementation.

## Our Custom API Implementation

We've built a complete REST API that wraps our StudyBuddy agent with proper session management. Let's dive deep into how it works.

### 🏗️ API Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│    Runner       │───▶│  StudyBuddy     │
│                 │    │                 │    │     Agent       │
├─────────────────┤    ├─────────────────┤    └─────────────────┘
│ Session Mgmt    │    │ Event Handling  │
│ Request/Response│    │ Message Routing │
└─────────────────┘    └─────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│        InMemorySessionService               │
│  ┌───────────────┬───────────────────────┐  │
│  │   user_id     │      Sessions         │  │
│  │   "student"   │ [session1, session2] │  │
│  └───────────────┴───────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 📁 Project Structure

```
src/api/
├── __init__.py          # Package exports
└── api_server.py        # Main FastAPI application
```

## 🧠 Core Components Explained

### 1. The Runner: Your Agent's Orchestra Conductor

The **Runner** is the central component that manages the execution of your StudyBuddy agent. Think of it as an orchestra conductor that coordinates between the API requests and the AI agent.

```python
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

# Initialize the StudyBuddy agent runner
runner = Runner(
    app_name="School Agents API",
    agent=root_agent,  # Our StudyBuddy agent
    session_service=InMemorySessionService()
)
```

**What the Runner does:**
- **Message Routing**: Takes your text queries and converts them to the format the agent expects
- **Event Handling**: Manages the async stream of responses from the AI model
- **Session Coordination**: Works with the session service to maintain conversation context
- **Error Management**: Handles failures gracefully and provides meaningful responses

### 2. Session Management: The Memory of Your AI

Session management is crucial for maintaining conversation context. Without it, every interaction would be like meeting the AI for the first time.

#### **Session Components:**

```python
class QueryRequest(BaseModel):
    query: str                          # The student's question
    session_id: Optional[str] = None    # For continuing conversations

# Our session management logic
user_id = "student"  # Consistent identifier for all students

if not request.session_id:
    # First interaction - create new session
    session = await runner.session_service.create_session(
        app_name="School Agents API",
        user_id=user_id,
        state={}
    )
    session_id = session.id
    is_new_session = True
else:
    # Continuing conversation - use existing session
    try:
        existing_session = await runner.session_service.get_session(
            app_name="School Agents API", 
            user_id=user_id,
            session_id=request.session_id
        )
        if existing_session:
            session_id = request.session_id
            is_new_session = False
    except Exception:
        # Session not found - create new one
        session = await runner.session_service.create_session(
            app_name="School Agents API",
            user_id=user_id, 
            state={}
        )
        session_id = session.id
        is_new_session = True
```

#### **Session Flow Visualization:**

```
First Request (no session_id):
┌─────────────┐    ┌────────────────┐    ┌─────────────┐
│   Student   │───▶│  Create New    │───▶│  Return     │
│ "Hello!"    │    │   Session      │    │ session_id  │
└─────────────┘    └────────────────┘    └─────────────┘

Follow-up Request (with session_id):
┌─────────────┐    ┌────────────────┐    ┌─────────────┐
│   Student   │───▶│  Find Existing │───▶│ Continue    │
│"What's 2+2?"│    │   Session      │    │Conversation │
└─────────────┘    └────────────────┘    └─────────────┘
```

### 3. InMemorySessionService: The Conversation Memory Bank

The `InMemorySessionService` stores all active conversations in memory. It's like the AI's short-term memory.

```python
from google.adk.sessions.in_memory_session_service import InMemorySessionService

session_service = InMemorySessionService()
```

**Key Methods:**
- `create_session()`: Creates a new conversation thread
- `get_session()`: Retrieves an existing conversation  
- `list_sessions()`: Shows all conversations for a user

**Important Note**: Since it's "in-memory", all sessions are lost when the server restarts. For production, you'd want a persistent session store (Redis, Database, etc.).

### 4. User ID vs Session ID: Understanding the Difference

#### **User ID (`user_id`)**
- **Purpose**: Identifies WHO is talking to the AI
- **Scope**: Groups all sessions for a specific user
- **Our Implementation**: `user_id = "student"` (single user for educational API)
- **Persistence**: Consistent across all interactions

#### **Session ID (`session_id`)**  
- **Purpose**: Identifies a SPECIFIC conversation thread
- **Scope**: One continuous conversation
- **Our Implementation**: Generated UUID (e.g., `"a7b72840-4783-404e-89d8-f02c546ed3f5"`)
- **Persistence**: Unique per conversation

#### **Relationship Diagram:**
```
user_id: "student"
├── session_id: "abc-123" → "Math homework help"
├── session_id: "def-456" → "Science questions" 
└── session_id: "ghi-789" → "History discussion"
```

## 🚀 Complete API Implementation

### **FastAPI Application Structure:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables (Google API key, etc.)
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="School Agents API",
    description="Simple API for interacting with StudyBuddy agent",
    version="1.0.0"
)

# Enable CORS for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **The Main Query Endpoint with Rate Limiting:**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/query")
@limiter.limit("50/day")  # Limit to 50 requests per day per IP
async def process_query(request: Request, query_request: QueryRequest):
    """Process query with StudyBuddy agent"""
    
    # Session management (detailed above)
    user_id = "student"
    # ... session logic ...
    
    # Create message for the agent
    message = types.Content(
        role='user',
        parts=[types.Part.from_text(text=query_request.query)]
    )
    
    # Get response from StudyBuddy
    response_parts = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id, 
        new_message=message
    ):
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_parts.append(str(part.text))
    
    # Return formatted response
    response_text = " ".join(response_parts)
    return {
        "response": response_text,
        "session_id": session_id,
        "new_session": is_new_session,
        "message": "Use this session_id in your next request to maintain conversation context" if is_new_session else "Continuing conversation with existing context"
    }
```

### **Rate Limiting Protection:**

We've added rate limiting to prevent API abuse:
- **50 requests per day per IP address** on the `/query` endpoint
- **Automatic blocking** when limit exceeded
- **Clean error responses** when rate limit hit
- **Memory-based tracking** (no external dependencies needed)

**Rate Limiting Features:**
```python
# Different rate limit options you can use:
@limiter.limit("50/day")        # 50 requests per day
@limiter.limit("10/minute")     # 10 requests per minute  
@limiter.limit("100/hour")      # 100 requests per hour
@limiter.limit("5/second")      # 5 requests per second
```

**Add to pyproject.toml:**
```toml
dependencies = [
    # ... other dependencies ...
    "slowapi>=0.1.9",
]
```

## 🔧 Running the API

### **Development Commands:**

```bash
# Direct execution (recommended)
python src/api/api_server.py

# Using uvicorn with auto-reload
uvicorn src.api.api_server:app --host 0.0.0.0 --port 8080 --reload

# Using the package export
uvicorn src.api:app --host 0.0.0.0 --port 8080 --reload
```

### **Testing the Session Management:**

```bash
# First request - establishes session
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, my name is Alice"}'

# Response includes session_id:
# {
#   "response": "Hi Alice! Nice to meet you...",
#   "session_id": "abc-123-def", 
#   "new_session": true
# }

# Follow-up request - maintains context
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is my name?",
    "session_id": "abc-123-def"
  }'

# Response remembers context:
# {
#   "response": "Your name is Alice!",
#   "session_id": "abc-123-def",
#   "new_session": false  
# }
```

## 💬 Building the Chat Interface

While the API is powerful, we need a user-friendly interface for students to interact with StudyBuddy. Let's create a modern chat UI that makes learning feel natural.

### **Why Vanilla HTML/CSS/JS Over React?**

For simple chat interfaces, you **don't need React** or other complex frameworks! Here's why:

**✅ Vanilla JS Advantages:**
- **Zero Build Process**: No webpack, babel, or complicated setup
- **Faster Load Times**: No framework overhead (React bundle ~40KB+ min)
- **Direct Deployment**: Single HTML file works anywhere
- **Easier Debugging**: No framework abstractions to debug
- **Lower Learning Curve**: Basic HTML/CSS/JS skills sufficient

**❌ When You DO Need React:**
- Complex state management across many components
- Large applications with hundreds of interactive elements
- Team already experienced with React ecosystem
- Need for component reusability across multiple pages

**Our Use Case**: A simple chat interface with ~10 interactive elements is perfect for vanilla JavaScript.

### **Server-Side Rendering (SSR) vs Client-Side Rendering**

Our approach uses **Server-Side Rendering** with FastAPI:

#### **Server-Side Rendering (Our Approach):**
```python
@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    # Server sends complete HTML to browser
    return HTMLResponse(content=html_content)
```

**✅ SSR Benefits:**
- **Instant Load**: HTML renders immediately
- **SEO Friendly**: Search engines see complete content
- **Works Without JS**: Basic functionality even if JS disabled
- **Better Performance**: No JS bundle downloading/parsing delay

#### **Client-Side Rendering (React/Vue):**
```javascript
// Browser downloads JS → JS builds DOM → User sees content
ReactDOM.render(<ChatApp />, document.getElementById('root'));
```

**❌ CSR Drawbacks for Simple Apps:**
- **Blank Page First**: User sees nothing until JS loads
- **SEO Issues**: Search engines struggle with JS-generated content
- **Performance Overhead**: Framework + bundling complexity
- **Development Complexity**: Build tools, transpilation, etc.

**Our Choice**: SSR for instant loading + enhanced with client-side JS for interactivity.

### **Frontend Architecture:**

```
┌─────────────────────┐
│    HTML/CSS/JS      │ ← Modern chat interface
│   Chat Interface    │
└─────────┬───────────┘
          │
          ▼ JavaScript fetch()
┌─────────────────────┐
│   FastAPI Server    │ ← Serves HTML + handles API
│                     │
├─────────────────────┤
│  GET /              │ ← Returns chat interface
│  POST /query        │ ← Processes messages  
└─────────────────────┘
```

```javascript
let sessionId = null;

// Add message to chat
function addMessage(content, isUser = false) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    messageDiv.innerHTML = `
        <div class="message-avatar">${isUser ? '👤' : '🎓'}</div>
        <div class="message-content">${content}</div>
    `;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Send message to API
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const query = input.value.trim();
    if (!query) return;

    addMessage(query, true);
    input.value = '';

    try {
        const requestBody = { query };
        if (sessionId) requestBody.session_id = sessionId;

        const response = await fetch('/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();
        if (response.ok) {
            sessionId = data.session_id; // Save for context
            addMessage(data.response);
        }
    } catch (error) {
        addMessage('Sorry, connection error. Please try again.');
    }
}
```

### **Integrating HTML with FastAPI:**

Now we need to serve this HTML file from our FastAPI server. Update the server to handle the root route:

```python
from fastapi.responses import HTMLResponse
from pathlib import Path

# Root endpoint - serve chat UI
@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    """Serve the StudyBuddy chat interface"""
    try:
        template_path = Path(__file__).parent / "templates" / "index.html"
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>StudyBuddy API</h1><p><a href='/docs'>View API Documentation</a></p>",
            status_code=200
        )
```

**💡 Complete Code Available**: The full HTML/CSS/JS implementation with styling, animations, and enhanced features is available in `src/api/templates/index.html` in your project.

### **Key Frontend Features:**

#### **1. Session Management Integration**
```javascript
// Automatic session continuity - no manual session handling needed
const requestBody = { query };
if (sessionId) requestBody.session_id = sessionId;

// Save session ID from API response
sessionId = data.session_id; // Preserved across requests
```

#### **2. Progressive Enhancement**
- **Works immediately**: HTML loads instantly (SSR)
- **Enhanced with JS**: Interactive features load progressively  
- **Graceful degradation**: Basic functionality without JavaScript
- **Mobile responsive**: Single CSS file handles all screen sizes

#### **3. Simple State Management**
```javascript
// No complex state management needed - just a few variables
let sessionId = null;      // For conversation continuity
let isLoading = false;     // Prevent duplicate submissions
```

#### **4. Zero Dependencies**
- **No npm packages**: Everything works with browser APIs
- **No build process**: Direct HTML/CSS/JS deployment
- **No bundling**: Single file deployment

### **When to Upgrade to React/Vue:**

If your chat interface needs these advanced features, consider a framework:
- **Multi-page application** with complex routing
- **Rich text editing** with formatting tools
- **File uploads** with progress tracking
- **Complex animations** requiring state orchestration
- **Team collaboration** features with real-time sync

### **Project Structure:**
```
src/api/
├── templates/
│   └── index.html          # Complete chat interface (470 lines)
├── api_server.py           # FastAPI server with HTML serving
└── __init__.py             # Package exports
```

### **Testing the Complete System:**

1. **Create the template directory:**
```bash
mkdir -p src/api/templates
# Copy the complete HTML code to src/api/templates/index.html
```

2. **Start the server:**
```bash
python src/api/api_server.py
```

3. **Open your browser to:**
```
http://localhost:8080/
```

4. **Test conversation flow:**
   - **First message**: "Hello, my name is Sarah"
   - **Follow-up**: "What's my name?" (should remember "Sarah")  
   - **New chat**: Click "New Chat" to start fresh

**Result**: A production-ready chat interface that loads instantly, works on mobile, and maintains conversation context - all without React!

## 🌐 Complete API Endpoints

- **`GET /`**: Modern chat interface (HTML)
- **`POST /query`**: Main interaction endpoint (JSON API)
- **`GET /docs`**: Interactive API documentation  
- **`GET /health`**: Health check endpoint
- **`GET /info`**: API information

## 🔑 Environment Setup

Your `.env` file should contain:
```bash
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-google-api-key-here
```

## 🐳 Docker Containerization

Let's containerize our StudyBuddy application for easy deployment anywhere that supports Docker.

### **1. Dockerfile**

Create a `Dockerfile` in your project root:

```dockerfile
# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager for faster dependency resolution
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Copy application source code
COPY src/ ./src/
COPY .env* ./

# Install dependencies globally (no virtual environment needed in container)
RUN uv pip install --system fastapi uvicorn[standard] pydantic python-dotenv google-adk matplotlib numpy python-multipart

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Command to run the application
CMD ["python", "src/api/api_server.py"]
```

### **2. .dockerignore**

Create `.dockerignore` to exclude unnecessary files:

```dockerignore
__pycache__/
*.py[cod]
.git/
.venv/
node_modules/
*.log
tests/
docs/
*.md
.DS_Store
Dockerfile*
docker-compose*.yml
```

### **3. Docker Compose (Optional)**

Create `docker-compose.yml` for easier development:

```yaml
version: '3.8'

services:
  studybuddy:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GOOGLE_GENAI_USE_VERTEXAI=FALSE
    volumes:
      - ./src:/app/src:ro  # Development mode
      - ./.env:/app/.env:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### **4. Building and Running**

#### **Option A: Docker Commands**
```bash
# Build the image
docker build -t studybuddy-chat .

# Run the container
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY="your-api-key-here" \
  studybuddy-chat

# Or run in background
docker run -d -p 8080:8080 \
  --name studybuddy \
  -e GOOGLE_API_KEY="your-api-key-here" \
  studybuddy-chat
```

#### **Option B: Docker Compose (Recommended)**
```bash
# Start the application
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### **5. Environment Variables**

Make sure your `.env` file contains:
```bash
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_GENAI_USE_VERTEXAI=FALSE
PORT=8080
```

### **6. Container Features**

Our Docker setup includes:
- **Multi-stage optimization**: Efficient layer caching
- **Security**: Non-root user, minimal attack surface
- **Health checks**: Automatic container health monitoring
- **Fast builds**: UV package manager for rapid dependency installation
- **Production ready**: Optimized for deployment

### **7. Deployment Options**

The containerized app can be deployed to:

#### **Cloud Platforms:**
- **Google Cloud Run**: `gcloud run deploy --source .`
- **AWS ECS/Fargate**: Deploy via ECR + ECS service
- **Azure Container Instances**: `az container create`
- **DigitalOcean App Platform**: Connect GitHub repo

#### **Self-Hosted:**
- **Dokploy**: Open-source Docker-based deployment platform (detailed below)
- **Docker Swarm**: Multi-container orchestration
- **Kubernetes**: For large-scale deployments
- **VPS**: Any server with Docker installed

#### **Quick Cloud Run Deployment:**
```bash
# Build and deploy to Google Cloud Run
gcloud run deploy studybuddy \
  --source . \
  --port 8080 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="your-key"
```

## 🌟 Dokploy: Open Source Self-Hosted Deployment

**Dokploy** is a powerful, open-source alternative to Vercel/Netlify for self-hosted deployments. It's perfect for developers who want the convenience of PaaS with the control of self-hosting.

**🔗 Official Website**: [dokploy.com](https://dokploy.com)  
**🐙 GitHub Repository**: [github.com/Dokploy/dokploy](https://github.com/Dokploy/dokploy)

### **Why Choose Dokploy?**

- **100% Free**: No usage limits, no vendor lock-in
- **Full Control**: Your data stays on your servers  
- **Docker Native**: Built specifically for containerized applications
- **Modern UI**: Clean web interface for managing deployments
- **Git Integration**: Deploy directly from GitHub/GitLab
- **SSL Automation**: Automatic HTTPS certificates via Let's Encrypt

### **Complete Dokploy Tutorial**

For a comprehensive step-by-step guide on setting up and deploying with Dokploy, watch this detailed tutorial:

**📺 Watch Tutorial**: [https://youtu.be/ELkPcuO5ebo?si=3pRwAcjW9d4p3FgK](https://youtu.be/ELkPcuO5ebo?si=3pRwAcjW9d4p3FgK)

This video covers everything from server setup to deployment, perfect for getting your StudyBuddy app live quickly and cost-effectively.

### **Real-World Example**

Our **StudyBuddy demo** is deployed using Dokploy:

**🔗 Live Demo**: [https://study_buddy.chotuai.in/](https://study_buddy.chotuai.in/)  
**📂 Source Code**: [https://github.com/arjunagi-a-rehman/school-agents/tree/function-calling](https://github.com/arjunagi-a-rehman/school-agents/tree/function-calling)

Dokploy represents the **democratization of deployment tools** - making professional deployment accessible to everyone through open-source innovation.

## 🚀 Production Deployment Summary

Your StudyBuddy chat application is now fully containerized and ready for deployment anywhere! The Docker setup ensures:

- **Consistent Environment**: Runs the same everywhere
- **Easy Scaling**: Container orchestration support  
- **Health Monitoring**: Built-in health checks
- **Security**: Non-root user, minimal dependencies
- **Fast Deployment**: Single command deployment to any platform

The session management ensures your StudyBuddy maintains conversation context, making it feel like a natural tutoring experience rather than isolated Q&A interactions.

## 🎯 What's Next: RAG (Retrieval Augmented Generation)

Congratulations! 🎉 You've successfully built and deployed a complete AI agent system with:

- ✅ **Custom Agent**: StudyBuddy with specialized tools
- ✅ **Function Calling**: Math visualization and student management  
- ✅ **REST API**: FastAPI with session management
- ✅ **Modern UI**: Responsive chat interface
- ✅ **Rate Limiting**: API protection and abuse prevention
- ✅ **Containerization**: Docker deployment ready
- ✅ **Live Deployment**: Production-ready with Dokploy

But we're just getting started! 🚀

### **Coming Next: RAG Implementation**

In our next tutorial, we'll enhance StudyBuddy with **Retrieval Augmented Generation (RAG)** capabilities:

**🧠 What is RAG?**
- **Knowledge Base Integration**: Connect to external documents and data
- **Semantic Search**: Find relevant information from your content
- **Enhanced Responses**: AI responses backed by your specific knowledge
- **Document Understanding**: Process PDFs, docs, websites, and databases

**📚 What We'll Build:**
- **StudyBuddy with Course Materials**: Upload textbooks, lecture notes, assignments
- **Intelligent Document Search**: Find relevant content across all materials  
- **Contextual Learning**: Answers grounded in your actual course content
- **Citation Support**: AI responses with source references

**🔧 Technologies We'll Explore:**
- **Vector Databases**: Pinecone, Weaviate, or Chroma
- **Embedding Models**: Text vectorization for semantic search
- **Document Processing**: PDF parsing, text extraction, chunking
- **Hybrid Search**: Combining keyword and semantic search

This will transform StudyBuddy from a general AI tutor into a **personalized learning companion** that knows your specific course materials inside and out!

**📖 Stay tuned for**: "Your First RAG System: Building Knowledge-Grounded AI Agents"

---

**Ready to deploy your StudyBuddy?** Use the links above to access the live demo and source code. Happy learning! 🎓

