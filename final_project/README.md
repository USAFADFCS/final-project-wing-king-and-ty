# 🎓 FAIR-LLM Class Scheduling Agent

An intelligent AI-powered class scheduling system built with the FAIR-LLM framework, demonstrating both **single-agent** and **multi-agent** architectures.

## 📋 Overview

This project creates a 2-day class schedule for 10 students, ensuring:
- ✅ Each student takes exactly **5 unique classes**
- ✅ At least **1 class per day** for each student
- ✅ **No class exceeds capacity**
- ✅ **No period conflicts** (students can't be in two places at once)
- ✅ Classes are offered during specific **time periods**

## 🤖 Two Implementations

### 1. Single-Agent System (`final_project.py`)
One intelligent agent uses 8 specialized tools to complete the entire workflow.

**Run it:**
```bash
python final_project/final_project.py
```

### 2. Multi-Agent System (`final_project_multi_agent.py`) ⭐ NEW!
A manager agent coordinates 3 specialized worker agents, each with their own tools and expertise.

**Run it:**
```bash
python final_project/final_project_multi_agent.py
```

👉 **See [README_MULTI_AGENT.md](README_MULTI_AGENT.md) for a detailed comparison!**

## 🚀 Quick Start

### 1. Set Up Environment

Create a `.env` file with your API keys:
```bash
# Use at least one of these (OpenAI recommended for best performance)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
HUGGINGFACE_API_KEY=hf_...
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the System

**Single-agent:**
```bash
python final_project/final_project.py
```

**Multi-agent:**
```bash
python final_project/final_project_multi_agent.py
```

### 4. Generate a Schedule

```
👤 You: generate schedule
```

## 📊 System Architecture

### Single-Agent Architecture
```
Agent
  ├─ ClassRetrievalTool
  ├─ SchedulerTool
  ├─ ClassNumberCheckerTool
  ├─ UniqueAttendanceCheckerTool
  ├─ ClassAttendanceCheckerTool
  ├─ PeriodConflictCheckerTool
  ├─ StructuredOutputFormatterTool
  └─ OutputValidatorTool
```

### Multi-Agent Architecture
```
Manager Agent
  ├─ Scheduler Agent
  │    ├─ ClassRetrievalTool
  │    └─ SchedulerTool
  ├─ Validator Agent
  │    ├─ ClassNumberCheckerTool
  │    ├─ UniqueAttendanceCheckerTool
  │    ├─ ClassAttendanceCheckerTool
  │    └─ PeriodConflictCheckerTool
  └─ Formatter Agent
       ├─ StructuredOutputFormatterTool
       └─ OutputValidatorTool
```

## 🛠️ Custom Tools

All tools are in the `final_project_tools/` directory:

| Tool | Purpose |
|------|---------|
| **ClassRetrievalTool** | Fetches available classes with capacities and periods |
| **SchedulerTool** | Generates schedules respecting all constraints |
| **ClassNumberCheckerTool** | Verifies each student has exactly 5 classes |
| **UniqueAttendanceCheckerTool** | Ensures no duplicate classes per student |
| **ClassAttendanceCheckerTool** | Checks class capacity limits |
| **PeriodConflictCheckerTool** | Detects scheduling conflicts |
| **StructuredOutputFormatterTool** | Formats schedule as a table |
| **OutputValidatorTool** | Validates output clarity |

## 📅 Sample Output

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
...
```

## 🎯 Learning Objectives

This project demonstrates:
- ✅ **Tool Creation**: Building custom tools for domain-specific tasks
- ✅ **ReAct Pattern**: Reasoning and acting cycle for agents
- ✅ **Multi-Agent Coordination**: Hierarchical task delegation
- ✅ **Constraint Satisfaction**: Solving complex scheduling problems
- ✅ **Agent Specialization**: Domain experts working together

## 🔧 Customization

### Add More Classes
Edit `final_project_tools/class_retrieval.py`:
```python
class_data = {
    "Day1": {
        "Physics": {"capacity": 5, "periods": [1, 3]},
        # Add more...
    },
    ...
}
```

### Add More Students
Modify the prompt in `final_project.py` or `final_project_multi_agent.py`:
```python
"Generate a 2-day class schedule for 20 students..."
```

### Add a New Constraint
1. Create a new checker tool in `final_project_tools/`
2. Register it with the appropriate agent
3. Update the workflow instructions

## 📚 Documentation

- **[README_MULTI_AGENT.md](README_MULTI_AGENT.md)** - Detailed single vs multi-agent comparison
- **[FAIR-LLM Framework Docs](../../README.md)** - Main framework documentation

## 🐛 Troubleshooting

**Issue: Schedule doesn't show up**
- The formatted table is extracted from the `StructuredOutputFormatterTool` output
- Check that the tool is being called successfully

**Issue: Classes exceed capacity**
- Verify `SchedulerTool` tracks capacity per day (not per period)
- Check capacity tracking logic in `scheduler.py`

**Issue: Period conflicts**
- Ensure `PeriodConflictCheckerTool` is running
- Verify scheduler checks `used_periods` before assignment

## 🤝 Contributing

Want to improve the system? Try:
- Adding more validation tools
- Implementing preference-based scheduling
- Creating a "Reporting Agent" for analytics
- Adding database persistence
- Building a web interface

## 📄 License

Part of the FAIR-LLM Framework (MIT License)

---

**Choose your adventure:**
- 🏃 Quick start? Use `final_project.py`
- 🎓 Learning multi-agent? Try `final_project_multi_agent.py`
- 📖 Want details? Read `README_MULTI_AGENT.md`

Happy scheduling! 🎉

