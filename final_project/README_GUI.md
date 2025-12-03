# 🎨 GUI Version - Multi-Agent Class Scheduling System

## Overview

A beautiful web-based GUI for the multi-agent scheduling system built with Gradio. This provides an intuitive interface for generating class schedules without using the command line!

## Features

✨ **Modern Web Interface**
- Clean, gradient-styled UI
- Real-time progress indicators
- Tabbed results view

🤖 **Multi-Agent Visualization**
- See each agent's progress in real-time
- View detailed workflow logs
- Separate tabs for schedule, validation, and workflow

📊 **Interactive Results**
- Formatted schedule table
- Validation results
- Complete agent workflow log

📚 **Dynamic Class Management** _(NEW!)_
- Add, update, or delete classes through the GUI
- View all classes with capacities and time periods
- Changes persist to database file

⚙️ **System Configuration** _(NEW!)_
- Customize number of students, classes, days
- Adjust scheduling parameters in real-time
- No code editing required!

## Installation

1. **Install Gradio** (if not already installed):
```bash
pip install gradio>=4.0.0
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

2. **Set up your API keys** in `.env`:
```bash
OPENAI_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here
```

## Running the GUI

Simply run:
```bash
python final_project/final_project_gui.py
```

The interface will automatically open in your browser at:
```
http://127.0.0.1:7860
```

## Using the Interface

### 🚀 Generate Schedule Tab

1. **Click "🚀 Generate Schedule"** button
2. **Watch the progress** as each agent works:
   - 🗓️ Scheduler Agent creates the schedule
   - ✅ Validator Agent checks constraints
   - 📋 Formatter Agent presents results
3. **View results** in the tabs:
   - **📅 Schedule**: The final formatted schedule
   - **✅ Validation**: Constraint checking results
   - **⚙️ Workflow**: Detailed agent activity log

### 📚 Manage Classes Tab _(NEW!)_

1. **View Current Classes**: Left panel shows all classes organized by day
2. **Add/Update a Class**:
   - Enter Day (e.g., `Day1`)
   - Enter Class Name (e.g., `Math`)
   - Set Capacity (e.g., `5`)
   - List Periods (e.g., `1, 3, 5`)
   - Click **➕ Add/Update Class**
3. **Delete a Class**:
   - Enter Day and Class Name
   - Click **🗑️ Delete Class**
4. **Refresh**: Click 🔄 to see updated class list

### ⚙️ System Config Tab _(NEW!)_

1. **View Current Settings**: Left panel shows active configuration
2. **Update Configuration**:
   - Set Number of Students (e.g., `10`)
   - Set Classes per Student (e.g., `5`)
   - Set Number of Days (e.g., `2`)
   - Set Periods per Day (e.g., `6`)
   - Set Min Classes per Day (e.g., `1`)
   - Click **💾 Save Configuration**
3. **Agents Reinitialize**: System automatically updates with new settings
4. **Refresh**: Click 🔄 to see updated configuration

> 💡 **Tip**: Changes to classes and configuration take effect immediately!

## Interface Sections

### 🚀 Generate Schedule Tab
- **Control Panel (Left)**: System overview, current config, generate button
- **Results Panel (Bottom)**: Schedule, validation, and workflow tabs

### 📚 Manage Classes Tab
- **Class Display (Left)**: Shows all classes with details
- **Management Panel (Right)**: Add/update and delete classes

### ⚙️ System Config Tab
- **Current Config (Left)**: Active system parameters
- **Update Panel (Right)**: Modify all settings

## Advantages Over CLI Version

✅ **User-Friendly**: No command line knowledge needed  
✅ **Visual Progress**: See agents working in real-time  
✅ **Organized Results**: Separate tabs for different outputs  
✅ **Persistent**: Results stay visible until next generation  
✅ **Shareable**: Can create public links with `share=True`  

## Customization

### Change Port
Edit line 379 in `final_project_gui.py`:
```python
demo.launch(server_port=7860)  # Change to your preferred port
```

### Enable Public Sharing
Edit line 381 in `final_project_gui.py`:
```python
demo.launch(share=True)  # Creates public gradio.live link
```

### Modify Styling
Edit the `custom_css` variable (lines 212-250) to customize colors, fonts, and layout.

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'gradio'`  
**Solution**: Install gradio: `pip install gradio>=4.0.0`

**Issue**: GUI doesn't open in browser  
**Solution**: Manually navigate to `http://127.0.0.1:7860`

**Issue**: Port already in use  
**Solution**: Change the port number or close the application using port 7860

**Issue**: Agents taking too long  
**Solution**: Make sure you're using OpenAI or Anthropic (HuggingFace CPU is very slow)

## Architecture

```
User Interface (Gradio)
    ↓
generate_schedule_async()
    ↓
┌─────────────────────────────────────┐
│  Phase 1: Scheduler Agent           │
│  - Retrieves class data              │
│  - Generates schedule                │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Phase 2: Validator Agent            │
│  - Checks class counts               │
│  - Validates capacity                │
│  - Checks period conflicts           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Phase 3: Formatter Agent            │
│  - Creates formatted table           │
│  - Validates output quality          │
└─────────────────────────────────────┘
    ↓
Display Results in Tabs
```

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual Feedback | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Progress Tracking | Real-time bars | Text only |
| Results Organization | Tabbed interface | Sequential output |
| User Interaction | Click button | Type commands |
| Setup Complexity | Same | Same |
| Performance | Same | Same |

## Tips

💡 **Best Experience**: Use with OpenAI GPT-4o-mini for fast, high-quality results  
💡 **Share Results**: Take screenshots or copy from the textboxes  
💡 **Multiple Runs**: Generate as many schedules as you want with one click  
💡 **Monitor Progress**: Watch the progress bar to see which agent is working  

## Files

- `final_project_gui.py` - Main GUI application with dynamic config
- `class_database.json` - Class data storage (auto-created)
- `system_config.json` - System parameters (auto-created)
- `final_project_multi_agent.py` - Original CLI version (still works!)
- `final_project_single_agent.py` - Single-agent CLI version

All versions use the same tools and now support dynamic configuration!

For detailed information on dynamic configuration, see `README_DYNAMIC_CONFIG.md`.

---

**Built with**: FAIR-LLM Framework, Gradio, Python asyncio  
**Project**: CS471 Final Project - Intelligent Scheduling System


