# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Personal Fitness Tool** built with Streamlit that provides AI-powered fitness assistance using local LLM models through Langflow workflows. The application combines traditional web frameworks with modern AI technologies for comprehensive health management.

## Development Commands

### Running the Application
```bash
streamlit run main.py
```

### Code Quality
```bash
# Lint code with Ruff (configured for 120 char line length, Google docstring style)
ruff check .
ruff format .

# Note: requirements.txt contains system packages, actual project deps are in pyproject.toml
```

### AI Service Dependencies
```bash
# Start Langflow service (required for AI features)
langflow run
# Service runs on http://127.0.0.1:7860
```

## Architecture Overview

### Core Components
- **main.py**: Streamlit UI orchestration with fragment-based components for performance
- **ai.py**: AI integration layer with Langflow workflows and error handling
- **db.py**: ChromaDB persistent storage setup with cosine similarity embeddings
- **profiles.py**: User profile CRUD operations with JSON serialization
- **form_submit.py**: Data persistence layer for updates and notes

### Data Flow
1. **Session State**: User profiles stored in Streamlit session state (ID always = 1)
2. **Database**: ChromaDB collections - "personal_data" for profiles, "notes" for user notes
3. **AI Integration**: Two workflows - macro generation and general Q&A via AskAI.json
4. **Storage Format**: All data serialized as JSON (not Python strings) for safety

### Key Patterns
- **Streamlit Fragments**: Extensive use of `@st.fragment` for granular UI updates
- **Error Handling**: All AI calls wrapped in try/catch with fallback responses
- **Connection Validation**: Real-time Langflow service status checking
- **Local-First**: Designed for local Ollama models and ChromaDB, no cloud dependencies

### Database Structure
- **health_notes/**: ChromaDB persistent storage directory
- **Collections**: personal_data (user profiles), notes (timestamped user notes)
- **Embedding**: Default ChromaDB embedding function (not using Ollama embeddings)

### AI Workflow Configuration
- **AskAI.json**: Large Langflow workflow file (66k+ lines) defining AI chat and macro generation
- **Macro Generation**: Endpoint /api/v1/run/macros with profile + goals input
- **Q&A System**: General fitness questions using profile context

## Important Notes

- Profile ID is hardcoded to 1 (single-user system)
- Langflow must be running on localhost:7860 for AI features
- Application uses fragments to minimize full page reruns
- All database operations use JSON serialization for security
- Error handling provides user-friendly messages when AI service unavailable

## Memories and Context

- Instruction to explain changes at each point before seeking edit confirmation