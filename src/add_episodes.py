"""
add_episodes.py

Demonstrates adding both text and JSON episodes to Graphiti's temporal knowledge graph.

This module shows how Graphiti ingests information from different sources:
1. Unstructured text (chat messages, emails, notes)
2. Structured JSON (API responses, database records, task tracker updates)

Each episode is timestamped, and Graphiti automatically:
- Extracts entities (people, projects, systems)
- Identifies relationships between entities
- Creates temporal edges that track when facts were valid
- Resolves contradictions when facts change over time

TUTORIAL NOTE: This is where RAG becomes memory. Graphiti doesn't just store text -
it builds a temporal graph that understands HOW information evolved.
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from graphiti_core.nodes import EpisodeType
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from setup_graphiti import setup_graphiti

console = Console()


async def add_text_episodes(graphiti):
    """
    Add unstructured text episodes to the knowledge graph.
    
    These episodes simulate messages from a team chat or email thread.
    Graphiti will extract entities (John, Sarah, Project Alpha) and relationships
    (John leads Project Alpha, Project Alpha status=blocked, etc.)
    
    Args:
        graphiti: Initialized Graphiti instance
    """
    console.print("\n[bold cyan]📝 Adding Text Episodes[/bold cyan]")
    console.print("These simulate unstructured messages from team chat/email\n")
    
    # TUTORIAL NOTE: Each episode represents a point-in-time observation.
    # The reference_time tells Graphiti WHEN this information was valid.
    # This is crucial for temporal queries later.
    
    episodes = [
        {
            "name": "Project Alpha Kickoff",
            "body": "Started Project Alpha today. John has been assigned as the lead engineer.",
            # CRITICAL: Must use timezone-aware datetimes (tzinfo=timezone.utc)
            # Timezone-naive datetimes cause intermittent errors in Graphiti's 
            # edge contradiction resolution algorithm
            "reference_time": datetime(2026, 1, 5, tzinfo=timezone.utc),
        },
        {
            "name": "Project Alpha Blocked",
            "body": "Project Alpha is now blocked. The API integration with the payment provider is failing. John is investigating.",
            "reference_time": datetime(2026, 1, 8, tzinfo=timezone.utc),
        },
        {
            "name": "Project Alpha Leadership Change",
            "body": "John has been reassigned to Project Beta. Sarah is now leading Project Alpha.",
            "reference_time": datetime(2026, 1, 12, tzinfo=timezone.utc),
        },
        {
            "name": "Project Alpha Unblocked",
            "body": "Sarah resolved the payment provider API issue. Project Alpha is now back in progress. Deadline moved to January 20th.",
            "reference_time": datetime(2026, 1, 14, tzinfo=timezone.utc),
        },
        {
            "name": "Project Alpha Complete",
            "body": "Sarah completed Project Alpha ahead of the new deadline. All tests passing. Deployed to production.",
            "reference_time": datetime(2026, 1, 18, tzinfo=timezone.utc),
        }
    ]
    
    # Add each episode to Graphiti
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for ep in episodes:
            task = progress.add_task(f"Adding: {ep['name']}", total=None)
            
            # TUTORIAL NOTE: add_episode is async because Graphiti uses an LLM
            # to extract entities and relationships. This can take 1-3 seconds per episode.
            #
            # API NOTE: Both `source` and `source_description` are required:
            #   - source: The EpisodeType enum (message, text, json)
            #   - source_description: A freetext label describing the source
            await graphiti.add_episode(
                name=ep["name"],
                episode_body=ep["body"],
                source=EpisodeType.message,
                source_description="team chat",
                reference_time=ep["reference_time"]
            )
            
            progress.update(task, completed=True)
            console.print(f"  ✓ {ep['name']} ({ep['reference_time'].strftime('%b %d')})", style="green")
    
    console.print(f"\n[bold green]✓ Added {len(episodes)} text episodes[/bold green]")


async def add_json_episode(graphiti):
    """
    Add a structured JSON episode to the knowledge graph.
    
    This simulates data from a structured source like a project management tool,
    CRM system, or API response. Graphiti can ingest both unstructured text
    and structured data, making it ideal for multi-modal enterprise memory.
    
    Args:
        graphiti: Initialized Graphiti instance
    """
    console.print("\n[bold cyan]📊 Adding JSON Episode[/bold cyan]")
    console.print("This simulates structured data from a project management tool\n")
    
    # TUTORIAL NOTE: Structured data from systems like Jira, Salesforce, etc.
    # This demonstrates that Graphiti isn't just for chat logs - it can ingest
    # structured enterprise data too.
    project_update = {
        "id": "ALPHA-001",
        "project": "Project Alpha",
        "status": "IN_PROGRESS",
        "assignee": "Sarah",
        "previous_assignee": "John",
        "priority": "HIGH",
        "notes": "Sarah took over from John due to reassignment to Project Beta."
    }
    
    reference_time = datetime(2026, 1, 15, tzinfo=timezone.utc)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Adding structured update", total=None)
        
        # TUTORIAL NOTE: For JSON episodes, you can pass the Python dictionary
        # directly as episode_body. Graphiti handles serialization internally.
        # Use source=EpisodeType.json to tell Graphiti this is structured data.
        await graphiti.add_episode(
            name="Project Alpha Structured Update",
            episode_body=json.dumps(project_update, indent=2),
            source=EpisodeType.json,
            source_description="project management tool",
            reference_time=reference_time
        )
        
        progress.update(task, completed=True)
    
    console.print(f"  ✓ Structured update added ({reference_time.strftime('%b %d')})", style="green")
    console.print("\n[bold green]✓ JSON episode ingested[/bold green]")


async def main():
    """
    Main function: Initialize Graphiti and add all episodes.
    """
    console.print(Panel.fit(
        "[bold white]ADDING EPISODES TO GRAPHITI[/bold white]\n\n"
        "This script demonstrates how Graphiti ingests information:\n"
        "  • Unstructured text (messages, emails, notes)\n"
        "  • Structured data (JSON from APIs, databases)\n\n"
        "Graphiti automatically extracts entities, relationships,\n"
        "and temporal information to build a knowledge graph.",
        title="📚 Episode Ingestion",
        border_style="cyan"
    ))
    
    try:
        # Initialize Graphiti
        graphiti = await setup_graphiti()
        
        # Add all episodes
        await add_text_episodes(graphiti)
        await add_json_episode(graphiti)
        
        # Summary
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✓ All episodes added successfully![/bold green]\n\n"
            "The knowledge graph now contains:\n"
            "  • Entities: John, Sarah, Project Alpha, Payment Provider API\n"
            "  • Relationships: leadership, status changes, assignments\n"
            "  • Timeline: Jan 5 → Jan 18, 2026\n\n"
            "Next: Query the memory to see temporal awareness in action\n"
            "Run: python src/query_memory.py",
            border_style="green"
        ))
        
        # Clean up
        await graphiti.close()
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
        console.print("\nMake sure:")
        console.print("  1. Neo4j is running (docker-compose up -d)")
        console.print("  2. Your .env file has a valid OPENAI_API_KEY")
        console.print("  3. Run: python src/setup_graphiti.py first")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())