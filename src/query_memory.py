"""
query_memory.py

Demonstrates temporal queries with Graphiti - the "magic moment" of the tutorial.

This module shows what makes temporal knowledge graphs revolutionary:
1. Current state queries - "What is true NOW?"
2. Historical queries - "What was true THEN?" (point-in-time)
3. Entity evolution - "How did this change over time?"

Unlike RAG, which retrieves similar documents regardless of time,
Graphiti understands temporal context and can answer questions about
any point in the timeline.

TUTORIAL NOTE: This is where the value proposition becomes crystal clear.
The same query with different time contexts returns completely different
(and correct) answers.
"""

import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from setup_graphiti import setup_graphiti

console = Console()


async def query_current_leader(graphiti):
    """
    Query 1: Current state - Who is leading Project Alpha NOW?
    
    This demonstrates standard knowledge graph querying.
    Expected answer: Sarah (as of our latest episode)
    """
    console.print("\n[bold cyan]Query 1: Current State[/bold cyan]")
    console.print("Question: [italic]Who is leading Project Alpha?[/italic]\n")
    
    # TUTORIAL NOTE: Without specifying a center_date, Graphiti returns
    # the current state of the knowledge graph (most recent information)
    results = await graphiti.search("Who is leading Project Alpha?")
    
    console.print("[bold]Graphiti Response:[/bold]")
    console.print(results)
    
    console.print("\n[dim]💡 RAG would return: Documents mentioning both John AND Sarah")
    console.print("   Memory returns: Sarah (current state)[/dim]")
    
    return results


async def query_historical_leader(graphiti):
    """
    Query 2: Historical (point-in-time) - Who WAS leading Project Alpha on Jan 8?
    
    This is the killer feature: temporal queries.
    On Jan 8, John was still the leader (Sarah took over on Jan 12).
    
    Expected answer: John
    """
    console.print("\n[bold cyan]Query 2: Historical / Point-in-Time[/bold cyan]")
    console.print("Question: [italic]Who was leading Project Alpha on January 8, 2026?[/italic]\n")
    
    # TUTORIAL NOTE: center_date parameter enables time travel!
    # Graphiti returns the state of the world as it was at that specific moment.
    # This is impossible with traditional RAG.
    historical_date = datetime(2026, 1, 8, tzinfo=timezone.utc)
    
    results = await graphiti.search(
        "Who was leading Project Alpha?",
        center_date=historical_date
    )
    
    console.print(f"[bold]Graphiti Response (as of {historical_date.strftime('%B %d, %Y')}):[/bold]")
    console.print(results)
    
    console.print("\n[dim]💡 RAG would return: Same documents as Query 1 (no temporal awareness)")
    console.print("   Memory returns: John (correct historical state)[/dim]")
    
    return results


async def query_current_status(graphiti):
    """
    Query 3: Current status - What is the status of Project Alpha NOW?
    
    Expected answer: Complete / Deployed to production
    """
    console.print("\n[bold cyan]Query 3: Current Project Status[/bold cyan]")
    console.print("Question: [italic]What is the status of Project Alpha?[/italic]\n")
    
    results = await graphiti.search("What is the status of Project Alpha?")
    
    console.print("[bold]Graphiti Response:[/bold]")
    console.print(results)
    
    console.print("\n[dim]💡 RAG might return: The 'BLOCKED' document (semantically richer)")
    console.print("   Memory returns: Complete/Deployed (current accurate state)[/dim]")
    
    return results


async def query_historical_status(graphiti):
    """
    Query 4: Historical status - What WAS the status on Jan 8?
    
    On Jan 8, the project was blocked due to API issues.
    This demonstrates temporal accuracy for status tracking.
    
    Expected answer: Blocked
    """
    console.print("\n[bold cyan]Query 4: Historical Project Status[/bold cyan]")
    console.print("Question: [italic]What was the status of Project Alpha on January 8, 2026?[/italic]\n")
    
    historical_date = datetime(2026, 1, 8, tzinfo=timezone.utc)
    
    results = await graphiti.search(
        "What was the status of Project Alpha?",
        center_date=historical_date
    )
    
    console.print(f"[bold]Graphiti Response (as of {historical_date.strftime('%B %d, %Y')}):[/bold]")
    console.print(results)
    
    console.print("\n[dim]💡 RAG would return: Mixed results (blocked + in progress + complete)")
    console.print("   Memory returns: Blocked (correct historical state)[/dim]")
    
    return results


async def query_entity_history(graphiti):
    """
    Query 5: Entity evolution - What happened with Project Alpha?
    
    This demonstrates narrative continuity - Graphiti can tell the complete
    story of an entity's evolution over time, not just disconnected chunks.
    
    Expected answer: Full timeline from kickoff to completion
    """
    console.print("\n[bold cyan]Query 5: Entity History / Timeline[/bold cyan]")
    console.print("Question: [italic]What happened with Project Alpha?[/italic]\n")
    
    # TUTORIAL NOTE: Without temporal constraints, Graphiti returns the full
    # narrative - how the entity evolved from start to finish with causal connections
    results = await graphiti.search("What happened with Project Alpha?")
    
    console.print("[bold]Graphiti Response:[/bold]")
    console.print(results)
    
    console.print("\n[dim]💡 RAG would return: Disconnected chunks with no timeline or causality")
    console.print("   Memory returns: Complete narrative with temporal flow[/dim]")
    
    return results


async def main():
    """
    Main function: Run all temporal query demonstrations.
    """
    console.print(Panel.fit(
        "[bold white]TEMPORAL QUERIES WITH GRAPHITI[/bold white]\n\n"
        "This demonstrates the power of temporal knowledge graphs:\n\n"
        "  1️⃣  Current state queries\n"
        "  2️⃣  Historical (point-in-time) queries\n"
        "  3️⃣  Entity evolution narratives\n\n"
        "[bold cyan]The same question with different time contexts\n"
        "returns different (and correct) answers.[/bold cyan]",
        title="🔮 Memory in Action",
        border_style="cyan"
    ))
    
    try:
        # Initialize Graphiti
        graphiti = await setup_graphiti()
        
        # Run all queries with visual separators
        await query_current_leader(graphiti)
        console.print("\n" + "─" * 80)
        
        await query_historical_leader(graphiti)
        console.print("\n" + "─" * 80)
        
        await query_current_status(graphiti)
        console.print("\n" + "─" * 80)
        
        await query_historical_status(graphiti)
        console.print("\n" + "─" * 80)
        
        await query_entity_history(graphiti)
        
        # Summary comparison table
        console.print("\n\n")
        comparison_table = Table(
            title="RAG vs. Memory: Side-by-Side Comparison",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        comparison_table.add_column("Capability", style="cyan")
        comparison_table.add_column("Traditional RAG", style="red")
        comparison_table.add_column("Temporal Memory (Graphiti)", style="green")
        
        comparison_table.add_row(
            "Current state",
            "❌ Returns similar docs\n(might be outdated)",
            "✓ Accurate current state"
        )
        comparison_table.add_row(
            "Historical queries",
            "❌ No time awareness\n(same results always)",
            "✓ Point-in-time accuracy\n(time travel)"
        )
        comparison_table.add_row(
            "Causal relationships",
            "❌ Disconnected chunks\n(contradictions)",
            "✓ Causal chains\n(what caused what)"
        )
        comparison_table.add_row(
            "Entity continuity",
            "❌ No narrative\n(just fragments)",
            "✓ Complete timeline\n(full story)"
        )
        
        console.print(comparison_table)
        
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✓ Temporal queries complete![/bold green]\n\n"
            "You've just seen memory in action:\n"
            "  • Time-aware retrieval\n"
            "  • Historical accuracy\n"
            "  • Narrative continuity\n\n"
            "[cyan]This is the foundation for true AI memory systems.[/cyan]",
            border_style="green"
        ))
        
        # Clean up
        await graphiti.close()
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        console.print("\nMake sure:")
        console.print("  1. Episodes have been added (python src/add_episodes.py)")
        console.print("  2. Neo4j is running (docker-compose up -d)")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
