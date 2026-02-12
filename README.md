# The Context Layer — Part 2a: Memory Beyond RAG

A complete, working demonstration of temporal knowledge graphs using **Graphiti** and **Neo4j** for the YouTube tutorial series "The Context Layer."

> **"RAG retrieves similar documents. Memory understands time, causality, and evolution."**

This project demonstrates why traditional RAG (Retrieval-Augmented Generation) fails to handle temporal information and how temporal knowledge graphs solve those limitations.

---

## 🎯 What This Demo Shows

### The 3 RAG Failure Modes

1. **Temporal Blindness** - RAG can't distinguish between old and new information
2. **Causal Disconnection** - RAG can't track how facts relate or supersede each other  
3. **Entity Continuity** - RAG returns disconnected chunks, not coherent narratives

### The Solution: Temporal Knowledge Graphs

- **Time-aware retrieval** - Query "as of" any point in the timeline
- **Causal relationships** - Track how decisions, changes, and events connect
- **Entity evolution** - Understand the complete story of how things changed

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** 
- **Docker** (for Neo4j)
- **OpenAI API Key** ([get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/atefataya/context-layer-part2a.git
cd context-layer-part2a

# 2. Start Neo4j
docker-compose up -d

# Wait 10-15 seconds for Neo4j to fully start

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment
cp env.template .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the full demo
python src/full_demo.py
```

That's it! The demo will walk you through RAG failures and temporal queries.

---

## 📁 Project Structure

```
context-layer-part2a/
├── README.md                    # You are here
├── requirements.txt             # Python dependencies
├── env.template                 # Environment variable template
├── docker-compose.yml           # Neo4j container configuration
├── src/
│   ├── setup_graphiti.py        # Initialize Graphiti + build indices
│   ├── demo_rag_failure.py      # Simulate 3 RAG failure modes
│   ├── add_episodes.py          # Add text + JSON episodes to graph
│   ├── query_memory.py          # Temporal queries (current + historical)
│   └── full_demo.py             # Complete end-to-end demo for video
└── data/
    └── sample_episodes.json     # Pre-built episode data
```

---

## 🎬 Demo Scripts

### 1. `demo_rag_failure.py` - The Problem

Simulates RAG's 3 failure modes with clear terminal output showing why RAG can't handle temporal, causal, and continuity challenges.

```bash
python src/demo_rag_failure.py
```

**Output:** Side-by-side comparison of what RAG returns vs. correct answers.

---

### 2. `add_episodes.py` - Building Memory

Adds episodes (text + JSON) to Graphiti. Watch as unstructured messages and structured data are ingested into a temporal knowledge graph.

```bash
python src/add_episodes.py
```

**Demonstrates:**
- Unstructured text episodes (team chat messages)
- Structured JSON episodes (project management tool data)
- Automatic entity and relationship extraction

---

### 3. `query_memory.py` - The Magic Moment

Run temporal queries that demonstrate memory's power:

```bash
python src/query_memory.py
```

**Queries:**

1. **Current state** - "Who is leading Project Alpha?" → Sarah
2. **Historical (Jan 8)** - "Who was leading Project Alpha?" → John  
3. **Current status** - "What is the status?" → Complete
4. **Historical status (Jan 8)** - "What was the status?" → Blocked
5. **Entity timeline** - "What happened with Project Alpha?" → Full narrative

---

### 4. `full_demo.py` - Complete Video Demo

The "press play and record" script. Runs the entire demo with pauses for presenter explanation.

```bash
python src/full_demo.py
```

**Flow:**
1. Environment check (Neo4j connection)
2. Graphiti initialization
3. RAG failure simulation
4. Episode ingestion
5. Temporal queries
6. Summary comparison

---

## 🧠 Key Concepts

### Temporal Knowledge Graphs vs. RAG

| Aspect | RAG | Temporal Memory |
|--------|-----|-----------------|
| **Storage** | Vector embeddings | Graph (entities + relationships + time) |
| **Retrieval** | Semantic similarity | Graph traversal with temporal context |
| **Time Awareness** | ❌ None | ✅ Native |
| **Causality** | ❌ Can't track | ✅ Explicit edges |
| **Historical Queries** | ❌ Impossible | ✅ Point-in-time accuracy |

### Why Timezone-Aware Datetimes?

```python
# ✅ Correct
reference_time = datetime(2026, 1, 5, tzinfo=timezone.utc)

# ❌ Incorrect (causes intermittent errors)
reference_time = datetime(2026, 1, 5)
```

Graphiti's edge contradiction resolution algorithm requires timezone-aware datetimes. Naive datetimes can cause intermittent failures.

---

## 🔧 Troubleshooting

### Neo4j Won't Start

```bash
# Check if Neo4j is running
docker ps

# View Neo4j logs
docker-compose logs neo4j

# Restart Neo4j
docker-compose down
docker-compose up -d
```

### "Connection Refused" Error

Wait 10-15 seconds after `docker-compose up -d`. Neo4j takes time to initialize.

### OpenAI API Key Issues

Make sure your `.env` file has:
```
OPENAI_API_KEY=sk-...your-key-here
```

---

## 📚 What's Next?

This demo is **Part 2a** of the Context Layer series.

**Coming in Part 2b:**
- **MCP Integration** - Model Context Protocol for agent memory
- **FalkorDB** - Lightweight alternative to Neo4j
- **Production Patterns** - Scaling, monitoring, and deployment
- **Enterprise Considerations** - Security, compliance, multi-tenancy

---

## 🎓 Learning Resources

### Graphiti Documentation
- [Graphiti Core GitHub](https://github.com/getzep/graphiti)
- [Graphiti Docs](https://docs.getzep.com/)

### Neo4j
- [Neo4j Graph Database](https://neo4j.com/)
- [Neo4j Browser](http://localhost:7474) (after starting Docker)

### Tutorial Series
- [Part 1: RAG Fundamentals](https://atefataya.com) *(placeholder)*
- [Part 2a: Memory Beyond RAG](https://atefataya.com) *(this video)*  
- [Part 2b: Production Patterns](https://atefataya.com) *(coming soon)*

---

## 🤝 Contributing

Found a bug? Have a suggestion? Open an issue or submit a PR!

This is a tutorial project designed for learning. Contributions that improve clarity, fix errors, or add educational value are welcome.

---

## 📜 License

MIT License - feel free to use this code for learning, teaching, or building your own projects.

---

## 👨‍💻 Author

**Atef Ataya**  
- Website: [atefataya.com](https://atefataya.com)
- YouTube: [Context Layer Series](https://youtube.com/@atefataya) *(placeholder)*
- GitHub: [@atefataya](https://github.com/atefataya)

---

## 🙏 Acknowledgments

- **Zep AI** for creating Graphiti
- **Neo4j** for the graph database
- The open-source community for making knowledge graphs accessible

---

## ⭐ Star This Repo

If this demo helped you understand temporal knowledge graphs, give it a star! ⭐

It helps others discover this resource.

---

**Ready to see memory in action? Run `python src/full_demo.py` and watch the magic! ✨**
