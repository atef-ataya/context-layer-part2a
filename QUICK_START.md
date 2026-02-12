# Quick Reference Guide

## 🚀 First-Time Setup (5 minutes)

```bash
# 1. Start Neo4j (wait 10-15 seconds after this)
docker-compose up -d

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp env.template .env
# Edit .env and add your OPENAI_API_KEY

# 4. Initialize Graphiti
python src/setup_graphiti.py
```

---

## 🎬 Running Individual Scripts

### Show RAG Failures (no API key needed)
```bash
python src/demo_rag_failure.py
```
**Duration:** ~30 seconds  
**Requires:** Nothing (pure Python simulation)

### Initialize Graphiti
```bash
python src/setup_graphiti.py
```
**Duration:** ~10 seconds  
**Requires:** Neo4j running

### Add Episodes
```bash
python src/add_episodes.py
```
**Duration:** ~30-60 seconds  
**Requires:** Neo4j + OpenAI API key

### Query Memory
```bash
python src/query_memory.py
```
**Duration:** ~20-40 seconds  
**Requires:** Episodes already added

### Full Demo (For Video Recording)
```bash
python src/full_demo.py
```
**Duration:** 3-5 minutes with pauses  
**Requires:** Neo4j + OpenAI API key

---

## 🔍 Verification Commands

### Check Neo4j is running
```bash
docker ps | grep neo4j
```

### Check Neo4j logs
```bash
docker-compose logs neo4j
```

### Access Neo4j Browser
Open: http://localhost:7474  
Username: `neo4j`  
Password: `password`

### Verify Python environment
```bash
python --version  # Should be 3.11+
pip list | grep graphiti
```

---

## 🐛 Common Issues

### "Connection refused" error
**Problem:** Neo4j not fully started  
**Solution:** Wait 15 seconds after `docker-compose up -d`

### "OPENAI_API_KEY not found"
**Problem:** .env file missing or incomplete  
**Solution:** 
```bash
cp env.template .env
# Edit .env and add your actual API key
```

### "No module named 'graphiti_core'"
**Problem:** Dependencies not installed  
**Solution:** `pip install -r requirements.txt`

### Neo4j won't start
**Problem:** Port conflict or Docker issue  
**Solution:**
```bash
docker-compose down
docker ps  # Check for port conflicts
docker-compose up -d
```

---

## 📊 Expected Output Examples

### demo_rag_failure.py
- 3 colored tables showing RAG failure modes
- Side-by-side comparison of RAG vs correct answers
- Clear visual separation between failure modes

### add_episodes.py
- Progress spinner for each episode
- Green checkmarks with timestamps
- Success summary

### query_memory.py
- 5 queries with formatted responses
- RAG vs Memory comparisons after each query
- Final comparison table

### full_demo.py
- ASCII art banner
- Section headers with separators
- Pause prompts for presenter
- Complete summary table at end

---

## 🎥 Video Recording Tips

1. **Terminal setup**: Use a dark theme with good contrast
2. **Font size**: Increase terminal font to 16pt+
3. **Window size**: Full screen or at least 120 columns wide
4. **Speed**: Let the full_demo.py run naturally with pauses
5. **Sections**: 
   - Intro: 30 seconds
   - RAG failures: 1-2 minutes
   - Episode ingestion: 30 seconds
   - Queries: 2 minutes
   - Summary: 30 seconds

---

## 🧹 Cleanup

```bash
# Stop Neo4j
docker-compose down

# Remove Neo4j data (fresh start)
docker-compose down -v

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## 📝 Environment Variables Quick Reference

| Variable | Example | Purpose |
|----------|---------|---------|
| NEO4J_URI | bolt://localhost:7687 | Neo4j connection |
| NEO4J_USER | neo4j | Neo4j username |
| NEO4J_PASSWORD | password | Neo4j password |
| OPENAI_API_KEY | sk-... | LLM for entity extraction |

---

**Ready to start? Run: `python src/full_demo.py`**
