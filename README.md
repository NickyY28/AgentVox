# AgentVox

> Adaptive Multi-Agent Voice AI Interview Platform

AgentVox is an AI-powered voice interview platform that conducts adaptive, evidence-based interviews through real-time conversation.

Unlike traditional interview systems that rely on fixed questions and surface-level signals, AgentVox adapts its questions based on the User's responses and evaluates candidates using job-relevant evidence.

## ✨ Core Idea

AgentVox follows an adaptive interview loop:

**Claim → Probe → Evidence → Reasoning → Evaluate**

The system analyzes the User's resume and target role, creates a competency-focused interview plan, conducts the interview through real-time voice, and dynamically generates follow-up questions when additional evidence is required.

## 🏗️ Architecture

[AgentVox Architecture![](https://app.eraser.io/workspace/unPKG2Byju4M0NN4cnBq/preview?diagram=H4JoyEwSe7BSmzUtf6XQk&type=embed)](https://app.eraser.io/workspace/unPKG2Byju4M0NN4cnBq?diagram=H4JoyEwSe7BSmzUtf6XQk)

## 🚀 Key Features

- 🎙️ Real-time voice interviews
- 📄 Resume-based interview context
- 💼 Job description / target-role analysis
- 🧠 Adaptive interview questioning
- 🔍 Claim and evidence detection
- 💡 Reasoning analysis
- 📊 Competency-based evaluation
- 🎯 Confidence-aware assessment
- 🔄 Dynamic follow-up questions
- 📝 Evidence-based interview feedback
- 🔎 Semantic retrieval using vector embeddings

## 🔄 Interview Flow

```text
Resume + Target Role
        ↓
Context Analysis
        ↓
Competency Mapping
        ↓
Interview Planning
        ↓
Real-Time Voice Interview
        ↓
Candidate Response
        ↓
Claim Detection
        ↓
Evidence Extraction
        ↓
Reasoning Analysis
        ↓
Evidence Check
     ↙       ↘
Insufficient  Sufficient
    ↓             ↓
Follow-up      Evaluation
    ↓             ↓
    └──────→ Next Question
                  ↓
            Final Feedback
```
