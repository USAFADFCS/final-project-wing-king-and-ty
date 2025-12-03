import json
import os
from fairlib import AbstractTool

class ClassRetrievalTool(AbstractTool):
    name = "ClassRetrievalTool"
    description = "Retrieves class availability, capacity, and time period information for each day. No input required."

    def use(self, tool_input: str) -> str:
        """
        Returns a JSON string of classes offered each day with maximum student capacities and time periods.
        Format: {"Day": {"ClassName": {"capacity": int, "periods": [period_numbers]}}}
        """
        # Get the path to the class database file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(os.path.dirname(current_dir), "class_database.json")
        
        # Load class data from the database file
        try:
            with open(db_path, 'r') as f:
                class_data = json.load(f)
        except FileNotFoundError:
            return json.dumps({"error": f"Database file not found at {db_path}"})
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON format in database file"})
        
        return json.dumps(class_data)
