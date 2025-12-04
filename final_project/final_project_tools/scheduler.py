import random
import json
import os
from fairlib import AbstractTool

class SchedulerTool(AbstractTool):
    name = "SchedulerTool"
    description = "Generates a schedule for students with period assignments. Reads configuration from system_config.json (number of students, classes per student, etc.). Input: JSON string of class_data from ClassRetrievalTool (with Day1, Day2 structure). Note: Do NOT pass student count - it's loaded automatically from config."

    def use(self, tool_input: str) -> str:
        """
        Args:
            tool_input (str): JSON string of class_data with capacity and periods

        Returns:
            str: JSON string of schedule with period assignments
            Format: {'Student1': {'Day1': [{'class': 'Math', 'period': 1}, ...], 'Day2': [...]}, ...}
        """
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            parsed_input, idx = decoder.raw_decode(tool_input)
            
            # Handle case where agent passes {"students": X, "classes": {...}}
            # We only need the class_data part
            if isinstance(parsed_input, dict) and "classes" in parsed_input:
                class_data = parsed_input["classes"]
            else:
                class_data = parsed_input
                
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"error": f"JSON parsing error: {str(e)}"})
        
        # Load system configuration
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(os.path.dirname(current_dir), "system_config.json")
            with open(config_path, 'r') as f:
                config = json.load(f)
        except:
            # Default configuration if file not found
            config = {
                "num_students": 10,
                "classes_per_student": 5,
                "num_days": 2,
                "min_classes_per_day": 1
            }
        
        # Generate student list based on config
        students = [f"Student{i}" for i in range(1, config["num_students"] + 1)]
        
        # Get list of days from class_data
        days = list(class_data.keys())
        
        schedule = {}
        
        # Track remaining capacity for each class per day (NOT per period)
        # Capacity is shared across all periods for a given class
        capacity_tracker = {}
        for day in days:
            if day in class_data:
                for class_name, info in class_data[day].items():
                    key = (day, class_name)
                    capacity_tracker[key] = info["capacity"]

        # Assign classes to each student
        for student in students:
            # Initialize schedule for all days
            schedule[student] = {day: [] for day in days}
            assigned_classes = set()  # Track unique classes
            
            # Distribute classes across days
            # Ensure at least min_classes_per_day per day
            num_days = len(days)
            classes_per_student = config["classes_per_student"]
            min_per_day = config["min_classes_per_day"]
            
            # Calculate distribution
            remaining_classes = classes_per_student - (min_per_day * num_days)
            day_targets = {day: min_per_day for day in days}
            
            # Distribute remaining classes randomly
            for _ in range(remaining_classes):
                random_day = random.choice(days)
                day_targets[random_day] += 1
            
            # Assign classes for each day
            for day in days:
                if day not in class_data:
                    continue
                
                target_for_day = day_targets[day]
                classes_list = list(class_data[day].keys())
                random.shuffle(classes_list)
                
                for class_name in classes_list:
                    if len(schedule[student][day]) >= target_for_day:
                        break
                    if class_name in assigned_classes:
                        continue
                        
                    # Check if class has capacity remaining
                    if capacity_tracker.get((day, class_name), 0) <= 0:
                        continue
                    
                    # Find available period (no time conflict)
                    used_periods = [entry["period"] for entry in schedule[student][day]]
                    available_periods = [
                        p for p in class_data[day][class_name]["periods"]
                        if p not in used_periods
                    ]
                    
                    if available_periods:
                        period = random.choice(available_periods)
                        schedule[student][day].append({
                            "class": class_name,
                            "period": period
                        })
                        assigned_classes.add(class_name)
                        capacity_tracker[(day, class_name)] -= 1
            
            # If we didn't meet the target, try to fill up
            total_assigned = sum(len(schedule[student][day]) for day in days)
            while total_assigned < classes_per_student:
                added = False
                for day in days:
                    if day not in class_data:
                        continue
                    if total_assigned >= classes_per_student:
                        break
                        
                    for class_name in class_data[day].keys():
                        if class_name in assigned_classes:
                            continue
                        if capacity_tracker.get((day, class_name), 0) <= 0:
                            continue
                        
                        used_periods = [entry["period"] for entry in schedule[student][day]]
                        available_periods = [
                            p for p in class_data[day][class_name]["periods"]
                            if p not in used_periods
                        ]
                        if available_periods:
                            period = random.choice(available_periods)
                            schedule[student][day].append({
                                "class": class_name,
                                "period": period
                            })
                            assigned_classes.add(class_name)
                            capacity_tracker[(day, class_name)] -= 1
                            total_assigned += 1
                            added = True
                            break
                    if added:
                        break
                
                if not added:
                    # Couldn't add more classes, break out
                    break

        return json.dumps(schedule)
