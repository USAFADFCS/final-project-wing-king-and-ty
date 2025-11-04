"""
FAIR-LLM Demo: Simplified Multi-Agent Class Scheduling System
--------------------------------------------------------------

This is a simplified multi-agent implementation that manually coordinates
specialized agents instead of using the HierarchicalAgentRunner.

Architecture:
- Scheduler Agent: Creates schedules
- Validator Agent: Checks constraints
- Formatter Agent: Presents results
- Main orchestrator: Manually coordinates the workflow

This avoids ManagerPlanner API compatibility issues while demonstrating
multi-agent collaboration!
"""

import asyncio
import os
from dotenv import load_dotenv
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


def create_agent(llm, tools, role_description):
    """
    Factory function to create specialized worker agents.
    """
    tool_registry = ToolRegistry()
    for tool in tools:
        tool_registry.register_tool(tool)
    
    planner = ReActPlanner(llm, tool_registry)
    executor = ToolExecutor(tool_registry)
    memory = WorkingMemory()
    
    agent = SimpleAgent(llm, planner, executor, memory, stateless=False)
    agent.role_description = role_description
    return agent


async def main():
    print("=" * 80)
    print("🤖 Simplified Multi-Agent Class Scheduling System")
    print("=" * 80)
    
    # === Initialize LLM ===
    print("\n📚 Initializing AI language model...")
    if settings.api_keys.openai_api_key:
        print("   Using OpenAI GPT-4o-mini")
        llm = OpenAIAdapter(
            api_key=settings.api_keys.openai_api_key,
            model_name="gpt-4o-mini"
        )
    elif settings.api_keys.anthropic_api_key:
        print("   Using Anthropic Claude")
        llm = AnthropicAdapter(
            api_key=settings.api_keys.anthropic_api_key,
            model_name="claude-3-5-sonnet-20241022"
        )
    else:
        print("   Using HuggingFace TinyLlama (SLOW)")
        llm = HuggingFaceAdapter(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            auth_token=os.getenv("HUGGINGFACE_API_KEY")
        )
    
    # === Create Specialized Agents ===
    print("\n👥 Building the agent team...")
    
    # 🗓️ SCHEDULER AGENT
    scheduler_agent = create_agent(
        llm,
        [ClassRetrievalTool(), SchedulerTool()],
        "You are a scheduling specialist. Retrieve class data and generate a 2-day schedule for 10 students. "
        "Each student must have exactly 5 unique classes with at least one class per day."
    )
    print("   ✓ Scheduler Agent created")
    
    # ✅ VALIDATOR AGENT
    validator_agent = create_agent(
        llm,
        [
            ClassNumberCheckerTool(),
            UniqueAttendanceCheckerTool(),
            ClassAttendanceCheckerTool(),
            PeriodConflictCheckerTool(),
        ],
        "You are a validation specialist. Check that the schedule meets all constraints: "
        "5 classes per student, no duplicates, capacity respected, no period conflicts."
    )
    print("   ✓ Validator Agent created")
    
    # 📋 FORMATTER AGENT
    formatter_agent = create_agent(
        llm,
        [StructuredOutputFormatterTool(), OutputValidatorTool()],
        "You are a presentation specialist. Format the schedule as a clear, readable table with periods."
    )
    print("   ✓ Formatter Agent created")
    
    print("\n🚀 Multi-agent team is ready!")
    
    # === Interaction Loop ===
    print("\n" + "=" * 80)
    print("💬 Multi-Agent Scheduling System")
    print("=" * 80)
    print("Type 'generate schedule' to create a schedule, or 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("👤 You: ").strip().lower()
            
            if user_input in ["quit", "exit"]:
                print("🤖 Team: Goodbye! 👋")
                break
            
            if "generate" in user_input:
                print("\n" + "=" * 80)
                print("⚙️  MULTI-AGENT WORKFLOW")
                print("=" * 80)
                
                # === PHASE 1: SCHEDULER AGENT ===
                print("\n🗓️  PHASE 1: Scheduler Agent - Creating Schedule")
                print("-" * 80)
                schedule_response = await scheduler_agent.arun(
                    "Retrieve class data and generate a 2-day schedule for 10 students. "
                    "Each student needs exactly 5 unique classes with at least one per day. "
                    "Output the final schedule JSON."
                )
                print(f"✅ Scheduler completed")
                
                # === PHASE 2: VALIDATOR AGENT ===
                print("\n✅ PHASE 2: Validator Agent - Checking Constraints")
                print("-" * 80)
                validation_response = await validator_agent.arun(
                    f"Validate this schedule meets all constraints:\n{schedule_response}\n\n"
                    "Use ClassNumberCheckerTool, UniqueAttendanceCheckerTool, "
                    "ClassAttendanceCheckerTool, and PeriodConflictCheckerTool. "
                    "Report any issues found."
                )
                print(f"✅ Validator completed")
                
                # === PHASE 3: FORMATTER AGENT ===
                print("\n📋 PHASE 3: Formatter Agent - Presenting Results")
                print("-" * 80)
                format_response = await formatter_agent.arun(
                    f"Format this schedule as a table:\n{schedule_response}\n\n"
                    "Use StructuredOutputFormatterTool to create a readable table with periods. "
                    "Present the final formatted schedule."
                )
                print(f"✅ Formatter completed")
                
                # === FINAL REPORT ===
                print("\n" + "=" * 80)
                print("📊 FINAL MULTI-AGENT REPORT")
                print("=" * 80)
                
                # Get the formatted table from the tool
                formatted_table = StructuredOutputFormatterTool.last_formatted_output
                
                if formatted_table:
                    print("\n📅 Final Schedule:")
                    print(formatted_table)
                    print("\n✅ Validation Summary:")
                    print(validation_response)
                else:
                    print("\n📅 Schedule:")
                    print(schedule_response)
                    print("\n✅ Validation:")
                    print(validation_response)
                    print("\n📋 Formatting:")
                    print(format_response)
                
                print("\n" + "=" * 80)
                print("✨ All agents completed their tasks successfully!")
                print("=" * 80)
            else:
                print("🤖 Team: Please type 'generate schedule' or 'quit'.")
        
        except KeyboardInterrupt:
            print("\n🤖 Team: Session ended by user.")
            break
        except Exception as e:
            print(f"❌ System error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

