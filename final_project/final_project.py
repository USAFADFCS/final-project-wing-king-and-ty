"""
FAIR-LLM Demo: Intelligent Class Scheduling Agent
--------------------------------------------------

This demo assembles a reasoning agent that builds a valid 2-day class schedule for 10 students.
The system uses multiple modular tools to coordinate scheduling, validation, and formatting,
demonstrating agentic reasoning and tool orchestration.

Agent Responsibilities:
    1. Retrieve available classes and capacities
    2. Generate a fair 2-day schedule ensuring:
        - 6 unique classes per day
        - 10 students total
        - Each student takes exactly 5 total classes (at least 1 per day)
        - No duplicate classes per student
        - No overbooked classes
    3. Format the result in a structured (table-like) format
"""

import asyncio
import os
import json
import re
from dotenv import load_dotenv
from fairlib import (
    ToolRegistry,
    ToolExecutor,
    WorkingMemory,
    SimpleAgent,
    RoleDefinition,
    HuggingFaceAdapter,
    OpenAIAdapter,
    AnthropicAdapter,
    SimpleReActPlanner,
)

# --- Step 2: Import custom FairLLM tools for scheduling ---
from final_project_tools.class_retrieval import ClassRetrievalTool
from final_project_tools.scheduler import SchedulerTool
from final_project_tools.checkers import (
    ClassNumberCheckerTool,
    UniqueAttendanceCheckerTool,
    ClassAttendanceCheckerTool,
    ClassCounterCheckerTool,
    ScheduleValidatorTool,
)
from final_project_tools.formatter import StructuredOutputFormatterTool
from final_project_tools.output_validator import OutputValidatorTool
from final_project_tools.period_validator import PeriodConflictCheckerTool


async def main():
    """Main entry point for the FairLLM Class Scheduler demo."""
    # Load environment variables from .env file
    load_dotenv()
    
    print("🏫 Initializing the FAIR-LLM Class Scheduling Agent...")

    # === (a) Brain: Language Model ===
    # Try different LLM providers (prefer faster cloud APIs)
    if os.getenv("OPENAI_API_KEY"):
        print("🤖 Using OpenAI GPT-4o-mini (fast)")
        llm = OpenAIAdapter(model_name="gpt-4o-mini")
    elif os.getenv("ANTHROPIC_API_KEY"):
        print("🤖 Using Anthropic Claude (fast)")
        llm = AnthropicAdapter(model_name="claude-3-5-sonnet-20241022")
    else:
        print("🤖 Using HuggingFace TinyLlama (SLOW - runs on CPU)")
        print("⚠️  Warning: This will be very slow. Consider using OpenAI or Anthropic API instead.")
        llm = HuggingFaceAdapter(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
            auth_token=os.getenv("HUGGINGFACE_API_KEY")
        )

    # === (b) Toolbelt: Register all scheduling tools ===
    tool_registry = ToolRegistry()

    tool_registry.register_tool(ClassRetrievalTool())
    tool_registry.register_tool(SchedulerTool())
    tool_registry.register_tool(ClassNumberCheckerTool())
    tool_registry.register_tool(UniqueAttendanceCheckerTool())
    tool_registry.register_tool(ClassAttendanceCheckerTool())
    tool_registry.register_tool(ClassCounterCheckerTool())
    tool_registry.register_tool(ScheduleValidatorTool())
    tool_registry.register_tool(PeriodConflictCheckerTool())
    tool_registry.register_tool(StructuredOutputFormatterTool())
    tool_registry.register_tool(OutputValidatorTool())

    print(f"✅ Registered tools: {[t.name for t in tool_registry.get_all_tools().values()]}")

    # === (c) Hands: Tool Executor ===
    executor = ToolExecutor(tool_registry)

    # === (d) Memory: Conversation Context ===
    memory = WorkingMemory()

    # === (e) Mind: Reasoning Engine ===
    planner = SimpleReActPlanner(llm, tool_registry)

    # Modify agent role / personality
    planner.prompt_builder.role_definition = RoleDefinition(
        "You are an intelligent scheduling assistant. Follow these steps EXACTLY:\n\n"
        "1. Use ClassRetrievalTool to get class data (includes capacity and periods)\n"
        "2. Use SchedulerTool with the class data JSON to generate a schedule with periods\n"
        "3. Use ClassNumberCheckerTool with ONLY the schedule JSON (no class_data)\n"
        "4. Use UniqueAttendanceCheckerTool with ONLY the schedule JSON (no class_data)\n"
        "5. Use PeriodConflictCheckerTool with ONLY the schedule JSON (no class_data)\n"
        "6. Use StructuredOutputFormatterTool with ONLY the schedule JSON (no class_data)\n"
        "7. Use OutputValidatorTool with schedule JSON and formatted table\n"
        "8. In your Final Answer, present the formatted table clearly\n\n"
        "CRITICAL RULES:\n"
        "- StructuredOutputFormatterTool expects ONLY schedule data, not class_data\n"
        "- Validation tools (steps 3-5) expect ONLY schedule data\n"
        "- Only ClassAttendanceCheckerTool needs both schedule and class_data\n"
        "- Your final answer must include the complete formatted schedule table!"
    )

    # === (f) Assemble the Agent ===
    agent = SimpleAgent(
        llm=llm,
        planner=planner,
        tool_executor=executor,
        memory=memory,
        max_steps=18,  # Increased to allow for period validation and output validation
    )

    print("🎓 Agent is ready to create schedules.")
    print("💬 Type 'generate schedule' to create one, or 'quit' to exit.\n")

    # === (g) Interaction Loop ===
    while True:
        try:
            user_input = input("👤 You: ").strip().lower()
            if user_input in ["quit", "exit"]:
                print("🤖 Agent: Goodbye! 👋")
                break

            if "generate" in user_input:
                print("⚙️ Generating schedule...")
                response = await agent.arun(
                    "Generate a 2-day class schedule for 10 students. "
                    "Each student must have at least one class per day, "
                    "take exactly 5 unique classes total, and classes cannot exceed their capacity."
                )
                
                # Post-process the response to display nicely formatted output
                print("\n🤖 Agent Response:")
                print("=" * 80)
                
                # Try to parse the response as JSON to extract formatted components
                try:
                    # Look for JSON structure in the response
                    json_match = re.search(r'\{[\s\S]*\}', response)
                    if json_match:
                        parsed = json.loads(json_match.group())
                        
                        # Display validation report
                        if "validation_report" in parsed:
                            report = parsed["validation_report"]
                            print("\n📊 Validation Report:")
                            print(f"   Clarity Score: {report.get('clarity_score', 'N/A')}/100")
                            print(f"   Summary: {report.get('summary', 'N/A')}")
                            print(f"   Students: {report.get('student_count', 'N/A')}")
                            print(f"   Total Classes: {report.get('total_classes', 'N/A')}")
                            
                            if report.get('issues'):
                                print(f"\n   ⚠️ Issues: {', '.join(report['issues'])}")
                            if report.get('suggestions'):
                                print(f"   💡 Suggestions: {', '.join(report['suggestions'])}")
                        
                        # Display formatted schedule (with proper line breaks)
                        if "formatted_schedule" in parsed:
                            print("\n📅 Final Schedule:")
                            print(parsed["formatted_schedule"])
                        else:
                            print(f"\n{response}")
                    else:
                        # If not JSON, just print the response
                        print(f"\n{response}")
                        
                except (json.JSONDecodeError, Exception):
                    # If parsing fails, display the raw response
                    print(f"\n{response}")
                
                print("\n" + "=" * 80)
            else:
                print("🤖 Agent: Please type 'generate schedule' or 'quit'.")

        except KeyboardInterrupt:
            print("\n🤖 Agent: Session ended by user.")
            break
        except Exception as e:
            print(f"❌ Agent error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
