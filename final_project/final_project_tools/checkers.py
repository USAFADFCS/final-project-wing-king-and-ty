from fairlib import FairLLMTool

# --- Ensure 5 total classes per student ---
class ClassNumberCheckerTool(FairLLMTool):
    name = "ClassNumberCheckerTool"
    description = "Checks that each student takes exactly 5 total classes."

    def execute(self, schedule):
        invalid = []
        for student, days in schedule.items():
            total_classes = len(days["Day1"]) + len(days["Day2"])
            if total_classes != 5:
                invalid.append(student)
        return {"valid": len(invalid) == 0, "invalid_students": invalid}


# --- Ensure no duplicate classes for the same student ---
class UniqueAttendanceCheckerTool(FairLLMTool):
    name = "UniqueAttendanceCheckerTool"
    description = "Ensures each student only attends unique classes."

    def execute(self, schedule):
        invalid = []
        for student, days in schedule.items():
            all_classes = days["Day1"] + days["Day2"]
            if len(all_classes) != len(set(all_classes)):
                invalid.append(student)
        return {"valid": len(invalid) == 0, "invalid_students": invalid}


# --- Check if any class exceeds capacity ---
class ClassAttendanceCheckerTool(FairLLMTool):
    name = "ClassAttendanceCheckerTool"
    description = "Ensures that no class exceeds its maximum capacity."

    def execute(self, schedule, class_data):
        counts = {}
        for student, days in schedule.items():
            for day, classes in days.items():
                for c in classes:
                    counts[(day, c)] = counts.get((day, c), 0) + 1

        exceeded = []
        for (day, c), num in counts.items():
            max_allowed = class_data.get(day, {}).get(c, None)
            if max_allowed is not None and num > max_allowed:
                exceeded.append((day, c, num, max_allowed))

        return {"valid": len(exceeded) == 0, "exceeded_classes": exceeded}


# --- Validate 6 unique courses per day ---
class ScheduleValidatorTool(FairLLMTool):
    name = "ScheduleValidatorTool"
    description = "Ensures that each day has exactly 6 unique courses offered."

    def execute(self, class_data):
        valid_days = []
        invalid_days = []
        for day, classes in class_data.items():
            if len(classes.keys()) == 6:
                valid_days.append(day)
            else:
                invalid_days.append(day)
        return {"valid": len(invalid_days) == 0, "invalid_days": invalid_days}


# --- Ensure all assigned classes exist in offerings ---
class ClassCounterCheckerTool(FairLLMTool):
    name = "ClassCounterCheckerTool"
    description = "Ensures all scheduled classes are from the offered course list."

    def execute(self, schedule, class_data):
        invalid_entries = []
        all_offered = set(sum([list(v.keys()) for v in class_data.values()], []))

        for student, days in schedule.items():
            for day, classes in days.items():
                for c in classes:
                    if c not in all_offered:
                        invalid_entries.append((student, day, c))

        return {"valid": len(invalid_entries) == 0, "invalid_entries": invalid_entries}
