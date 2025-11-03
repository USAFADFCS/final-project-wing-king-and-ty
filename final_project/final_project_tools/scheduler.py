import random
from fairlib import FairLLMTool

class SchedulerTool(FairLLMTool):
    name = "SchedulerTool"
    description = "Generates a preliminary 2-day schedule for 10 students."

    def execute(self, class_data):
        """
        Args:
            class_data (dict): Output from ClassRetrievalTool (classes per day)

        Returns:
            dict: schedule = { 'Student1': {'Day1': [...], 'Day2': [...]}, ... }
        """
        students = [f"Student{i}" for i in range(1, 11)]
        schedule = {}

        for student in students:
            schedule[student] = {"Day1": [], "Day2": []}
            # Each student must take 5 total unique classes, at least 1 per day
            all_classes = list(set(class_data["Day1"]) | set(class_data["Day2"]))
            chosen_classes = random.sample(all_classes, 5)
            random.shuffle(chosen_classes)

            # Distribute randomly between Day1 and Day2
            day1_classes = random.sample(chosen_classes, random.randint(1, 4))
            day2_classes = [c for c in chosen_classes if c not in day1_classes]

            schedule[student]["Day1"] = day1_classes
            schedule[student]["Day2"] = day2_classes

        return schedule
