# 🎓 AI-Powered Class Scheduling System

> **An intelligent multi-agent scheduling system built with the FAIR-LLM framework**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FAIR-LLM](https://img.shields.io/badge/FAIR--LLM-v0.1+-green.svg)](https://github.com/fair-llm)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [System Versions](#-system-versions)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dynamic Configuration](#-dynamic-configuration)
- [Architecture](#-architecture)
- [Custom Tools](#-custom-tools)
- [Configuration Files](#-configuration-files)
- [Troubleshooting](#-troubleshooting)
- [Customization](#-customization)
- [Learning Objectives](#-learning-objectives)
- [Contributing](#-contributing)

---

## 🎯 Overview

This project demonstrates an **AI-powered class scheduling system** that creates optimized student schedules while respecting complex constraints. Built with the FAIR-LLM framework, it showcases both single-agent and multi-agent architectures with a modern web-based GUI.

### What It Does

Creates class schedules for students across multiple days, ensuring:
- ✅ Each student takes the **exact number of required classes**
- ✅ **At least minimum classes per day** for each student
- ✅ **No class exceeds capacity**
- ✅ **No period conflicts** (students can't be in two places at once)
- ✅ **All classes are unique** per student (no duplicates)
- ✅ Classes are offered during specific **time periods**

### Why It's Special

- 🎨 **Beautiful Web GUI** with real-time progress visualization
- 🤖 **Multi-Agent Architecture** with specialized AI agents
- ⚙️ **Fully Dynamic Configuration** - no code editing required
- 📊 **Complete Validation** with multiple constraint checkers
- 🔧 **Highly Customizable** for any scheduling scenario

---

## ✨ Features

### 🎨 Modern Web Interface
- Clean, gradient-styled GUI built with Gradio
- Real-time progress indicators showing agent activity
- Tabbed results view for schedule, validation, and workflow
- No command line knowledge required

### 🤖 Multi-Agent System
- **Scheduler Agent**: Creates optimized schedules
- **Validator Agent**: Checks all constraints
- **Formatter Agent**: Presents results beautifully
- **Manager Agent**: Coordinates the team (CLI version)
- Each agent specializes in specific tasks

### 📚 Dynamic Class Management (NEW!)
- Add, update, or delete classes through GUI
- View all classes with capacities and time periods
- Changes persist to `class_database.json`
- Real-time updates without restart

### ⚙️ System Configuration (NEW!)
- Customize number of students (any number!)
- Set classes per student
- Configure number of days
- Adjust periods per day
- Set minimum classes per day
- All changes take effect immediately

### 🛡️ Comprehensive Validation
- **ClassNumberCheckerTool**: Verifies correct class count
- **UniqueAttendanceCheckerTool**: Ensures no duplicates
- **ClassAttendanceCheckerTool**: Checks capacity limits
- **PeriodConflictCheckerTool**: Detects time conflicts
- **OutputValidatorTool**: Validates output clarity

### 🔌 LLM Support
- OpenAI GPT-4o-mini (recommended)
- Anthropic Claude 3.5 Sonnet
- HuggingFace models (CPU fallback)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Use at least one (OpenAI recommended for best performance)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_KEY=hf_...
```

### 3. Launch the GUI

```bash
python final_project/final_project_gui.py
```

The interface opens automatically at `http://127.0.0.1:7860`

### 4. Generate a Schedule

1. Click **🚀 Generate Schedule** button
2. Watch agents work in real-time
3. View results in the tabs

That's it! 🎉

---

## 🎭 System Versions

This project includes **three different implementations** to demonstrate various architectural approaches:

### 1. 🎨 Multi-Agent GUI (Recommended)
**File**: `final_project_gui.py`

- ✅ Beautiful web interface
- ✅ Three specialized agents
- ✅ Real-time progress tracking
- ✅ Dynamic configuration management
- ✅ Best user experience

**Run it:**
```bash
python final_project/final_project_gui.py
```

### 2. 👥 Multi-Agent CLI
**File**: `final_project_multi_agent.py`

- ✅ Command-line interface
- ✅ Simplified agent coordination
- ✅ Manual workflow orchestration
- ✅ Good for learning agent patterns

**Run it:**
```bash
python final_project/final_project_multi_agent.py
```

### 3. 🤖 Single-Agent CLI
**File**: `final_project_single_agent.py`

- ✅ One agent with all tools
- ✅ Simpler architecture
- ✅ Easier to debug
- ✅ Good for prototyping

**Run it:**
```bash
python final_project/final_project_single_agent.py
```

### Comparison

| Feature | Single-Agent | Multi-Agent CLI | Multi-Agent GUI |
|---------|--------------|-----------------|-----------------|
| **User Interface** | CLI | CLI | Web GUI ✨ |
| **Agent Count** | 1 | 3 workers | 3 workers |
| **Specialization** | Generalist | Specialists | Specialists |
| **Progress Tracking** | Text | Text | Visual bars ✨ |
| **Configuration** | Code editing | Code editing | GUI panels ✨ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ ✨ |
| **Learning Value** | ReAct pattern | Multi-agent | Full system |
| **Best For** | Prototyping | CLI workflows | Production use ✨ |

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- At least one LLM API key (OpenAI, Anthropic, or HuggingFace)

### Step-by-Step

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:

Create a `.env` file in the project root:
```bash
# Choose at least one provider
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
```

5. **Verify installation**:
```bash
python final_project/final_project_gui.py
```

If the GUI opens, you're ready to go! 🎉

---

## 💡 Usage

### Using the Web GUI

#### Tab 1: 🚀 Generate Schedule

1. **View Current Configuration**: Left panel shows system settings
2. **Click "🚀 Generate Schedule"**: Starts the multi-agent workflow
3. **Watch Progress**: Real-time indicators show each agent's activity
4. **View Results**: Three sub-tabs display different outputs:
   - **📅 Schedule**: Formatted table with all student schedules
   - **✅ Validation**: Detailed constraint checking results
   - **⚙️ Workflow**: Complete log of agent interactions

#### Tab 2: 📚 Manage Classes

**View Classes** (Left Panel):
- Shows all classes organized by day
- Displays capacity and time periods for each class
- Click 🔄 Refresh to update

**Add/Update Class** (Right Panel):
```
Day: Day1
Class Name: Chemistry
Capacity: 6
Periods: 2, 4, 6
```
Click **➕ Add/Update Class**

**Delete Class** (Right Panel):
```
Day: Day1
Class Name: Chemistry
```
Click **🗑️ Delete Class**

#### Tab 3: ⚙️ System Config

**View Settings** (Left Panel):
- Current number of students
- Classes per student
- Number of days
- Periods per day
- Minimum classes per day

**Update Configuration** (Right Panel):
```
Number of Students: 20
Classes per Student: 6
Number of Days: 3
Periods per Day: 7
Minimum Classes per Day: 2
```
Click **💾 Save Configuration**

> 💡 **Tip**: Agents automatically reinitialize with new settings!

### Using the CLI Versions

#### Multi-Agent CLI
```bash
python final_project/final_project_multi_agent.py
```

The system will:
1. Initialize three specialized agents
2. Run through the scheduling workflow
3. Display the formatted schedule
4. Show validation results

#### Single-Agent CLI
```bash
python final_project/final_project_single_agent.py
```

The agent will:
1. Retrieve class data
2. Generate the schedule
3. Validate all constraints
4. Format and display results

---

## ⚙️ Dynamic Configuration

### Overview

The system supports **complete dynamic configuration** through the GUI. You can customize everything without editing code!

### Configuration Files

Two JSON files control the system:

#### `class_database.json`

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

**Properties**:
- **capacity**: Maximum students allowed
- **periods**: Time periods when class is offered (array of integers)

#### `system_config.json`

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

**Parameters**:
- **num_students**: Total students to schedule
- **classes_per_student**: Classes each student must take
- **num_days**: Number of days in the schedule
- **periods_per_day**: Time periods available each day
- **min_classes_per_day**: Minimum classes per student per day

### Dynamic Behavior

When you update configuration:
1. Changes are saved to JSON files
2. Agents automatically reinitialize
3. Next schedule uses new parameters
4. No code editing or restart needed!

### Validation Rules

**Class Management**:
- ✅ Capacity must be ≥ 1
- ✅ At least one period required
- ✅ Periods must be comma-separated numbers
- ✅ Day and class name required

**System Configuration**:
- ✅ All values must be ≥ 1
- ✅ `classes_per_student` ≥ `min_classes_per_day` × `num_days`
- ✅ Configuration must be mathematically feasible

### Capacity Planning

Total capacity should satisfy:

```
total_capacity ≥ num_students × classes_per_student / num_days
```

**Example**: For 10 students × 5 classes / 2 days = **25 class slots per day needed**

### Example Use Cases

#### Scenario 1: Add a New Class
```
1. Go to "📚 Manage Classes" tab
2. Fill in:
   - Day: Day1
   - Name: Psychology
   - Capacity: 8
   - Periods: 1, 2, 5, 6
3. Click "Add/Update Class"
4. Generate new schedule → Psychology available!
```

#### Scenario 2: Schedule 20 Students
```
1. Go to "⚙️ System Config" tab
2. Update:
   - Number of Students: 20
   - Classes per Student: 6
3. Click "Save Configuration"
4. Generate schedule → 20 students scheduled!
```

#### Scenario 3: Create 5-Day Schedule
```
1. Go to "📚 Manage Classes" tab
2. Add classes for Day3, Day4, Day5
3. Go to "⚙️ System Config" tab
4. Set Number of Days: 5
5. Generate schedule → 5-day schedule created!
```

---

## 🏗️ Architecture

### Multi-Agent Architecture (GUI)

```
User Interface (Gradio)
    ↓
generate_schedule_async()
    ↓
┌─────────────────────────────────────┐
│  Phase 1: Scheduler Agent           │
│  Tools:                              │
│  - ClassRetrievalTool                │
│  - SchedulerTool                     │
│                                      │
│  Task: Retrieve classes and create   │
│        optimized schedule            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Phase 2: Validator Agent            │
│  Tools:                              │
│  - ClassNumberCheckerTool            │
│  - UniqueAttendanceCheckerTool       │
│  - ClassAttendanceCheckerTool        │
│  - PeriodConflictCheckerTool         │
│                                      │
│  Task: Verify all constraints        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Phase 3: Formatter Agent            │
│  Tools:                              │
│  - StructuredOutputFormatterTool     │
│  - OutputValidatorTool               │
│                                      │
│  Task: Create readable table         │
└─────────────────────────────────────┘
    ↓
Display Results in Tabs
```

### Agent Roles

#### 🗓️ Scheduler Agent
- **Purpose**: Generate class schedules
- **Expertise**: Understanding class availability, capacity constraints, and creating fair distributions
- **Tools**: ClassRetrievalTool, SchedulerTool
- **Output**: JSON schedule with student assignments

#### ✅ Validator Agent
- **Purpose**: Verify scheduling constraints
- **Expertise**: Checking class counts, uniqueness, capacity limits, and period conflicts
- **Tools**: 4 specialized checker tools
- **Output**: Validation report with pass/fail status

#### 📋 Formatter Agent
- **Purpose**: Present results clearly
- **Expertise**: Creating readable tables and validating output quality
- **Tools**: StructuredOutputFormatterTool, OutputValidatorTool
- **Output**: Formatted schedule table

### Data Flow

```
Configuration Files (JSON)
    ↓
ClassRetrievalTool (reads class_database.json)
    ↓
SchedulerTool (reads system_config.json)
    ↓
Schedule JSON
    ↓
Validator Tools (check constraints)
    ↓
Validation Report
    ↓
Formatter Tools (create table)
    ↓
Final Output
```

---

## 🛠️ Custom Tools

All tools inherit from `AbstractTool` and are located in `final_project_tools/`:

### Data Retrieval

#### ClassRetrievalTool
- **Purpose**: Fetch available classes from database
- **Input**: None (reads from `class_database.json`)
- **Output**: JSON with classes, capacities, and periods
- **Features**: Error handling for missing/invalid files

### Scheduling

#### SchedulerTool
- **Purpose**: Generate optimized schedules
- **Input**: Class data JSON
- **Output**: Student schedule JSON with period assignments
- **Algorithm**:
  - Reads system configuration dynamically
  - Distributes classes across days
  - Ensures minimum classes per day
  - Avoids period conflicts
  - Respects capacity limits
  - Guarantees unique classes per student

### Validation

#### ClassNumberCheckerTool
- **Purpose**: Verify each student has correct class count
- **Input**: Schedule JSON
- **Output**: Validation result with invalid students list
- **Check**: `len(classes) == classes_per_student`

#### UniqueAttendanceCheckerTool
- **Purpose**: Ensure no duplicate classes per student
- **Input**: Schedule JSON
- **Output**: Validation result with duplicates found
- **Check**: All class names unique for each student

#### ClassAttendanceCheckerTool
- **Purpose**: Verify capacity limits not exceeded
- **Input**: Schedule JSON and class data JSON
- **Output**: Validation result with capacity violations
- **Check**: Student count per class ≤ capacity

#### PeriodConflictCheckerTool
- **Purpose**: Detect time conflicts
- **Input**: Schedule JSON
- **Output**: Validation result with conflicts found
- **Check**: No two classes in same period for same student/day

### Formatting

#### StructuredOutputFormatterTool
- **Purpose**: Create readable schedule table
- **Input**: Schedule JSON
- **Output**: Formatted ASCII table with periods
- **Features**: 
  - Uses `tabulate` library
  - Groups by student and day
  - Shows period information
  - Stores output in class variable for retrieval

#### OutputValidatorTool
- **Purpose**: Validate output clarity and completeness
- **Input**: Schedule JSON and formatted output
- **Output**: Clarity score with suggestions
- **Checks**:
  - Completeness (all students included)
  - Data integrity (valid JSON structure)
  - Format quality (table structure)
  - Class distribution (balanced assignments)
  - Period information (included and valid)

### Tool Architecture

```python
class CustomTool(AbstractTool):
    name = "ToolName"
    description = "What the tool does and expects"
    
    def use(self, tool_input: str) -> str:
        """
        Main tool logic
        
        Args:
            tool_input: JSON string or text input
            
        Returns:
            JSON string with results
        """
        # Implementation
        return json.dumps(result)
```

---

## 📁 Configuration Files

### File Locations

```
final_project/
├── class_database.json          # Class data (auto-created)
├── system_config.json           # System parameters (auto-created)
├── final_project_gui.py         # GUI application
├── final_project_multi_agent.py # Multi-agent CLI
├── final_project_single_agent.py# Single-agent CLI
└── final_project_tools/         # Custom tools directory
    ├── class_retrieval.py
    ├── scheduler.py
    ├── checkers.py
    ├── period_validator.py
    ├── formatter.py
    └── output_validator.py
```

### Auto-Creation

Both configuration files are **created automatically** with default values if they don't exist:

**Default `class_database.json`**: 6 classes per day across 2 days
**Default `system_config.json`**: 10 students, 5 classes each, 2 days, 6 periods, 1 min per day

### Manual Editing

You can also edit JSON files directly:

```bash
# Edit classes
notepad final_project/class_database.json

# Edit configuration
notepad final_project/system_config.json
```

Changes take effect on next schedule generation.

---

## 🐛 Troubleshooting

### Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'gradio'`
```bash
# Solution: Install missing package
pip install gradio>=4.0.0
```

**Problem**: `Python version too old`
```bash
# Solution: Upgrade Python
# Download Python 3.11+ from python.org
python --version  # Verify version
```

### GUI Issues

**Problem**: GUI doesn't open in browser
```bash
# Solution: Manually navigate to
http://127.0.0.1:7860
```

**Problem**: Port already in use
```bash
# Solution: Change port in final_project_gui.py (line ~695)
demo.launch(server_port=7861)  # Use different port
```

**Problem**: GUI shows errors
```bash
# Check your .env file has valid API keys
# Try using OpenAI or Anthropic instead of HuggingFace
```

### Scheduling Issues

**Problem**: Schedule generation fails
```
Possible causes:
1. Insufficient capacity (increase class capacities)
2. Invalid configuration (check validation rules)
3. Too many students for available classes
4. Period constraints too restrictive
```

**Solution**: Check the validation tab for specific errors

**Problem**: Classes exceed capacity
```
# Verify capacity tracking in SchedulerTool
# Ensure capacity is per-class-per-day, not per-period
```

**Problem**: Period conflicts detected
```
# Check PeriodConflictCheckerTool output
# Verify scheduler checks used_periods
# Ensure classes offer multiple period options
```

**Problem**: Students don't have enough classes
```
# Increase classes_per_student in config
# Add more classes to database
# Check that constraints are feasible
```

### Configuration Issues

**Problem**: Classes not appearing
```
1. Check day name matches exactly (case-sensitive)
2. Click refresh button
3. Verify class_database.json saved correctly
```

**Problem**: Config changes don't take effect
```
1. Click "Save Configuration" button
2. Wait for "Agents reinitialized" message
3. Try generating a new schedule
```

**Problem**: Validation error when saving config
```
# Check constraint: classes_per_student ≥ min_classes_per_day × num_days
# Example: 5 classes ≥ 2 min/day × 2 days = 4 ✅
#          5 classes ≥ 3 min/day × 2 days = 6 ❌
```

### API Key Issues

**Problem**: API key errors
```bash
# Verify .env file exists in project root
# Check key format (no spaces, no quotes)
# Ensure key is valid and has credits
# Try a different provider
```

**Problem**: Slow generation with HuggingFace
```
# This is expected (CPU inference is slow)
# Solution: Use OpenAI or Anthropic instead
# They're much faster (cloud GPUs)
```

### Debug Mode

Enable detailed logging:

```python
# Add to top of final_project_gui.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🔧 Customization

### Adding a New Class

**Via GUI** (Recommended):
```
1. Go to "📚 Manage Classes" tab
2. Fill in class details
3. Click "Add/Update Class"
```

**Via JSON**:
```json
{
    "Day1": {
        "Physics": {
            "capacity": 5,
            "periods": [1, 3, 5]
        }
    }
}
```

### Adding a New Day

**Via GUI**:
```
1. Add classes for "Day3" in Manage Classes
2. Update "Number of Days" to 3 in System Config
3. Generate schedule
```

**Via JSON**:
```json
{
    "Day1": { ... },
    "Day2": { ... },
    "Day3": { ... }  // Add new day
}
```

Update `system_config.json`:
```json
{
    "num_days": 3  // Update count
}
```

### Changing System Parameters

**Via GUI** (Recommended):
```
Go to "⚙️ System Config" tab
Update any parameter
Click "Save Configuration"
```

**Via JSON**:
```json
{
    "num_students": 20,
    "classes_per_student": 7,
    "num_days": 5,
    "periods_per_day": 8,
    "min_classes_per_day": 1
}
```

### Creating a New Tool

1. **Create tool file** in `final_project_tools/`:

```python
from fairlib import AbstractTool
import json

class MyCustomTool(AbstractTool):
    name = "MyCustomTool"
    description = "Description of what it does"
    
    def use(self, tool_input: str) -> str:
        # Your logic here
        result = {"status": "success"}
        return json.dumps(result)
```

2. **Register with agent** in `final_project_gui.py`:

```python
from final_project_tools.my_custom_tool import MyCustomTool

# Add to appropriate agent
validator_agent = create_agent(
    llm,
    [
        MyCustomTool(),  # Add here
        # ... other tools
    ],
    "Role description"
)
```

3. **Update role description** to mention new tool

### Customizing GUI Appearance

**Change port**:
```python
# Line ~695 in final_project_gui.py
demo.launch(server_port=8080)  # Custom port
```

**Enable public sharing**:
```python
demo.launch(share=True)  # Creates public URL
```

**Modify colors**:
```python
# Edit header gradient (line ~222)
background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# Change to your colors
```

### Adding a New Agent (Advanced)

```python
# Create new agent
reporting_agent = create_agent(
    llm,
    [ReportingTool(), AnalyticsTool()],
    "You are a reporting specialist. Generate analytics and reports."
)

# Add to workflow
analytics_response = await reporting_agent.arun(
    f"Generate analytics for this schedule: {schedule_response}"
)
```

---

## 🎓 Learning Objectives

This project demonstrates key AI and software engineering concepts:

### AI/ML Concepts
- ✅ **Multi-Agent Systems**: Hierarchical coordination and task delegation
- ✅ **ReAct Pattern**: Reasoning and acting cycle for autonomous agents
- ✅ **Tool-Based Architecture**: Modular, reusable components
- ✅ **LLM Integration**: Using multiple AI providers
- ✅ **Agent Specialization**: Domain experts working together

### Software Engineering
- ✅ **Clean Architecture**: Separation of concerns
- ✅ **CRUD Operations**: Create, Read, Update, Delete
- ✅ **Configuration Management**: Dynamic system parameters
- ✅ **Data Persistence**: JSON file storage
- ✅ **Input Validation**: Error prevention and handling
- ✅ **User Interface Design**: Modern web GUI with Gradio

### Algorithms
- ✅ **Constraint Satisfaction**: Solving complex scheduling problems
- ✅ **Resource Allocation**: Capacity planning and distribution
- ✅ **Conflict Resolution**: Avoiding time and capacity conflicts
- ✅ **Optimization**: Fair and efficient schedule generation

### Best Practices
- ✅ **Documentation**: Comprehensive README and inline comments
- ✅ **Error Handling**: Graceful failure and recovery
- ✅ **Testing**: Validation tools for quality assurance
- ✅ **Modularity**: Reusable components and tools
- ✅ **User Experience**: Intuitive interface and feedback

---

## 📊 Sample Output

### Schedule Table

```
+-----------+------------------------------------------------+---------------------------------------------------------+
| Student   | Day 1 Classes (Period)                         | Day 2 Classes (Period)                                  |
+===========+================================================+=========================================================+
| Student1  | Art (P3), PE (P5), Science (P2), Math (P1)     | Biology (P4)                                            |
+-----------+------------------------------------------------+---------------------------------------------------------+
| Student2  | Music (P2)                                     | Math (P1), Biology (P2), ComputerSci (P5), English (P3) |
+-----------+------------------------------------------------+---------------------------------------------------------+
| Student3  | Music (P2), Math (P5), History (P1)            | PE (P5), ComputerSci (P2)                               |
+-----------+------------------------------------------------+---------------------------------------------------------+
| Student4  | PE (P3), History (P4)                          | Math (P3), English (P1), Music (P6), ComputerSci (P5)   |
+-----------+------------------------------------------------+---------------------------------------------------------+
| Student5  | Math (P3), Art (P5), Science (P4)              | PE (P2), English (P3)                                   |
+-----------+------------------------------------------------+---------------------------------------------------------+
```

### Validation Report

```
✅ Class Count: PASSED
   - All students have exactly 5 classes

✅ Unique Classes: PASSED
   - No duplicate classes found

✅ Capacity Limits: PASSED
   - No classes exceed capacity

✅ Period Conflicts: PASSED
   - No time conflicts detected

✨ Schedule is valid and ready to use!
```

---

## 🤝 Contributing

Want to improve the system? Here are some ideas:

### Easy Enhancements
- [ ] Add more classes to the database
- [ ] Create preset configurations for different scenarios
- [ ] Add export functionality (PDF, CSV, Excel)
- [ ] Implement dark mode for GUI

### Medium Enhancements
- [ ] Add student preference-based scheduling
- [ ] Create a "Reporting Agent" for analytics
- [ ] Implement schedule comparison tool
- [ ] Add undo/redo for configuration changes

### Advanced Enhancements
- [ ] Database backend (SQLite/PostgreSQL)
- [ ] User authentication and multi-user support
- [ ] RESTful API for external integration
- [ ] Mobile-responsive design
- [ ] Real-time collaboration features
- [ ] Machine learning for optimal scheduling

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📚 Additional Resources

### Documentation
- **FAIR-LLM Framework**: [Main repository](https://github.com/fair-llm)
- **Gradio Documentation**: [gradio.app](https://gradio.app)
- **Python asyncio**: [docs.python.org](https://docs.python.org/3/library/asyncio.html)

### Related Concepts
- Multi-agent systems
- Constraint satisfaction problems
- ReAct (Reasoning + Acting) pattern
- Tool-augmented language models

### Research Papers
- ReAct: Synergizing Reasoning and Acting in Language Models
- Multi-Agent Systems for Complex Problem Solving
- Constraint Satisfaction in AI Planning

---

## 📄 License

Part of the FAIR-LLM Framework (MIT License)

---

## 🎯 Project Stats

- **Version**: 2.0
- **Lines of Code**: ~2,500+
- **Custom Tools**: 8
- **Agents**: 3 specialized + 1 manager (CLI)
- **Configuration Options**: 5 major parameters
- **Supported LLMs**: OpenAI, Anthropic, HuggingFace
- **GUI Tabs**: 3 main tabs with multiple sub-tabs
- **Documentation Files**: 5 comprehensive guides

---

## 🌟 Acknowledgments

Built with:
- **FAIR-LLM Framework**: Core agent framework
- **Gradio**: Web interface
- **OpenAI/Anthropic**: LLM providers
- **Tabulate**: Table formatting
- **Python-dotenv**: Environment management

CS471 Final Project - Intelligent Scheduling System

---

## 🚀 Get Started Now!

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API key

# 3. Launch
python final_project/final_project_gui.py

# 4. Enjoy!
# Open browser at http://127.0.0.1:7860
```

**Questions?** Check the [Troubleshooting](#-troubleshooting) section  
**Want to customize?** See [Customization](#-customization)  
**Learning?** Review [Learning Objectives](#-learning-objectives)

Happy scheduling! 🎉✨

---

*Made with ❤️ using AI and Python*
