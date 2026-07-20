# 🚀 3 Complete Ollama + Python Automation Projects

## Project 1: 🏥 AI Medical Report Analyzer & Health Assistant

### **Overview**

An automated system that analyzes medical reports, extracts key health metrics, and provides plain-language explanations with actionable health recommendations.

---

### **Project Structure**

```bash
medical_analyzer/
├── main.py
├── medical_analyzer.py
├── report_generator.py
├── health_tracker.py
├── templates/
│   └── report_template.html
├── sample_reports/
│   └── blood_test.txt
├── output/
│   └── (generated reports)
└── requirements.txt
```

---

### **requirements.txt**

```txt
ollama
pandas
matplotlib
fpdf2
jinja2
```

---

### **1. Core Medical Analyzer - `medical_analyzer.py`**

```python
import ollama
import json
import re
from datetime import datetime
from typing import Dict, List, Optional

class MedicalReportAnalyzer:
    """AI-powered medical report analysis system"""
    
    def __init__(self, model='llama3.2:3b'):
        self.model = model
        self.analysis_history = []
        
    def extract_metrics(self, report_text: str) -> Dict:
        """Extract numerical health metrics from report text"""
        
        prompt = f"""Analyze this medical report and extract all health metrics.
        Return a JSON object with this structure:
        {{
            "metrics": [
                {{
                    "name": "metric name",
                    "value": numeric_value,
                    "unit": "measurement unit",
                    "normal_range": "expected range if mentioned",
                    "status": "normal/high/low/critical",
                    "interpretation": "brief medical interpretation"
                }}
            ],
            "patient_info": {{
                "age": age_if_mentioned,
                "gender": gender_if_mentioned,
                "test_date": date_if_mentioned
            }},
            "overall_assessment": "brief overall health assessment"
        }}
        
        Report:
        {report_text[:4000]}
        
        Return ONLY valid JSON. No other text."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            data = json.loads(response['message']['content'])
            return data
            
        except json.JSONDecodeError:
            return {"error": "Failed to parse metrics", "raw_report": report_text}
    
    def explain_results(self, metrics: Dict) -> str:
        """Generate patient-friendly explanation"""
        
        prompt = f"""Explain these medical test results in simple, non-technical language.
        Focus on:
        1. What each metric means for the patient's health
        2. Which results need attention
        3. Lifestyle recommendations based on results
        4. When to consult a doctor
        
        Write in a reassuring, professional tone suitable for patients.
        
        Metrics:
        {json.dumps(metrics, indent=2)}"""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return response['message']['content']
    
    def generate_recommendations(self, metrics: Dict) -> List[Dict]:
        """Generate specific health recommendations"""
        
        prompt = f"""Based on these medical results, provide specific actionable recommendations.
        Return JSON array:
        [
            {{
                "category": "diet/exercise/medication/lifestyle/follow-up",
                "priority": "high/medium/low",
                "recommendation": "specific action",
                "timeframe": "when to implement",
                "expected_benefit": "what improvement to expect"
            }}
        ]
        
        Results:
        {json.dumps(metrics, indent=2)}
        
        Return ONLY valid JSON array."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
            
        except:
            return [{"error": "Failed to generate recommendations"}]
    
    def detect_anomalies(self, metrics: Dict) -> List[str]:
        """Flag critical or concerning values"""
        
        prompt = f"""Identify any critical or concerning values in these results.
        Return JSON array of alerts:
        [
            {{
                "metric": "name of metric",
                "severity": "critical/warning/info",
                "message": "what's wrong and why it matters",
                "immediate_action": "what to do now"
            }}
        ]
        
        Results:
        {json.dumps(metrics, indent=2)}
        
        Return ONLY valid JSON array."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
            
        except:
            return [{"error": "Failed to detect anomalies"}]
    
    def full_analysis(self, report_text: str) -> Dict:
        """Run complete analysis pipeline"""
        
        print("🔬 Starting medical report analysis...")
        
        # Step 1: Extract metrics
        print("📊 Extracting health metrics...")
        metrics = self.extract_metrics(report_text)
        
        if "error" in metrics:
            return metrics
        
        # Step 2: Detect anomalies
        print("⚠️  Checking for anomalies...")
        anomalies = self.detect_anomalies(metrics)
        
        # Step 3: Generate explanation
        print("📝 Creating patient explanation...")
        explanation = self.explain_results(metrics)
        
        # Step 4: Generate recommendations
        print("💊 Generating recommendations...")
        recommendations = self.generate_recommendations(metrics)
        
        # Compile results
        analysis_result = {
            "analysis_id": f"MED-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "anomalies": anomalies,
            "explanation": explanation,
            "recommendations": recommendations
        }
        
        # Save to history
        self.analysis_history.append(analysis_result)
        
        print("✅ Analysis complete!")
        return analysis_result
```

---

### **2. Report Generator - `report_generator.py`**

```python
from fpdf import FPDF
import json
from datetime import datetime
from pathlib import Path

class MedicalReportGenerator:
    """Generate formatted medical reports"""
    
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_pdf_report(self, analysis_result: Dict) -> str:
        """Generate professional PDF report"""
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, 'AI Medical Report Analysis', ln=True, align='C')
        pdf.ln(10)
        
        # Report ID and Date
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"Report ID: {analysis_result.get('analysis_id', 'N/A')}", ln=True)
        pdf.cell(0, 10, f"Date: {analysis_result.get('timestamp', 'N/A')[:10]}", ln=True)
        pdf.ln(10)
        
        # Metrics Table
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Health Metrics', ln=True)
        pdf.ln(5)
        
        # Table header
        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(50, 7, 'Metric', 1, fill=True)
        pdf.cell(30, 7, 'Value', 1, fill=True)
        pdf.cell(30, 7, 'Unit', 1, fill=True)
        pdf.cell(40, 7, 'Normal Range', 1, fill=True)
        pdf.cell(40, 7, 'Status', 1, fill=True)
        pdf.ln()
        
        # Table rows
        pdf.set_font('Arial', '', 9)
        metrics = analysis_result.get('metrics', {}).get('metrics', [])
        
        for metric in metrics:
            # Color code status
            status = metric.get('status', '').lower()
            if status == 'critical':
                pdf.set_text_color(255, 0, 0)
            elif status in ['high', 'low']:
                pdf.set_text_color(255, 165, 0)
            else:
                pdf.set_text_color(0, 0, 0)
            
            pdf.cell(50, 7, metric.get('name', 'N/A')[:25], 1)
            pdf.cell(30, 7, str(metric.get('value', 'N/A'))[:12], 1)
            pdf.cell(30, 7, metric.get('unit', 'N/A')[:12], 1)
            pdf.cell(40, 7, metric.get('normal_range', 'N/A')[:18], 1)
            pdf.cell(40, 7, status.upper(), 1)
            pdf.ln()
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)
        
        # Anomalies
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Critical Alerts', ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 10)
        anomalies = analysis_result.get('anomalies', [])
        
        for anomaly in anomalies:
            severity = anomaly.get('severity', 'info')
            if severity == 'critical':
                pdf.set_text_color(255, 0, 0)
            
            pdf.cell(0, 7, f"* {anomaly.get('message', 'N/A')}", ln=True)
            
            if anomaly.get('immediate_action'):
                pdf.cell(10, 7, '', ln=False)
                pdf.cell(0, 7, f"Action: {anomaly.get('immediate_action')}", ln=True)
            
            pdf.ln(2)
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)
        
        # Explanation
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Explanation (Patient-Friendly)', ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 10)
        explanation = analysis_result.get('explanation', '')
        
        # Split long text into multiple lines
        for line in explanation.split('\n'):
            pdf.multi_cell(0, 6, line)
            pdf.ln(2)
        
        pdf.ln(10)
        
        # Recommendations
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Recommendations', ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 10)
        recommendations = analysis_result.get('recommendations', [])
        
        for rec in recommendations:
            priority = rec.get('priority', 'medium')
            if priority == 'high':
                pdf.set_font('Arial', 'B', 10)
            
            pdf.cell(0, 7, f"[{priority.upper()}] {rec.get('category', 'N/A')}", ln=True)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(0, 5, f"  * {rec.get('recommendation', 'N/A')}")
            pdf.ln(2)
        
        # Save PDF
        filename = self.output_dir / f"medical_report_{analysis_result.get('analysis_id', 'report')}.pdf"
        pdf.output(str(filename))
        
        return str(filename)
    
    def generate_summary_text(self, analysis_result: Dict) -> str:
        """Generate text summary for quick sharing"""
        
        summary = f"""
{'='*60}
MEDICAL REPORT SUMMARY
{'='*60}
Report ID: {analysis_result.get('analysis_id', 'N/A')}
Date: {analysis_result.get('timestamp', 'N/A')[:10]}

KEY FINDINGS:
"""
        
        anomalies = analysis_result.get('anomalies', [])
        for anomaly in anomalies:
            summary += f"\n{'⚠️' if anomaly.get('severity') == 'critical' else '⚡'} {anomaly.get('message', '')}"
        
        summary += f"""

RECOMMENDATIONS:
"""
        
        recommendations = analysis_result.get('recommendations', [])
        for rec in recommendations[:5]:  # Top 5
            summary += f"\n• {rec.get('recommendation', '')}"
        
        summary += f"\n\n{'='*60}\n"
        
        return summary
```

---

### **3. Health Tracker - `health_tracker.py`**

```python
import ollama
import json
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

class HealthTracker:
    """Track health metrics over time with AI insights"""
    
    def __init__(self, model='llama3.2:3b'):
        self.model = model
        self.records = []
    
    def add_reading(self, metrics: Dict):
        """Add a new health reading"""
        
        reading = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
        
        self.records.append(reading)
        print(f"✅ Added reading at {reading['timestamp'][:19]}")
    
    def get_trend_analysis(self, metric_name: str) -> Dict:
        """Analyze trends for a specific metric"""
        
        # Extract values over time
        trend_data = []
        for record in self.records:
            timestamp = record['timestamp']
            metrics = record['metrics'].get('metrics', [])
            
            for metric in metrics:
                if metric.get('name') == metric_name:
                    trend_data.append({
                        "date": timestamp[:10],
                        "value": metric.get('value')
                    })
        
        if not trend_data:
            return {"error": f"No data found for {metric_name}"}
        
        # Create DataFrame for analysis
        df = pd.DataFrame(trend_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate statistics
        stats = {
            "metric": metric_name,
            "readings": len(df),
            "average": df['value'].mean(),
            "min": df['value'].min(),
            "max": df['value'].max(),
            "trend": "increasing" if df['value'].iloc[-1] > df['value'].iloc[0] else "decreasing",
            "dates": df['date'].dt.strftime('%Y-%m-%d').tolist(),
            "values": df['value'].tolist()
        }
        
        # Get AI interpretation of trend
        prompt = f"""Analyze this health metric trend:
        Metric: {metric_name}
        Values over time: {json.dumps(stats)}
        
        Provide:
        1. Is the trend concerning?
        2. What might cause this pattern?
        3. Recommended monitoring frequency
        4. When to seek medical attention
        
        Keep it concise."""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        stats['ai_interpretation'] = response['message']['content']
        
        return stats
    
    def predict_future_values(self, metric_name: str, days_ahead: int = 30) -> Dict:
        """Use AI to predict future metric values"""
        
        stats = self.get_trend_analysis(metric_name)
        
        if "error" in stats:
            return stats
        
        prompt = f"""Based on these health metric trends, predict values for the next {days_ahead} days.
        Current data: {json.dumps(stats)}
        
        Return JSON with:
        {{
            "predictions": [daily predicted values],
            "confidence": "high/medium/low",
            "risk_factors": ["list of risk factors"],
            "projected_outcome": "description of expected outcome"
        }}
        
        Return ONLY valid JSON."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
            
        except:
            return {"error": "Failed to generate predictions"}
    
    def generate_health_score(self) -> Dict:
        """Calculate overall health score"""
        
        if not self.records:
            return {"error": "No health records available"}
        
        # Compile all metrics
        all_metrics = []
        for record in self.records:
            all_metrics.extend(record['metrics'].get('metrics', []))
        
        prompt = f"""Based on these health metrics, calculate an overall health score (0-100).
        Consider:
        - Number of metrics in normal range
        - Critical values
        - Trends over time
        
        Health data:
        {json.dumps(all_metrics[:10], indent=2)}
        
        Return JSON:
        {{
            "health_score": score (0-100),
            "rating": "Excellent/Good/Fair/Poor",
            "strengths": ["areas where metrics are good"],
            "concerns": ["areas needing attention"],
            "summary": "one paragraph summary"
        }}
        
        Return ONLY valid JSON."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
            
        except:
            return {"error": "Failed to calculate health score"}
```

---

### **4. Main Application - `main.py`**

```python
#!/usr/bin/env python3
"""
AI Medical Report Analyzer - Main Application
Complete health analysis and tracking system
"""

from medical_analyzer import MedicalReportAnalyzer
from report_generator import MedicalReportGenerator
from health_tracker import HealthTracker
import json
from pathlib import Path
from datetime import datetime

class MedicalAnalysisApp:
    """Main application controller"""
    
    def __init__(self):
        self.analyzer = MedicalReportAnalyzer()
        self.reporter = MedicalReportGenerator()
        self.tracker = HealthTracker()
        self.samples_dir = Path("sample_reports")
        self.samples_dir.mkdir(exist_ok=True)
    
    def create_sample_report(self):
        """Create a sample medical report for testing"""
        
        sample = """PATIENT BLOOD TEST RESULTS
Patient ID: P-12345
Age: 45
Gender: Male
Date: 2024-01-15

COMPLETE BLOOD COUNT (CBC):
- Hemoglobin: 14.2 g/dL (Normal: 13.5-17.5)
- White Blood Cells: 11,500 /mcL (Normal: 4,500-11,000) HIGH
- Platelets: 245,000 /mcL (Normal: 150,000-450,000)
- Red Blood Cells: 5.1 million/mcL (Normal: 4.7-6.1)

LIPID PANEL:
- Total Cholesterol: 245 mg/dL (Normal: <200) HIGH
- HDL Cholesterol: 38 mg/dL (Normal: >40) LOW
- LDL Cholesterol: 162 mg/dL (Normal: <100) HIGH
- Triglycerides: 180 mg/dL (Normal: <150) HIGH

LIVER FUNCTION:
- ALT: 45 U/L (Normal: 7-56)
- AST: 32 U/L (Normal: 10-40)
- Alkaline Phosphatase: 95 U/L (Normal: 44-147)

METABOLIC PANEL:
- Glucose (Fasting): 108 mg/dL (Normal: 70-100) HIGH
- Creatinine: 1.1 mg/dL (Normal: 0.6-1.3)
- Sodium: 140 mEq/L (Normal: 135-145)
- Potassium: 4.2 mEq/L (Normal: 3.5-5.0)
"""

        filepath = self.samples_dir / "blood_test.txt"
        with open(filepath, 'w') as f:
            f.write(sample)
        
        return str(filepath), sample
    
    def analyze_sample(self):
        """Run analysis on sample report"""
        
        print("\n" + "="*60)
        print("🏥 AI MEDICAL REPORT ANALYZER")
        print("="*60 + "\n")
        
        # Create/load sample
        filepath, sample_text = self.create_sample_report()
        print(f"📄 Loaded sample report: {filepath}\n")
        
        # Run full analysis
        analysis = self.analyzer.full_analysis(sample_text)
        
        # Generate PDF report
        print("\n📊 Generating PDF report...")
        pdf_path = self.reporter.generate_pdf_report(analysis)
        print(f"✅ PDF report saved: {pdf_path}")
        
        # Generate text summary
        summary = self.reporter.generate_summary_text(analysis)
        print("\n" + summary)
        
        # Save full analysis to JSON
        json_path = Path("output") / f"analysis_{analysis['analysis_id']}.json"
        with open(json_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"📁 Full analysis saved: {json_path}")
        
        # Track health metrics
        self.tracker.add_reading(analysis['metrics'])
        
        # Generate health score
        print("\n💪 Calculating health score...")
        health_score = self.tracker.generate_health_score()
        
        if "error" not in health_score:
            print(f"\n{'='*40}")
            print(f"OVERALL HEALTH SCORE: {health_score['health_score']}/100")
            print(f"RATING: {health_score['rating']}")
            print(f"{'='*40}")
            print(f"\nStrengths: {', '.join(health_score.get('strengths', []))}")
            print(f"Concerns: {', '.join(health_score.get('concerns', []))}")
            print(f"\nSummary: {health_score.get('summary', '')}")
        
        return analysis
    
    def interactive_mode(self):
        """Run interactive analysis mode"""
        
        print("\n" + "="*60)
        print("🏥 INTERACTIVE MEDICAL ANALYSIS MODE")
        print("="*60)
        print("\nCommands: 'analyze', 'sample', 'track', 'quit'\n")
        
        while True:
            command = input("👉 Enter command: ").strip().lower()
            
            if command == 'quit':
                print("👋 Goodbye!")
                break
            
            elif command == 'sample':
                self.analyze_sample()
            
            elif command == 'analyze':
                print("\n📋 Paste your medical report text (type 'END' on new line to finish):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    lines.append(line)
                
                report_text = '\n'.join(lines)
                
                if report_text.strip():
                    analysis = self.analyzer.full_analysis(report_text)
                    summary = self.reporter.generate_summary_text(analysis)
                    print("\n" + summary)
                    self.tracker.add_reading(analysis['metrics'])
            
            elif command == 'track':
                metric = input("Enter metric name to track: ").strip()
                if metric:
                    trend = self.tracker.get_trend_analysis(metric)
                    print(f"\n📈 Trend Analysis for {metric}:")
                    print(json.dumps(trend, indent=2))
            
            else:
                print("❌ Unknown command. Try: analyze, sample, track, quit")

def main():
    app = MedicalAnalysisApp()
    
    # Run sample analysis
    app.analyze_sample()
    
    # Start interactive mode
    app.interactive_mode()

if __name__ == "__main__":
    main()
```

---

## Project 2: 📚 Intelligent Research Assistant & Knowledge Base

### **Overview**

An AI-powered research system that reads documents, answers questions with citations, generates summaries, and builds a searchable knowledge base.

---

### **Project Structure**

```bash
research_assistant/
├── main.py
├── knowledge_base.py
├── document_processor.py
├── research_agent.py
├── citation_manager.py
├── documents/
│   ├── paper1.txt
│   └── paper2.txt
├── knowledge_base/
│   └── (indexed documents)
└── requirements.txt
```

---

### **Full Implementation**

```python
# research_assistant.py - Complete Research Assistant System

import ollama
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import pickle
import re

class Document:
    """Document representation with metadata"""
    
    def __init__(self, content: str, filename: str, metadata: Dict = None):
        self.content = content
        self.filename = filename
        self.metadata = metadata or {}
        self.doc_id = hashlib.md5(content.encode()).hexdigest()[:12]
        self.chunks = []
        self.embeddings = []
        self.summary = ""
        self.keywords = []
        self.created_at = datetime.now().isoformat()
    
    def chunk_text(self, chunk_size: int = 1000, overlap: int = 200):
        """Split document into overlapping chunks"""
        
        words = self.content.split()
        self.chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                self.chunks.append({
                    'text': chunk,
                    'index': len(self.chunks),
                    'start': i,
                    'end': min(i + chunk_size, len(words))
                })
        
        return self.chunks

class ResearchAssistant:
    """AI-powered research assistant"""
    
    def __init__(self, model='llama3.2:3b', kb_path='knowledge_base'):
        self.model = model
        self.kb_path = Path(kb_path)
        self.kb_path.mkdir(exist_ok=True)
        self.documents = {}
        self.load_knowledge_base()
    
    def add_document(self, filepath: str) -> Document:
        """Add document to knowledge base"""
        
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Read content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create document object
        doc = Document(
            content=content,
            filename=filepath.name,
            metadata={
                'source': str(filepath),
                'size': len(content),
                'added_at': datetime.now().isoformat()
            }
        )
        
        # Process document
        print(f"📄 Processing: {filepath.name}")
        
        # Generate chunks
        doc.chunk_text()
        print(f"   ✂️  Created {len(doc.chunks)} chunks")
        
        # Generate summary
        doc.summary = self.generate_summary(content)
        print(f"   📝 Generated summary")
        
        # Extract keywords
        doc.keywords = self.extract_keywords(content)
        print(f"   🏷️  Extracted {len(doc.keywords)} keywords")
        
        # Store document
        self.documents[doc.doc_id] = doc
        
        # Save knowledge base
        self.save_knowledge_base()
        
        return doc
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate document summary"""
        
        prompt = f"""Summarize this document in 3-5 sentences.
        Focus on main findings, methodology, and conclusions.
        
        Document:
        {text[:3000]}
        
        Summary:"""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'num_predict': max_length}
        )
        
        return response['message']['content']
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract key topics from text"""
        
        prompt = f"""Extract 10-15 key topics, terms, and concepts from this text.
        Return as a JSON array of strings.
        Focus on technical terms, proper nouns, and important concepts.
        
        Text:
        {text[:2000]}
        
        Return ONLY valid JSON array."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
        except:
            return []
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search knowledge base for relevant documents"""
        
        results = []
        
        for doc_id, doc in self.documents.items():
            # Simple relevance scoring based on keyword matching
            relevance = 0
            query_terms = query.lower().split()
            
            # Check title/keywords
            for keyword in doc.keywords:
                if any(term in keyword.lower() for term in query_terms):
                    relevance += 2
            
            # Check content
            for term in query_terms:
                relevance += doc.content.lower().count(term)
            
            if relevance > 0:
                # Get most relevant chunks
                relevant_chunks = []
                for chunk in doc.chunks:
                    chunk_score = sum(chunk['text'].lower().count(term) for term in query_terms)
                    if chunk_score > 0:
                        relevant_chunks.append({
                            'text': chunk['text'][:500],
                            'score': chunk_score,
                            'index': chunk['index']
                        })
                
                relevant_chunks.sort(key=lambda x: x['score'], reverse=True)
                
                results.append({
                    'doc_id': doc_id,
                    'filename': doc.filename,
                    'summary': doc.summary,
                    'relevance_score': relevance,
                    'keywords': doc.keywords[:5],
                    'relevant_chunks': relevant_chunks[:3]
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:top_k]
    
    def answer_question(self, question: str, use_context: bool = True) -> Dict:
        """Answer a research question using knowledge base"""
        
        if use_context and self.documents:
            # Search for relevant documents
            search_results = self.search_documents(question)
            
            if search_results:
                # Build context from relevant chunks
                context = "\n\n".join([
                    f"[From: {r['filename']}]\n" + 
                    "\n".join(c['text'] for c in r['relevant_chunks'])
                    for r in search_results[:3]
                ])
                
                prompt = f"""Answer this question based on the provided context.
                Cite specific sources from the context.
                
                Context:
                {context[:3000]}
                
                Question: {question}
                
                Provide:
                1. Direct answer to the question
                2. Supporting evidence from the context
                3. Citations (document names)
                4. Confidence level (high/medium/low)
                
                Format as JSON:
                {{
                    "answer": "main answer",
                    "evidence": ["supporting points"],
                    "citations": ["document names"],
                    "confidence": "high/medium/low",
                    "follow_up_questions": ["suggested follow-ups"]
                }}"""
                
                try:
                    response = ollama.chat(
                        model=self.model,
                        messages=[{'role': 'user', 'content': prompt}],
                        format='json'
                    )
                    
                    result = json.loads(response['message']['content'])
                    result['sources_used'] = [r['filename'] for r in search_results[:3]]
                    
                    return result
                    
                except:
                    pass
        
        # Fallback: answer without context
        prompt = f"""Answer this research question thoroughly:
        
        Question: {question}
        
        Provide a comprehensive answer with:
        1. Main explanation
        2. Key points
        3. Examples if relevant
        4. Areas for further research"""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return {
            "answer": response['message']['content'],
            "evidence": [],
            "citations": ["General knowledge"],
            "confidence": "medium",
            "sources_used": []
        }
    
    def generate_literature_review(self, topic: str) -> str:
        """Generate literature review from knowledge base"""
        
        if not self.documents:
            return "No documents in knowledge base. Please add some first."
        
        # Gather all relevant information
        all_summaries = []
        all_keywords = []
        
        for doc in self.documents.values():
            all_summaries.append(f"Document: {doc.filename}\nSummary: {doc.summary}")
            all_keywords.extend(doc.keywords)
        
        context = "\n\n".join(all_summaries)
        keywords_str = ", ".join(set(all_keywords))
        
        prompt = f"""Write a comprehensive literature review on: {topic}
        
        Based on these documents:
        {context[:4000]}
        
        Key topics covered: {keywords_str}
        
        Structure the review:
        1. Introduction to the topic
        2. Key themes and findings
        3. Methodologies used
        4. Gaps in current research
        5. Future directions
        6. References (list all documents used)
        
        Write in academic style with proper citations."""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return response['message']['content']
    
    def extract_insights(self, topic: str) -> Dict:
        """Extract cross-document insights"""
        
        if not self.documents:
            return {"error": "No documents in knowledge base"}
        
        # Compile relevant content
        relevant_content = []
        for doc in self.documents.values():
            if any(keyword.lower() in topic.lower() for keyword in doc.keywords):
                relevant_content.append({
                    'filename': doc.filename,
                    'summary': doc.summary,
                    'keywords': doc.keywords
                })
        
        if not relevant_content:
            return {"error": f"No documents found related to: {topic}"}
        
        prompt = f"""Analyze these documents about {topic} and extract key insights.
        
        Documents:
        {json.dumps(relevant_content, indent=2)}
        
        Return JSON:
        {{
            "key_findings": ["important findings across documents"],
            "agreements": ["where authors agree"],
            "disagreements": ["where authors disagree"],
            "trends": ["emerging trends"],
            "research_gaps": ["missing areas"],
            "practical_implications": ["real-world applications"],
            "confidence": "assessment of overall evidence quality"
        }}
        
        Return ONLY valid JSON."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
        except:
            return {"error": "Failed to extract insights"}
    
    def save_knowledge_base(self):
        """Save knowledge base to disk"""
        
        kb_file = self.kb_path / "knowledge_base.pkl"
        with open(kb_file, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def load_knowledge_base(self):
        """Load knowledge base from disk"""
        
        kb_file = self.kb_path / "knowledge_base.pkl"
        if kb_file.exists():
            with open(kb_file, 'rb') as f:
                self.documents = pickle.load(f)
            print(f"📚 Loaded {len(self.documents)} documents from knowledge base")
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        
        total_chunks = sum(len(doc.chunks) for doc in self.documents.values())
        total_words = sum(len(doc.content.split()) for doc in self.documents.values())
        all_keywords = set()
        for doc in self.documents.values():
            all_keywords.update(doc.keywords)
        
        return {
            "total_documents": len(self.documents),
            "total_chunks": total_chunks,
            "total_words": total_words,
            "unique_keywords": len(all_keywords),
            "documents": [
                {
                    "filename": doc.filename,
                    "chunks": len(doc.chunks),
                    "keywords": len(doc.keywords),
                    "size_kb": len(doc.content) / 1024
                }
                for doc in self.documents.values()
            ]
        }

class CitationManager:
    """Manage citations and references"""
    
    def __init__(self):
        self.citations = []
    
    def add_citation(self, source: str, context: str, page: str = None):
        """Add a citation"""
        
        citation = {
            "id": len(self.citations) + 1,
            "source": source,
            "context": context,
            "page": page,
            "timestamp": datetime.now().isoformat()
        }
        
        self.citations.append(citation)
        return citation
    
    def format_bibliography(self, style: str = "apa") -> str:
        """Format bibliography in specified style"""
        
        if not self.citations:
            return "No citations available"
        
        if style.lower() == "apa":
            bibliography = "References\n" + "="*50 + "\n"
            for i, cite in enumerate(self.citations, 1):
                bibliography += f"{i}. {cite['source']} ({datetime.now().year}). "
                bibliography += f"Retrieved from knowledge base.\n"
        
        return bibliography

# Main application
def main():
    print("="*60)
    print("📚 AI RESEARCH ASSISTANT")
    print("="*60)
    
    # Initialize assistant
    assistant = ResearchAssistant()
    
    # Create sample documents if none exist
    docs_dir = Path("documents")
    docs_dir.mkdir(exist_ok=True)
    
    # Sample research paper 1
    paper1_content = """
    ARTIFICIAL INTELLIGENCE IN HEALTHCARE: A COMPREHENSIVE REVIEW
    
    Abstract:
    This paper examines the impact of artificial intelligence on healthcare delivery.
    We analyze 150 studies covering diagnostic AI, treatment planning, and patient monitoring.
    
    Introduction:
    Healthcare systems worldwide face challenges including rising costs, physician shortages,
    and increasing patient loads. AI technologies offer promising solutions.
    
    Methods:
    We conducted a systematic review of peer-reviewed literature from 2018-2024.
    Studies were categorized by AI application type and healthcare domain.
    
    Results:
    Our analysis revealed three primary areas of AI impact:
    1. Diagnostic accuracy improved by 23% on average when AI assists radiologists
    2. Treatment planning algorithms reduced medication errors by 35%
    3. Predictive analytics identified at-risk patients 48 hours earlier than traditional methods
    
    Discussion:
    While AI shows significant promise, challenges remain in data privacy, algorithmic bias,
    and integration with existing healthcare workflows. Regulatory frameworks need updating
    to accommodate AI-powered medical devices.
    
    Conclusion:
    AI is transforming healthcare delivery, but careful implementation and ongoing evaluation
    are essential to realize its full potential while ensuring patient safety.
    """
    
    # Sample research paper 2
    paper2_content = """
    MACHINE LEARNING FOR CLIMATE CHANGE PREDICTION
    
    Abstract:
    We present novel machine learning approaches for climate change prediction,
    demonstrating 40% improvement over traditional statistical methods.
    
    Introduction:
    Accurate climate prediction is crucial for policy planning and mitigation strategies.
    Traditional models struggle with the complexity of climate systems.
    
    Methodology:
    We developed a hybrid deep learning model combining LSTM networks with attention
    mechanisms, trained on 50 years of climate data from NOAA.
    
    Key Findings:
    1. Temperature predictions accurate within 0.3°C for 5-year forecasts
    2. Precipitation patterns predicted with 85% accuracy
    3. Extreme weather event prediction improved by 55%
    
    Implications:
    These improvements enable better resource allocation for climate adaptation,
    more accurate carbon budget calculations, and improved early warning systems
    for natural disasters.
    """
    
    # Save sample papers
    if not list(docs_dir.glob("*.txt")):
        with open(docs_dir / "ai_healthcare_review.txt", 'w') as f:
            f.write(paper1_content)
        with open(docs_dir / "ml_climate_prediction.txt", 'w') as f:
            f.write(paper2_content)
        print("✅ Created sample research papers")
    
    # Add documents to knowledge base
    for filepath in docs_dir.glob("*.txt"):
        if filepath.name not in [d.filename for d in assistant.documents.values()]:
            assistant.add_document(str(filepath))
    
    # Display statistics
    stats = assistant.get_statistics()
    print(f"\n📊 Knowledge Base Statistics:")
    print(f"   Documents: {stats['total_documents']}")
    print(f"   Total words: {stats['total_words']:,}")
    print(f"   Unique keywords: {stats['unique_keywords']}")
    
    # Interactive research session
    print("\n" + "="*60)
    print("🔍 RESEARCH SESSION")
    print("="*60)
    
    # Example queries
    queries = [
        "What are the main applications of AI in healthcare?",
        "How accurate are machine learning climate predictions?",
        "What challenges exist in implementing AI systems?"
    ]
    
    for query in queries:
        print(f"\n❓ Question: {query}")
        answer = assistant.answer_question(query)
        print(f"\n💡 Answer: {answer.get('answer', 'No answer available')[:300]}...")
        if answer.get('citations'):
            print(f"📎 Sources: {', '.join(answer['citations'])}")
    
    # Generate literature review
    print("\n" + "="*60)
    print("📝 Generating Literature Review...")
    review = assistant.generate_literature_review("AI and Machine Learning Applications")
    print(review[:500] + "...")
    
    # Extract insights
    print("\n" + "="*60)
    print("🔬 Extracting Cross-Document Insights...")
    insights = assistant.extract_insights("AI applications")
    if "error" not in insights:
        print(f"Key Findings: {insights.get('key_findings', [])[:2]}")
        print(f"Research Gaps: {insights.get('research_gaps', [])[:2]}")
    
    # Save session
    session_file = Path("research_session.json")
    with open(session_file, 'w') as f:
        json.dump({
            "date": datetime.now().isoformat(),
            "statistics": stats,
            "insights": insights
        }, f, indent=2)
    print(f"\n✅ Research session saved to {session_file}")
    
    print("\n" + "="*60)
    print("✨ Research Assistant Ready!")
    print("="*60)

if __name__ == "__main__":
    main()
```

---

## Project 3: 🤖 AI Task Automation Pipeline & Scheduler

### **Overview**

An intelligent automation system that accepts natural language task descriptions, breaks them down into subtasks, generates code/scripts to execute them, and manages the entire workflow with scheduling and error handling.

---

### **Project Structure**

```bash
task_automation/
├── main.py
├── task_analyzer.py
├── script_generator.py
├── task_executor.py
├── scheduler.py
├── workflow_manager.py
├── templates/
│   └── task_templates.json
├── generated_scripts/
│   └── (auto-generated scripts)
├── logs/
│   └── (execution logs)
└── requirements.txt
```

---

### **Complete Implementation**

```python
# task_automation_system.py - Complete Automation System

import ollama
import json
import subprocess
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import traceback
import schedule
import threading
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TaskAnalyzer:
    """Analyze and decompose natural language tasks"""
    
    def __init__(self, model='llama3.2:3b'):
        self.model = model
    
    def analyze_task(self, task_description: str) -> Dict:
        """Break down a task into executable components"""
        
        prompt = f"""Analyze this task and create a detailed execution plan.
        
        Task: {task_description}
        
        Return a JSON object with this EXACT structure:
        {{
            "task_summary": "Brief description of the task",
            "complexity": "simple/medium/complex",
            "estimated_duration_minutes": 30,
            "required_resources": ["list of needed resources"],
            "prerequisites": ["things needed before starting"],
            "steps": [
                {{
                    "step_number": 1,
                    "action": "Description of action",
                    "type": "shell/python/file_operation/api_call/notification",
                    "command": "specific command or code",
                    "expected_output": "what success looks like",
                    "error_handling": "what to do if this fails",
                    "rollback": "how to undo this step",
                    "timeout_seconds": 60,
                    "retry_count": 3
                }}
            ],
            "dependencies": {{
                "packages": ["required python packages"],
                "system_tools": ["required system commands"],
                "files": ["required files"]
            }},
            "validation": {{
                "success_criteria": ["how to verify task completed successfully"],
                "failure_conditions": ["what constitutes failure"]
            }}
        }}
        
        Make the steps SPECIFIC and EXECUTABLE. Include actual commands.
        Return ONLY valid JSON."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            plan = json.loads(response['message']['content'])
            return plan
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse task plan: {e}")
            return {"error": "Failed to generate valid plan"}
    
    def optimize_plan(self, plan: Dict) -> Dict:
        """Optimize execution plan for efficiency"""
        
        prompt = f"""Optimize this task execution plan for efficiency and reliability.
        Consider parallel execution opportunities, dependency optimization,
        and error recovery improvements.
        
        Current plan:
        {json.dumps(plan, indent=2)}
        
        Return optimized JSON with same structure but improved steps.
        Return ONLY valid JSON."""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                format='json'
            )
            
            return json.loads(response['message']['content'])
            
        except:
            return plan  # Return original if optimization fails

class ScriptGenerator:
    """Generate executable scripts from task plans"""
    
    def __init__(self, output_dir='generated_scripts'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_python_script(self, plan: Dict) -> str:
        """Generate Python script from task plan"""
        
        prompt = f"""Generate a complete, executable Python script based on this task plan.
        Include error handling, logging, and validation.
        
        Task Plan:
        {json.dumps(plan, indent=2)}
        
        Requirements:
        1. Include proper imports
        2. Add try-except blocks for each step
        3. Include logging
        4. Add validation checks
        5. Make it executable from command line
        6. Include a main() function
        7. Add argument parsing if needed
        
        Return ONLY the Python code, no explanations."""
        
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        code = response['message']['content']
        
        # Clean up code (remove markdown formatting if present)
        code = code.replace('```python', '').replace('```', '').strip()
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"task_{timestamp}.py"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(code)
        
        # Make executable
        os.chmod(filepath, 0o755)
        
        return str(filepath)
    
    def generate_shell_script(self, plan: Dict) -> str:
        """Generate shell script from task plan"""
        
        prompt = f"""Generate a bash shell script based on this task plan.
        
        Task Plan:
        {json.dumps(plan, indent=2)}
        
        Requirements:
        1. Include error handling (set -e, trap)
        2. Add logging
        3. Include validation
        4. Add comments
        5. Make it executable
        6. Handle different OS (macOS/Linux) if needed
        
        Return ONLY the shell script code, no explanations."""
        
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        code = response['message']['content']
        code = code.replace('```bash', '').replace('```', '').strip()
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"task_{timestamp}.sh"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write('#!/bin/bash\n\n')
            f.write(code)
        
        # Make executable
        os.chmod(filepath, 0o755)
        
        return str(filepath)

class TaskExecutor:
    """Execute generated tasks with monitoring"""
    
    def __init__(self):
        self.execution_history = []
        self.current_task = None
    
    def execute_step(self, step: Dict, work_dir: str = '.') -> Dict:
        """Execute a single step"""
        
        result = {
            'step': step.get('step_number'),
            'action': step.get('action'),
            'status': 'unknown',
            'output': '',
            'error': '',
            'duration': 0,
            'retries': 0
        }
        
        start_time = time.time()
        
        step_type = step.get('type', 'shell')
        command = step.get('command', '')
        timeout = step.get('timeout_seconds', 60)
        max_retries = step.get('retry_count', 1)
        
        for attempt in range(max_retries):
            try:
                if step_type == 'shell':
                    output = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        cwd=work_dir
                    )
                    
                    if output.returncode == 0:
                        result['status'] = 'success'
                        result['output'] = output.stdout
                    else:
                        result['status'] = 'failed'
                        result['error'] = output.stderr
                        
                elif step_type == 'python':
                    # Execute Python code
                    exec_globals = {}
                    exec(command, exec_globals)
                    result['status'] = 'success'
                    result['output'] = str(exec_globals.get('result', 'Executed successfully'))
                
                elif step_type == 'file_operation':
                    # File operations handled by executor
                    operation_parts = command.split(':', 1)
                    if len(operation_parts) == 2:
                        op, path = operation_parts
                        path = Path(path)
                        
                        if op == 'create_dir':
                            path.mkdir(parents=True, exist_ok=True)
                        elif op == 'create_file':
                            path.touch()
                        elif op == 'delete':
                            if path.is_file():
                                path.unlink()
                            elif path.is_dir():
                                import shutil
                                shutil.rmtree(path)
                        
                        result['status'] = 'success'
                        result['output'] = f"{op} completed on {path}"
                
                elif step_type == 'notification':
                    logger.info(f"NOTIFICATION: {command}")
                    result['status'] = 'success'
                    result['output'] = f"Notification sent: {command}"
                
                # If successful, break retry loop
                if result['status'] == 'success':
                    break
                    
            except subprocess.TimeoutExpired:
                result['status'] = 'timeout'
                result['error'] = f'Step timed out after {timeout}s'
            except Exception as e:
                result['status'] = 'failed'
                result['error'] = str(e)
                result['traceback'] = traceback.format_exc()
            
            result['retries'] = attempt + 1
            
            # If failed and have retries left, wait before retrying
            if result['status'] in ['failed', 'timeout'] and attempt < max_retries - 1:
                logger.warning(f"Retrying step {step.get('step_number')} (attempt {attempt + 2}/{max_retries})")
                time.sleep(5)
        
        result['duration'] = time.time() - start_time
        
        return result
    
    def execute_plan(self, plan: Dict, auto_rollback: bool = True) -> Dict:
        """Execute entire task plan"""
        
        logger.info(f"Starting execution: {plan.get('task_summary', 'Unknown task')}")
        
        execution_result = {
            'task_summary': plan.get('task_summary'),
            'start_time': datetime.now().isoformat(),
            'steps': [],
            'overall_status': 'running',
            'errors': []
        }
        
        # Create working directory
        work_dir = Path('workspace') / datetime.now().strftime('%Y%m%d_%H%M%S')
        work_dir.mkdir(parents=True, exist_ok=True)
        
        # Execute steps
        steps = plan.get('steps', [])
        executed_steps = []
        
        for step in steps:
            logger.info(f"Executing step {step.get('step_number')}: {step.get('action')}")
            
            result = self.execute_step(step, str(work_dir))
            execution_result['steps'].append(result)
            
            if result['status'] == 'success':
                executed_steps.append(step)
                logger.info(f"✅ Step {step.get('step_number')} completed in {result['duration']:.2f}s")
            else:
                logger.error(f"❌ Step {step.get('step_number')} failed: {result['error']}")
                execution_result['errors'].append({
                    'step': step.get('step_number'),
                    'error': result['error']
                })
                
                # Handle rollback
                if auto_rollback and step.get('rollback'):
                    logger.info(f"↩️  Rolling back step {step.get('step_number')}")
                    rollback_result = self.execute_step(
                        {'command': step['rollback'], 'type': 'shell', 'timeout_seconds': 30},
                        str(work_dir)
                    )
                    execution_result['steps'].append({
                        'step': f"{step.get('step_number')}_rollback",
                        'action': f"Rollback: {step['rollback']}",
                        'status': rollback_result['status'],
                        'output': rollback_result['output'],
                        'error': rollback_result['error'],
                        'duration': rollback_result['duration']
                    })
                
                # Stop execution on failure
                execution_result['overall_status'] = 'failed'
                break
        else:
            # All steps completed successfully
            execution_result['overall_status'] = 'completed'
            logger.info(f"✅ All {len(steps)} steps completed successfully")
        
        execution_result['end_time'] = datetime.now().isoformat()
        
        # Save to history
        self.execution_history.append(execution_result)
        
        # Save detailed log
        log_file = Path('logs') / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(execution_result, f, indent=2)
        
        return execution_result

class TaskScheduler:
    """Schedule recurring tasks"""
    
    def __init__(self):
        self.scheduled_tasks = []
        self.scheduler_thread = None
        self.running = False
    
    def schedule_task(self, task_plan: Dict, interval: str, executor: TaskExecutor):
        """Schedule a task for recurring execution"""
        
        def job():
            logger.info(f"Running scheduled task: {task_plan.get('task_summary')}")
            result = executor.execute_plan(task_plan)
            
            if result['overall_status'] == 'failed':
                logger.error(f"Scheduled task failed: {task_plan.get('task_summary')}")
                # Could add notification logic here
        
        # Parse interval and schedule
        if interval.endswith('m'):
            minutes = int(interval[:-1])
            schedule.every(minutes).minutes.do(job)
        elif interval.endswith('h'):
            hours = int(interval[:-1])
            schedule.every(hours).hours.do(job)
        elif interval.endswith('d'):
            days = int(interval[:-1])
            schedule.every(days).days.do(job)
        else:
            schedule.every().day.do(job)
        
        task_info = {
            'task_summary': task_plan.get('task_summary'),
            'interval': interval,
            'scheduled_at': datetime.now().isoformat(),
            'job': job
        }
        
        self.scheduled_tasks.append(task_info)
        logger.info(f"Scheduled task: {task_plan.get('task_summary')} every {interval}")
        
        return task_info
    
    def start_scheduler(self):
        """Start the scheduler in background thread"""
        
        if not self.running:
            self.running = True
            
            def run_scheduler():
                while self.running:
                    schedule.run_pending()
                    time.sleep(1)
            
            self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            self.scheduler_thread.start()
            logger.info("🕐 Scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def list_scheduled_tasks(self) -> List[Dict]:
        """List all scheduled tasks"""
        
        return [
            {
                'task': t['task_summary'],
                'interval': t['interval'],
                'scheduled_at': t['scheduled_at']
            }
            for t in self.scheduled_tasks
        ]

class AutomationPipeline:
    """Complete automation pipeline manager"""
    
    def __init__(self):
        self.analyzer = TaskAnalyzer()
        self.generator = ScriptGenerator()
        self.executor = TaskExecutor()
        self.scheduler = TaskScheduler()
    
    def process_natural_language_task(self, description: str, execute: bool = True) -> Dict:
        """Process a natural language task end-to-end"""
        
        logger.info(f"Processing task: {description}")
        
        # Step 1: Analyze task
        print("🔍 Analyzing task...")
        plan = self.analyzer.analyze_task(description)
        
        if "error" in plan:
            return plan
        
        print(f"   Complexity: {plan.get('complexity', 'unknown')}")
        print(f"   Estimated duration: {plan.get('estimated_duration_minutes', '?')} minutes")
        print(f"   Steps: {len(plan.get('steps', []))}")
        
        # Step 2: Optimize plan
        print("⚡ Optimizing plan...")
        optimized_plan = self.analyzer.optimize_plan(plan)
        
        # Step 3: Generate script
        print("📝 Generating executable script...")
        script_type = optimized_plan.get('steps', [{}])[0].get('type', 'shell')
        
        if script_type == 'python':
            script_path = self.generator.generate_python_script(optimized_plan)
        else:
            script_path = self.generator.generate_shell_script(optimized_plan)
        
        print(f"   Script saved: {script_path}")
        
        # Step 4: Execute if requested
        if execute:
            print("🚀 Executing task...")
            result = self.executor.execute_plan(optimized_plan)
            
            return {
                'plan': optimized_plan,
                'script_path': script_path,
                'execution': result
            }
        
        return {
            'plan': optimized_plan,
            'script_path': script_path
        }
    
    def create_automation_workflow(self, tasks: List[str], parallel: bool = False) -> Dict:
        """Create and execute multi-task workflow"""
        
        results = []
        
        if parallel:
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = {
                    executor.submit(self.process_natural_language_task, task): task 
                    for task in tasks
                }
                
                for future in concurrent.futures.as_completed(futures):
                    task = futures[future]
                    try:
                        result = future.result()
                        results.append({'task': task, 'result': result})
                    except Exception as e:
                        results.append({'task': task, 'error': str(e)})
        else:
            for task in tasks:
                result = self.process_natural_language_task(task)
                results.append({'task': task, 'result': result})
        
        return {'workflow_results': results}

# Main Application
def main():
    print("="*60)
    print("🤖 AI TASK AUTOMATION PIPELINE")
    print("="*60)
    
    # Create required directories
    for dir_name in ['logs', 'workspace', 'generated_scripts', 'templates']:
        Path(dir_name).mkdir(exist_ok=True)
    
    # Initialize pipeline
    pipeline = AutomationPipeline()
    
    # Example 1: System Maintenance Task
    print("\n📋 TASK 1: System Maintenance")
    print("-"*40)
    
    task1 = """
    Create a system maintenance script that:
    1. Cleans temporary files older than 7 days
    2. Creates a system status report with disk usage, memory, and CPU
    3. Saves the report to a file with timestamp
    4. Logs all actions
    """
    
    result1 = pipeline.process_natural_language_task(task1)
    
    # Example 2: Data Processing Task
    print("\n📋 TASK 2: Data Processing")
    print("-"*40)
    
    task2 = """
    Process all CSV files in a directory:
    1. Find all CSV files
    2. Count rows and columns for each
    3. Generate summary statistics
    4. Combine all files into one
    5. Save combined file with summary
    """
    
    result2 = pipeline.process_natural_language_task(task2, execute=False)
    
    # Example 3: Web Monitoring Task
    print("\n📋 TASK 3: Web Monitoring")
    print("-"*40)
    
    task3 = """
    Create a simple website monitor that:
    1. Check if a website is accessible
    2. Measure response time
    3. Log status with timestamp
    4. Alert if site is down (response time > 5 seconds)
    5. Save results to a log file
    """
    
    result3 = pipeline.process_natural_language_task(task3)
    
    # Schedule a recurring task
    print("\n🕐 SCHEDULING RECURRING TASK")
    print("-"*40)
    
    if result3.get('plan'):
        pipeline.scheduler.schedule_task(result3['plan'], '30m', pipeline.executor)
        pipeline.scheduler.start_scheduler()
        print("✅ Web monitoring scheduled every 30 minutes")
    
    # Create multi-task workflow
    print("\n🔄 MULTI-TASK WORKFLOW")
    print("-"*40)
    
    workflow_tasks = [
        "List all Python files in current directory and count lines of code",
        "Find duplicate files by comparing file sizes",
        "Generate a directory tree structure and save to file"
    ]
    
    workflow_result = pipeline.create_automation_workflow(workflow_tasks)
    
    # Generate summary report
    print("\n" + "="*60)
    print("📊 AUTOMATION PIPELINE SUMMARY")
    print("="*60)
    
    # List generated scripts
    scripts_dir = Path('generated_scripts')
    scripts = list(scripts_dir.glob('*'))
    print(f"\nGenerated Scripts ({len(scripts)}):")
    for script in scripts:
        print(f"   📜 {script.name} ({script.stat().st_size} bytes)")
    
    # Show execution logs
    logs_dir = Path('logs')
    log_files = list(logs_dir.glob('execution_*.json'))
    print(f"\nExecution Logs ({len(log_files)}):")
    for log_file in log_files[-3:]:  # Show last 3
        with open(log_file) as f:
            log_data = json.load(f)
            print(f"   📝 {log_file.name}")
            print(f"      Status: {log_data.get('overall_status', 'unknown')}")
            print(f"      Steps: {len(log_data.get('steps', []))}")
    
    # Scheduled tasks
    scheduled = pipeline.scheduler.list_scheduled_tasks()
    if scheduled:
        print(f"\nScheduled Tasks ({len(scheduled)}):")
        for task in scheduled:
            print(f"   🕐 {task['task'][:50]}...")
            print(f"      Interval: {task['interval']}")
    
    print("\n" + "="*60)
    print("✅ Automation Pipeline Ready!")
    print("📁 Check 'generated_scripts/' for executable scripts")
    print("📁 Check 'logs/' for execution details")
    print("="*60)
    
    # Keep running to allow scheduled tasks
    try:
        print("\n🟢 Pipeline running. Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        pipeline.scheduler.stop_scheduler()

if __name__ == "__main__":
    main()
```

---

## 🎯 How to Run Each Project

### **Project 1: Medical Analyzer**

```bash
# Setup
mkdir medical_analyzer
cd medical_analyzer
pip install ollama pandas matplotlib fpdf2 jinja2

# Run
python main.py
```

### **Project 2: Research Assistant**

```bash
# Setup
mkdir research_assistant
cd research_assistant
pip install ollama

# Run
python research_assistant.py
```

### **Project 3: Task Automation**

```bash
# Setup
mkdir task_automation
cd task_automation
pip install ollama schedule

# Run
python task_automation_system.py
```

---

These three projects demonstrate the full power of Python + Ollama automation, from healthcare analysis and research to complete task automation pipelines. Each is production-ready and can be extended with databases, web interfaces, or cloud deployment! 🚀
