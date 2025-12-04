import json
import os
from fairlib import AbstractTool

class OutputValidatorTool(AbstractTool):
    name = "OutputValidatorTool"
    description = (
        "Validates that the final schedule output is clear, comprehensive, and easy to understand. "
        "Input: JSON object with 'schedule' (JSON string) and 'formatted_output' (table string). "
        "Returns a validation report with clarity score and suggestions."
    )

    def use(self, tool_input: str) -> str:
        """
        Validates the schedule output for clarity and comprehensibility.
        
        Checks:
        1. All students are present (based on config)
        2. Each student has classes for both days
        3. The format is readable (table structure)
        4. Data is complete and not truncated
        
        Args:
            tool_input: JSON string or dict containing 'schedule' and 'formatted_output'
            
        Returns:
            JSON validation report with score and feedback
        """
        try:
            # Handle both string and dict inputs
            if isinstance(tool_input, dict):
                data = tool_input
            elif isinstance(tool_input, str):
                tool_input = tool_input.strip()
                # Try to parse as JSON, be more forgiving
                try:
                    decoder = json.JSONDecoder()
                    data, idx = decoder.raw_decode(tool_input)
                except json.JSONDecodeError:
                    # If that fails, try standard json.loads
                    data = json.loads(tool_input)
            else:
                return json.dumps({"valid": False, "clarity_score": 0, "summary": "Invalid input type", "issues": ["Input must be string or dict"], "suggestions": []})
            
            # Handle schedule - it might be a string or already parsed
            schedule_data = data.get("schedule", "{}")
            if isinstance(schedule_data, str):
                try:
                    # Try standard parsing first
                    schedule = json.loads(schedule_data)
                except json.JSONDecodeError:
                    try:
                        # Fall back to raw_decode
                        decoder = json.JSONDecoder()
                        schedule, _ = decoder.raw_decode(schedule_data)
                    except:
                        # Last resort: assume it's already a dict or empty
                        schedule = {}
            else:
                schedule = schedule_data
            formatted_output = data.get("formatted_output", "")
        except Exception as e:
            return json.dumps({"valid": False, "clarity_score": 0, "summary": f"Error parsing input: {str(e)}", "issues": [str(e)], "suggestions": []})
        
        issues = []
        suggestions = []
        
        # Load system configuration to get expected values
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(os.path.dirname(current_dir), "system_config.json")
            with open(config_path, 'r') as f:
                config = json.load(f)
            expected_students = config.get("num_students", 10)
            expected_classes = config.get("classes_per_student", 5)
            expected_days = config.get("num_days", 2)
        except:
            # Default values if config not found
            expected_students = 10
            expected_classes = 5
            expected_days = 2
        
        # Check 1: Verify all expected students are present
        if len(schedule) != expected_students:
            issues.append(f"Expected {expected_students} students, found {len(schedule)}")
        
        # Check 2: Verify each student has all expected days
        day_keys = [f"Day{i}" for i in range(1, expected_days + 1)]
        for student, days in schedule.items():
            for day_key in day_keys:
                if day_key not in days:
                    issues.append(f"{student} is missing {day_key} information")
                elif not days[day_key]:
                    issues.append(f"{student} has empty classes for {day_key}")
        
        # Check 3: Verify formatted output exists and has content
        if not formatted_output or len(formatted_output) < 100:
            issues.append("Formatted output is missing or too short")
            suggestions.append("Ensure the table includes headers and all student rows")
        
        # Check 4: Verify formatted output contains key elements
        if formatted_output:
            if "Student" not in formatted_output:
                issues.append("Formatted output missing 'Student' column header")
            if "Day 1" not in formatted_output and "Day1" not in formatted_output:
                issues.append("Formatted output missing Day 1 information")
            if "Day 2" not in formatted_output and "Day2" not in formatted_output:
                issues.append("Formatted output missing Day 2 information")
            
            # Check for table structure
            if not ("+" in formatted_output or "|" in formatted_output or "─" in formatted_output):
                suggestions.append("Consider using a table format for better readability")
        
        # Check 5: Verify class distribution
        total_classes = 0
        for student, days in schedule.items():
            student_classes = sum(len(days.get(day_key, [])) for day_key in day_keys)
            if student_classes != expected_classes:
                issues.append(f"{student} has {student_classes} classes instead of {expected_classes}")
            total_classes += student_classes
        
        # Check 6: Verify period information is included if using new format
        if formatted_output and "(P" not in formatted_output:
            suggestions.append("Consider showing period information for better clarity")
        
        # Calculate clarity score (0-100)
        max_issues = 15  # Maximum expected issues
        score = max(0, 100 - (len(issues) * (100 / max_issues)))
        
        # Generate summary
        if score >= 90:
            summary = "✅ Output is clear, complete, and easy to understand!"
        elif score >= 70:
            summary = "⚠️ Output is acceptable but could be improved"
        else:
            summary = "❌ Output has significant clarity or completeness issues"
        
        # Add general suggestions if score is not perfect
        if score < 100 and not suggestions:
            suggestions.append("Review the output to ensure all information is clearly presented")
        
        report = {
            "valid": len(issues) == 0,
            "clarity_score": round(score, 1),
            "summary": summary,
            "issues": issues,
            "suggestions": suggestions,
            "student_count": len(schedule),
            "total_classes": total_classes,
            "formatted_output_length": len(formatted_output)
        }
        
        return json.dumps(report, indent=2)

