import os
import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import List, Dict, Any


def auto_discover_tools(tools_dir: Path) -> List[Dict[str, Any]]:
    """
    Automatically discover and load tools from the tools directory.
    
    This function scans the tools directory for Python files and attempts to
    automatically register functions as tools based on naming conventions.
    """
    tools = []
    
    if not tools_dir.exists():
        return tools
    
    # Get all Python files in the tools directory
    for py_file in tools_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        module_name = py_file.stem
        
        try:
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for functions that should be exposed as tools
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    # Check if function has proper docstring and is marked for tool usage
                    if hasattr(obj, '__doc__') and obj.__doc__:
                        # Functions starting with tool-specific names are auto-registered
                        if any(name.startswith(prefix) for prefix in ['calculate', 'convert', 'get_', 'solve_']):
                            tool = {
                                "name": name,
                                "description": obj.__doc__.strip().split('\n')[0],  # First line of docstring
                                "function": obj
                            }
                            tools.append(tool)
                            
        except Exception as e:
            print(f"Warning: Failed to load tools from {module_name}: {e}")
    
    return tools


def load_tools_with_auto_discovery(config: dict, agent_dir: Path) -> List[Dict[str, Any]]:
    """
    Load tools using both explicit configuration and auto-discovery.
    
    First loads tools explicitly defined in config, then auto-discovers
    additional tools from the tools directory.
    """
    tools = []
    
    # Load explicitly configured tools first
    if 'tools' in config:
        for tool_config in config['tools']:
            try:
                # Import the module dynamically
                module_name = tool_config['module']
                module_path = f"{agent_dir.name}.{module_name}"
                module = importlib.import_module(module_path, package=f"src.agents")
                
                # Get the function from the module
                function_name = tool_config['function']
                function = getattr(module, function_name)
                
                # Create tool definition
                tool = {
                    "name": tool_config['name'],
                    "description": tool_config['description'],
                    "function": function
                }
                tools.append(tool)
                
            except Exception as e:
                print(f"Warning: Failed to load configured tool {tool_config.get('name', 'unknown')}: {e}")
    
    # Auto-discover additional tools
    tools_dir = agent_dir / "tools"
    auto_tools = auto_discover_tools(tools_dir)
    
    # Add auto-discovered tools that aren't already configured
    configured_names = {tool['name'] for tool in tools}
    for auto_tool in auto_tools:
        if auto_tool['name'] not in configured_names:
            tools.append(auto_tool)
    
    return tools
