# HeadphoneAI 🎧
### A live demo of RAG + MCP + LLM — search, compare, and buy headphones using AI

---

## What is this?

This is a working demo of how modern AI systems are built — using a headphone shopping assistant as the example.

It shows three things working together in real time:
- 🧠 **LLM** — understands what you're asking
- 🔍 **RAG** — looks up real products from a catalogue
- 🔗 **MCP** — takes actions (add to cart, apply discounts, check stock)

---

## Before you start — you need two things

### 1. Python (free)
Check if you already have it — open Terminal (Mac) or Command Prompt (Windows) and type:
```
python --version
```
If you see a version number, you're good. If not, download it from:
👉 https://www.python.org/downloads/

> ⚠️ Windows users: During install, make sure to check **"Add Python to PATH"**

---

### 2. An OpenAI API Key (you'll enter this in the app)
👉 https://platform.openai.com/api-keys

---

## How to run it

### Windows
1. Download and unzip this folder
2. Double-click **`start.bat`**
3. A browser window will open automatically at `http://localhost:8000`

### Mac / Linux
1. Download and unzip this folder
2. Double-click **`start.sh`**
   - If it doesn't open, right-click → Open With → Terminal
3. A browser window will open automatically at `http://localhost:8000`

---

## Using the app

1. **Enter your OpenAI API key** in the setup screen — it's only used in this session, never saved
2. Click **"Initialise & Load Catalogue"** — this embeds the 20 headphones into a local database (takes ~10 seconds)
3. Start chatting!

### Try these prompts in order:
```
"Best headphones under ₹2000"
"Compare the first two"
"Add the second one to cart"
"Check stock for WH-CH520"
"Apply discount SAVE10"
```

### Discount codes
| Code | Discount |
|------|----------|
| SAVE10 | 10% off |
| BUDGET20 | 20% off |
| FIRST15 | 15% off |

---

## Something went wrong?

| Problem | Fix |
|---------|-----|
| "Python not found" | Install from python.org — check "Add to PATH" on Windows |
| "Failed to install dependencies" | Run `pip install -r requirements.txt` manually in Terminal |
| Browser doesn't open | Go to http://localhost:8000 manually |
| API key error | Make sure the key starts with `sk-` and has credits |
| Port already in use | Change `--port 8000` to `--port 8080` in the start script |

---

## Tech stack (for the curious)
`Python · FastAPI · LangChain · ChromaDB · OpenAI gpt-4o-mini`
