"""
FAIR-LLM Demo: Multi-Agent Class Scheduling System - GUI Version
----------------------------------------------------------------

A beautiful Gradio interface for the multi-agent scheduling system.
Features:
- One-click schedule generation
- Real-time agent workflow visualization
- Formatted schedule display
- Validation results
- Dynamic class and system configuration

Run with: python final_project/final_project_gui.py
"""

import asyncio
import os
import json
from dotenv import load_dotenv
import gradio as gr
from fairlib import (
    settings,
    ToolRegistry,
    ToolExecutor,
    WorkingMemory,
    SimpleAgent,
    OpenAIAdapter,
    AnthropicAdapter,
    HuggingFaceAdapter,
    ReActPlanner,
)

# Import custom scheduling tools
from final_project_tools.class_retrieval import ClassRetrievalTool
from final_project_tools.scheduler import SchedulerTool
from final_project_tools.checkers import (
    ClassNumberCheckerTool,
    UniqueAttendanceCheckerTool,
    ClassAttendanceCheckerTool,
)
from final_project_tools.period_validator import PeriodConflictCheckerTool
from final_project_tools.formatter import StructuredOutputFormatterTool
from final_project_tools.output_validator import OutputValidatorTool

# Load environment variables
load_dotenv()

# Configure settings
settings.api_keys.openai_api_key = os.getenv("OPENAI_API_KEY")
settings.api_keys.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# File paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CLASS_DB_PATH = os.path.join(CURRENT_DIR, "class_database.json")
CONFIG_PATH = os.path.join(CURRENT_DIR, "system_config.json")


def load_class_database():
    """Load class database from JSON file."""
    try:
        with open(CLASS_DB_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_class_database(data):
    """Save class database to JSON file."""
    try:
        with open(CLASS_DB_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return True, "✅ Class database saved successfully!"
    except Exception as e:
        return False, f"❌ Error saving database: {str(e)}"


def load_system_config():
    """Load system configuration from JSON file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default configuration
        return {
            "num_students": 10,
            "classes_per_student": 5,
            "num_days": 2,
            "periods_per_day": 6,
            "min_classes_per_day": 1
        }
    except json.JSONDecodeError:
        return {
            "num_students": 10,
            "classes_per_student": 5,
            "num_days": 2,
            "periods_per_day": 6,
            "min_classes_per_day": 1
        }


def save_system_config(config):
    """Save system configuration to JSON file."""
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        return True, "✅ Configuration saved successfully!"
    except Exception as e:
        return False, f"❌ Error saving configuration: {str(e)}"


def create_agent(llm, tools, role_description):
    """Factory function to create specialized worker agents."""
    tool_registry = ToolRegistry()
    for tool in tools:
        tool_registry.register_tool(tool)
    
    planner = ReActPlanner(llm, tool_registry)
    executor = ToolExecutor(tool_registry)
    memory = WorkingMemory()
    
    agent = SimpleAgent(llm, planner, executor, memory, stateless=False)
    agent.role_description = role_description
    return agent


# Global agents (initialized once)
scheduler_agent = None
validator_agent = None
formatter_agent = None
llm_name = ""


def initialize_agents():
    """Initialize all agents (called once at startup)."""
    global scheduler_agent, validator_agent, formatter_agent, llm_name
    
    # Load configuration
    config = load_system_config()
    
    # Initialize LLM
    if settings.api_keys.openai_api_key:
        llm_name = "OpenAI GPT-4o-mini"
        llm = OpenAIAdapter(
            api_key=settings.api_keys.openai_api_key,
            model_name="gpt-4o-mini"
        )
    elif settings.api_keys.anthropic_api_key:
        llm_name = "Anthropic Claude 3.5 Sonnet"
        llm = AnthropicAdapter(
            api_key=settings.api_keys.anthropic_api_key,
            model_name="claude-3-5-sonnet-20241022"
        )
    else:
        llm_name = "HuggingFace TinyLlama (CPU - Very Slow)"
        llm = HuggingFaceAdapter(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            auth_token=os.getenv("HUGGINGFACE_API_KEY")
        )
    
    # Create Scheduler Agent with dynamic configuration
    scheduler_agent = create_agent(
        llm,
        [ClassRetrievalTool(), SchedulerTool()],
        f"You are a scheduling specialist. Retrieve class data and generate a {config['num_days']}-day schedule "
        f"for {config['num_students']} students. Each student must have exactly {config['classes_per_student']} "
        f"unique classes with at least {config['min_classes_per_day']} class per day."
    )
    
    # Create Validator Agent
    validator_agent = create_agent(
        llm,
        [
            ClassNumberCheckerTool(),
            UniqueAttendanceCheckerTool(),
            ClassAttendanceCheckerTool(),
            PeriodConflictCheckerTool(),
        ],
        f"You are a validation specialist. Check that the schedule meets all constraints: "
        f"{config['classes_per_student']} classes per student, no duplicates, capacity respected, no period conflicts."
    )
    
    # Create Formatter Agent
    formatter_agent = create_agent(
        llm,
        [StructuredOutputFormatterTool(), OutputValidatorTool()],
        "You are a presentation specialist. Format the schedule as a clear, readable table with periods."
    )
    
    return f"✅ Multi-Agent System Ready!\n🤖 Using: {llm_name}"


async def generate_schedule_async(progress=gr.Progress()):
    """Generate schedule using the multi-agent system."""
    workflow_log = []
    
    # Load current configuration
    config = load_system_config()
    
    try:
        # Phase 1: Scheduler Agent
        progress(0.1, desc="🗓️ Scheduler Agent: Creating schedule...")
        workflow_log.append("=" * 80)
        workflow_log.append("PHASE 1: SCHEDULER AGENT")
        workflow_log.append("=" * 80)
        workflow_log.append(f"🗓️ Creating {config['num_days']}-day schedule for {config['num_students']} students...")
        
        schedule_response = await scheduler_agent.arun(
            f"Retrieve class data and generate a {config['num_days']}-day schedule for {config['num_students']} students. "
            f"Each student needs exactly {config['classes_per_student']} unique classes with at least {config['min_classes_per_day']} per day. "
            "Output the final schedule JSON."
        )
        workflow_log.append("✅ Schedule created successfully!\n")
        
        # Phase 2: Validator Agent
        progress(0.4, desc="✅ Validator Agent: Checking constraints...")
        workflow_log.append("=" * 80)
        workflow_log.append("PHASE 2: VALIDATOR AGENT")
        workflow_log.append("=" * 80)
        workflow_log.append("✅ Validating constraints...")
        
        validation_response = await validator_agent.arun(
            f"Validate this schedule meets all constraints:\n{schedule_response}\n\n"
            "Use ClassNumberCheckerTool, UniqueAttendanceCheckerTool, "
            "ClassAttendanceCheckerTool, and PeriodConflictCheckerTool. "
            "Report any issues found."
        )
        workflow_log.append("✅ Validation completed!\n")
        
        # Phase 3: Formatter Agent
        progress(0.7, desc="📋 Formatter Agent: Creating table...")
        workflow_log.append("=" * 80)
        workflow_log.append("PHASE 3: FORMATTER AGENT")
        workflow_log.append("=" * 80)
        workflow_log.append("📋 Formatting schedule as table...")
        
        format_response = await formatter_agent.arun(
            f"Format this schedule as a table:\n{schedule_response}\n\n"
            "Use StructuredOutputFormatterTool to create a readable table with periods. "
            "Present the final formatted schedule."
        )
        workflow_log.append("✅ Formatting completed!\n")
        
        progress(1.0, desc="✨ Complete!")
        
        # Get formatted table
        formatted_table = StructuredOutputFormatterTool.last_formatted_output
        
        if not formatted_table:
            # Fallback HTML formatting
            formatted_table = f"""
            <div style="padding: 30px; background: #fef5e7; border-left: 5px solid #f39c12; border-radius: 8px; font-family: 'Segoe UI', sans-serif;">
                <h3 style="color: #d68910; margin: 0 0 15px 0;">⚠️ Table Formatting Issue</h3>
                <p style="color: #7d6608; margin: 10px 0;">The schedule was generated but formatting failed. Raw schedule data:</p>
                <pre style="background: white; padding: 15px; border-radius: 4px; overflow-x: auto; font-size: 12px; margin-top: 10px; color: #2d3748;">{schedule_response}</pre>
            </div>
            """
        
        workflow_summary = "\n".join(workflow_log)
        
        return (
            formatted_table,
            validation_response,
            workflow_summary,
            "✅ Schedule generated successfully!"
        )
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        import traceback
        traceback_str = traceback.format_exc()
        
        # Format error as HTML
        error_html = f"""
        <div style="padding: 30px; background: #fee; border-left: 5px solid #f56565; border-radius: 8px; font-family: 'Segoe UI', sans-serif;">
            <h3 style="color: #c53030; margin: 0 0 15px 0;">❌ Schedule Generation Failed</h3>
            <p style="color: #742a2a; margin: 10px 0;"><strong>Error:</strong> {str(e)}</p>
            <details style="margin-top: 15px;">
                <summary style="cursor: pointer; color: #742a2a; font-weight: 600;">View Technical Details</summary>
                <pre style="background: #fff; padding: 15px; border-radius: 4px; overflow-x: auto; font-size: 12px; margin-top: 10px; color: #2d3748;">{traceback_str}</pre>
            </details>
        </div>
        """
        
        return (
            error_html,
            f"❌ Validation not performed due to error",
            f"{error_msg}\n\nTraceback:\n{traceback_str}",
            error_msg
        )


def get_class_data_display():
    """Get formatted display of current class data."""
    class_data = load_class_database()
    if not class_data:
        return "No class data available. Please add classes."
    
    display = []
    for day, classes in class_data.items():
        display.append(f"\n{'='*60}")
        display.append(f"{day}")
        display.append('='*60)
        for class_name, info in classes.items():
            periods_str = ", ".join(map(str, info.get('periods', [])))
            display.append(f"  📚 {class_name}")
            display.append(f"      Capacity: {info.get('capacity', 'N/A')}")
            display.append(f"      Periods: [{periods_str}]")
        display.append("")
    
    return "\n".join(display)


def add_or_update_class(day, class_name, capacity, periods_str):
    """Add or update a class in the database."""
    if not day or not class_name or not capacity:
        return False, "❌ Please fill in all required fields (Day, Class Name, Capacity)"
    
    try:
        capacity = int(capacity)
        if capacity < 1:
            return False, "❌ Capacity must be at least 1"
    except ValueError:
        return False, "❌ Capacity must be a valid number"
    
    # Parse periods
    try:
        periods = [int(p.strip()) for p in periods_str.split(",") if p.strip()]
        if not periods:
            return False, "❌ Please provide at least one period (e.g., 1, 2, 3)"
    except ValueError:
        return False, "❌ Periods must be comma-separated numbers (e.g., 1, 3, 5)"
    
    # Load current database
    class_data = load_class_database()
    
    # Ensure day exists
    if day not in class_data:
        class_data[day] = {}
    
    # Add or update class
    class_data[day][class_name] = {
        "capacity": capacity,
        "periods": sorted(periods)
    }
    
    # Save
    success, msg = save_class_database(class_data)
    if success:
        return True, f"✅ Class '{class_name}' added/updated successfully on {day}!"
    return success, msg


def delete_class(day, class_name):
    """Delete a class from the database."""
    if not day or not class_name:
        return False, "❌ Please select a day and class name"
    
    class_data = load_class_database()
    
    if day not in class_data or class_name not in class_data[day]:
        return False, f"❌ Class '{class_name}' not found on {day}"
    
    del class_data[day][class_name]
    
    # Remove day if empty
    if not class_data[day]:
        del class_data[day]
    
    success, msg = save_class_database(class_data)
    if success:
        return True, f"✅ Class '{class_name}' deleted from {day}!"
    return success, msg


def get_system_config_display():
    """Get formatted display of current system configuration."""
    config = load_system_config()
    return f"""
📊 Current Configuration:
{'='*50}
Number of Students: {config.get('num_students', 'N/A')}
Classes per Student: {config.get('classes_per_student', 'N/A')}
Number of Days: {config.get('num_days', 'N/A')}
Periods per Day: {config.get('periods_per_day', 'N/A')}
Minimum Classes per Day: {config.get('min_classes_per_day', 'N/A')}
"""


def get_system_config_display_dual():
    """Get formatted display for both config textboxes (returns same value twice)."""
    display = get_system_config_display()
    return display, display


def update_system_config(num_students, classes_per_student, num_days, periods_per_day, min_classes_per_day):
    """Update system configuration."""
    try:
        config = {
            "num_students": int(num_students),
            "classes_per_student": int(classes_per_student),
            "num_days": int(num_days),
            "periods_per_day": int(periods_per_day),
            "min_classes_per_day": int(min_classes_per_day)
        }
        
        # Validation
        if any(v < 1 for v in config.values()):
            return False, "❌ All values must be at least 1"
        
        if config["classes_per_student"] < config["min_classes_per_day"] * config["num_days"]:
            return False, f"❌ Classes per student must be >= min_classes_per_day * num_days"
        
        success, msg = save_system_config(config)
        
        if success:
            # Reinitialize agents with new configuration
            initialize_agents()
            return True, f"{msg}\n⚠️ Agents reinitialized with new configuration."
        
        return success, msg
        
    except ValueError:
        return False, "❌ All fields must be valid numbers"


def generate_schedule_sync():
    """Synchronous wrapper for async schedule generation."""
    return asyncio.run(generate_schedule_async())


# Note: Using Gradio's built-in theme system and inline styles for compatibility


def create_gui():
    """Create the Gradio interface."""
    
    # Initialize agents
    init_message = initialize_agents()
    print(init_message)
    
    with gr.Blocks(title="Multi-Agent Class Scheduler") as demo:
        # Header with inline styles
        gr.Markdown(
            f"""
            <div style="text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h1>🤖 Multi-Agent Class Scheduling System</h1>
            <p>AI-powered collaborative scheduling with specialized agents</p>
            <p style="font-size: 14px; margin-top: 10px;">💡 {llm_name}</p>
            </div>
            """
        )
        
        # Main tabs
        with gr.Tabs():
            # ==================== SCHEDULE GENERATION TAB ====================
            with gr.Tab("🚀 Generate Schedule"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        ### 📋 System Overview
                        
                        **Three Specialized Agents:**
                        - 🗓️ **Scheduler**: Creates class schedules
                        - ✅ **Validator**: Checks constraints
                        - 📋 **Formatter**: Presents results
                        """)
                        
                        # Show current config
                        config_display = gr.Textbox(
                            label="Current Configuration",
                            value=get_system_config_display(),
                            lines=8,
                            interactive=False
                        )
                        
                        refresh_config_btn = gr.Button("🔄 Refresh Config", size="sm")
                        
                        gr.Markdown("---")
                        
                        generate_btn = gr.Button(
                            "🚀 Generate Schedule",
                            variant="primary",
                            size="lg"
                        )
                        
                        status_output = gr.Textbox(
                            label="Status",
                            placeholder="Click the button to start...",
                            interactive=False,
                            max_lines=2
                        )
                
                # Results section
                gr.Markdown("---")
                gr.Markdown("## 📊 Results")
                
                with gr.Tabs():
                    with gr.Tab("📅 Schedule"):
                        schedule_output = gr.HTML(
                            label="Generated Schedule",
                            value="<div style='text-align: center; padding: 40px; color: #718096;'>Click 'Generate Schedule' to create a schedule...</div>"
                        )
                    
                    with gr.Tab("✅ Validation"):
                        validation_output = gr.Textbox(
                            label="Validation Results",
                            placeholder="Validation results will appear here...",
                            lines=15,
                            interactive=False
                        )
                    
                    with gr.Tab("⚙️ Workflow"):
                        workflow_output = gr.Textbox(
                            label="Agent Workflow Log",
                            placeholder="Workflow details will appear here...",
                            lines=20,
                            interactive=False
                        )
            
            # ==================== CLASS MANAGEMENT TAB ====================
            with gr.Tab("📚 Manage Classes"):
                gr.Markdown("""
                ### 📚 Class Database Management
                Add, update, or delete classes from the database.
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("#### Current Classes")
                        class_display = gr.Textbox(
                            label="All Classes",
                            value=get_class_data_display(),
                            lines=20,
                            interactive=False
                        )
                        refresh_classes_btn = gr.Button("🔄 Refresh", size="sm")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("#### Add/Update Class")
                        
                        day_input = gr.Textbox(
                            label="Day (e.g., Day1, Day2)",
                            placeholder="Day1"
                        )
                        class_name_input = gr.Textbox(
                            label="Class Name",
                            placeholder="Math"
                        )
                        capacity_input = gr.Number(
                            label="Capacity",
                            value=5,
                            minimum=1
                        )
                        periods_input = gr.Textbox(
                            label="Periods (comma-separated)",
                            placeholder="1, 3, 5"
                        )
                        
                        add_class_btn = gr.Button("➕ Add/Update Class", variant="primary")
                        class_status = gr.Textbox(label="Status", interactive=False, max_lines=2)
                        
                        gr.Markdown("---")
                        gr.Markdown("#### Delete Class")
                        
                        del_day_input = gr.Textbox(
                            label="Day",
                            placeholder="Day1"
                        )
                        del_class_input = gr.Textbox(
                            label="Class Name",
                            placeholder="Math"
                        )
                        
                        delete_class_btn = gr.Button("🗑️ Delete Class", variant="stop")
                        delete_status = gr.Textbox(label="Status", interactive=False, max_lines=2)
            
            # ==================== SYSTEM CONFIGURATION TAB ====================
            with gr.Tab("⚙️ System Config"):
                gr.Markdown("""
                ### ⚙️ System Configuration
                Configure scheduling parameters. Changes will reinitialize the agents.
                """)
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### Current Configuration")
                        sys_config_display = gr.Textbox(
                            label="Active Settings",
                            value=get_system_config_display(),
                            lines=8,
                            interactive=False
                        )
                        refresh_sys_config_btn = gr.Button("🔄 Refresh", size="sm")
                    
                    with gr.Column():
                        gr.Markdown("#### Update Configuration")
                        
                        num_students_input = gr.Number(
                            label="Number of Students",
                            value=10,
                            minimum=1
                        )
                        classes_per_student_input = gr.Number(
                            label="Classes per Student",
                            value=5,
                            minimum=1
                        )
                        num_days_input = gr.Number(
                            label="Number of Days",
                            value=2,
                            minimum=1
                        )
                        periods_per_day_input = gr.Number(
                            label="Periods per Day",
                            value=6,
                            minimum=1
                        )
                        min_classes_per_day_input = gr.Number(
                            label="Minimum Classes per Day",
                            value=1,
                            minimum=1
                        )
                        
                        update_config_btn = gr.Button("💾 Save Configuration", variant="primary")
                        config_status = gr.Textbox(label="Status", interactive=False, max_lines=3)
        
        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; font-size: 12px;">
        <p>Built with FAIR-LLM Framework | Multi-Agent Architecture</p>
        <p>CS471 Final Project - Intelligent Scheduling System</p>
        </div>
        """)
        
        # ==================== EVENT HANDLERS ====================
        
        # Schedule generation
        generate_btn.click(
            fn=generate_schedule_sync,
            inputs=[],
            outputs=[schedule_output, validation_output, workflow_output, status_output]
        )
        
        # Config refresh
        refresh_config_btn.click(
            fn=get_system_config_display,
            inputs=[],
            outputs=[config_display]
        )
        
        # Class management
        refresh_classes_btn.click(
            fn=get_class_data_display,
            inputs=[],
            outputs=[class_display]
        )
        
        add_class_btn.click(
            fn=lambda d, c, cap, p: add_or_update_class(d, c, cap, p),
            inputs=[day_input, class_name_input, capacity_input, periods_input],
            outputs=[class_status]
        ).then(
            fn=get_class_data_display,
            inputs=[],
            outputs=[class_display]
        )
        
        delete_class_btn.click(
            fn=lambda d, c: delete_class(d, c),
            inputs=[del_day_input, del_class_input],
            outputs=[delete_status]
        ).then(
            fn=get_class_data_display,
            inputs=[],
            outputs=[class_display]
        )
        
        # System config
        refresh_sys_config_btn.click(
            fn=get_system_config_display,
            inputs=[],
            outputs=[sys_config_display]
        )
        
        update_config_btn.click(
            fn=lambda s, c, d, p, m: update_system_config(s, c, d, p, m),
            inputs=[
                num_students_input,
                classes_per_student_input,
                num_days_input,
                periods_per_day_input,
                min_classes_per_day_input
            ],
            outputs=[config_status]
        ).then(
            fn=get_system_config_display_dual,
            inputs=[],
            outputs=[sys_config_display, config_display]
        )
    
    return demo


if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Starting Multi-Agent Class Scheduling GUI...")
    print("=" * 80)
    
    demo = create_gui()
    
    print("\n✅ GUI Ready! Opening in browser...")
    print("=" * 80)
    
    # Launch with share=True to get a public link (optional)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,  # Set to True for public link
        show_error=True
    )

