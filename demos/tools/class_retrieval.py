from fairlib import FairLLMTool

class ClassRetrievalTool(FairLLMTool):
    name = "ClassRetrievalTool"
    description = "Retrieves class availability and capacity information for each day."

    def execute(self):
        """
        Returns a dictionary of classes offered each day with maximum student capacities.
        """
        return {
            "Day1": {
                "Math": 5,
                "Science": 6,
                "History": 4,
                "Art": 5,
                "Music": 5,
                "PE": 8,
            },
            "Day2": {
                "Math": 5,
                "Biology": 6,
                "English": 6,
                "ComputerSci": 5,
                "Music": 5,
                "PE": 8,
            },
        }
