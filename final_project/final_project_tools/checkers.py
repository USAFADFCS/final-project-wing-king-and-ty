import json
from fairlib import AbstractTool

# --- Ensure 5 total classes per student ---
class ClassNumberCheckerTool(AbstractTool):
    name = "ClassNumberCheckerTool"
    description = "Checks that each student takes exactly 5 total classes. Input: JSON string of schedule data."

    def use(self, tool_input: str) -> str:
        try:
            # Try to parse JSON, handling potential trailing whitespace or data
            tool_input = tool_input.strip()
            # Find the last complete JSON object
            decoder = json.JSONDecoder()
            schedule, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "invalid_students": [], "error": f"JSON parsing error: {str(e)}"})
        
        invalid = []
        for student, days in schedule.items():
            total_classes = len(days.get("Day1", [])) + len(days.get("Day2", []))
            if total_classes != 5:
                invalid.append(student)
        return json.dumps({"valid": len(invalid) == 0, "invalid_students": invalid})


# --- Ensure no duplicate classes for the same student ---
class UniqueAttendanceCheckerTool(AbstractTool):
    name = "UniqueAttendanceCheckerTool"
    description = "Ensures each student only attends unique classes. Input: JSON string of schedule data."

    def use(self, tool_input: str) -> str:
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            schedule, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "invalid_students": [], "error": f"JSON parsing error: {str(e)}"})
        
        invalid = []
        for student, days in schedule.items():
            # Extract class names from schedule entries (which may include period info)
            day1_classes = [entry.get("class", entry) if isinstance(entry, dict) else entry for entry in days.get("Day1", [])]
            day2_classes = [entry.get("class", entry) if isinstance(entry, dict) else entry for entry in days.get("Day2", [])]
            all_classes = day1_classes + day2_classes
            if len(all_classes) != len(set(all_classes)):
                invalid.append(student)
        return json.dumps({"valid": len(invalid) == 0, "invalid_students": invalid})


# --- Check if any class exceeds capacity ---
class ClassAttendanceCheckerTool(AbstractTool):
    name = "ClassAttendanceCheckerTool"
    description = "Ensures that no class exceeds its maximum capacity. Input: JSON object with 'schedule' and 'class_data' keys."

    def use(self, tool_input: str) -> str:
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            data, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "exceeded_classes": [], "error": f"JSON parsing error: {str(e)}"})
        
        schedule = data.get("schedule", data)
        class_data = data.get("class_data", {})
        
        counts = {}
        for student, days in schedule.items():
            for day, classes in days.items():
                for entry in classes:
                    # Extract class name (handle both old and new format)
                    class_name = entry.get("class", entry) if isinstance(entry, dict) else entry
                    counts[(day, class_name)] = counts.get((day, class_name), 0) + 1

        exceeded = []
        for (day, class_name), num in counts.items():
            class_info = class_data.get(day, {}).get(class_name, None)
            # Handle both old format (int capacity) and new format (dict with capacity)
            if isinstance(class_info, dict):
                max_allowed = class_info.get("capacity")
            else:
                max_allowed = class_info
            
            if max_allowed is not None and num > max_allowed:
                exceeded.append([day, class_name, num, max_allowed])

        return json.dumps({"valid": len(exceeded) == 0, "exceeded_classes": exceeded})


# --- Validate 6 unique courses per day ---
class ScheduleValidatorTool(AbstractTool):
    name = "ScheduleValidatorTool"
    description = "Ensures that each day has exactly 6 unique courses offered. Input: JSON string of class_data."

    def use(self, tool_input: str) -> str:
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            class_data, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "invalid_days": [], "error": f"JSON parsing error: {str(e)}"})
        valid_days = []
        invalid_days = []
        for day, classes in class_data.items():
            if len(classes.keys()) == 6:
                valid_days.append(day)
            else:
                invalid_days.append(day)
        return json.dumps({"valid": len(invalid_days) == 0, "invalid_days": invalid_days})


# --- Ensure all assigned classes exist in offerings ---
class ClassCounterCheckerTool(AbstractTool):
    name = "ClassCounterCheckerTool"
    description = "Ensures all scheduled classes are from the offered course list. Input: JSON object with 'schedule' and 'class_data' keys."

    def use(self, tool_input: str) -> str:
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            data, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "invalid_entries": [], "error": f"JSON parsing error: {str(e)}"})
        
        schedule = data.get("schedule", data)
        class_data = data.get("class_data", {})
        
        invalid_entries = []
        all_offered = set(sum([list(v.keys()) for v in class_data.values()], []))

        for student, days in schedule.items():
            for day, classes in days.items():
                for entry in classes:
                    # Extract class name (handle both old and new format)
                    class_name = entry.get("class", entry) if isinstance(entry, dict) else entry
                    if class_name not in all_offered:
                        invalid_entries.append([student, day, class_name])

        return json.dumps({"valid": len(invalid_entries) == 0, "invalid_entries": invalid_entries})
