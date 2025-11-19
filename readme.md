# CuriosityAI – Democratizing Learning

CuriosityAI is a learning companion that generates comprehensive, tailored educational content on any topic you choose. It adapts to your skill level, language preferences, and learning needs, making high-quality knowledge accessible to everyone.

## Demo

You can try a live demo of the project here:  
**[Demo Link](https://huggingface.co/spaces/sameerrawat07/curiosityAI)**

---

## Overview
Modern learners face an overwhelming abundance of information. Books, videos, courses, blogs—yet finding trustworthy, relevant, and properly structured resources remains difficult, especially outside one’s area of expertise.

CuriosityAI solves this by handling the heavy lifting: researching, structuring, and generating clear, user-friendly content tailored to your background. Whether you’re a beginner or an expert, CuriosityAI produces content that meets you where you are.

---

## Features (Proof of Concept)
The current POC implements a Streamlit-based web app capable of:

- Taking a topic, difficulty level (Beginner/Intermediate/Expert), and preferred language
- Generating a structured learning plan (5 sections: intro → conclusion)
- Writing each section via LLM calls
- Creating a cohesive final article from all sections
- Translating the article to the user’s chosen language

This is powered by a custom LangGraph workflow and Google Gemini models.

---

## System Workflow
1. **User Input**: Topic, competence level (Beginner/Intermediate/Expert), and language.
2. **Section Planning**: The system uses an LLM to generate 5 relevant sections.
3. **Section Generation**: Each section is written independently by the LLM.
4. **Compilation**: All sections are merged and rewritten into a cohesive article.
5. **Language Conversion**: The final article is translated if needed.

---

## Tech Stack
- **Python**
- **Streamlit** (web interface)
- **LangGraph** (workflow orchestration)
- **LangChain** (LLM abstractions)
- **Google Gemini** models
- **pydantic** for structured output
- **dotenv** for environment variable management

---

## Future Development
CuriosityAI aims to evolve into a full agentic learning system with:

### **Architectural Enhancements**
- Context-aware sequential writing (short-term memory)
- Integrated research tools (search, Wikipedia, arXiv)
- Evaluator–optimizer architecture with parallelism

### **Expanded Output Formats**
- Articles enriched with generated images
- Audiobooks & podcasts via TTS models
- 50-page book generation pipeline
- Short-form educational videos (YouTube Shorts style)

### **User Engagement Improvements**
- Interactive chat with generated content (text + audio)
- Save and revisit past learning sessions

---

## Research Questions
CuriosityAI also provides a foundation for studying how users learn via AI-generated content:

1. **Single-agent vs. multi-agent**: How does content quality degrade as token count increases for a single writer compared to multiple agents handling sections?
2. **Evaluator bounds**: How many optimization iterations maximize quality without diminishing returns?
3. **Format preferences**: Which content format is most/least preferred by users, and what does this imply about modern learning behavior?
4. **User interaction patterns**: What types of questions do users ask about generated content, and what does this reveal about AI-assisted learning?