"""
Student Management Tool for Study Buddy Agent

This tool provides comprehensive student data management capabilities including
reading, writing, and updating student information, progress tracking, and session history.

Following Google ADK Function Tools best practices with proper type hints, 
docstrings, and parameter definitions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


# Path to the student data file - go up to src/, then to resources/
STUDENT_DATA_PATH = Path(__file__).parent.parent.parent.parent / "resources" / "student.json"


def _load_student_data() -> Dict[str, Any]:
    """
    Load student data from JSON file.
    
    Returns:
        Dict[str, Any]: Student data dictionary
    """
    try:
        with open(STUDENT_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default structure if file doesn't exist or is corrupted
        return {
            "student_id": "student_001",
            "name": "Student",
            "email": "",
            "grade_level": "",
            "subjects": [],
            "learning_preferences": {
                "learning_style": "",
                "difficulty_level": "intermediate",
                "preferred_topics": []
            },
            "progress": {
                "total_sessions": 0,
                "subjects_studied": {},
                "achievements": [],
                "study_streak": 0,
                "last_study_date": None
            },
            "weak_topics": {
                "struggling_areas": [],
                "needs_review": [],
                "improvement_needed": {}
            },
            "session_history": [],
            "goals": [],
            "notes": "",
            "created_at": None,
            "updated_at": None
        }


def _save_student_data(data: Dict[str, Any]) -> bool:
    """
    Save student data to JSON file.
    
    Args:
        data (Dict[str, Any]): Student data to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Update timestamp
        data["updated_at"] = datetime.now().isoformat()
        
        # Ensure directory exists
        STUDENT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(STUDENT_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving student data: {e}")
        return False


def get_student_profile() -> Dict[str, Any]:
    """
    Retrieve the complete student profile including personal info, preferences, and progress.
    
    Returns:
        Dict[str, Any]: Complete student profile data
    """
    return _load_student_data()


def update_student_info(name: Optional[str] = None, 
                       email: Optional[str] = None, 
                       grade_level: Optional[str] = None) -> Dict[str, str]:
    """
    Update basic student information like name, email, and grade level.
    
    Args:
        name (str, optional): Student's name
        email (str, optional): Student's email address  
        grade_level (str, optional): Student's current grade level
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    
    if name is not None:
        data["name"] = name
    if email is not None:
        data["email"] = email
    if grade_level is not None:
        data["grade_level"] = grade_level
        
    # Set created_at if this is the first time setting basic info
    if data["created_at"] is None:
        data["created_at"] = datetime.now().isoformat()
    
    success = _save_student_data(data)
    
    if success:
        return {"status": "success", "message": "Student information updated successfully"}
    else:
        return {"status": "error", "message": "Failed to update student information"}


def add_subject(subject: str) -> Dict[str, str]:
    """
    Add a new subject to the student's subject list.
    
    Args:
        subject (str): Name of the subject to add
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    
    if subject not in data["subjects"]:
        data["subjects"].append(subject)
        
        # Initialize subject in progress tracking
        if subject not in data["progress"]["subjects_studied"]:
            data["progress"]["subjects_studied"][subject] = {
                "sessions": 0,
                "total_time_minutes": 0,
                "last_studied": None,
                "topics_covered": []
            }
        
        success = _save_student_data(data)
        
        if success:
            return {"status": "success", "message": f"Subject '{subject}' added successfully"}
        else:
            return {"status": "error", "message": "Failed to add subject"}
    else:
        return {"status": "info", "message": f"Subject '{subject}' already exists"}


def update_learning_preferences(learning_style: Optional[str] = None,
                               difficulty_level: Optional[str] = None,
                               preferred_topics: Optional[List[str]] = None) -> Dict[str, str]:
    """
    Update student's learning preferences and settings.
    
    Args:
        learning_style (str, optional): Learning style preference (e.g., 'visual', 'auditory', 'kinesthetic')
        difficulty_level (str, optional): Preferred difficulty level ('beginner', 'intermediate', 'advanced')
        preferred_topics (List[str], optional): List of preferred study topics
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    
    if learning_style is not None:
        data["learning_preferences"]["learning_style"] = learning_style
    if difficulty_level is not None:
        data["learning_preferences"]["difficulty_level"] = difficulty_level
    if preferred_topics is not None:
        data["learning_preferences"]["preferred_topics"] = preferred_topics
    
    success = _save_student_data(data)
    
    if success:
        return {"status": "success", "message": "Learning preferences updated successfully"}
    else:
        return {"status": "error", "message": "Failed to update learning preferences"}


def record_study_session(subject: str, 
                        duration_minutes: int, 
                        topics_covered: List[str],
                        session_notes: Optional[str] = None) -> Dict[str, str]:
    """
    Record a completed study session with progress tracking.
    
    Args:
        subject (str): Subject studied in this session
        duration_minutes (int): Duration of the study session in minutes
        topics_covered (List[str]): List of topics covered in this session
        session_notes (str, optional): Additional notes about the session
        
    Returns:
        Dict[str, str]: Status message with session details
    """
    data = _load_student_data()
    current_time = datetime.now().isoformat()
    
    # Update overall progress
    data["progress"]["total_sessions"] += 1
    
    # Update subject-specific progress
    if subject not in data["progress"]["subjects_studied"]:
        data["progress"]["subjects_studied"][subject] = {
            "sessions": 0,
            "total_time_minutes": 0,
            "last_studied": None,
            "topics_covered": []
        }
    
    subject_progress = data["progress"]["subjects_studied"][subject]
    subject_progress["sessions"] += 1
    subject_progress["total_time_minutes"] += duration_minutes
    subject_progress["last_studied"] = current_time
    
    # Add new topics to the list
    for topic in topics_covered:
        if topic not in subject_progress["topics_covered"]:
            subject_progress["topics_covered"].append(topic)
    
    # Update study streak
    last_study_date = data["progress"]["last_study_date"]
    if last_study_date:
        last_date = datetime.fromisoformat(last_study_date).date()
        today = datetime.now().date()
        
        if (today - last_date).days == 1:
            data["progress"]["study_streak"] += 1
        elif (today - last_date).days > 1:
            data["progress"]["study_streak"] = 1
    else:
        data["progress"]["study_streak"] = 1
    
    data["progress"]["last_study_date"] = current_time
    
    # Add to session history
    session_record = {
        "date": current_time,
        "subject": subject,
        "duration_minutes": duration_minutes,
        "topics_covered": topics_covered,
        "notes": session_notes or ""
    }
    data["session_history"].append(session_record)
    
    # Keep only last 50 sessions to prevent file from growing too large
    if len(data["session_history"]) > 50:
        data["session_history"] = data["session_history"][-50:]
    
    success = _save_student_data(data)
    
    if success:
        return {
            "status": "success", 
            "message": f"Study session recorded: {duration_minutes} minutes of {subject}",
            "total_sessions": data["progress"]["total_sessions"],
            "study_streak": data["progress"]["study_streak"]
        }
    else:
        return {"status": "error", "message": "Failed to record study session"}


def add_goal(goal_description: str, target_date: Optional[str] = None) -> Dict[str, str]:
    """
    Add a new learning goal for the student.
    
    Args:
        goal_description (str): Description of the learning goal
        target_date (str, optional): Target completion date in YYYY-MM-DD format
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    
    goal = {
        "id": len(data["goals"]) + 1,
        "description": goal_description,
        "target_date": target_date,
        "created_at": datetime.now().isoformat(),
        "completed": False,
        "completed_at": None
    }
    
    data["goals"].append(goal)
    success = _save_student_data(data)
    
    if success:
        return {"status": "success", "message": f"Goal added: {goal_description}"}
    else:
        return {"status": "error", "message": "Failed to add goal"}


def complete_goal(goal_id: int) -> Dict[str, str]:
    """
    Mark a goal as completed.
    
    Args:
        goal_id (int): ID of the goal to mark as completed
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    
    for goal in data["goals"]:
        if goal["id"] == goal_id:
            goal["completed"] = True
            goal["completed_at"] = datetime.now().isoformat()
            
            # Add to achievements
            achievement = f"Completed goal: {goal['description']}"
            if achievement not in data["progress"]["achievements"]:
                data["progress"]["achievements"].append(achievement)
            
            success = _save_student_data(data)
            
            if success:
                return {"status": "success", "message": f"Goal '{goal['description']}' marked as completed!"}
            else:
                return {"status": "error", "message": "Failed to update goal"}
    
    return {"status": "error", "message": f"Goal with ID {goal_id} not found"}


def get_progress_summary() -> Dict[str, Any]:
    """
    Get a comprehensive progress summary for the student.
    
    Returns:
        Dict[str, Any]: Progress summary including sessions, subjects, and achievements
    """
    data = _load_student_data()
    progress = data["progress"]
    
    # Calculate total study time
    total_minutes = sum(
        subject_data["total_time_minutes"] 
        for subject_data in progress["subjects_studied"].values()
    )
    
    return {
        "total_sessions": progress["total_sessions"],
        "total_study_time_minutes": total_minutes,
        "total_study_time_hours": round(total_minutes / 60, 1),
        "study_streak": progress["study_streak"],
        "subjects_count": len(progress["subjects_studied"]),
        "subjects_studied": list(progress["subjects_studied"].keys()),
        "achievements_count": len(progress["achievements"]),
        "recent_achievements": progress["achievements"][-5:] if progress["achievements"] else [],
        "active_goals": len([g for g in data["goals"] if not g["completed"]]),
        "completed_goals": len([g for g in data["goals"] if g["completed"]]),
        "last_study_date": progress["last_study_date"]
    }


def add_notes(notes: str) -> Dict[str, str]:
    """
    Add or update general notes for the student.
    
    Args:
        notes (str): Notes to add or update
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    data["notes"] = notes
    
    success = _save_student_data(data)
    
    if success:
        return {"status": "success", "message": "Notes updated successfully"}
    else:
        return {"status": "error", "message": "Failed to update notes"}


def get_recent_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the most recent study sessions.
    
    Args:
        limit (int): Maximum number of sessions to return (default: 10)
        
    Returns:
        List[Dict[str, Any]]: List of recent study sessions
    """
    data = _load_student_data()
    sessions = data["session_history"][-limit:] if data["session_history"] else []
    return list(reversed(sessions))  # Most recent first


def add_weak_topic(subject: str, topic: str, difficulty_level: str = "struggling", notes: Optional[str] = None) -> Dict[str, str]:
    """
    Add a topic that the student is struggling with or needs to review.
    
    Args:
        subject (str): Subject name (e.g., "Maths", "Physics") 
        topic (str): Specific topic the student is struggling with
        difficulty_level (str): Level of difficulty - "struggling", "needs_review", or "improvement_needed"
        notes (str, optional): Additional notes about why this is a weak topic
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    
    weak_entry = {
        "subject": subject,
        "topic": topic,
        "date_identified": datetime.now().isoformat(),
        "notes": notes or "",
        "times_reviewed": 0,
        "last_reviewed": None
    }
    
    # Add to appropriate category
    if difficulty_level == "struggling":
        # Check if already exists
        if not any(item["topic"] == topic and item["subject"] == subject 
                  for item in data["weak_topics"]["struggling_areas"]):
            data["weak_topics"]["struggling_areas"].append(weak_entry)
    
    elif difficulty_level == "needs_review":
        if not any(item["topic"] == topic and item["subject"] == subject 
                  for item in data["weak_topics"]["needs_review"]):
            data["weak_topics"]["needs_review"].append(weak_entry)
    
    elif difficulty_level == "improvement_needed":
        key = f"{subject}:{topic}"
        if key not in data["weak_topics"]["improvement_needed"]:
            data["weak_topics"]["improvement_needed"][key] = weak_entry
    
    success = _save_student_data(data)
    
    if success:
        return {"status": "success", "message": f"Added '{topic}' in {subject} to {difficulty_level} list"}
    else:
        return {"status": "error", "message": "Failed to add weak topic"}


def update_weak_topic_review(subject: str, topic: str, improvement_notes: Optional[str] = None) -> Dict[str, str]:
    """
    Mark a weak topic as reviewed and potentially improved.
    
    Args:
        subject (str): Subject name
        topic (str): Topic that was reviewed
        improvement_notes (str, optional): Notes about the review session
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    current_time = datetime.now().isoformat()
    found = False
    
    # Search in struggling areas
    for item in data["weak_topics"]["struggling_areas"]:
        if item["topic"] == topic and item["subject"] == subject:
            item["times_reviewed"] += 1
            item["last_reviewed"] = current_time
            if improvement_notes:
                item["notes"] += f" | Review ({current_time}): {improvement_notes}"
            found = True
            break
    
    # Search in needs review
    if not found:
        for item in data["weak_topics"]["needs_review"]:
            if item["topic"] == topic and item["subject"] == subject:
                item["times_reviewed"] += 1
                item["last_reviewed"] = current_time
                if improvement_notes:
                    item["notes"] += f" | Review ({current_time}): {improvement_notes}"
                found = True
                break
    
    # Search in improvement needed
    if not found:
        key = f"{subject}:{topic}"
        if key in data["weak_topics"]["improvement_needed"]:
            item = data["weak_topics"]["improvement_needed"][key]
            item["times_reviewed"] += 1
            item["last_reviewed"] = current_time
            if improvement_notes:
                item["notes"] += f" | Review ({current_time}): {improvement_notes}"
            found = True
    
    if found:
        success = _save_student_data(data)
        if success:
            return {"status": "success", "message": f"Updated review for '{topic}' in {subject}"}
        else:
            return {"status": "error", "message": "Failed to update weak topic"}
    else:
        return {"status": "info", "message": f"Topic '{topic}' in {subject} not found in weak topics"}


def remove_weak_topic(subject: str, topic: str, reason: str = "mastered") -> Dict[str, str]:
    """
    Remove a topic from weak topics list (e.g., when student has mastered it).
    
    Args:
        subject (str): Subject name
        topic (str): Topic to remove
        reason (str): Reason for removal (default: "mastered")
        
    Returns:
        Dict[str, str]: Status message indicating success or failure
    """
    data = _load_student_data()
    removed = False
    
    # Remove from struggling areas
    original_count = len(data["weak_topics"]["struggling_areas"])
    data["weak_topics"]["struggling_areas"] = [
        item for item in data["weak_topics"]["struggling_areas"] 
        if not (item["topic"] == topic and item["subject"] == subject)
    ]
    if len(data["weak_topics"]["struggling_areas"]) < original_count:
        removed = True
    
    # Remove from needs review
    original_count = len(data["weak_topics"]["needs_review"])
    data["weak_topics"]["needs_review"] = [
        item for item in data["weak_topics"]["needs_review"] 
        if not (item["topic"] == topic and item["subject"] == subject)
    ]
    if len(data["weak_topics"]["needs_review"]) < original_count:
        removed = True
    
    # Remove from improvement needed
    key = f"{subject}:{topic}"
    if key in data["weak_topics"]["improvement_needed"]:
        del data["weak_topics"]["improvement_needed"][key]
        removed = True
    
    if removed:
        # Add to achievements
        achievement = f"Mastered weak topic: {topic} in {subject} - {reason}"
        if achievement not in data["progress"]["achievements"]:
            data["progress"]["achievements"].append(achievement)
        
        success = _save_student_data(data)
        if success:
            return {"status": "success", "message": f"Removed '{topic}' from weak topics - {reason}!"}
        else:
            return {"status": "error", "message": "Failed to remove weak topic"}
    else:
        return {"status": "info", "message": f"Topic '{topic}' in {subject} not found in weak topics"}


def get_weak_topics_summary() -> Dict[str, Any]:
    """
    Get a comprehensive summary of all weak topics and areas needing improvement.
    
    Returns:
        Dict[str, Any]: Summary of weak topics by category and subject
    """
    data = _load_student_data()
    weak_topics = data["weak_topics"]
    
    # Organize by subject
    by_subject = {}
    
    # Process struggling areas
    for item in weak_topics["struggling_areas"]:
        subject = item["subject"]
        if subject not in by_subject:
            by_subject[subject] = {"struggling": [], "needs_review": [], "improvement_needed": []}
        by_subject[subject]["struggling"].append(item)
    
    # Process needs review
    for item in weak_topics["needs_review"]:
        subject = item["subject"]
        if subject not in by_subject:
            by_subject[subject] = {"struggling": [], "needs_review": [], "improvement_needed": []}
        by_subject[subject]["needs_review"].append(item)
    
    # Process improvement needed
    for key, item in weak_topics["improvement_needed"].items():
        subject = item["subject"]
        if subject not in by_subject:
            by_subject[subject] = {"struggling": [], "needs_review": [], "improvement_needed": []}
        by_subject[subject]["improvement_needed"].append(item)
    
    return {
        "total_struggling": len(weak_topics["struggling_areas"]),
        "total_needs_review": len(weak_topics["needs_review"]),
        "total_improvement_needed": len(weak_topics["improvement_needed"]),
        "by_subject": by_subject,
        "most_reviewed_topics": sorted(
            [item for item in weak_topics["struggling_areas"] + weak_topics["needs_review"] + list(weak_topics["improvement_needed"].values())],
            key=lambda x: x["times_reviewed"],
            reverse=True
        )[:5]
    }
