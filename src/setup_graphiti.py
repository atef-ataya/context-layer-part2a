"""
setup_graphiti.py

Initializes the Graphiti temporal knowledge graph and builds necessary indices in Neo4j.

This module handles:
1. Loading environment variables (Neo4j connection, OpenAI API key)
2. Initializing Graphiti with the configured LLM
3. Building graph indices for optimal query performance

TUTORIAL NOTE: This setup must run before adding episodes or querying the graph.
Neo4j must be running (via docker-compose) before executing this script.
"""

import os
import asyncio
from dotenv import load_dotenv
from graphiti_core import Graphiti
from rich.console import Console
from rich.panel import Panel

# Initialize rich console for beautiful terminal output
console = Console()


async def setup_graphiti() -> Graphiti:
    """
    Initialize Graphiti and build necessary Neo4j indices.
    
    Returns:
        Graphiti: Configured Graphiti instance ready for use
        
    Raises:
        Exception: If Neo4j connection fails or required env vars are missing
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # TUTORIAL NOTE: These environment variables are required for Graphiti to work
    # NEO4J_* variables configure the graph database connection
    # OPENAI_API_KEY enables the LLM to extract entities and relationships
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        console.print("[bold red]❌ Error:[/bold red] OPENAI_API_KEY not found in environment")
        console.print("Please copy env.template to .env and add your OpenAI API key")
        raise ValueError("OPENAI_API_KEY is required")
    
    console.print(Panel.fit(
        "[bold cyan]Initializing Graphiti[/bold cyan]\n"
        f"Neo4j URI: {neo4j_uri}\n"
        f"Neo4j User: {neo4j_user}",
        title="🚀 Setup"
    ))
    
    try:
        # TUTORIAL NOTE: Graphiti takes Neo4j credentials directly.
        # It creates and manages the database driver internally.
        console.print("Connecting to Neo4j and initializing Graphiti...", style="yellow")
        graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)
        
        # Build indices for optimal query performance
        # This creates database indices on key properties used in graph traversal
        console.print("Building Neo4j indices...", style="yellow")
        await graphiti.build_indices_and_constraints()
        console.print("✓ Indices built successfully", style="green")
        
        console.print("[bold green]✓ Graphiti initialized and ready[/bold green]")
        
        return graphiti
        
    except Exception as e:
        console.print(f"[bold red]❌ Setup failed:[/bold red] {str(e)}")
        console.print("\n[yellow]Troubleshooting:[/yellow]")
        console.print("1. Ensure Neo4j is running: docker-compose up -d")
        console.print("2. Wait 10-15 seconds for Neo4j to fully start")
        console.print("3. Check Neo4j browser at http://localhost:7474")
        console.print("4. Verify credentials match docker-compose.yml")
        raise


async def main():
    """
    Main function for standalone execution of setup.
    """
    try:
        graphiti = await setup_graphiti()
        console.print("\n[bold green]Setup complete![/bold green] You can now:")
        console.print("  • Add episodes: python src/add_episodes.py")
        console.print("  • Query memory: python src/query_memory.py")
        console.print("  • Run full demo: python src/full_demo.py")
        
        # Clean up
        await graphiti.close()
        
    except Exception as e:
        console.print(f"\n[bold red]Setup failed. Please fix the errors above and try again.[/bold red]")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())