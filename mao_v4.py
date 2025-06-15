#!/usr/bin/env python3
"""
OC - Main CLI Entry Point
Uses the clean terminal interface for beautiful UX
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add interfaces to path
sys.path.append(str(Path(__file__).parent))

from interfaces.terminal import OCTerminalInterface


async def main():
    """🚀 Main CLI entry point using clean interface"""
    
    parser = argparse.ArgumentParser(
        description="OC - AI Workflow Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python oc_main.py "Create a marketing strategy for my startup"
  python oc_main.py --job-app "job_description.txt" --company "TechCorp"
  python oc_main.py --list-workflows
  python oc_main.py --stats --verbose
        """
    )
    
    parser.add_argument("goal", nargs="?", help="Natural language goal to execute")
    parser.add_argument("--workspace", "-w", help="Custom workspace directory")
    parser.add_argument("--job-app", help="Job description file for job application workflow")
    parser.add_argument("--company", help="Company name for job application")
    parser.add_argument("--list-workflows", action="store_true", help="List all workflows")
    parser.add_argument("--stats", action="store_true", help="Show orchestrator stats")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show technical details")
    parser.add_argument("--free-only", action="store_true", help="Use only free models")
    parser.add_argument("--privacy", action="store_true", help="Use privacy-focused models")
    
    args = parser.parse_args()
    
    # Initialize OC with verbosity setting
    try:
        oc = OCTerminalInterface(verbose=args.verbose)
    except Exception as e:
        print(f"❌ Failed to initialize OC: {e}")
        sys.exit(1)
    
    # Handle different command types
    if args.stats:
        mao.get_stats()
        return
    
    if args.list_workflows:
        mao.list_workflows()
        return
    
    if args.job_app:
        if not args.company:
            print("❌ --company is required when using --job-app")
            sys.exit(1)
        
        # Read job description
        try:
            with open(args.job_app, 'r') as f:
                job_description = f.read()
        except FileNotFoundError:
            print(f"❌ Job description file not found: {args.job_app}")
            sys.exit(1)
        
        result = await mao.job_application_workflow(
            job_description, 
            args.company, 
            args.workspace
        )
        
        if result.get("success"):
            print(f"\n🎉 Job application package created!")
            print(f"📁 Files saved to: {result['workspace']}")
        else:
            print(f"❌ Job application failed: {result.get('error')}")
            sys.exit(1)
    
    elif args.goal:
        # Set up preferences
        preferences = {}
        if args.free_only:
            preferences["free_only"] = True
        if args.privacy:
            preferences["privacy_focused"] = True
        
        result = await mao.execute_goal(args.goal, args.workspace, preferences)
        
        if result.get("success"):
            mao.display.success_summary(result["workspace"], result["total_cost"])
        elif result.get("cancelled"):
            print("👋 See you next time!")
        else:
            print(f"❌ Goal failed: {result.get('error')}")
            sys.exit(1)
    
    else:
        # Interactive mode
        print("🎭 OC - AI Workflow Orchestrator")
        print("Type your goal in natural language, or 'quit' to exit")
        print("=" * 60)
        
        while True:
            try:
                goal = input("\n🎯 Goal: ").strip()
                
                if goal.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not goal:
                    continue
                
                if goal.lower() == 'stats':
                    mao.get_stats()
                    continue
                
                if goal.lower() == 'list':
                    mao.list_workflows()
                    continue
                
                result = await mao.execute_goal(goal)
                
                if result.get("success"):
                    mao.display.success_summary(result["workspace"], result["total_cost"])
                elif not result.get("cancelled"):
                    print("Try rephrasing your goal or type 'quit' to exit")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
