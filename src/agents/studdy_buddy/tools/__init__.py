"""
Student Management Tools for Study Buddy Agent

This package contains tools for comprehensive student data management
including progress tracking, goal setting, and session recording.
"""

from .student_manager import (
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

from .math_visualizer import (
    draw_geometric_shape,
    plot_function,
    create_coordinate_system,
    visualize_trigonometry
)

__all__ = [
    'get_student_profile',
    'update_student_info',
    'add_subject',
    'update_learning_preferences',
    'record_study_session',
    'add_goal',
    'complete_goal',
    'get_progress_summary',
    'add_notes',
    'get_recent_sessions',
    # Weak topics management
    'add_weak_topic',
    'update_weak_topic_review',
    'remove_weak_topic',
    'get_weak_topics_summary',
    # Math visualization tools
    'draw_geometric_shape',
    'plot_function', 
    'create_coordinate_system',
    'visualize_trigonometry'
]
