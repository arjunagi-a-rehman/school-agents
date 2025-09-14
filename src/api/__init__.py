"""
School Agents API Package

This package contains the FastAPI-based REST API for the school agents system.
It provides endpoints for interacting with StudyBuddy and other educational agents.
"""

__version__ = "1.0.0"

# Export main components for easy importing
from .api_server import app, runner

__all__ = ["app", "runner", "__version__"]
