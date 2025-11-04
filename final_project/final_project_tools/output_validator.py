import json
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
        1. All 10 students are present
        2. Each student has classes for both days
        3. The format is readable (table structure)
        4. Data is complete and not truncated
        
        Args:
            tool_input: JSON string containing 'schedule' and 'formatted_output'
            
        Returns:
            JSON validation report with score and feedback
        """
        try:
            tool_input = tool_input.strip()
            decoder = json.JSONDecoder()
            data, idx = decoder.raw_decode(tool_input)
            
            # Handle schedule - it might be a string or already parsed
            schedule_data = data.get("schedule", "{}")
            if isinstance(schedule_data, str):
                schedule, _ = decoder.raw_decode(schedule_data)
            else:
                schedule = schedule_data
            formatted_output = data.get("formatted_output", "")
        except (json.JSONDecodeError, ValueError) as e:
            return json.dumps({"valid": False, "clarity_score": 0, "summary": f"Error parsing input: {str(e)}", "issues": [str(e)], "suggestions": []})
        
        issues = []
        suggestions = []
        
        # Check 1: Verify all 10 students are present
        if len(schedule) != 10:
            issues.append(f"Expected 10 students, found {len(schedule)}")
        
        # Check 2: Verify each student has both days
        for student, days in schedule.items():
            if "Day1" not in days or "Day2" not in days:
                issues.append(f"{student} is missing day information")
            elif not days["Day1"] or not days["Day2"]:
                issues.append(f"{student} has empty classes for one or both days")
        
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
            day1_count = len(days.get("Day1", []))
            day2_count = len(days.get("Day2", []))
            student_classes = day1_count + day2_count
            if student_classes != 5:
                issues.append(f"{student} has {student_classes} classes instead of 5")
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

