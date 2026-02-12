"""
full_demo.py

Complete end-to-end demonstration script for YouTube video recording.

This script orchestrates the entire demo flow:
1. Title banner and intro
2. Graphiti initialization (includes Neo4j connection)
3. RAG failure simulation (the problem)
4. Episode ingestion (building the solution)
5. Temporal queries (the magic moment)
6. Summary and next steps

Designed to be run on camera with clear visual output and pauses
for the presenter to explain concepts between sections.

TUTORIAL NOTE: This is the "press play and record" script for the video.
All output is formatted for visual clarity during screen recording.
"""

import asyncio
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv
from rich.markup import escape
from rich.console import Console
from rich.panel import Panel

# Import our demo modules
from demo_rag_failure import main as demo_rag_failures
from setup_graphiti import setup_graphiti
from add_episodes import add_text_episodes, add_json_episode
from query_memory import (
    query_current_leader,
    query_historical_leader,
    query_current_status,
    query_historical_status,
    query_entity_history
)

console = Console()


def print_banner():
    """
    Print the main title banner for the video.
    """
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              THE CONTEXT LAYER — Part 2a                     ║
║                                                              ║
║           Memory Beyond RAG: Temporal Knowledge Graphs       ║
║                                                              ║
║                    Featuring: Graphiti + Neo4j               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("\n[dim]A hands-on demonstration by Atef Ataya\natefataya.com[/dim]\n")


def pause_for_presenter(message: str = "Press Enter to continue..."):
    """
    Pause execution to allow presenter to speak to camera.
    
    Args:
        message: Custom prompt message
    """
    console.print(f"\n[dim italic]{message}[/dim italic]")
    input()


async def main():
    """
    Main demo orchestration function.
    """
    # 1. BANNER AND INTRO
    print_banner()
    
    console.print(Panel.fit(
        "[bold]This demo shows:[/bold]\n\n"
        "  🔍 Why RAG fails (3 failure modes)\n"
        "  🧠 How temporal knowledge graphs solve it\n"
        "  ✨ Memory in action (temporal queries)\n\n"
        "[dim]Estimated runtime: 3-5 minutes[/dim]",
        title="📋 Overview",
        border_style="cyan"
    ))
    
    pause_for_presenter()
    
    # 2. GRAPHITI INITIALIZATION (also verifies Neo4j connection)
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 1: Initialize Graphiti + Neo4j[/bold cyan]\n")
    
    try:
        graphiti = await setup_graphiti()
        console.print()
    except Exception as e:
        console.print(f"[bold red]Failed to initialize Graphiti: {e}[/bold red]")
        console.print("\n[yellow]Please ensure:[/yellow]")
        console.print("  1. Neo4j is running: docker-compose up -d")
        console.print("  2. Wait 10-15 seconds for Neo4j to start")
        console.print("  3. Your .env file has a valid OPENAI_API_KEY")
        sys.exit(1)
    
    pause_for_presenter("Press Enter to see why RAG fails...")
    
    # 3. RAG FAILURE SIMULATION
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 2: The Problem - RAG Failure Modes[/bold cyan]\n")
    
    # Run the RAG failure demo (synchronous)
    demo_rag_failures()
    
    pause_for_presenter("Press Enter to see the solution...")
    
    # 4. EPISODE INGESTION
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 3: Building Memory - Add Episodes[/bold cyan]\n")
    
    console.print(Panel.fit(
        "Now we'll add the same Project Alpha information to Graphiti.\n"
        "Instead of independent documents, Graphiti builds a temporal graph\n"
        "that understands relationships, causality, and time.",
        border_style="yellow"
    ))
    console.print()
    
    try:
        await add_text_episodes(graphiti)
        await add_json_episode(graphiti)
    except Exception as e:
        console.print(f"[bold red]Failed to add episodes: {e}[/bold red]")
        await graphiti.close()
        sys.exit(1)
    
    pause_for_presenter("Press Enter to query the memory...")
    
    # 5. TEMPORAL QUERIES (The Magic Moment)
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 4: The Magic - Temporal Queries[/bold cyan]\n")
    
    console.print(Panel.fit(
        "[bold yellow]This is where the value becomes clear.[/bold yellow]\n\n"
        "We'll ask the same questions at different points in time\n"
        "and get different (correct) answers.",
        border_style="yellow"
    ))
    
    try:
        # Current state queries
        console.print("\n[bold white]Current State Queries:[/bold white]")
        await query_current_leader(graphiti)
        console.print("\n" + "─" * 60)
        await query_current_status(graphiti)
        
        console.print("\n\n[bold white]Historical (Time Travel) Queries:[/bold white]")
        await query_historical_leader(graphiti)
        console.print("\n" + "─" * 60)
        await query_historical_status(graphiti)
        
        console.print("\n\n[bold white]Entity Evolution:[/bold white]")
        await query_entity_history(graphiti)
        
    except Exception as e:
        console.print(f"[bold red]Query failed: {e}[/bold red]")
        await graphiti.close()
        sys.exit(1)
    
    # 6. SUMMARY AND COMPARISON
    console.print("\n\n" + "=" * 80 + "\n")
    console.print("[bold cyan]Summary: RAG vs. Memory[/bold cyan]\n")
    
    from rich.table import Table
    from rich import box
    
    comparison_table = Table(
        title="The Fundamental Difference",
        box=box.DOUBLE,
        show_header=True,
        header_style="bold magenta",
        title_style="bold white"
    )
    comparison_table.add_column("Aspect", style="cyan", width=25)
    comparison_table.add_column("RAG", style="red", width=30)
    comparison_table.add_column("Temporal Memory", style="green", width=30)
    
    comparison_table.add_row(
        "Storage Model",
        "Independent documents\n(vector embeddings)",
        "Temporal knowledge graph\n(entities + relationships + time)"
    )
    comparison_table.add_row(
        "Retrieval Method",
        "Semantic similarity\n(cosine distance)",
        "Graph traversal\n(temporal context-aware)"
    )
    comparison_table.add_row(
        "Temporal Awareness",
        "❌ None\n(all docs treated equally)",
        "✓ Native\n(valid_at / invalid_at)"
    )
    comparison_table.add_row(
        "Causality",
        "❌ Cannot track\n(contradictions common)",
        "✓ Explicit edges\n(A causes B)"
    )
    comparison_table.add_row(
        "Entity Evolution",
        "❌ Disconnected chunks",
        "✓ Complete narrative"
    )
    comparison_table.add_row(
        "Historical Queries",
        "❌ Impossible",
        "✓ Bi-temporal model"
    )
    
    console.print(comparison_table)
    
    # 7. NEXT STEPS
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]✓ Demo Complete![/bold green]\n\n"
        "[bold white]What you've learned:[/bold white]\n"
        "  • RAG's 3 fundamental limitations\n"
        "  • How temporal knowledge graphs solve them\n"
        "  • Practical implementation with Graphiti + Neo4j\n\n"
        "[bold cyan]Coming in Part 2b:[/bold cyan]\n"
        "  • MCP integration (Model Context Protocol)\n"
        "  • FalkorDB as a lightweight alternative\n"
        "  • Production deployment patterns\n"
        "  • Enterprise-scale considerations\n\n"
        "[dim]GitHub: [link]https://github.com/atefataya/context-layer-part2a[/link]\n"
        "Tutorial: [link]https://atefataya.com[/link][/dim]",
        title="🎬 That's a Wrap!",
        border_style="green"
    ))
    
    # Clean up
    await graphiti.close()
    
    console.print("\n[bold cyan]Thank you for watching![/bold cyan]")
    console.print("[dim]Don't forget to subscribe and check out Part 2b![/dim]\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted by user. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {escape(str(e))}")
        sys.exit(1)