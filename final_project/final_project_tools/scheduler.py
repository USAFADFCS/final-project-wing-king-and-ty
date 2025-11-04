import random
import json
from fairlib import AbstractTool

class SchedulerTool(AbstractTool):
    name = "SchedulerTool"
    description = "Generates a preliminary 2-day schedule for 10 students with period assignments. Input: JSON string of class_data from ClassRetrievalTool."

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
            class_data, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"error": f"JSON parsing error: {str(e)}"})
        students = [f"Student{i}" for i in range(1, 11)]
        schedule = {}
        
        # Track remaining capacity for each class per day (NOT per period)
        # Capacity is shared across all periods for a given class
        capacity_tracker = {}
        for day in ["Day1", "Day2"]:
            for class_name, info in class_data[day].items():
                key = (day, class_name)
                capacity_tracker[key] = info["capacity"]

        # Assign classes to each student
        for student in students:
            schedule[student] = {"Day1": [], "Day2": []}
            assigned_classes = set()  # Track unique classes
            
            # We need exactly 5 classes, with at least 1 per day
            target_day1 = random.randint(1, 4)  # 1-4 classes on Day1
            target_day2 = 5 - target_day1        # Remaining on Day2
            
            # Assign Day1 classes
            day1_classes_list = list(class_data["Day1"].keys())
            random.shuffle(day1_classes_list)
            
            for class_name in day1_classes_list:
                if len(schedule[student]["Day1"]) >= target_day1:
                    break
                if class_name in assigned_classes:
                    continue
                    
                # Check if class has capacity remaining
                if capacity_tracker.get(("Day1", class_name), 0) <= 0:
                    continue
                
                # Find available period (no time conflict)
                used_periods = [entry["period"] for entry in schedule[student]["Day1"]]
                available_periods = [
                    p for p in class_data["Day1"][class_name]["periods"]
                    if p not in used_periods
                ]
                
                if available_periods:
                    period = random.choice(available_periods)
                    schedule[student]["Day1"].append({
                        "class": class_name,
                        "period": period
                    })
                    assigned_classes.add(class_name)
                    capacity_tracker[("Day1", class_name)] -= 1
            
            # Assign Day2 classes
            day2_classes_list = list(class_data["Day2"].keys())
            random.shuffle(day2_classes_list)
            
            for class_name in day2_classes_list:
                if len(schedule[student]["Day2"]) >= target_day2:
                    break
                if class_name in assigned_classes:
                    continue
                    
                # Check if class has capacity remaining
                if capacity_tracker.get(("Day2", class_name), 0) <= 0:
                    continue
                
                # Find available period (no time conflict)
                used_periods = [entry["period"] for entry in schedule[student]["Day2"]]
                available_periods = [
                    p for p in class_data["Day2"][class_name]["periods"]
                    if p not in used_periods
                ]
                
                if available_periods:
                    period = random.choice(available_periods)
                    schedule[student]["Day2"].append({
                        "class": class_name,
                        "period": period
                    })
                    assigned_classes.add(class_name)
                    capacity_tracker[("Day2", class_name)] -= 1
            
            # If we didn't get exactly 5, try to fill up
            while len(schedule[student]["Day1"]) + len(schedule[student]["Day2"]) < 5:
                # Try adding to either day
                for day in ["Day1", "Day2"]:
                    if len(schedule[student]["Day1"]) + len(schedule[student]["Day2"]) >= 5:
                        break
                    if day == "Day1" and len(schedule[student]["Day1"]) >= 5:
                        continue
                    if day == "Day2" and len(schedule[student]["Day2"]) >= 5:
                        continue
                        
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
                            break
                else:
                    # Couldn't add more classes, break out
                    break

        return json.dumps(schedule)
