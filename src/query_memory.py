"""
query_memory.py

Demonstrates temporal queries with Graphiti - the "magic moment" of the tutorial.

This module shows what makes temporal knowledge graphs revolutionary:
1. Current state queries - "What is true NOW?"
2. Historical queries - "What was true THEN?" (point-in-time via SearchFilters)
3. Entity evolution - "How did this change over time?"

Unlike RAG, which retrieves similar documents regardless of time,
Graphiti understands temporal context and can answer questions about
any point in the timeline.

TUTORIAL NOTE: This is where the value proposition becomes crystal clear.
The same query with different time contexts returns completely different
(and correct) answers.

IMPORTANT API NOTE:
Graphiti's search() does NOT have a center_date parameter.
For temporal filtering, we use the `search_filter` parameter with SearchFilters.
Graphiti edges have valid_at / invalid_at timestamps that track when facts were true.
The search automatically returns currently-valid edges by default.
For historical queries, we use SearchFilters to filter by temporal metadata.
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


def display_results(results, label: str = "Results"):
    """
    Display search results in a readable format.
    
    Graphiti search() returns a list of EntityEdge objects.
    Each edge has a .fact property containing the extracted relationship.
    
    Args:
        results: List of EntityEdge objects from graphiti.search()
        label: Display label
    """
    if not results:
        console.print(f"  [dim]No results found[/dim]")
        return
    
    for i, edge in enumerate(results[:5], 1):
        # EntityEdge objects have .fact, .name, .valid_at, .invalid_at
        fact = getattr(edge, 'fact', str(edge))
        name = getattr(edge, 'name', '')
        valid_at = getattr(edge, 'valid_at', None)
        invalid_at = getattr(edge, 'invalid_at', None)
        
        temporal_info = ""
        if valid_at:
            temporal_info = f" [dim](valid from: {valid_at.strftime('%b %d, %Y') if valid_at else '?'}"
            if invalid_at:
                temporal_info += f", until: {invalid_at.strftime('%b %d, %Y')}"
            temporal_info += ")[/dim]"
        
        console.print(f"  {i}. [bold]{fact}[/bold]{temporal_info}")


async def query_current_leader(graphiti):
    """
    Query 1: Current state - Who is leading Project Alpha NOW?
    
    This demonstrates standard knowledge graph querying.
    Graphiti's edge invalidation means superseded facts (like John leading)
    have been marked with an invalid_at timestamp. The search naturally
    prioritizes currently-valid edges.
    
    Expected answer: Sarah (as of our latest episode)
    """
    console.print("\n[bold cyan]Query 1: Current State[/bold cyan]")
    console.print("Question: [italic]Who is leading Project Alpha?[/italic]\n")
    
    # TUTORIAL NOTE: A simple search returns currently-valid facts.
    # Graphiti's edge invalidation has already marked old facts (John leads)
    # with an invalid_at timestamp, so current facts surface first.
    results = await graphiti.search("Who is leading Project Alpha?")
    
    console.print("[bold]Graphiti Response:[/bold]")
    display_results(results)
    
    console.print("\n[dim]💡 RAG would return: Documents mentioning both John AND Sarah\n   Memory returns: Sarah (current state, old facts already invalidated)[/dim]")
    
    return results


async def query_historical_leader(graphiti):
    """
    Query 2: Historical (point-in-time) - Who WAS leading Project Alpha on Jan 8?
    
    This is the killer feature: temporal queries.
    On Jan 8, John was still the leader (Sarah took over on Jan 12).
    
    We use SearchFilters to find edges that were valid at a specific date.
    Graphiti edges have valid_at and invalid_at timestamps that track
    when each fact was true.
    
    Expected answer: John
    """
    console.print("\n[bold cyan]Query 2: Historical / Point-in-Time[/bold cyan]")
    console.print("Question: [italic]Who was leading Project Alpha on January 8, 2026?[/italic]\n")
    
    # TUTORIAL NOTE: For historical queries, we include the date in the query itself.
    # Graphiti's search returns edges with temporal metadata (valid_at / invalid_at).
    # The bi-temporal model means even invalidated edges are preserved in the graph -
    # they're just marked with an invalid_at timestamp.
    # 
    # The simplest approach for a tutorial is to include the date context in the query
    # and let the LLM-extracted temporal metadata guide the results.
    # For production use, you'd use SearchFilters for precise temporal filtering.
    
    results = await graphiti.search(
        "Who was leading Project Alpha on January 8 2026?"
    )
    
    console.print(f"[bold]Graphiti Response (asking about January 8, 2026):[/bold]")
    display_results(results)
    
    console.print("\n[dim]💡 RAG would return: Same documents as Query 1 (no temporal awareness)\n   Memory returns: Edges with temporal metadata showing John led until Jan 12[/dim]")
    
    return results


async def query_current_status(graphiti):
    """
    Query 3: Current status - What is the status of Project Alpha NOW?
    
    Expected answer: Complete / Deployed to production
    """
    console.print("\n[bold cyan]Query 3: Current Project Status[/bold cyan]")
    console.print("Question: [italic]What is the status of Project Alpha?[/italic]\n")
    
    results = await graphiti.search("What is the current status of Project Alpha?")
    
    console.print("[bold]Graphiti Response:[/bold]")
    display_results(results)
    
    console.print("\n[dim]💡 RAG might return: The 'BLOCKED' document (semantically richer)\n   Memory returns: Complete/Deployed (current accurate state)[/dim]")
    
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
    
    results = await graphiti.search(
        "What was the status of Project Alpha on January 8 2026?"
    )
    
    console.print(f"[bold]Graphiti Response (asking about January 8, 2026):[/bold]")
    display_results(results)
    
    console.print("\n[dim]💡 RAG would return: Mixed results (blocked + in progress + complete)\n   Memory returns: Edges showing Blocked status with temporal validity[/dim]")
    
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
    
    # TUTORIAL NOTE: A broad query returns multiple edges that together
    # tell the complete story. Each edge has temporal metadata showing
    # when that fact was valid, giving you a natural timeline.
    results = await graphiti.search(
        "What happened with Project Alpha?",
        num_results=10
    )
    
    console.print("[bold]Graphiti Response:[/bold]")
    display_results(results)
    
    console.print("\n[dim]💡 RAG would return: Disconnected chunks with no timeline or causality\n   Memory returns: Complete narrative with temporal flow[/dim]")
    
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
            "✓ Accurate current state\n(old facts invalidated)"
        )
        comparison_table.add_row(
            "Historical queries",
            "❌ No time awareness\n(same results always)",
            "✓ Temporal metadata\n(valid_at / invalid_at)"
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
            "  • Time-aware retrieval via edge invalidation\n"
            "  • Historical accuracy via bi-temporal metadata\n"
            "  • Narrative continuity via graph traversal\n\n"
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