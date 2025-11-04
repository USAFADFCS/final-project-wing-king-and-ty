# Class Scheduling System: Single-Agent vs Multi-Agent

This project demonstrates two different architectures for building an AI-powered class scheduling system using the FAIR-LLM framework.

## 📁 Files

- **`final_project.py`** - Single-agent system (simpler)
- **`final_project_multi_agent.py`** - Multi-agent system (more advanced)

---

## 🤖 Single-Agent System (`final_project.py`)

### Architecture
```
Single Agent
    ↓
    Uses 8 Tools:
    ├── ClassRetrievalTool
    ├── SchedulerTool
    ├── ClassNumberCheckerTool
    ├── UniqueAttendanceCheckerTool
    ├── ClassAttendanceCheckerTool
    ├── PeriodConflictCheckerTool
    ├── StructuredOutputFormatterTool
    └── OutputValidatorTool
```

### Characteristics
- **One agent** orchestrates all tasks
- **Sequential processing** - agent decides tool order
- **Simple to understand** and debug
- **Good for**: Straightforward workflows, learning, prototyping

### How It Works
1. Agent receives user request
2. Agent plans which tools to use and in what order
3. Agent calls tools one by one
4. Agent synthesizes final answer

---

## 👥 Multi-Agent System (`final_project_multi_agent.py`)

### Architecture
```
Manager Agent
    ↓ delegates to
    ├── Scheduler Agent (ClassRetrievalTool, SchedulerTool)
    ├── Validator Agent (4 checker tools)
    └── Formatter Agent (StructuredOutputFormatterTool, OutputValidatorTool)
```

### Characteristics
- **Four specialized agents** with distinct roles
- **Hierarchical delegation** - manager coordinates team
- **Each agent has specific expertise** and tools
- **More realistic** team-based problem solving
- **Good for**: Complex workflows, specialization, scalability

### How It Works
1. Manager Agent receives user request
2. Manager analyzes request and creates subtasks
3. Manager delegates subtasks to specialized worker agents:
   - **Scheduler Agent**: "Create a schedule for 10 students"
   - **Validator Agent**: "Check if this schedule meets all constraints"
   - **Formatter Agent**: "Format this schedule as a table"
4. Each worker completes their specialized task
5. Manager synthesizes all results into final answer

### Agent Roles

#### 🗓️ Scheduler Agent
- **Purpose**: Generate class schedules
- **Tools**: ClassRetrievalTool, SchedulerTool
- **Expertise**: Understanding class availability, capacity, and creating fair schedules

#### ✅ Validator Agent
- **Purpose**: Verify scheduling constraints
- **Tools**: ClassNumberCheckerTool, UniqueAttendanceCheckerTool, ClassAttendanceCheckerTool, PeriodConflictCheckerTool
- **Expertise**: Checking class counts, uniqueness, capacity limits, period conflicts

#### 📋 Formatter Agent
- **Purpose**: Present results clearly
- **Tools**: StructuredOutputFormatterTool, OutputValidatorTool
- **Expertise**: Creating readable tables, validating output clarity

#### 👔 Manager Agent
- **Purpose**: Coordinate the team
- **Tools**: None (delegates to workers)
- **Expertise**: Understanding user requests, task decomposition, synthesizing results

---

## 🚀 Running the Systems

### Single-Agent System
```bash
python final_project/final_project.py
```

### Multi-Agent System
```bash
python final_project/final_project_multi_agent.py
```

Both systems:
- Require the same environment variables (`.env` file)
- Support OpenAI, Anthropic, or HuggingFace LLMs
- Produce the same output (a validated 2-day schedule)

---

## 🎯 Key Differences

| Aspect | Single-Agent | Multi-Agent |
|--------|--------------|-------------|
| **Complexity** | Simple | More complex |
| **Agents** | 1 | 4 (1 manager + 3 workers) |
| **Coordination** | Internal (one agent) | Hierarchical (manager delegates) |
| **Specialization** | One generalist | Multiple specialists |
| **Debugging** | Easier (one reasoning chain) | Harder (multiple interactions) |
| **Scalability** | Limited | Better (add more agents) |
| **Realism** | Task-focused | Team-focused |
| **Performance** | Faster (fewer LLM calls) | Slower (more coordination) |

---

## 📚 Learning Objectives

### Single-Agent System Teaches:
- ✅ Tool creation and registration
- ✅ ReAct reasoning pattern
- ✅ Sequential task planning
- ✅ Agent-tool interaction

### Multi-Agent System Teaches:
- ✅ Agent specialization
- ✅ Hierarchical coordination
- ✅ Task delegation
- ✅ Multi-agent collaboration patterns
- ✅ Role-based problem solving

---

## 🤔 Which Should You Use?

### Use **Single-Agent** if:
- You're learning the framework
- The task is straightforward
- You want simple debugging
- Performance is critical
- You need quick prototyping

### Use **Multi-Agent** if:
- You need specialized expertise
- Task naturally decomposes into subtasks
- You want realistic team simulation
- Scalability matters
- Different agents need different tools/models

---

## 🔧 Customization

### Adding a New Tool (Single-Agent)
1. Create tool class inheriting from `AbstractTool`
2. Register in `ToolRegistry`
3. Update agent's role definition

### Adding a New Agent (Multi-Agent)
1. Create agent using `create_agent()` helper
2. Assign specialized tools
3. Write clear role description
4. Add to `workers` dictionary
5. Manager will automatically learn to delegate to it!

---

## 💡 Next Steps

1. **Try both systems** - compare their behavior
2. **Add more constraints** - implement new checker tools
3. **Create new agents** - add a "Reporting Agent" for analytics
4. **Experiment with models** - try different LLMs for different agents
5. **Add persistence** - save schedules to a database

Enjoy exploring multi-agent AI systems! 🎓✨

