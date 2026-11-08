# Glossary of GenAI Terms

Terms that appear in the [GenAI applications report](genai-applications-report.md),
explained **in my own words** with examples from my own experience.
The [term graph](term-graph.png) shows how often each term is used in the report and which terms appear together.

**Contents:**
[Generative AI](#1-generative-ai) ·
[LLM](#2-llm-large-language-model) ·
[Token](#3-token) ·
[Context Window](#4-context-window) ·
[Prompt](#5-prompt) ·
[Prompt Engineering](#6-prompt-engineering) ·
[Hallucination](#7-hallucination) ·
[RAG](#8-rag-retrieval-augmented-generation) ·
[Embedding](#9-embedding) ·
[Vector Database](#10-vector-database) ·
[Fine-tuning](#11-fine-tuning) ·
[Inference](#12-inference) ·
[AI Agent](#13-ai-agent) ·
[Agentic Workflow](#14-agentic-workflow) ·
[Tool Calling](#15-tool-calling) ·
[Copilot](#16-copilot) ·
[Multimodal Model](#17-multimodal-model) ·
[Guardrails](#18-guardrails) ·
[Prompt Injection](#19-prompt-injection) ·
[Human-in-the-Loop](#20-human-in-the-loop) ·
[AI-Native Tool](#21-ai-native-tool) ·
[Agentic Harness](#22-agentic-harness) ·
[Vibe Coding](#23-vibe-coding) ·
[Tokenomics](#24-tokenomics)

---

### 1. Generative AI

Generative AI is a type of artificial intelligence that can create new content, such as text, images,
videos, music, and even code.

*Example:* when I ask ChatGPT to write an email, explain a difficult topic, or help me with programming,
I'm using generative AI.

### 2. LLM (Large Language Model)

An LLM is an AI model trained on huge amounts of text so it can understand and generate human language.
Basically, it's the technology behind many AI chatbots.

*Example:* GPT is an LLM that can answer questions, write code, translate languages, and have
conversations with people.

### 3. Token

A token is a small piece of text that an AI model processes. It can be a word, part of a word, or even
a punctuation mark. One important thing is that one token doesn't always mean one word.

*Example:* when I send a message to ChatGPT, the model breaks it into tokens before processing it.

### 4. Context Window

A context window is the amount of information an AI model can work with at one time. A larger context
window means the AI can consider more information at once, but it doesn't guarantee that it will
remember every detail perfectly.

*Example:* if I upload a long document and ask questions about it, the model can only process the
information that fits into its context window.

### 5. Prompt

A prompt is simply an instruction or question that we give to an AI model. The more clearly I explain
what I want, the easier it is for the AI to give me a useful answer.

*Example:* "Write a motivation letter for my university application" is a prompt.

### 6. Prompt Engineering

Prompt engineering means writing better instructions to get better results from AI.

*Example:* instead of saying "Write my CV", I could say: "Create a professional CV for a Junior Machine
Learning Engineer. Focus on my Python skills, AI projects, and work experience." The second prompt gives
more details, so the AI has a better idea of what I need.

### 7. Hallucination

An AI hallucination happens when an AI model generates incorrect or completely made-up information and
presents it as if it were true. That's why I think it's important to double-check information,
especially when it comes to research, statistics, or important decisions.

*Example:* I might ask ChatGPT to recommend scientific papers, and it could give me the title of a paper
that doesn't actually exist.

### 8. RAG (Retrieval-Augmented Generation)

RAG is a method that allows AI to search for relevant information before generating an answer. Instead
of relying only on what the model learned during training, it can use information from documents,
databases, or other sources. This helps make the answers more accurate and relevant.

*Example:* imagine I create an AI assistant for a university. Students can ask questions about
scholarships, deadlines, or admission requirements, and the assistant searches the university's
documents before answering.

### 9. Embedding

An embedding is a way of converting information, such as text, into numbers that represent its meaning.
AI models use these numbers to understand how similar different pieces of information are.

*Example:* the sentences "How can I find a job?" and "Where can I look for employment?" have similar
meanings, even though they use different words. Embeddings help AI recognize that similarity.

### 10. Vector Database

A vector database is a database designed to store and search embeddings. It helps AI systems find
information based on meaning rather than just matching exact words. Popular examples include Pinecone,
Chroma, and Weaviate.

*Example:* if I build a chatbot with thousands of documents, a vector database can help it quickly find
the information most relevant to a user's question.

### 11. Fine-tuning

Fine-tuning means taking an AI model that has already been trained and training it further on a specific
dataset. The goal is to make the model better at a particular task. Instead of training a completely new
model from scratch, I improve an existing one.

*Example:* if I want an AI model to understand medical terminology or respond in a specific style, I could
fine-tune it using relevant examples.

### 12. Inference

Inference is the process of using an already trained AI model to generate an answer or make a prediction.
Training is when the model learns, while inference is when it uses what it has learned.

*Example:* when I type a question into ChatGPT and receive a response, the model is performing inference.

### 13. AI Agent

An AI agent is an AI system that can do more than just answer questions. It can make decisions, use
tools, and take actions to complete a task. The main idea is that the AI can take actions to achieve a
goal, rather than just provide information.

*Example:* instead of simply telling me how to organize my schedule, an AI agent could check my calendar,
find available time slots, and create events.

### 14. Agentic Workflow

An agentic workflow is a process where AI can decide what steps to take, use different tools, and adjust
its actions based on the results. Instead of following only one fixed instruction, the AI can choose its
next steps depending on what it finds.

*Example:* imagine I ask an AI system to research universities for my master's degree. It could search
for universities, compare admission requirements, check scholarship opportunities, and organize the
results into a table.

### 15. Tool Calling

Tool calling is when an AI model uses external tools or services to complete a task. The model doesn't
have to do everything by itself. It can use other tools when needed.

*Example:* ChatGPT might use a calculator to solve a mathematical problem, search the internet for
current information, or interact with an API.

### 16. Copilot

A copilot is an AI assistant that helps people complete tasks while they remain in control. The idea is
that AI works alongside a person instead of completely replacing them.

*Example:* GitHub Copilot helps developers write code by suggesting functions, completing lines, and
explaining programming concepts.

### 17. Multimodal Model

A multimodal model is an AI model that can work with different types of information, such as text,
images, audio, and video. Some multimodal models can also understand spoken questions, analyze videos,
or generate images. Basically, they aren't limited to text.

*Example:* I can upload a photo of a math problem and ask an AI model to explain how to solve it.

### 18. Guardrails

Guardrails are rules and safety mechanisms that help control how an AI system behaves. They can prevent
the AI from generating harmful content, sharing private information, or performing actions it shouldn't
perform. Guardrails don't make an AI system completely safe, but they help reduce risks.

*Example:* if I create an AI assistant for students, I might add guardrails to stop it from revealing
personal data or giving inappropriate advice.

### 19. Prompt Injection

Prompt injection is a type of attack where someone tries to manipulate an AI system by placing malicious
instructions inside content the AI reads. The danger is that the AI might treat those instructions as
something it should follow.

*Example:* imagine an AI assistant is reading a document to answer a question. Someone could hide
instructions inside that document telling the AI to ignore its original task and reveal confidential
information.

### 20. Human-in-the-Loop

Human-in-the-loop means that a real person is involved in checking, guiding, or approving an AI system's
decisions. I think this is especially important when AI is used in education, healthcare, recruitment,
or other areas where mistakes can seriously affect people.

*Example:* an AI model might evaluate job interview answers and suggest scores, but a human recruiter
reviews the results before making a final decision.

### 21. AI-Native Tool

An AI-native tool is a product that was designed around artificial intelligence from the beginning. AI
isn't just an extra feature added later. It's a central part of how the product works. Without AI, the
product would work very differently or lose much of its main functionality.

*Example:* an AI-native coding tool might allow users to describe what they want in natural language and
then help generate, edit, and debug the code.

### 22. Agentic Harness

An agentic harness is the system around an AI model that helps it work as an agent. It provides the
tools, instructions, memory, permissions, and environment the model needs to complete tasks. The AI
model is like the brain, while the harness provides the tools and structure that allow it to actually do
the work.

*Example:* if I want an AI coding agent to build an application, the harness might allow it to read
project files, edit code, run tests, and check errors.

### 23. Vibe Coding

Vibe coding is a way of building software by describing what you want to AI instead of writing all the
code yourself. It's a fast way to create prototypes and experiment with ideas. However, AI-generated code
can still contain bugs or security problems, so it needs to be tested and reviewed.

*Example:* I could tell an AI coding assistant: "Build me a website where students can create profiles,
upload their CVs, and apply for internships." The AI would generate code based on my instructions, and I
could keep asking it to make changes.

### 24. Tokenomics

In the context of AI, tokenomics refers to the costs and economics of using tokens in AI models. Many AI
services charge based on how many tokens we send to the model and how many tokens it generates in
response. Longer prompts, larger documents, and longer responses can increase expenses. Understanding
tokenomics helps developers build AI applications that are more cost-effective.

*Example:* if I build an AI chatbot that serves thousands of users, I need to think about how many tokens
each conversation uses and how much those conversations cost.

*Note:* the word "tokenomics" is commonly used in cryptocurrency, where it refers to the economic design
of digital tokens. In AI, people sometimes use it informally to discuss token usage and costs.
