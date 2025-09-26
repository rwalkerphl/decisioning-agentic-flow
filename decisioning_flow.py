#!/usr/bin/env python3
"""
Decisioning Agentic Flow - Main Entry Point
Execute intelligent business decision-making with autonomous agents
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from orchestration.orchestrator import DecisioningOrchestrator

async def main():
    """Main execution function"""

    print("🎯 DECISIONING AGENTIC FLOW")
    print("=" * 50)
    print("Intelligent Business Decision-Making System")
    print("Powered by Autonomous Agents")
    print("=" * 50)
    print()

    try:
        # Initialize the orchestrator
        orchestrator = DecisioningOrchestrator()

        # Execute full decisioning analysis
        results = await orchestrator.run_decisioning_analysis()

        print("\n🎉 SUCCESS!")
        print("Decisioning analysis completed with strategic recommendations ready.")
        print("\n📋 Quick Access:")
        print("• Executive Summary: executive_summary.json")
        print("• Full Results: decisioning_results.json")
        print("• Dashboard: streamlit run dashboards/decisioning_dashboard.py")

        return results

    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())