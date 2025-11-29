"""
Habit Tracker Tool - Track study progress and habits
"""

import json
import os
from datetime import datetime


TRACKER_FILE = "study_progress.json"


def load_tracker():
    """Load tracker data from file"""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, 'r') as f:
            return json.load(f)
    return {"entries": []}


def save_tracker(data):
    """Save tracker data to file"""
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def track_activity(task: str, hours: float = None, status: str = "completed") -> dict:
    """
    Track a study activity
    
    Args:
        task: Task description
        hours: Hours spent (optional)
        status: Status of task (completed/in_progress)
        
    Returns:
        dict: Confirmation message
    """
    data = load_tracker()
    
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task": task,
        "hours": hours,
        "status": status
    }
    
    data["entries"].append(entry)
    save_tracker(data)
    
    return {
        "type": "tracker",
        "action": "added",
        "entry": entry,
        "message": f"✅ Tracked: {task}" + (f" ({hours}h)" if hours else "")
    }


def get_progress() -> dict:
    """
    Get all tracked progress
    
    Returns:
        dict: All entries and summary
    """
    data = load_tracker()
    entries = data.get("entries", [])
    
    total_hours = sum(e.get("hours", 0) or 0 for e in entries)
    total_tasks = len(entries)
    
    return {
        "type": "progress",
        "total_tasks": total_tasks,
        "total_hours": total_hours,
        "entries": entries
    }


def clear_tracker() -> dict:
    """Clear all tracker data"""
    save_tracker({"entries": []})
    return {
        "type": "tracker",
        "action": "cleared",
        "message": "🗑️ Tracker cleared"
    }

