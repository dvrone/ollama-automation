# Python + Ollama Automation Manual 🚀

## Complete Setup & Usage Guide

---

## 📋 Prerequisites

Before starting, ensure you have:

- Python 3.8+ installed
- Terminal/Command Prompt access
- At least 8GB RAM (16GB recommended for larger models)
- 10GB+ free disk space

---

## 🔧 Step 1: Install Ollama

### **macOS**

```bash
# Download from website or use brew
brew install ollama
```

### **Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### **Windows**

```bash
# Download installer from https://ollama.com/download/windows
# Or use WSL2:
wsl --install
# Then in WSL:
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 🚀 Step 2: Start Ollama Service

```bash
# Start the Ollama server (keep this terminal open)
ollama serve
```

**Verify it's running:**

```bash
# In a new terminal
ollama list
```

---

## 📦 Step 3: Install Python Ollama Package

```bash
# Create a virtual environment (recommended)
python -m venv ollama_env

# Activate it
# Windows:
ollama_env\Scripts\activate
# macOS/Linux:
source ollama_env/bin/activate

# Install the package
pip install ollama
```

**Check installation:**

```bash
pip show ollama
# Should show version and details
```

---

## 🤖 Step 4: Pull Your First Model

```bash
# Pull a lightweight model (good for testing)
ollama pull llama3.2:1b

# Or pull a more capable model
ollama pull llama3.2:3b

# See available models
ollama list
```

---

## 💻 Step 5: Basic Python Scripts

### **Script 1: Simple Text Generation**

Create `basic_chat.py`:

```python
import ollama

def simple_chat():
    """Basic text generation example"""
    
    response = ollama.chat(
        model='llama3.2:1b',
        messages=[
            {
                'role': 'user',
                'content': 'Explain quantum computing in one sentence.'
            }
        ]
    )
    
    print("🤖 AI Response:")
    print(response['message']['content'])
    print(f"\n📊 Tokens used: {response.get('total_duration', 'N/A')}")

if __name__ == "__main__":
    simple_chat()
```

**Run it:**

```bash
python basic_chat.py
```

---

### **Script 2: Streaming Responses**

Create `streaming_chat.py`:

```python
import ollama

def streaming_chat():
    """Example with real-time streaming output"""
    
    print("🤖 AI is thinking...\n")
    
    stream = ollama.chat(
        model='llama3.2:1b',
        messages=[
            {
                'role': 'user',
                'content': 'Write a short poem about AI.'
            }
        ],
        stream=True  # Enable streaming
    )
    
    full_response = ""
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content
    
    print("\n\n✅ Complete!")

if __name__ == "__main__":
    streaming_chat()
```

**Run it:**

```bash
python streaming_chat.py
```

---

## 🔄 Step 6: Advanced Automation Examples

### **Script 3: Multi-turn Conversation**

Create `conversation.py`:

```python
import ollama

class AIAssistant:
    def __init__(self, model='llama3.2:3b'):
        self.model = model
        self.conversation_history = []
    
    def chat(self, user_input):
        """Maintain conversation context"""
        
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get AI response
        response = ollama.chat(
            model=self.model,
            messages=self.conversation_history
        )
        
        # Add AI response to history
        ai_message = response['message']['content']
        self.conversation_history.append({
            'role': 'assistant',
            'content': ai_message
        })
        
        return ai_message
    
    def clear_history(self):
        """Reset conversation"""
        self.conversation_history = []
        print("🧹 Conversation history cleared!")

def main():
    assistant = AIAssistant()
    
    print("🤖 AI Assistant Ready! (type 'clear' to reset, 'quit' to exit)\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'clear':
            assistant.clear_history()
            continue
        
        if user_input:
            response = assistant.chat(user_input)
            print(f"AI: {response}\n")

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python conversation.py
```

---

### **Script 4: Document Processing Automation**

Create `document_processor.py`:

```python
import ollama
import os
from pathlib import Path

class DocumentProcessor:
    def __init__(self, model='llama3.2:3b'):
        self.model = model
    
    def summarize_file(self, file_path):
        """Read and summarize a text file"""
        
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate summary
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'Summarize this document in 3-5 bullet points:\n\n{content[:4000]}'
                }
            ]
        )
        
        return response['message']['content']
    
    def extract_keywords(self, text):
        """Extract key topics from text"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'Extract 10 key topics/keywords from this text as comma-separated list:\n\n{text[:2000]}'
                }
            ]
        )
        
        return response['message']['content']
    
    def batch_process_folder(self, folder_path):
        """Process all txt files in a folder"""
        
        results = {}
        folder = Path(folder_path)
        
        for file_path in folder.glob('*.txt'):
            print(f"📄 Processing: {file_path.name}")
            
            summary = self.summarize_file(file_path)
            results[file_path.name] = {
                'summary': summary
            }
            
            # Save summary
            output_path = folder / f"{file_path.stem}_summary.txt"
            with open(output_path, 'w') as f:
                f.write(summary)
            
            print(f"✅ Summary saved to: {output_path.name}")
        
        return results

def main():
    processor = DocumentProcessor()
    
    # Example: Process a single file
    sample_text = """Artificial intelligence is transforming industries 
    across the globe. From healthcare to finance, AI systems are making 
    decisions faster and more accurately than ever before. Machine learning 
    algorithms can detect patterns in data that humans might miss."""
    
    # Save sample text
    with open('sample.txt', 'w') as f:
        f.write(sample_text)
    
    # Process it
    print("🔍 Analyzing document...")
    keywords = processor.extract_keywords(sample_text)
    print(f"📌 Keywords: {keywords}")
    
    summary = processor.summarize_file('sample.txt')
    print(f"📝 Summary: {summary}")

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python document_processor.py
```

---

### **Script 5: Email Automation**

Create `email_automation.py`:

```python
import ollama
import json
from datetime import datetime

class EmailAutomation:
    def __init__(self, model='llama3.2:3b'):
        self.model = model
    
    def classify_email(self, email_content):
        """Classify email priority and category"""
        
        prompt = f"""Analyze this email and return JSON with:
        - priority: high/medium/low
        - category: work/personal/spam/urgent
        - needs_response: true/false
        - suggested_response: brief response if needed
        
        Email: {email_content}
        
        Return ONLY valid JSON:"""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            format='json'  # Request JSON output
        )
        
        try:
            return json.loads(response['message']['content'])
        except:
            return {"error": "Failed to parse response"}
    
    def generate_reply(self, original_email, tone='professional'):
        """Generate email reply"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'''Write a {tone} reply to this email:
                    
                    Original: {original_email}
                    
                    Keep it concise and polite.'''
                }
            ]
        )
        
        return response['message']['content']
    
    def process_inbox(self, emails):
        """Process multiple emails"""
        
        results = []
        for i, email in enumerate(emails, 1):
            print(f"\n📧 Processing email {i}/{len(emails)}")
            
            classification = self.classify_email(email)
            results.append({
                'original': email[:100] + "...",
                'classification': classification,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"   Priority: {classification.get('priority', 'unknown')}")
            print(f"   Category: {classification.get('category', 'unknown')}")
        
        return results

def main():
    automator = EmailAutomation()
    
    # Sample emails
    sample_emails = [
        "URGENT: Server down in production. Need immediate fix!",
        "Hi team, here's the weekly report. Please review when you get a chance.",
        "CONGRATULATIONS! You've won a free iPhone! Click here to claim!",
        "Can we schedule a meeting for next week to discuss the Q4 plans?"
    ]
    
    # Process emails
    results = automator.process_inbox(sample_emails)
    
    # Generate reply for urgent email
    print("\n" + "="*50)
    print("📝 Generating reply for urgent email...")
    reply = automator.generate_reply(sample_emails[0], tone='urgent')
    print(f"Suggested reply:\n{reply}")
    
    # Save results
    with open('email_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n✅ Results saved to email_results.json")

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python email_automation.py
```

---

## 🛠️ Step 7: System Monitoring & Automation

### **Script 6: Log Analyzer**

Create `log_analyzer.py`:

```python
import ollama
import subprocess
import platform

class LogAnalyzer:
    def __init__(self, model='llama3.2:3b'):
        self.model = model
    
    def get_system_logs(self, lines=50):
        """Get system logs based on OS"""
        
        system = platform.system()
        
        try:
            if system == 'Darwin':  # macOS
                result = subprocess.run(
                    ['log', 'show', '--last', '1h', '--predicate', 
                     'eventMessage contains "error"'],
                    capture_output=True, text=True, timeout=10
                )
            elif system == 'Linux':
                result = subprocess.run(
                    ['journalctl', '-n', str(lines), '-p', '3'],
                    capture_output=True, text=True, timeout=10
                )
            else:  # Windows
                return "System log access not supported on Windows via this script"
            
            return result.stdout[-2000:]  # Last 2000 chars
        except Exception as e:
            return f"Error reading logs: {e}"
    
    def analyze_logs(self, log_content):
        """Use AI to analyze logs"""
        
        if not log_content or len(log_content) < 10:
            return "No significant log data to analyze"
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'''Analyze these system logs and provide:
                    1. Critical issues found
                    2. Potential causes
                    3. Recommended actions
                    4. Risk level (high/medium/low)
                    
                    Logs:
                    {log_content}'''
                }
            ]
        )
        
        return response['message']['content']
    
    def monitor_continuously(self, interval_seconds=300):
        """Monitor logs periodically"""
        import time
        
        print(f"🔄 Starting log monitoring (every {interval_seconds}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                print(f"\n⏰ Check at {time.strftime('%H:%M:%S')}")
                print("="*50)
                
                logs = self.get_system_logs()
                analysis = self.analyze_logs(logs)
                
                print(analysis)
                
                # Save to file
                with open('log_analysis.txt', 'a') as f:
                    f.write(f"\n--- {time.ctime()} ---\n")
                    f.write(analysis)
                    f.write("\n")
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")

def main():
    analyzer = LogAnalyzer()
    
    print("🔍 Testing log analysis...")
    logs = analyzer.get_system_logs()
    
    if logs:
        print(f"📋 Retrieved {len(logs)} characters of logs")
        analysis = analyzer.analyze_logs(logs)
        print("\n📊 Analysis Results:")
        print(analysis)

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python log_analyzer.py
```

---

## 🎯 Step 8: Utility Scripts

### **Script 7: Code Assistant**

Create `code_assistant.py`:

```python
import ollama
import sys

class CodeAssistant:
    def __init__(self, model='llama3.2:3b'):
        self.model = model
    
    def review_code(self, code, language='python'):
        """Review code for improvements"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'''Review this {language} code and provide:
                    1. Potential bugs
                    2. Performance improvements
                    3. Best practice violations
                    4. Security concerns
                    
                    Code:
                    ```{language}
                    {code}
                    ```'''
                }
            ]
        )
        
        return response['message']['content']
    
    def explain_code(self, code):
        """Explain what code does"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'Explain this code in simple terms:\n```\n{code}\n```'
                }
            ]
        )
        
        return response['message']['content']
    
    def generate_tests(self, code):
        """Generate unit tests"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'Generate pytest unit tests for this code:\n```python\n{code}\n```'
                }
            ]
        )
        
        return response['message']['content']

def main():
    assistant = CodeAssistant()
    
    sample_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
    
def process_data(data):
    results = []
    for item in data:
        if item > 0:
            results.append(item * 2)
    return results
    """
    
    print("🔍 Code Review:")
    print(assistant.review_code(sample_code))
    
    print("\n" + "="*50)
    print("📖 Code Explanation:")
    print(assistant.explain_code(sample_code))

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python code_assistant.py
```

---

## 🌐 Step 9: API Server with FastAPI

### **Script 8: Ollama API Server**

Create `ollama_server.py`:

```bash
# First install FastAPI and uvicorn
pip install fastapi uvicorn
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import uvicorn

app = FastAPI(title="Ollama Automation API")

class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3.2:1b"
    max_tokens: int = 500

class ChatResponse(BaseModel):
    response: str
    model: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    
    try:
        response = ollama.chat(
            model=request.model,
            messages=[{'role': 'user', 'content': request.prompt}]
        )
        
        return ChatResponse(
            response=response['message']['content'],
            model=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models"""
    
    try:
        models = ollama.list()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ollama-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run the server:**

```bash
python ollama_server.py
```

**Test the API:**

```bash
# In another terminal
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?", "model": "llama3.2:1b"}'
```

---

## 🔥 Step 10: Advanced Automation Pipeline

### **Script 9: Complete Workflow Automation**

Create `workflow_automation.py`:

```python
import ollama
import json
import os
from pathlib import Path
from datetime import datetime

class WorkflowAutomation:
    """Complete automation pipeline"""
    
    def __init__(self, model='llama3.2:3b'):
        self.model = model
        self.workflow_history = []
    
    def step1_analyze_requirement(self, task_description):
        """Analyze and break down task"""
        
        prompt = f"""Analyze this task and break it down into subtasks.
        Return JSON array of subtasks with:
        - name: subtask name
        - complexity: simple/medium/complex
        - estimated_time: in minutes
        
        Task: {task_description}
        
        Return ONLY valid JSON array."""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        
        try:
            return json.loads(response['message']['content'])
        except:
            return [{"name": "Error parsing", "complexity": "unknown"}]
    
    def step2_generate_solution(self, subtask):
        """Generate solution for a subtask"""
        
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': f'''Provide a detailed solution for this subtask:
                    {json.dumps(subtask, indent=2)}
                    
                    Include:
                    1. Step-by-step approach
                    2. Required resources
                    3. Potential challenges
                    4. Success criteria'''
                }
            ]
        )
        
        return response['message']['content']
    
    def step3_execute_workflow(self, task):
        """Execute complete workflow"""
        
        print(f"🚀 Starting workflow for: {task[:100]}...\n")
        
        # Step 1: Analyze
        print("📊 Step 1: Analyzing task...")
        subtasks = self.step1_analyze_requirement(task)
        
        if isinstance(subtasks, list):
            print(f"✅ Identified {len(subtasks)} subtasks\n")
        else:
            print("❌ Failed to analyze task")
            return None
        
        # Step 2: Generate solutions
        workflow_result = {
            'original_task': task,
            'timestamp': datetime.now().isoformat(),
            'subtasks': [],
            'total_estimated_time': 0
        }
        
        for i, subtask in enumerate(subtasks, 1):
            print(f"🔧 Processing subtask {i}/{len(subtasks)}: {subtask.get('name', 'Unknown')}")
            
            solution = self.step2_generate_solution(subtask)
            
            workflow_result['subtasks'].append({
                'subtask': subtask,
                'solution': solution,
                'completed': False
            })
            
            workflow_result['total_estimated_time'] += subtask.get('estimated_time', 30)
        
        # Save results
        output_file = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(workflow_result, f, indent=2)
        
        print(f"\n✅ Workflow complete!")
        print(f"📁 Results saved to: {output_file}")
        print(f"⏱️  Total estimated time: {workflow_result['total_estimated_time']} minutes")
        
        return workflow_result

def main():
    # Example tasks to automate
    tasks = [
        "Set up a CI/CD pipeline for a Python web application",
        "Create a data backup strategy for a small business",
        "Plan a team building event for 20 people"
    ]
    
    automator = WorkflowAutomation()
    
    # Process first task
    result = automator.step3_execute_workflow(tasks[0])
    
    # Print summary
    if result:
        print("\n" + "="*50)
        print("📋 WORKFLOW SUMMARY")
        print("="*50)
        for subtask in result['subtasks']:
            print(f"\n✅ {subtask['subtask']['name']}")
            print(f"   Complexity: {subtask['subtask']['complexity']}")
            print(f"   Time: {subtask['subtask']['estimated_time']} min")

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python workflow_automation.py
```

---

## 📚 Useful Ollama Commands Reference

```bash
# List all models
ollama list

# Pull a model
ollama pull model_name

# Remove a model
ollama rm model_name

# Show model info
ollama show model_name

# Run a model directly in terminal
ollama run llama3.2:1b

# Copy a model
ollama cp source_model new_model_name

# Create custom model from Modelfile
ollama create mymodel -f ./Modelfile

# Check running processes
ollama ps

# Stop a running model
ollama stop model_name
```

---

## 🎯 Best Practices

### 1. **Model Selection**

```python
# For simple tasks (fast, less memory)
model = 'llama3.2:1b'

# For complex tasks (slower, more accurate)
model = 'llama3.2:3b'  # or 'mistral', 'codellama'
```

### 2. **Error Handling Template**

```python
def safe_ollama_call(prompt, model='llama3.2:1b', retries=3):
    for attempt in range(retries):
        try:
            response = ollama.chat(
                model=model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"Retry {attempt + 1}/{retries} after error: {e}")
            import time
            time.sleep(2)
```

### 3. **Performance Optimization**

```python
# Set timeout for long operations
response = ollama.chat(
    model=model,
    messages=[...],
    options={
        'temperature': 0.7,
        'num_predict': 500,  # Max tokens to generate
        'top_k': 40,
        'top_p': 0.9
    }
)
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

```bash
# 1. Connection Error
# Solution: Ensure Ollama is running
ollama serve

# 2. Model Not Found
ollama pull llama3.2:1b

# 3. Out of Memory
# Use smaller model
ollama pull llama3.2:1b  # instead of 3b or larger

# 4. Check if service is running
curl http://localhost:11434/api/tags

# 5. Reset everything
ollama stop
# Then restart
ollama serve
```

---

## 🎉 Complete Example Project Structure

```bash
ollama_automation/
├── requirements.txt
├── config.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── logger.py
├── scripts/
│   ├── basic_chat.py
│   ├── streaming_chat.py
│   ├── conversation.py
│   ├── document_processor.py
│   ├── email_automation.py
│   ├── log_analyzer.py
│   ├── code_assistant.py
│   └── workflow_automation.py
├── server/
│   └── ollama_server.py
└── README.md
```

**requirements.txt:**

```txt
ollama
fastapi
uvicorn
pydantic
```

**Install all dependencies:**

```bash
pip install -r requirements.txt
```

---

## ✅ Quick Start Checklist

1. ✅ Install Ollama
2. ✅ Start Ollama service (`ollama serve`)
3. ✅ Create Python virtual environment
4. ✅ `pip install ollama`
5. ✅ Pull at least one model (`ollama pull llama3.2:1b`)
6. ✅ Run `basic_chat.py` to test
7. ✅ Experiment with different scripts
8. ✅ Build your own automation!

---

## 📊 Performance Benchmarks

| Model | RAM Usage | Speed | Best For |
| ----- | --------- | ----- | -------- |
| llama3.2:1b | ~2GB | Fast | Simple tasks, testing |
| llama3.2:3b | ~4GB | Medium | General purpose |
| mistral | ~6GB | Medium | Complex reasoning |
| codellama | ~8GB | Slow | Code generation |

---

This manual provides everything you need to start building Python + Ollama automations! Start with basic scripts and progressively build more complex automation workflows. 🚀
