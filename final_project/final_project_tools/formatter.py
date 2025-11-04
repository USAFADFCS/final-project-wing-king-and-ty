import json
from fairlib import AbstractTool
from tabulate import tabulate

class StructuredOutputFormatterTool(AbstractTool):
    name = "StructuredOutputFormatterTool"
    description = "Formats the final schedule into a readable table with periods. Input: JSON string of schedule data."
    
    # Class variable to store the last formatted output
    last_formatted_output = None

    def use(self, tool_input: str) -> str:
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            data, idx = decoder.raw_decode(tool_input)
        except (json.JSONDecodeError, ValueError) as e:
            return f"Error parsing schedule: {str(e)}"
        
        # Handle case where schedule is wrapped in an object
        if "schedule" in data and isinstance(data["schedule"], dict):
            schedule = data["schedule"]
        else:
            schedule = data
        
        table = []
        for student, days in schedule.items():
            # Skip non-student entries (like class_data)
            if not isinstance(days, dict) or "Day1" not in days or "Day2" not in days:
                continue
            # Format Day 1 classes with periods
            day1_formatted = []
            for entry in days.get("Day1", []):
                if isinstance(entry, dict) and "class" in entry and "period" in entry:
                    day1_formatted.append(f"{entry['class']} (P{entry['period']})")
                elif isinstance(entry, dict) and "class" in entry:
                    day1_formatted.append(str(entry['class']))
                else:
                    day1_formatted.append(str(entry))
            
            # Format Day 2 classes with periods
            day2_formatted = []
            for entry in days.get("Day2", []):
                if isinstance(entry, dict) and "class" in entry and "period" in entry:
                    day2_formatted.append(f"{entry['class']} (P{entry['period']})")
                elif isinstance(entry, dict) and "class" in entry:
                    day2_formatted.append(str(entry['class']))
                else:
                    day2_formatted.append(str(entry))
            
            row = [
                student,
                ", ".join(day1_formatted) if day1_formatted else "(none)",
                ", ".join(day2_formatted) if day2_formatted else "(none)",
            ]
            table.append(row)
        
        if not table:
            return "Error: No valid student schedules found to format"

        headers = ["Student", "Day 1 Classes (Period)", "Day 2 Classes (Period)"]
        formatted_output = tabulate(table, headers, tablefmt="grid")
        
        # Store the formatted output for later retrieval
        StructuredOutputFormatterTool.last_formatted_output = formatted_output
        
        return formatted_output
