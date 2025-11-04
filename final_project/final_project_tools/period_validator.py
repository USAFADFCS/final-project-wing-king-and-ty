import json
from fairlib import AbstractTool

class PeriodConflictCheckerTool(AbstractTool):
    name = "PeriodConflictCheckerTool"
    description = "Checks that no student has two classes in the same period on the same day. Input: JSON string of schedule data with periods."

    def use(self, tool_input: str) -> str:
        """
        Validates that students don't have period conflicts.
        
        Args:
            tool_input: JSON string of schedule with period assignments
            
        Returns:
            JSON validation report with conflicts
        """
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            schedule, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "conflicts": [], "error": f"JSON parsing error: {str(e)}"})
        conflicts = []
        
        for student, days in schedule.items():
            # Check Day1 for period conflicts
            day1_periods = {}
            for class_entry in days.get("Day1", []):
                period = class_entry.get("period")
                class_name = class_entry.get("class")
                if period in day1_periods:
                    conflicts.append({
                        "student": student,
                        "day": "Day1",
                        "period": period,
                        "classes": [day1_periods[period], class_name]
                    })
                else:
                    day1_periods[period] = class_name
            
            # Check Day2 for period conflicts
            day2_periods = {}
            for class_entry in days.get("Day2", []):
                period = class_entry.get("period")
                class_name = class_entry.get("class")
                if period in day2_periods:
                    conflicts.append({
                        "student": student,
                        "day": "Day2",
                        "period": period,
                        "classes": [day2_periods[period], class_name]
                    })
                else:
                    day2_periods[period] = class_name
        
        return json.dumps({
            "valid": len(conflicts) == 0,
            "conflicts": conflicts,
            "total_conflicts": len(conflicts)
        })

