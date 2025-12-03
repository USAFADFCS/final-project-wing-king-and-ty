# Dynamic Configuration Guide

## Overview

The Multi-Agent Class Scheduling System now supports **dynamic configuration** through the GUI, allowing you to customize both the class database and system parameters without editing code.

## Features

### 1. 📚 Class Database Management

Manage all available classes through the GUI:

- **View All Classes**: See all classes organized by day with their capacities and time periods
- **Add/Update Classes**: Create new classes or modify existing ones
- **Delete Classes**: Remove classes from the database
- **Persistent Storage**: All changes are saved to `class_database.json`

#### Class Properties:
- **Day**: Which day the class is offered (e.g., `Day1`, `Day2`)
- **Class Name**: Name of the class (e.g., `Math`, `Science`)
- **Capacity**: Maximum number of students (e.g., `5`)
- **Periods**: Time periods when the class is offered (e.g., `1, 3, 5`)

### 2. ⚙️ System Configuration

Customize scheduling parameters:

- **Number of Students**: Total students to schedule
- **Classes per Student**: How many classes each student needs
- **Number of Days**: Schedule duration in days
- **Periods per Day**: Time periods available per day
- **Minimum Classes per Day**: Minimum classes each student must have per day

All settings are saved to `system_config.json` and agents are automatically reinitialized when configuration changes.

## Configuration Files

### `class_database.json`

Stores all class information:

```json
{
    "Day1": {
        "Math": {
            "capacity": 5,
            "periods": [1, 3, 5]
        },
        "Science": {
            "capacity": 6,
            "periods": [2, 4]
        }
    },
    "Day2": {
        "Math": {
            "capacity": 5,
            "periods": [1, 3, 5]
        },
        "Biology": {
            "capacity": 6,
            "periods": [2, 4]
        }
    }
}
```

### `system_config.json`

Stores system parameters:

```json
{
    "num_students": 10,
    "classes_per_student": 5,
    "num_days": 2,
    "periods_per_day": 6,
    "min_classes_per_day": 1
}
```

## Using the GUI

### Managing Classes

1. Navigate to the **📚 Manage Classes** tab
2. View current classes in the left panel
3. Use the right panel to:
   - **Add a class**: Fill in all fields and click "Add/Update Class"
   - **Update a class**: Enter the same day and class name with new values
   - **Delete a class**: Enter day and class name in the delete section

#### Example: Adding a Class

```
Day: Day1
Class Name: Chemistry
Capacity: 4
Periods: 2, 4, 6
```

Click **➕ Add/Update Class**

### Updating System Configuration

1. Navigate to the **⚙️ System Config** tab
2. View current settings in the left panel
3. Modify values in the right panel:
   - Enter new values for each parameter
   - Click **💾 Save Configuration**
4. Agents will automatically reinitialize with the new settings

#### Example: Scheduling 20 Students

```
Number of Students: 20
Classes per Student: 6
Number of Days: 3
Periods per Day: 7
Minimum Classes per Day: 2
```

Click **💾 Save Configuration**

## Validation Rules

### Class Management
- ✅ Capacity must be at least 1
- ✅ At least one period must be specified
- ✅ Periods must be comma-separated numbers
- ✅ Day and class name are required

### System Configuration
- ✅ All values must be at least 1
- ✅ `classes_per_student` ≥ `min_classes_per_day` × `num_days`
- ✅ Configuration must be mathematically feasible

## Dynamic Behavior

### Scheduler Tool
- Automatically adapts to the number of students
- Distributes classes according to `classes_per_student`
- Ensures `min_classes_per_day` constraint
- Works with any number of days in the database

### Agent Instructions
- Agents receive updated role descriptions with new parameters
- Validation tools check against current configuration
- Formatter adjusts to display all days and students

## Best Practices

### Planning Your Schedule

1. **Start with Configuration**: Set your system parameters first
2. **Add Classes**: Create enough classes to accommodate all students
3. **Check Capacity**: Ensure total capacity ≥ number of students
4. **Test Generation**: Run a schedule and check validation results
5. **Iterate**: Adjust classes or configuration as needed

### Capacity Planning

Total capacity should satisfy:

```
total_capacity ≥ num_students × classes_per_student / num_days
```

Example for 10 students × 5 classes / 2 days = 25 class slots per day needed

### Period Distribution

- Distribute periods evenly to avoid scheduling conflicts
- More periods per class = more flexibility
- Consider limiting periods if classes have specific time requirements

## Troubleshooting

### Classes Not Appearing
- Check that the day name matches exactly (case-sensitive)
- Refresh the class display
- Verify `class_database.json` was saved correctly

### Schedule Generation Fails
- Ensure sufficient capacity across all classes
- Check that periods don't create impossible constraints
- Verify configuration values are feasible

### Validation Errors
- Review capacity limits (may need to increase)
- Check for period conflicts in the database
- Ensure enough classes exist for all students

## Advanced Usage

### Multiple Days

You can add any number of days to the database:

```json
{
    "Monday": { ... },
    "Tuesday": { ... },
    "Wednesday": { ... },
    "Thursday": { ... },
    "Friday": { ... }
}
```

Update `num_days` in the configuration to match.

### Custom Student Numbers

The system scales from 1 to any reasonable number of students (tested up to 100). Larger numbers may require:
- More classes
- Higher capacities
- More time to generate schedules

### Flexible Periods

Periods can be any positive integers. Use whatever numbering makes sense for your institution:
- Standard: `1, 2, 3, 4, 5, 6`
- With lunch: `1, 2, 3, 5, 6, 7` (skip 4 for lunch)
- Custom times: `8, 9, 10, 13, 14, 15` (using hours)

## Technical Details

### File Locations
- `final_project/class_database.json` - Class data
- `final_project/system_config.json` - System settings
- Both are created automatically if missing (with defaults)

### Auto-Reload
- Class database is loaded on each schedule generation
- Configuration is loaded when agents are initialized
- Changes take effect immediately (no restart needed)

### Thread Safety
- File operations use atomic writes
- Each operation is independent
- Safe for multiple users (though not recommended for concurrent editing)

## Summary

The dynamic configuration system provides:

✅ **Flexibility**: Customize all aspects of scheduling  
✅ **Ease of Use**: No code editing required  
✅ **Persistence**: Changes are saved automatically  
✅ **Validation**: Built-in checks prevent invalid configurations  
✅ **Real-time**: Changes take effect immediately  

Perfect for testing different scenarios, adapting to changing needs, or demonstrating the system's versatility!

