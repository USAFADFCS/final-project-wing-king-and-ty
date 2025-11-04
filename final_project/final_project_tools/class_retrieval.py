import json
from fairlib import AbstractTool

class ClassRetrievalTool(AbstractTool):
    name = "ClassRetrievalTool"
    description = "Retrieves class availability, capacity, and time period information for each day. No input required."

    def use(self, tool_input: str) -> str:
        """
        Returns a JSON string of classes offered each day with maximum student capacities and time periods.
        Format: {"Day": {"ClassName": {"capacity": int, "periods": [period_numbers]}}}
        """
        class_data = {
            "Day1": {
                "Math": {"capacity": 5, "periods": [1, 3, 5]},
                "Science": {"capacity": 6, "periods": [2, 4]},
                "History": {"capacity": 4, "periods": [1, 4]},
                "Art": {"capacity": 5, "periods": [3, 5]},
                "Music": {"capacity": 5, "periods": [2, 4, 6]},
                "PE": {"capacity": 8, "periods": [1, 3, 5, 6]},
            },
            "Day2": {
                "Math": {"capacity": 5, "periods": [1, 3, 5]},
                "Biology": {"capacity": 6, "periods": [2, 4]},
                "English": {"capacity": 6, "periods": [1, 3, 4]},
                "ComputerSci": {"capacity": 5, "periods": [2, 5, 6]},
                "Music": {"capacity": 5, "periods": [3, 4, 6]},
                "PE": {"capacity": 8, "periods": [1, 2, 5]},
            },
        }
        return json.dumps(class_data)
