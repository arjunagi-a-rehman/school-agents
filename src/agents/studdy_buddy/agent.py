import os
from pathlib import Path
import yaml
from google.adk import Agent
from google.adk.tools import google_search

# Import student management tools
from .tools.student_manager import (
    get_student_profile,
    update_student_info,
    add_subject,
    update_learning_preferences,
    record_study_session,
    add_goal,
    complete_goal,
    get_progress_summary,
    add_notes,
    get_recent_sessions,
    # Weak topics management
    add_weak_topic,
    update_weak_topic_review,
    remove_weak_topic,
    get_weak_topics_summary
)



def load_agent_config(config_path: str) -> dict:
    """Load agent configuration from YAML file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_prompt(prompt_path: str) -> str:
    """Load prompt content from markdown file."""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def create_study_buddy_agent() -> Agent:
    """Create and configure the Study Buddy agent."""
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Load configuration
    config_path = current_dir / 'agent_config.yml'
    config = load_agent_config(config_path)
    
    # Load prompt
    prompt_path = current_dir / config['agent']['prompt_file']
    instruction = load_prompt(prompt_path)
    
    # Create agent with loaded configuration
    agent = Agent(
        name=config['agent']['name'],
        description=config['agent']['description'],
        model=config['agent']['model'],
        instruction=instruction,
    )
    
    return agent


# Create the agent instance
root_agent = create_study_buddy_agent()