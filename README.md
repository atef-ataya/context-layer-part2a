# The Context Layer — Part 2a: Memory Beyond RAG

A working demonstration of temporal knowledge graphs using **Graphiti** and **Neo4j** for the YouTube tutorial series "The Context Layer."

> **"RAG retrieves similar documents. Memory understands time, causality, and evolution."**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker
- OpenAI API Key ([get one here](https://platform.openai.com/api-keys))

### Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/atefataya/context-layer-part2a.git
cd context-layer-part2a

# 2. Start Neo4j (wait 10-15 seconds after this)
docker-compose up -d

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment
cp env.template .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the full demo
python src/full_demo.py
```

---

## 🎬 Demo Scripts

| Script                           | What it does                         | Requires              |
| -------------------------------- | ------------------------------------ | --------------------- |
| `python src/demo_rag_failure.py` | Simulates 3 RAG failure modes        | Nothing (pure Python) |
| `python src/setup_graphiti.py`   | Initializes Graphiti + Neo4j indices | Neo4j running         |
| `python src/add_episodes.py`     | Adds 5 text + 1 JSON episode         | Neo4j + OpenAI key    |
| `python src/query_memory.py`     | Runs temporal queries                | Episodes added first  |
| `python src/full_demo.py`        | Complete end-to-end demo             | Neo4j + OpenAI key    |

---

## 🧠 What This Demo Shows

### The 3 RAG Failure Modes

1. **Temporal Blindness** — old detailed docs outscore new concise updates
2. **Causal Disconnection** — can't track that Fact B supersedes Fact A
3. **Entity Continuity** — returns disconnected chunks, not coherent narratives

### The Solution: Graphiti's Temporal Knowledge Graph

- Edges have `valid_at` / `invalid_at` timestamps tracking when facts were true
- Edge invalidation automatically handles contradictions when new info arrives
- Bi-temporal model preserves full history while surfacing current state

---

## 📁 Project Structure

```
context-layer-part2a/
├── docker-compose.yml       # Neo4j container (ports 7474, 7687)
├── env.template             # Environment variables template
├── requirements.txt         # Python dependencies
├── src/
│   ├── setup_graphiti.py    # Initialize Graphiti + build indices
│   ├── demo_rag_failure.py  # Simulate 3 RAG failure modes
│   ├── add_episodes.py      # Add text + JSON episodes
│   ├── query_memory.py      # Temporal queries
│   └── full_demo.py         # Complete demo for video
└── data/
    └── sample_episodes.json # Episode data reference
```

---

## 🔧 Troubleshooting

**"Connection refused"** — Wait 15 seconds after `docker-compose up -d`

**"OPENAI_API_KEY not found"** — Run `cp env.template .env` and add your key

**"No module named graphiti_core"** — Run `pip install -r requirements.txt`

**Neo4j won't start** — Check for port conflicts: `docker ps`, then `docker-compose down && docker-compose up -d`

---

## 📚 Coming in Part 2b

- MCP Integration (Model Context Protocol)
- FalkorDB as a lightweight alternative
- Production deployment patterns
- Enterprise-scale considerations

---

## 👨‍💻 Author

**Atef Ataya** — [atefataya.com](https://atefataya.com) · [GitHub](https://github.com/atefataya) · [YouTube](https://youtube.com/@atefataya)

MIT License
