"""
demo_rag_failure.py

Demonstrates the 3 core failure modes of traditional RAG systems using simulated examples.

This script does NOT use Graphiti - it's a pure Python simulation showing why RAG fails
to handle temporal, causal, and entity continuity challenges. Each failure mode is
demonstrated with mock documents, simulated similarity scores, and clear comparisons
between what RAG returns vs. what the correct answer should be.

TUTORIAL NOTE: This demonstrates the PROBLEM that temporal knowledge graphs solve.
"""

import math
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def simulate_cosine_similarity(doc_text: str, query: str) -> float:
    """
    Simulate cosine similarity scoring between document and query.
    
    In real RAG, this would use embeddings. Here we approximate based on:
    - Keyword overlap
    - Document length (longer docs often have richer semantic content)
    
    Args:
        doc_text: Document text to score
        query: Query text
        
    Returns:
        float: Simulated similarity score between 0 and 1
    """
    # Normalize texts to lowercase for comparison
    doc_lower = doc_text.lower()
    query_lower = query.lower()
    
    # Count keyword matches
    query_words = set(query_lower.split())
    doc_words = set(doc_lower.split())
    overlap = len(query_words.intersection(doc_words))
    
    # Longer documents with more keywords tend to score higher in real embeddings
    # This simulates that bias
    length_factor = math.log(len(doc_words) + 1) / 10
    overlap_factor = overlap / len(query_words) if query_words else 0
    
    # Combine factors with some noise
    score = min(0.95, overlap_factor * 0.6 + length_factor * 0.4)
    return round(score, 3)


def demo_failure_mode_1_temporal_blindness():
    """
    Failure Mode 1: Temporal Blindness
    
    RAG retrieves documents based on semantic similarity, NOT temporal relevance.
    If an old document is semantically richer, it will score higher than a newer
    but more concise update. This leads to returning outdated information.
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold red]FAILURE MODE 1: TEMPORAL BLINDNESS[/bold red]\n"
        "RAG doesn't understand time. It retrieves based on similarity alone.",
        border_style="red"
    ))
    
    # Create two documents: one old (detailed), one new (concise)
    old_doc = {
        "date": "January 5, 2026",
        "text": "Project Alpha status update: The project is currently BLOCKED due to critical API integration issues with the payment provider. The team has identified multiple endpoints returning 401 errors. John is leading the investigation and working with the external vendor support team. Estimated resolution time is unknown. This is impacting our Q1 roadmap significantly."
    }
    
    new_doc = {
        "date": "January 12, 2026", 
        "text": "Project Alpha is now IN PROGRESS. Issues resolved."
    }
    
    query = "What is the status of Project Alpha?"
    
    # Simulate RAG similarity scoring
    old_score = simulate_cosine_similarity(old_doc["text"], query)
    new_score = simulate_cosine_similarity(new_doc["text"], query)
    
    # Display documents
    console.print("\n[bold cyan]Documents in RAG vector store:[/bold cyan]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim")
    table.add_column("Content")
    table.add_column("Similarity Score", justify="right")
    
    table.add_row(
        old_doc["date"],
        old_doc["text"][:80] + "...",
        f"[bold yellow]{old_score}[/bold yellow]"
    )
    table.add_row(
        new_doc["date"],
        new_doc["text"],
        f"{new_score}"
    )
    
    console.print(table)
    
    # Show what RAG returns (highest score)
    console.print(f"\n[bold]Query:[/bold] {query}")
    console.print(f"[bold red]❌ RAG Returns:[/bold red] {old_doc['text'][:100]}...")
    console.print(f"[bold green]✓ Correct Answer:[/bold green] Project Alpha is IN PROGRESS (as of Jan 12)")
    
    console.print("\n[yellow]Why RAG fails:[/yellow] The old document has richer semantic content")
    console.print("(more keywords, more context) so it scores higher despite being outdated.")


def demo_failure_mode_2_causal_disconnection():
    """
    Failure Mode 2: Causal Disconnection
    
    RAG treats each document independently. It cannot understand that Document B
    (MongoDB migration) supersedes Document A (PostgreSQL decision). Both documents
    mention databases, so both score similarly, forcing the LLM to guess.
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold red]FAILURE MODE 2: CAUSAL DISCONNECTION[/bold red]\n"
        "RAG can't understand causality. It returns conflicting documents.",
        border_style="red"
    ))
    
    doc_a = {
        "date": "January 3, 2026",
        "text": "Architecture decision: We decided to use PostgreSQL for the user service. It provides excellent ACID guarantees and our team has deep expertise with it."
    }
    
    doc_b = {
        "date": "January 10, 2026",
        "text": "Migration completed: User service now running on MongoDB. The migration took 3 days and all data has been successfully transferred."
    }
    
    query = "What database does the user service use?"
    
    # Both documents are highly relevant to the query
    score_a = simulate_cosine_similarity(doc_a["text"], query)
    score_b = simulate_cosine_similarity(doc_b["text"], query)
    
    console.print("\n[bold cyan]Documents in RAG vector store:[/bold cyan]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim")
    table.add_column("Content")
    table.add_column("Similarity Score", justify="right")
    
    table.add_row(
        doc_a["date"],
        doc_a["text"],
        f"[bold yellow]{score_a}[/bold yellow]"
    )
    table.add_row(
        doc_b["date"],
        doc_b["text"],
        f"[bold yellow]{score_b}[/bold yellow]"
    )
    
    console.print(table)
    
    console.print(f"\n[bold]Query:[/bold] {query}")
    console.print(f"[bold red]❌ RAG Returns:[/bold red] BOTH documents (similar scores)")
    console.print("   → LLM sees: 'PostgreSQL' AND 'MongoDB' - which one is current? 🤷")
    console.print(f"[bold green]✓ Correct Answer:[/bold green] MongoDB (the PostgreSQL decision was superseded)")
    
    console.print("\n[yellow]Why RAG fails:[/yellow] No causal chain linking the decision to the migration.")
    console.print("RAG doesn't know that Document B invalidates Document A.")


def demo_failure_mode_3_entity_continuity():
    """
    Failure Mode 3: Entity Continuity
    
    RAG returns individual chunks about an entity but cannot construct a coherent
    narrative or timeline. You get disconnected facts without understanding how
    the entity evolved over time or what the full story is.
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold red]FAILURE MODE 3: ENTITY CONTINUITY[/bold red]\n"
        "RAG returns disconnected chunks. No narrative, no timeline.",
        border_style="red"
    ))
    
    chunks = [
        {
            "date": "Monday, Jan 5",
            "text": "John is leading the API redesign project.",
            "score": 0.812
        },
        {
            "date": "Wednesday, Jan 7",
            "text": "The API redesign ownership has been transferred from John to Sarah due to John's reassignment to Project Beta.",
            "score": 0.834
        },
        {
            "date": "Friday, Jan 9",
            "text": "Sarah completed the API redesign. All endpoints now follow REST best practices. Documentation updated.",
            "score": 0.798
        }
    ]
    
    query = "Who worked on the API redesign?"
    
    console.print("\n[bold cyan]Documents in RAG vector store:[/bold cyan]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim")
    table.add_column("Content")
    table.add_column("Score", justify="right")
    
    for chunk in chunks:
        table.add_row(
            chunk["date"],
            chunk["text"],
            f"[bold yellow]{chunk['score']}[/bold yellow]"
        )
    
    console.print(table)
    
    console.print(f"\n[bold]Query:[/bold] {query}")
    console.print("[bold red]❌ RAG Returns:[/bold red] Three disconnected chunks")
    console.print("   → LLM sees: John mentioned, Sarah mentioned, but no timeline or story")
    
    console.print("\n[bold green]✓ Correct Answer (with full context):[/bold green]")
    console.print("   John started the API redesign, ownership transferred to Sarah on Jan 7")
    console.print("   due to John's reassignment, and Sarah completed it on Jan 9.")
    
    console.print("\n[yellow]Why RAG fails:[/yellow] Each chunk is retrieved independently.")
    console.print("RAG has no concept of entity evolution or temporal continuity.")


def main():
    """
    Run all three RAG failure mode demonstrations.
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold white]THE 3 FAILURE MODES OF TRADITIONAL RAG[/bold white]\n\n"
        "This demo simulates how RAG systems fail to handle:\n"
        "  1️⃣  Temporal information (old vs. new)\n"
        "  2️⃣  Causal relationships (A causes B)\n"
        "  3️⃣  Entity continuity (how things evolve)\n\n"
        "[dim]Note: These are simulations. Real RAG would use embeddings,\n"
        "but the failure patterns are identical.[/dim]",
        title="🔍 RAG LIMITATIONS",
        border_style="bright_blue"
    ))
    
    # Run all three demos
    demo_failure_mode_1_temporal_blindness()
    demo_failure_mode_2_causal_disconnection()
    demo_failure_mode_3_entity_continuity()
    
    # Summary
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]💡 The Solution: Temporal Knowledge Graphs[/bold cyan]\n\n"
        "Instead of independent documents with similarity scores,\n"
        "we need a graph that understands:\n\n"
        "  • [green]Time[/green] - when facts were true\n"
        "  • [green]Causality[/green] - how facts relate and evolve\n"
        "  • [green]Continuity[/green] - the complete story of entities\n\n"
        "That's what Graphiti provides. Let's see it in action! ➡️",
        border_style="cyan"
    ))


if __name__ == "__main__":
    main()
