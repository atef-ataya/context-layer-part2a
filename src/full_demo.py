"""
full_demo.py

Complete end-to-end demonstration script for YouTube video recording.

This script orchestrates the entire demo flow:
1. Title banner and intro
2. Neo4j connection check
3. Graphiti initialization
4. RAG failure simulation (the problem)
5. Episode ingestion (building the solution)
6. Temporal queries (the magic moment)
7. Summary and next steps

Designed to be run on camera with clear visual output and pauses
for the presenter to explain concepts between sections.

TUTORIAL NOTE: This is the "press play and record" script for the video.
All output is formatted for visual clarity during screen recording.
"""

import asyncio
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from neo4j import AsyncGraphDatabase

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
    console.print("\n[dim]A hands-on demonstration by Atef Ataya")
    console.print("atefataya.com[/dim]\n")


async def check_neo4j_connection() -> bool:
    """
    Verify that Neo4j is running and accessible.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    console.print("[bold yellow]Checking Neo4j connection...[/bold yellow]")
    
    load_dotenv()
    import os
    
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    
    try:
        driver = AsyncGraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        async with driver.session() as session:
            result = await session.run("RETURN 1 as test")
            await result.single()
        
        await driver.close()
        console.print("✓ Neo4j is running and accessible\n", style="green")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Neo4j connection failed![/bold red]")
        console.print(f"Error: {str(e)}\n")
        console.print("[yellow]Please start Neo4j:[/yellow]")
        console.print("  docker-compose up -d")
        console.print("\nThen wait 10-15 seconds for Neo4j to fully start.")
        return False


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
    
    # 2. NEO4J CONNECTION CHECK
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 1: Environment Check[/bold cyan]\n")
    
    if not await check_neo4j_connection():
        console.print("[bold red]Demo cannot proceed without Neo4j. Exiting.[/bold red]")
        sys.exit(1)
    
    # 3. GRAPHITI INITIALIZATION
    console.print("=" * 80 + "\n")
    console.print("[bold cyan]STEP 2: Initialize Graphiti[/bold cyan]\n")
    
    try:
        graphiti = await setup_graphiti()
        console.print()
    except Exception as e:
        console.print(f"[bold red]Failed to initialize Graphiti: {e}[/bold red]")
        sys.exit(1)
    
    pause_for_presenter("Press Enter to see why RAG fails...")
    
    # 4. RAG FAILURE SIMULATION
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 3: The Problem - RAG Failure Modes[/bold cyan]\n")
    
    # Run the RAG failure demo (synchronous)
    demo_rag_failures()
    
    pause_for_presenter("Press Enter to see the solution...")
    
    # 5. EPISODE INGESTION
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 4: Building Memory - Add Episodes[/bold cyan]\n")
    
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
    
    # 6. TEMPORAL QUERIES (The Magic Moment)
    console.print("\n" + "=" * 80 + "\n")
    console.print("[bold cyan]STEP 5: The Magic - Temporal Queries[/bold cyan]\n")
    
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
    
    # 7. SUMMARY AND COMPARISON
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
        "✓ Native\n(time is first-class)"
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
        "✓ Point-in-time accuracy"
    )
    
    console.print(comparison_table)
    
    # 8. NEXT STEPS
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
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        sys.exit(1)
