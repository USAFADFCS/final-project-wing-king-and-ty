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
            if not isinstance(days, dict):
                continue
            
            # Get all days dynamically
            day_keys = sorted([k for k in days.keys() if k.startswith("Day")])
            if not day_keys:
                continue
                
            # Format classes for each day
            formatted_days = []
            for day in day_keys:
                day_classes = []
                for entry in days.get(day, []):
                    if isinstance(entry, dict) and "class" in entry and "period" in entry:
                        day_classes.append(f"{entry['class']} (P{entry['period']})")
                    elif isinstance(entry, dict) and "class" in entry:
                        day_classes.append(str(entry['class']))
                    else:
                        day_classes.append(str(entry))
                formatted_days.append(", ".join(day_classes) if day_classes else "(none)")
            
            row = [student] + formatted_days
            table.append(row)
        
        if not table:
            return "Error: No valid student schedules found to format"

        # Get day headers dynamically
        first_student_days = sorted([k for k in list(schedule.values())[0].keys() if k.startswith("Day")])
        headers = ["Student"] + [f"{day} Classes (Period)" for day in first_student_days]
        
        # Generate HTML output
        html_output = self._generate_html_table(table, headers)
        
        # Also generate text output for backward compatibility
        text_output = tabulate(table, headers, tablefmt="grid")
        
        # Store the HTML formatted output for later retrieval
        StructuredOutputFormatterTool.last_formatted_output = html_output
        
        return html_output
    
    def _generate_html_table(self, table, headers):
        """Generate a beautifully styled HTML table."""
        html = """
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px;">
            <h2 style="text-align: center; color: #2d3748; margin-bottom: 20px; font-size: 24px;">
                📅 Student Class Schedule
            </h2>
            <div style="overflow-x: auto; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <thead>
                        <tr style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white;">
        """
        
        # Add headers
        for i, header in enumerate(headers):
            padding = "16px 24px" if i == 0 else "16px 12px"
            text_align = "left" if i == 0 else "left"
            html += f"""
                            <th style="padding: {padding}; text-align: {text_align}; font-weight: 600; font-size: 15px; border-bottom: 3px solid #5a67d8;">
                                {header}
                            </th>
            """
        
        html += """
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add rows
        for i, row in enumerate(table):
            bg_color = "#f7fafc" if i % 2 == 0 else "#ffffff"
            html += f"""
                        <tr style="background-color: {bg_color}; transition: background-color 0.2s;">
            """
            
            for j, cell in enumerate(row):
                padding = "14px 24px" if j == 0 else "14px 12px"
                font_weight = "600" if j == 0 else "400"
                color = "#2d3748" if j == 0 else "#4a5568"
                border_color = "#e2e8f0"
                
                # Parse and style individual classes
                if j > 0:  # Day columns
                    styled_cell = self._style_classes(cell)
                else:
                    styled_cell = cell
                
                html += f"""
                            <td style="padding: {padding}; border-bottom: 1px solid {border_color}; color: {color}; font-weight: {font_weight};">
                                {styled_cell}
                            </td>
                """
            
            html += """
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
            <div style="margin-top: 15px; text-align: center; color: #718096; font-size: 12px;">
                <p style="margin: 5px 0;">✅ Schedule generated successfully | Total Students: """ + str(len(table)) + """</p>
            </div>
        </div>
        """
        
        return html
    
    def _style_classes(self, classes_text):
        """Add styling to individual classes."""
        if classes_text == "(none)":
            return '<span style="color: #a0aec0; font-style: italic;">No classes</span>'
        
        # Split by comma and style each class
        classes = classes_text.split(", ")
        styled_classes = []
        
        # Color palette for classes
        colors = [
            "#667eea",  # Purple
            "#f093fb",  # Pink
            "#4facfe",  # Blue
            "#43e97b",  # Green
            "#fa709a",  # Rose
            "#feca57",  # Yellow
            "#48dbfb",  # Cyan
            "#ff6348",  # Orange
        ]
        
        for i, class_item in enumerate(classes):
            color = colors[i % len(colors)]
            styled_classes.append(
                f'<span style="display: inline-block; padding: 4px 10px; margin: 2px 4px 2px 0; '
                f'background: {color}20; color: {color}; border-left: 3px solid {color}; '
                f'border-radius: 4px; font-size: 13px; font-weight: 500;">'
                f'{class_item}</span>'
            )
        
        return '<div style="line-height: 2;">' + ''.join(styled_classes) + '</div>'
