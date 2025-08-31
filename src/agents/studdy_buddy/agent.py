import os
import importlib
from pathlib import Path
import yaml
from google.adk import Agent
from google.adk.tools import google_search


def load_agent_config(config_path: str) -> dict:
    """Load agent configuration from YAML file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_prompt(prompt_path: str) -> str:
    """Load prompt content from markdown file."""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def load_tools_from_config(config: dict, agent_dir: Path) -> list:
    """Load tools dynamically from configuration."""
    tools = []
    
    if 'tools' not in config:
        return tools
    
    for tool_config in config['tools']:
        try:
            # Check if it's a built-in tool
            if 'builtin' in tool_config:
                builtin_name = tool_config['builtin']
                if builtin_name == 'google_search':
                    tools.append(google_search)
                else:
                    print(f"Warning: Unknown built-in tool: {builtin_name}")
            
            # Handle custom tools with module and class
            elif 'module' in tool_config and 'class' in tool_config:
                # Import the module dynamically
                module_name = tool_config['module']
                module_path = f"{agent_dir.name}.{module_name}"
                module = importlib.import_module(module_path, package=f"src.agents")
                
                # Get the tool class from the module and instantiate it
                class_name = tool_config['class']
                tool_class = getattr(module, class_name)
                tool_instance = tool_class()
                
                tools.append(tool_instance)
            
            else:
                print(f"Warning: Tool config missing required fields: {tool_config}")
                
        except Exception as e:
            print(f"Warning: Failed to load tool {tool_config.get('name', 'unknown')}: {e}")
    
    return tools


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
    
    # Load tools from configuration
    tools = load_tools_from_config(config, current_dir)
    
    # Create agent with loaded configuration and tools
    agent = Agent(
        name=config['agent']['name'],
        description=config['agent']['description'],
        model=config['agent']['model'],
        instruction=instruction,
        tools=tools
    )
    
    return agent


# Create the agent instance
root_agent = create_study_buddy_agent()