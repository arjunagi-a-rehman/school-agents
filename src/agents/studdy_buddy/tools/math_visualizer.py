"""
Math Visualization Tool for Study Buddy Agent

This tool creates mathematical figures, graphs, and visualizations using Matplotlib
to help students understand concepts visually.

Following Google ADK Function Tools best practices with proper type hints, 
docstrings, and parameter definitions.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import base64
import io
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime

# Try to import ADK artifacts for better image display
try:
    from google.adk.core import Artifact
    ADK_ARTIFACTS_AVAILABLE = True
except ImportError:
    ADK_ARTIFACTS_AVAILABLE = False


# Directory to save visualizations  
VISUALIZATIONS_DIR = Path(__file__).parent.parent.parent.parent / "resources" / "visualizations"


def _ensure_viz_directory() -> None:
    """Ensure the visualizations directory exists."""
    VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)


def _save_and_encode_figure(fig, filename_prefix: str = "math_viz") -> Dict[str, str]:
    """
    Save figure to file and return both file path and base64 encoding.
    Also try to create ADK Artifact if available.
    
    Args:
        fig: Matplotlib figure object
        filename_prefix: Prefix for the filename
        
    Returns:
        Dict with file_path, base64_data, and potentially artifact
    """
    _ensure_viz_directory()
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    file_path = VISUALIZATIONS_DIR / filename
    
    # Save to file
    fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
    
    # Create base64 encoding and artifact
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    image_bytes = buffer.read()
    base64_data = base64.b64encode(image_bytes).decode('utf-8')
    
    result = {
        "file_path": str(file_path),
        "base64_data": f"data:image/png;base64,{base64_data}",
        "filename": filename,
        "image_display_message": f"📊 Visualization created! Open this file to view: {filename}"
    }
    
    # Try to create ADK Artifact for better display
    if ADK_ARTIFACTS_AVAILABLE:
        try:
            artifact = Artifact(
                content_type="image/png",
                data=image_bytes,
                title=f"Mathematical Visualization: {filename_prefix}"
            )
            result["artifact"] = artifact
            result["display_method"] = "artifact"
        except Exception:
            result["display_method"] = "file_only"
    else:
        result["display_method"] = "file_only"
    
    plt.close(fig)  # Free memory
    return result


def draw_geometric_shape(shape_type: str, 
                        dimensions: Dict[str, float],
                        labels: bool = True,
                        grid: bool = True,
                        title: Optional[str] = None) -> Dict[str, Any]:
    """
    Draw geometric shapes like triangles, circles, rectangles, etc.
    
    Args:
        shape_type (str): Type of shape - "triangle", "circle", "rectangle", "square"
        dimensions (Dict[str, float]): Shape dimensions (varies by shape type)
        labels (bool): Whether to add labels and measurements
        grid (bool): Whether to show grid
        title (str, optional): Title for the figure
        
    Returns:
        Dict[str, Any]: Figure data including file path and base64 encoding
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    try:
        if shape_type.lower() == "triangle":
            # Expects: {"base": float, "height": float} or {"side_a": float, "side_b": float, "side_c": float}
            if "base" in dimensions and "height" in dimensions:
                base = dimensions["base"]
                height = dimensions["height"]
                # Right triangle at origin
                x_coords = [0, base, 0, 0]
                y_coords = [0, 0, height, 0]
                
                if labels:
                    ax.text(base/2, -0.3, f"Base = {base}", ha='center', fontsize=12)
                    ax.text(-0.5, height/2, f"Height = {height}", va='center', rotation=90, fontsize=12)
                    # Calculate hypotenuse
                    hypotenuse = np.sqrt(base**2 + height**2)
                    ax.text(base/2 + 0.2, height/2, f"Hypotenuse = {hypotenuse:.2f}", 
                           rotation=-np.degrees(np.arctan(height/base)), fontsize=12)
            
            elif all(key in dimensions for key in ["side_a", "side_b", "side_c"]):
                # General triangle using Heron's formula for area
                a, b, c = dimensions["side_a"], dimensions["side_b"], dimensions["side_c"]
                # Place triangle using coordinates
                x_coords = [0, a, None, 0]  # Will calculate third point
                y_coords = [0, 0, None, 0]
                # Calculate third vertex using law of cosines
                cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
                if -1 <= cos_C <= 1:  # Valid triangle
                    angle_C = np.arccos(cos_C)
                    x_coords[2] = b * np.cos(angle_C)
                    y_coords[2] = b * np.sin(angle_C)
                else:
                    return {"status": "error", "message": "Invalid triangle dimensions - triangle inequality violated"}
                
                if labels:
                    ax.text(a/2, -0.3, f"Side a = {a}", ha='center', fontsize=12)
                    ax.text(-0.3, y_coords[2]/2, f"Side b = {b}", va='center', rotation=90, fontsize=12)
                    ax.text((a + x_coords[2])/2, y_coords[2]/2 + 0.3, f"Side c = {c}", ha='center', fontsize=12)
            
            else:
                return {"status": "error", "message": "Triangle requires either 'base' and 'height' or 'side_a', 'side_b', and 'side_c'"}
            
            ax.plot(x_coords, y_coords, 'b-', linewidth=2)
            ax.fill(x_coords[:-1], y_coords[:-1], alpha=0.3, color='lightblue')
        
        elif shape_type.lower() == "circle":
            # Expects: {"radius": float} or {"diameter": float}
            if "radius" in dimensions:
                radius = dimensions["radius"]
            elif "diameter" in dimensions:
                radius = dimensions["diameter"] / 2
            else:
                return {"status": "error", "message": "Circle requires 'radius' or 'diameter'"}
            
            circle = patches.Circle((0, 0), radius, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
            ax.add_patch(circle)
            
            if labels:
                # Draw radius line
                ax.plot([0, radius], [0, 0], 'r-', linewidth=2)
                ax.text(radius/2, 0.2, f"r = {radius}", ha='center', fontsize=12, color='red')
                ax.text(0, -radius-0.5, f"Area = π × r² = {np.pi * radius**2:.2f}", ha='center', fontsize=12)
                ax.text(0, -radius-0.8, f"Circumference = 2π × r = {2 * np.pi * radius:.2f}", ha='center', fontsize=12)
        
        elif shape_type.lower() in ["rectangle", "square"]:
            if shape_type.lower() == "square":
                if "side" in dimensions:
                    width = height = dimensions["side"]
                else:
                    return {"status": "error", "message": "Square requires 'side' dimension"}
            else:
                if "width" in dimensions and "height" in dimensions:
                    width, height = dimensions["width"], dimensions["height"]
                else:
                    return {"status": "error", "message": "Rectangle requires 'width' and 'height'"}
            
            rectangle = patches.Rectangle((0, 0), width, height, linewidth=2, 
                                        edgecolor='blue', facecolor='lightblue', alpha=0.3)
            ax.add_patch(rectangle)
            
            if labels:
                ax.text(width/2, -0.3, f"Width = {width}", ha='center', fontsize=12)
                ax.text(-0.5, height/2, f"Height = {height}", va='center', rotation=90, fontsize=12)
                ax.text(width/2, height + 0.3, f"Area = {width * height}", ha='center', fontsize=12)
                ax.text(width/2, height + 0.6, f"Perimeter = {2*(width + height)}", ha='center', fontsize=12)
        
        else:
            return {"status": "error", "message": f"Unsupported shape type: {shape_type}"}
        
        # Set equal aspect ratio and add grid
        ax.set_aspect('equal')
        if grid:
            ax.grid(True, alpha=0.3)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        else:
            ax.set_title(f"{shape_type.title()} Visualization", fontsize=16, fontweight='bold')
        
        # Auto-scale the axes
        ax.autoscale()
        margin = 0.1
        xlims = ax.get_xlim()
        ylims = ax.get_ylim()
        ax.set_xlim(xlims[0] - margin, xlims[1] + margin)
        ax.set_ylim(ylims[0] - margin, ylims[1] + margin)
        
        # Save and return
        result = _save_and_encode_figure(fig, f"geometry_{shape_type}")
        result["status"] = "success"
        result["message"] = f"{shape_type.title()} visualization created successfully"
        result["shape_type"] = shape_type
        result["dimensions"] = dimensions
        
        return result
        
    except Exception as e:
        plt.close(fig)
        return {"status": "error", "message": f"Error creating shape: {str(e)}"}


def plot_function(function_type: str,
                 parameters: Dict[str, float],
                 x_min: Optional[float] = None,
                 x_max: Optional[float] = None,
                 grid: bool = True,
                 title: Optional[str] = None) -> Dict[str, Any]:
    """
    Plot mathematical functions like linear, quadratic, trigonometric, etc.
    
    Args:
        function_type (str): Type of function - "linear", "quadratic", "sine", "cosine", "tan", "exponential", "logarithmic"
        parameters (Dict[str, float]): Function parameters (varies by function type)
        x_min (float, optional): Minimum x value for plotting range (default: -10)
        x_max (float, optional): Maximum x value for plotting range (default: 10)
        grid (bool): Whether to show grid
        title (str, optional): Title for the figure
        
    Returns:
        Dict[str, Any]: Figure data including file path and base64 encoding
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    try:
        # Set default values if not provided
        if x_min is None:
            x_min = -10
        if x_max is None:
            x_max = 10
            
        x = np.linspace(x_min, x_max, 1000)
        
        if function_type.lower() == "linear":
            # y = mx + b
            m = parameters.get("slope", 1)
            b = parameters.get("intercept", 0)
            y = m * x + b
            function_label = f"y = {m}x + {b}" if b >= 0 else f"y = {m}x - {abs(b)}"
        
        elif function_type.lower() == "quadratic":
            # y = ax^2 + bx + c
            a = parameters.get("a", 1)
            b = parameters.get("b", 0)
            c = parameters.get("c", 0)
            y = a * x**2 + b * x + c
            function_label = f"y = {a}x² + {b}x + {c}"
            
            # Find and mark vertex
            vertex_x = -b / (2 * a)
            vertex_y = a * vertex_x**2 + b * vertex_x + c
            ax.plot(vertex_x, vertex_y, 'ro', markersize=8, label=f'Vertex ({vertex_x:.2f}, {vertex_y:.2f})')
        
        elif function_type.lower() == "sine":
            # y = A * sin(B * x + C) + D
            amplitude = parameters.get("amplitude", 1)
            frequency = parameters.get("frequency", 1)
            phase = parameters.get("phase", 0)
            vertical_shift = parameters.get("vertical_shift", 0)
            y = amplitude * np.sin(frequency * x + phase) + vertical_shift
            function_label = f"y = {amplitude}sin({frequency}x + {phase}) + {vertical_shift}"
        
        elif function_type.lower() == "cosine":
            # y = A * cos(B * x + C) + D
            amplitude = parameters.get("amplitude", 1)
            frequency = parameters.get("frequency", 1)
            phase = parameters.get("phase", 0)
            vertical_shift = parameters.get("vertical_shift", 0)
            y = amplitude * np.cos(frequency * x + phase) + vertical_shift
            function_label = f"y = {amplitude}cos({frequency}x + {phase}) + {vertical_shift}"
        
        elif function_type.lower() == "tan":
            # y = A * tan(B * x + C) + D
            amplitude = parameters.get("amplitude", 1)
            frequency = parameters.get("frequency", 1)
            phase = parameters.get("phase", 0)
            vertical_shift = parameters.get("vertical_shift", 0)
            y = amplitude * np.tan(frequency * x + phase) + vertical_shift
            function_label = f"y = {amplitude}tan({frequency}x + {phase}) + {vertical_shift}"
            # Limit y values to prevent extreme plotting
            y = np.where(np.abs(y) > 100, np.nan, y)
        
        elif function_type.lower() == "exponential":
            # y = A * b^x + C
            amplitude = parameters.get("amplitude", 1)
            base = parameters.get("base", np.e)
            vertical_shift = parameters.get("vertical_shift", 0)
            y = amplitude * (base ** x) + vertical_shift
            function_label = f"y = {amplitude} × {base}^x + {vertical_shift}"
        
        elif function_type.lower() == "logarithmic":
            # y = A * log_b(x) + C
            amplitude = parameters.get("amplitude", 1)
            base = parameters.get("base", np.e)
            vertical_shift = parameters.get("vertical_shift", 0)
            # Only plot for positive x values
            x_positive = x[x > 0]
            if len(x_positive) == 0:
                return {"status": "error", "message": "Logarithmic function requires positive x values"}
            
            if base == np.e:
                y_positive = amplitude * np.log(x_positive) + vertical_shift
                function_label = f"y = {amplitude}ln(x) + {vertical_shift}"
            else:
                y_positive = amplitude * np.log(x_positive) / np.log(base) + vertical_shift
                function_label = f"y = {amplitude}log_{base}(x) + {vertical_shift}"
            
            ax.plot(x_positive, y_positive, 'b-', linewidth=2, label=function_label)
        
        else:
            return {"status": "error", "message": f"Unsupported function type: {function_type}"}
        
        # Plot the function (if not logarithmic, which is handled above)
        if function_type.lower() != "logarithmic":
            ax.plot(x, y, 'b-', linewidth=2, label=function_label)
        
        # Add axes through origin
        ax.axhline(y=0, color='k', linewidth=0.8)
        ax.axvline(x=0, color='k', linewidth=0.8)
        
        # Add grid
        if grid:
            ax.grid(True, alpha=0.3)
        
        # Labels and title
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('y', fontsize=14)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        else:
            ax.set_title(f"{function_type.title()} Function", fontsize=16, fontweight='bold')
        
        ax.legend(fontsize=12)
        
        # Save and return
        result = _save_and_encode_figure(fig, f"function_{function_type}")
        result["status"] = "success"
        result["message"] = f"{function_type.title()} function plot created successfully"
        result["function_type"] = function_type
        result["parameters"] = parameters
        result["function_equation"] = function_label
        
        return result
        
    except Exception as e:
        plt.close(fig)
        return {"status": "error", "message": f"Error plotting function: {str(e)}"}


def create_coordinate_system(x_min: Optional[float] = None,
                           x_max: Optional[float] = None,
                           y_min: Optional[float] = None,
                           y_max: Optional[float] = None,
                           grid_spacing: float = 1.0,
                           points: Optional[List[List[float]]] = None,
                           point_labels: Optional[List[str]] = None,
                           title: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a coordinate system with optional points marked.
    
    Args:
        x_min (float, optional): Minimum x value (default: -10)
        x_max (float, optional): Maximum x value (default: 10)
        y_min (float, optional): Minimum y value (default: -10) 
        y_max (float, optional): Maximum y value (default: 10)
        grid_spacing (float): Spacing between grid lines
        points (List[List[float]], optional): Points to mark as [[x1,y1], [x2,y2], ...]
        point_labels (List[str], optional): Labels for the points
        title (str, optional): Title for the figure
        
    Returns:
        Dict[str, Any]: Figure data including file path and base64 encoding
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    try:
        # Set default values if not provided
        if x_min is None:
            x_min = -10
        if x_max is None:
            x_max = 10
        if y_min is None:
            y_min = -10
        if y_max is None:
            y_max = 10
            
        # Set the ranges
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        # Create major grid
        ax.grid(True, alpha=0.3, linewidth=0.8)
        
        # Create minor grid with specified spacing
        ax.set_xticks(np.arange(x_min, x_max + 1, grid_spacing))
        ax.set_yticks(np.arange(y_min, y_max + 1, grid_spacing))
        ax.grid(True, alpha=0.2, linewidth=0.5)
        
        # Draw main axes through origin
        ax.axhline(y=0, color='black', linewidth=1.5, zorder=5)
        ax.axvline(x=0, color='black', linewidth=1.5, zorder=5)
        
        # Add arrow heads to axes
        ax.annotate('', xy=(x_max, 0), xytext=(x_max-0.5, 0),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
        ax.annotate('', xy=(0, y_max), xytext=(0, y_max-0.5),
                   arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
        
        # Label axes
        ax.text(x_max-0.5, -0.8, 'x', fontsize=16, fontweight='bold', ha='center')
        ax.text(0.5, y_max-0.5, 'y', fontsize=16, fontweight='bold', va='center')
        
        # Mark origin
        ax.plot(0, 0, 'ko', markersize=6, zorder=10)
        ax.text(0.3, -0.3, 'O (0,0)', fontsize=12, ha='left')
        
        # Plot points if provided
        if points:
            for i, point in enumerate(points):
                x, y = point[0], point[1]
                ax.plot(x, y, 'ro', markersize=8, zorder=10)
                
                # Add labels if provided
                if point_labels and i < len(point_labels):
                    label = point_labels[i]
                else:
                    label = f'({x}, {y})'
                
                ax.text(x + 0.3, y + 0.3, label, fontsize=12, ha='left', 
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Set title
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        else:
            ax.set_title('Coordinate System', fontsize=16, fontweight='bold')
        
        # Set equal aspect ratio
        ax.set_aspect('equal')
        
        # Add subtle number labels on axes
        for x_val in range(int(x_min), int(x_max) + 1):
            if x_val != 0 and x_val % max(1, int(grid_spacing)) == 0:
                ax.text(x_val, -0.4, str(x_val), ha='center', va='top', fontsize=10)
        
        for y_val in range(int(y_min), int(y_max) + 1):
            if y_val != 0 and y_val % max(1, int(grid_spacing)) == 0:
                ax.text(-0.4, y_val, str(y_val), ha='right', va='center', fontsize=10)
        
        # Save and return
        result = _save_and_encode_figure(fig, "coordinate_system")
        result["status"] = "success" 
        result["message"] = "Coordinate system created successfully"
        result["x_range"] = [x_min, x_max]
        result["y_range"] = [y_min, y_max]
        result["points"] = points or []
        
        return result
        
    except Exception as e:
        plt.close(fig)
        return {"status": "error", "message": f"Error creating coordinate system: {str(e)}"}


def visualize_trigonometry(angle_degrees: float,
                          show_unit_circle: bool = True,
                          show_triangle: bool = True,
                          show_values: bool = True,
                          title: Optional[str] = None) -> Dict[str, Any]:
    """
    Create trigonometry visualization showing unit circle, angle, and triangle.
    
    Args:
        angle_degrees (float): Angle in degrees to visualize
        show_unit_circle (bool): Whether to show the unit circle
        show_triangle (bool): Whether to show the right triangle
        show_values (bool): Whether to show sin, cos, tan values
        title (str, optional): Title for the figure
        
    Returns:
        Dict[str, Any]: Figure data including file path and base64 encoding
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    try:
        # Convert to radians
        angle_radians = np.radians(angle_degrees)
        
        # Calculate trig values
        cos_val = np.cos(angle_radians)
        sin_val = np.sin(angle_radians)
        tan_val = np.tan(angle_radians) if np.abs(np.cos(angle_radians)) > 1e-10 else np.inf
        
        if show_unit_circle:
            # Draw unit circle
            circle = patches.Circle((0, 0), 1, linewidth=2, edgecolor='blue', fill=False)
            ax.add_patch(circle)
            
            # Draw coordinate axes
            ax.axhline(y=0, color='black', linewidth=1)
            ax.axvline(x=0, color='black', linewidth=1)
        
        # Draw angle arc
        if angle_degrees != 0:
            arc_angles = np.linspace(0, angle_radians, 50)
            arc_radius = 0.3
            arc_x = arc_radius * np.cos(arc_angles)
            arc_y = arc_radius * np.sin(arc_angles)
            ax.plot(arc_x, arc_y, 'green', linewidth=2, label=f'Angle = {angle_degrees}°')
        
        # Point on unit circle
        point_x, point_y = cos_val, sin_val
        ax.plot(point_x, point_y, 'ro', markersize=10, zorder=10)
        ax.text(point_x + 0.1, point_y + 0.1, f'({cos_val:.3f}, {sin_val:.3f})', 
               fontsize=12, ha='left', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Draw radius line to point
        ax.plot([0, point_x], [0, point_y], 'r-', linewidth=3, label='Radius = 1')
        
        if show_triangle:
            # Draw right triangle
            ax.plot([0, point_x], [0, 0], 'orange', linewidth=2, label=f'Adjacent = cos({angle_degrees}°) = {cos_val:.3f}')
            ax.plot([point_x, point_x], [0, point_y], 'purple', linewidth=2, label=f'Opposite = sin({angle_degrees}°) = {sin_val:.3f}')
            
            # Right angle indicator
            if angle_degrees % 90 != 0:  # Don't show for 0°, 90°, 180°, 270°
                square_size = 0.1
                square = patches.Rectangle((point_x - square_size, 0), square_size, square_size, 
                                         linewidth=1, edgecolor='black', facecolor='none')
                ax.add_patch(square)
        
        if show_values:
            # Display trig values
            tan_display = f"{tan_val:.4f}" if not np.isinf(tan_val) else "undefined"
            values_text = f"""Trigonometric Values for {angle_degrees}°:
sin({angle_degrees}°) = {sin_val:.4f}
cos({angle_degrees}°) = {cos_val:.4f}
tan({angle_degrees}°) = {tan_display}"""
            
            ax.text(-1.8, 1.5, values_text, fontsize=12, va='top', ha='left',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
        
        # Set equal aspect ratio and limits
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Labels
        ax.set_xlabel('x (cosine)', fontsize=14)
        ax.set_ylabel('y (sine)', fontsize=14)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        else:
            ax.set_title(f'Trigonometry Visualization - {angle_degrees}°', fontsize=16, fontweight='bold')
        
        ax.legend(loc='upper right', fontsize=10)
        
        # Save and return
        result = _save_and_encode_figure(fig, f"trigonometry_{angle_degrees}")
        result["status"] = "success"
        result["message"] = f"Trigonometry visualization for {angle_degrees}° created successfully"
        result["angle_degrees"] = angle_degrees
        result["trig_values"] = {
            "sin": sin_val,
            "cos": cos_val, 
            "tan": tan_val if not np.isinf(tan_val) else "undefined"
        }
        
        return result
        
    except Exception as e:
        plt.close(fig)
        return {"status": "error", "message": f"Error creating trigonometry visualization: {str(e)}"}
