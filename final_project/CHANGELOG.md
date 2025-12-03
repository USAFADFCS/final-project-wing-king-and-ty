# Changelog - Class Scheduling System

## Version 2.0 - Dynamic Configuration (Current)

### 🎉 Major Features Added

#### Dynamic Class Management
- ✅ Add, update, and delete classes through GUI
- ✅ View all classes organized by day
- ✅ Edit capacities and time periods
- ✅ Changes persist to `class_database.json`
- ✅ No code editing required

#### Dynamic System Configuration
- ✅ Customize number of students (default: 10)
- ✅ Set classes per student (default: 5)
- ✅ Configure number of days (default: 2)
- ✅ Set periods per day (default: 6)
- ✅ Define minimum classes per day (default: 1)
- ✅ Settings saved to `system_config.json`
- ✅ Automatic agent reinitialization on config change

#### Enhanced Scheduler Tool
- ✅ Reads configuration dynamically
- ✅ Adapts to any number of students
- ✅ Works with any number of days
- ✅ Scales to custom requirements

#### Enhanced GUI
- ✅ Three-tab interface:
  - 🚀 Generate Schedule (original functionality)
  - 📚 Manage Classes (new!)
  - ⚙️ System Config (new!)
- ✅ Real-time updates
- ✅ Input validation
- ✅ Status feedback for all operations

### 📚 Documentation Added
- `README_DYNAMIC_CONFIG.md` - Complete guide to dynamic features
- Updated `README_GUI.md` - New tab descriptions and usage
- `CHANGELOG.md` - Version history (this file)

### 🔧 Technical Changes

#### New Files
- `class_database.json` - Persistent class storage
- `system_config.json` - Persistent system parameters

#### Modified Files
- `final_project_gui.py`:
  - Added class management functions
  - Added config management functions
  - New GUI tabs and event handlers
  - Dynamic agent initialization
  
- `final_project_tools/class_retrieval.py`:
  - Now reads from `class_database.json`
  - Error handling for missing/invalid files
  
- `final_project_tools/scheduler.py`:
  - Reads `system_config.json` for parameters
  - Dynamic student count
  - Dynamic day handling
  - Flexible class distribution

### 🎯 Benefits
- **User-Friendly**: Configure everything through GUI
- **Flexible**: Test different scenarios easily
- **Scalable**: Support any number of students/classes
- **Persistent**: Changes saved automatically
- **No Downtime**: Updates take effect immediately

---

## Version 1.0 - Multi-Agent System

### Initial Features

#### Multi-Agent Architecture
- ✅ Scheduler Agent: Creates schedules
- ✅ Validator Agent: Checks constraints
- ✅ Formatter Agent: Presents results
- ✅ Manual workflow coordination

#### Custom Tools
- ✅ `ClassRetrievalTool`: Fetch class data
- ✅ `SchedulerTool`: Generate schedules
- ✅ `ClassNumberCheckerTool`: Validate class counts
- ✅ `UniqueAttendanceCheckerTool`: Check uniqueness
- ✅ `ClassAttendanceCheckerTool`: Verify capacity
- ✅ `PeriodConflictCheckerTool`: Check time conflicts
- ✅ `StructuredOutputFormatterTool`: Format tables
- ✅ `OutputValidatorTool`: Validate output quality

#### Gradio GUI
- ✅ Web-based interface
- ✅ Real-time progress indicators
- ✅ Tabbed results view
- ✅ LLM provider display

#### Constraint Support
- ✅ Fixed 10 students, 2 days
- ✅ 5 classes per student
- ✅ At least 1 class per day
- ✅ Class capacity limits
- ✅ Period conflict prevention

#### LLM Support
- ✅ OpenAI GPT-4o-mini
- ✅ Anthropic Claude 3.5 Sonnet
- ✅ HuggingFace TinyLlama (fallback)

### Documentation
- `README.md` - Project overview
- `README_MULTI_AGENT.md` - Multi-agent architecture
- `README_GUI.md` - GUI usage guide

---

## Version 0.5 - Single Agent System

### Initial Development
- ✅ Single agent with all tools
- ✅ Command-line interface
- ✅ Basic scheduling logic
- ✅ Hardcoded class data
- ✅ Fixed parameters

---

## Future Enhancements (Potential)

### Possible Features
- 🔮 Database backend (SQLite/PostgreSQL)
- 🔮 User authentication and multi-user support
- 🔮 Schedule export (PDF, CSV, Excel)
- 🔮 Conflict resolution suggestions
- 🔮 Historical schedule storage
- 🔮 Analytics and reporting
- 🔮 Drag-and-drop schedule editing
- 🔮 Email/notification integration
- 🔮 Mobile-responsive design
- 🔮 RESTful API for integration

---

**Current Version**: 2.0  
**Last Updated**: December 2025  
**Maintained By**: CS471 Final Project Team

