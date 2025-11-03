from fairlib import FairLLMTool
from tabulate import tabulate

class StructuredOutputFormatterTool(FairLLMTool):
    name = "StructuredOutputFormatterTool"
    description = "Formats the final schedule into a readable table."

    def execute(self, schedule):
        table = []
        for student, days in schedule.items():
            row = [
                student,
                ", ".join(days["Day1"]),
                ", ".join(days["Day2"]),
            ]
            table.append(row)

        headers = ["Student", "Day 1 Classes", "Day 2 Classes"]
        return tabulate(table, headers, tablefmt="grid")
