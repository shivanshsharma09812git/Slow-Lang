# Slow-Lang 🐌

**The slowest programming language to ever exist**

A hilariously over-engineered [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) interpreter written in Python using FastAPI. Every operation makes HTTP requests to itself, creating a deliberately slow and inefficient (but working!) interpreter.

## What is This?

Slow-Lang is a Brainfuck interpreter that takes "microservices architecture" to its logical extreme. Instead of executing operations directly, each function makes HTTP requests to other endpoints on the same server, creating a recursive chain of API calls. It's a beautiful example of "just because you can, doesn't mean you should."

## Challenge Rules

This project was created under specific constraints:

- ✋ **No loops** - Only recursion allowed (via HTTP requests)
- 🎯 **Functions must work** - Performance doesn't matter, correctness does

## Features

✨ **HTTP-based execution** - Every operation is an API call  
✨ **Self-congratulating routes** - Routes "greet" each other to validate execution  
✨ **Recursive HTTP chains** - Watch a microservices nightmare unfold in real-time  
✨ **CORS enabled** - Call this from anywhere (please don't)  
✨ **Full Brainfuck support** - Loops, I/O, memory management, and all  
✨ **Hello World takes 20 minutes** - Intentionally inefficient ⏳

## Brainfuck Commands

| Command | Description |
|---------|-------------|
| `+` | Increment current cell |
| `-` | Decrement current cell |
| `>` | Move pointer right |
| `<` | Move pointer left |
| `[` | Loop start (while cell != 0) |
| `]` | Loop end (while cell != 0) |
| `.` | Output cell as ASCII character |
| `,` | Input character into current cell |

## Installation

### Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- httpx

### Setup

**Unix/Linux/Mac:**
```bash
git clone https://github.com/shivanshsharma09812git/Slow-Lang
cd Slow-Lang

# Optional: create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows:**
Use WSL (Windows Subsystem for Linux) for best results.

## Usage

1. **Create a Brainfuck program** in `main.sl`:
   ```brainfuck
   ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.
   ```
   (This outputs "Hello World!")

2. **Run the interpreter**:
   ```bash
   python main.py
   ```

3. **Watch the magic happen** as the server makes thousands of HTTP requests to itself! ☕

## How It Works

The interpreter processes Brainfuck programs through several stages:

1. **ASCII Table Generation** - Builds a complete ASCII lookup table (0-255) via recursive HTTP calls
2. **File Reading** - Reads the `.sl` file in chunks through the `/buff/fn` endpoint
3. **Tokenization** - Converts the input into token strings through `read_until` API calls
4. **Intermediate Language** - Converts Brainfuck symbols to token names (PLUS, MINUS, LOOP_START, etc.)
5. **Interpretation** - Executes tokens one by one, each operation making HTTP requests

## Architecture

```
FastAPI Server (http://127.0.0.1:8000/)
│
├── /ascii/fn              - Build ASCII character table (0-255)
├── /buff/fn               - Read file buffers
├── /len/fn                - Get file length
├── /intermediate/fn       - Convert to intermediate language
├── /make_intermediate/fn  - Create .isl file
├── /read_until/fn         - Read until delimiter
├── /get_tokens/fn         - Tokenize intermediate language
└── /interpret/fn          - Execute Brainfuck tokens
    
Each route has a corresponding /greet endpoint for validation
```

## Performance Notes

⚠️ **Extremely slow** - This is 100% intentional!

The recursive HTTP architecture ensures maximum latency:
- 30,000 cell memory (typical Brainfuck)
- Up to 10,000 concurrent connections
- Nested HTTP calls for loop operations
- Self-greeting validation on every single operation

**Expected performance:**
- Hello World: ~20 minutes
- Simple arithmetic: Several minutes per operation

## Project Structure

```
Slow-Lang/
├── main.py           - Main interpreter with FastAPI routes
├── slowapi.py        - FastAPI wrapper module
├── main.sl           - Input Brainfuck program
├── main.isl          - Generated intermediate language
└── requirements.txt  - Python dependencies
```

## Example Programs

### Hello World
```brainfuck
++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.
```

### Simple Output
```brainfuck
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
```
(Outputs 'H')

## Why Does This Exist?

This project is an exercise in over-engineering and a cautionary tale about microservices. It demonstrates:

- 🔄 The power of recursion (and why you shouldn't use it everywhere)
- 📡 The hidden costs of HTTP overhead in distributed systems
- 🤯 Why constraints breed creative (but questionable) solutions
- 💀 That working code isn't always good code
- 😅 You can technically do anything with enough HTTP requests

## Technical Highlights

- **Zero loops** - Everything is recursion via HTTP
- **Asynchronous execution** - Uses `asyncio` and `httpx`
- **Recursive pointer management** - Brainfuck pointer position through recursion
- **Self-validating routes** - Cross-endpoint greeting system
- **Infinite connection limits** - `max_connections=10000`

## Warnings

⚠️ **DO NOT RUN ON:**
- Old computers
- Production systems
- Systems with limited bandwidth
- During a meteor shower

✅ **ONLY FOR:**
- Educational purposes
- Entertainment
- Understanding why certain architectural choices are bad
- Making developers question their life choices

## License

Use at your own risk. This code is intentionally terrible.

---

**Disclaimer**: This is a joke project demonstrating poor architectural decisions. It should never be used in real applications. Please don't base your career decisions on this code. 😄
