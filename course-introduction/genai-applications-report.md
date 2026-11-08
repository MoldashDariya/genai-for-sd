# Generative AI Applications: Research Report

**Author:** Dariya Moldash
**Course:** Generative AI for Software Development 2026-2027 (TechOrda), Course Introduction

## Introduction

Generative AI (GenAI) is a class of models that produce new content (text, code, images, audio)
instead of only classifying or predicting a number. Most modern GenAI products are built on top of a
Large Language Model (LLM): a neural network trained on a huge amount of text that predicts the next
token of a sequence. Users control the model with a prompt, and the amount of text the model can
"see" at once is limited by its context window.

This report looks at eight areas where GenAI is already used in practice. Every use case is described
in two paragraphs: the first one explains what the solution does and its **business value**, the second
one covers the **technical challenges** and **weak points**. After that comes a short list of
**existing implementations** with a link and a one-sentence description.

| # | Use case | Main GenAI technique |
|---|---|---|
| 1 | [AI coding assistants](#1-ai-coding-assistants) | LLM + IDE integration (copilot) |
| 2 | [Autonomous coding agents](#2-autonomous-coding-agents) | AI agent + tool calling |
| 3 | [Customer support chatbots](#3-customer-support-chatbots) | RAG + guardrails |
| 4 | [Enterprise knowledge search](#4-enterprise-knowledge-search) | RAG + embeddings + vector database |
| 5 | [Automated software testing](#5-automated-software-testing) | LLM code generation |
| 6 | [Marketing and creative content](#6-marketing-and-creative-content) | Multimodal models |
| 7 | [Healthcare clinical documentation](#7-healthcare-clinical-documentation) | Speech-to-text + LLM summarization |
| 8 | [Personalized education](#8-personalized-education) | LLM tutor + prompt engineering |

---

## 1. AI coding assistants

An AI coding assistant is built into the IDE: it suggests the next lines of code, explains unfamiliar
code, writes documentation and answers questions about the project in a chat. This is the classic
copilot pattern, where the developer stays in control and the AI only proposes changes. **Business
value:** developers spend much less time on boilerplate, typical patterns and searching documentation;
new team members understand a large codebase faster because they can simply ask about it; routine work
such as unit tests, comments and simple refactoring is done in a consistent way.

**Technical challenges and weak points:** the model has to get the right part of the project into its
context window (the open file, related classes, project conventions), and big repositories do not fit
completely. Suggestions must appear in a fraction of a second, so inference has to be fast and cheap,
and the company must control data privacy because code is sent to an external model provider. The main
weakness is code that looks correct but calls functions that do not exist (hallucination) or hides
subtle bugs and security vulnerabilities; developers may also accept suggestions without reading them
("automation bias"), and quality is much lower for rare programming languages.

**Existing implementations:**
- [GitHub Copilot](https://github.com/features/copilot) — code completion, chat and code review inside VS Code, JetBrains IDEs and GitHub; students of this course get an educational licence.
- [Cursor](https://cursor.com) — an AI-native code editor (a fork of VS Code) where chat and multi-file edits are the main way of working.
- [Tabnine](https://www.tabnine.com) — a privacy-focused coding assistant that can run on the company's own servers.
- [Amazon Q Developer](https://aws.amazon.com/q/developer/) — the AWS assistant for writing code, upgrading Java versions and working with AWS services.

---

## 2. Autonomous coding agents

An AI agent goes a step further than a copilot: it receives a task in natural language ("fix this
failing test", "add an endpoint") and completes it by itself. It reads files, runs commands and tests,
looks at the results and repeats until the task is done. This is called an agentic workflow, and it is
possible because the model can use tools (tool calling); the program that runs the model in such a loop
and gives it access to files and the terminal is called an agentic harness. **Business value:** whole
tasks, not just single lines, are automated (bug fixes, migrations, dependency updates), an engineer can
run several tasks in parallel and act as a reviewer instead of a typist, and routine maintenance becomes
much cheaper. It also makes "vibe coding" possible: a person describes the desired result in natural
language and the agent writes all the code, so even non-programmers can build simple tools.

**Technical challenges and weak points:** the agent needs a safe sandbox because it executes real
commands; long tasks need planning and memory, because the context window fills up and old information
has to be summarised or dropped; and it is hard for the agent to decide when the task is really
finished. A small mistake early in the plan can grow into a large wrong change, and agents can be
manipulated through text in files or web pages they read (prompt injection). Running many steps costs
many tokens, so planning this cost (tokenomics) becomes a real part of the project budget, and a
human-in-the-loop review is still needed before the change is merged.

**Existing implementations:**
- [Claude Code](https://www.anthropic.com/claude-code) — an agentic coding tool from Anthropic that works in the terminal and IDE, edits files and runs commands.
- [OpenAI Codex](https://openai.com/codex/) — a coding agent that works in a cloud sandbox and in the CLI and can prepare pull requests.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — an open-source command-line agent from Google.
- [EPAM AI/Run CodeMie CLI](https://github.com/codemie-ai/codemie-code) — EPAM's open-source CLI that runs its own coding agent and manages other agents from one place; CodeMie is available to students of this course.

---

## 3. Customer support chatbots

A support chatbot answers customer questions 24/7: order status, refunds, how to use the product.
Modern bots do not follow fixed scripts: they find the answer in the company's help articles (RAG),
write it in natural language and hand the conversation to a person when they are not sure. **Business
value:** most simple requests are solved instantly without waiting in a queue, support costs drop while
human agents focus on complex and emotional cases, and support becomes available in many languages
without hiring a team for each one.

**Technical challenges and weak points:** answers must be based only on current company documents, so
the knowledge base has to be kept up to date and well indexed; the bot needs integrations with internal
systems (orders, payments, CRM) through APIs; and guardrails must prevent the bot from promising things
the company does not offer. When the bot invents a policy that does not exist, the company can be held
responsible for it. Customers get frustrated when the bot does not understand them and does not pass
them to a person, and personal data of customers goes through the model, which creates privacy risks.

**Existing implementations:**
- [Intercom Fin](https://fin.ai) — an AI agent for customer service that answers from the company's help center content.
- [Zendesk AI](https://www.zendesk.com/service/ai/) — AI agents and assistant features inside the Zendesk support platform.
- [Klarna AI assistant](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/) — a well-known case where the assistant handled two thirds of Klarna's customer service chats in its first month.

---

## 4. Enterprise knowledge search

Employees ask questions in natural language and get an answer collected from internal documents:
wikis, Confluence, SharePoint, tickets, e-mails. The documents are split into chunks, converted to
embeddings and stored in a vector database; for each question the system retrieves the most similar
chunks and gives them to the LLM. This is Retrieval-Augmented Generation (RAG), and it is usually
preferred over fine-tuning the model on company documents, because the index can be updated every day,
while retraining a model is slow and expensive. **Business value:** people spend less time searching for
information and asking colleagues, knowledge does not get lost when employees leave, and every answer
contains links to its sources, so it can be checked.

**Technical challenges and weak points:** access rights are critical, because a user must only see
answers built from documents they are allowed to read; the way documents are split and the choice of the
embedding model strongly affect quality; and the index must be updated whenever documents change. If the
retrieval step finds the wrong documents, the model confidently gives a wrong answer, old or
contradictory documents lead to outdated answers, and the cost of indexing and storage grows with the
amount of data.

**Existing implementations:**
- [Glean](https://www.glean.com) — an enterprise search and assistant platform that connects to many company tools.
- [Microsoft 365 Copilot](https://www.microsoft.com/microsoft-365/copilot) — an assistant in Word, Outlook, Teams and other apps that uses the user's company data.
- [Notion AI](https://www.notion.com/product/ai) — a Q&A and writing assistant over a team's Notion workspace.
- [EPAM AI DIAL](https://dialx.ai) — EPAM's open-source platform that gives access to different LLMs and lets companies build RAG applications on top of them.

---

## 5. Automated software testing

GenAI writes unit tests, generates test data, turns test cases written in plain English into automated
tests and explains why a test failed. **Business value:** test coverage grows for legacy code that had no
tests at all, QA engineers can describe tests in natural language instead of maintaining fragile
scripts, and CI/CD pipelines give faster feedback to the team.

**Technical challenges and weak points:** generated tests must really check the expected behaviour and
not just repeat what the current code does; they also have to compile and run, so the tool must
understand the build system and dependencies, and UI tests must survive changes of the page layout. The
model may write tests that always pass, which gives a false feeling of safety, and if the code already
has a bug, the generated test may "lock in" the wrong behaviour. Without review the test suite quickly
becomes large and hard to maintain.

**Existing implementations:**
- [Diffblue Cover](https://www.diffblue.com) — automatically writes Java unit tests for existing code.
- [Qodo](https://www.qodo.ai) — AI for code review and test generation in the IDE and in pull requests.
- [testRigor](https://testrigor.com) — end-to-end tests written in plain English and executed automatically.

---

## 6. Marketing and creative content

Multimodal models create texts, images, video and voice for advertising, social media, product
descriptions and design drafts. **Business value:** content is produced many times faster and in many
variants for A/B testing, messages can be personalised for different customer segments and languages,
and small companies get design and copywriting quality that used to be expensive.

**Technical challenges and weak points:** it is hard to keep a consistent brand style and voice across
thousands of generated pieces and to control the result precisely (layout, exact text on images,
product details), and image and video generation needs a lot of computing power. Copyright is still an
open question, both for the training data and for the ownership of generated content; the content often
looks generic and repetitive; and the risk of deepfakes and misleading content makes many companies
require labelling of AI-generated material.

**Existing implementations:**
- [Adobe Firefly](https://www.adobe.com/products/firefly.html) — image and video generation integrated into Photoshop and other Adobe tools.
- [Canva Magic Studio](https://www.canva.com/magic/) — a set of AI design and writing tools inside Canva.
- [Jasper](https://www.jasper.ai) — an AI platform for marketing texts with brand voice settings.
- [Midjourney](https://www.midjourney.com) — a popular image generation service.

---

## 7. Healthcare clinical documentation

During an appointment the system listens to the conversation between the doctor and the patient (with
consent), turns speech into text and writes a structured clinical note, which the doctor checks and
signs. **Business value:** doctors spend much less time on paperwork and more time with patients, burnout
of medical staff goes down, and medical records become more complete and standardised.

**Technical challenges and weak points:** medical terminology, accents and noisy rooms make speech
recognition difficult; medical data is protected by strict regulations (for example HIPAA in the USA and
GDPR in Europe); and the solution must integrate with electronic health record systems. A small error in
a medicine name or dose can harm the patient, and the model may add details that were never said, so the
doctor must always review the note. Because the cost of a mistake is so high, adoption is slow and the
legal risks are significant.

**Existing implementations:**
- [Microsoft Dragon Copilot](https://www.microsoft.com/en-us/health-solutions/clinical-workflow/dragon-copilot) — a clinical voice assistant (formerly Nuance DAX) that creates documentation from the conversation.
- [Abridge](https://www.abridge.com) — generates clinical notes from patient-doctor conversations.

---

## 8. Personalized education

An AI tutor explains topics, asks guiding questions, checks answers and adapts to the level of each
student. Good tutors are instructed through a carefully designed system prompt not to give the final
answer immediately, but to help the student think. **Business value:** every student gets something close
to a personal tutor at low cost, teachers save time on preparing materials and checking routine tasks,
and language learning becomes more interactive thanks to conversation practice at any time.

**Technical challenges and weak points:** prompt engineering and guardrails are needed so that the tutor
teaches instead of simply solving the task; explanations must be adapted to the age and knowledge level
of the student; and the data of children must be protected. Students can use GenAI to cheat instead of
learning, wrong explanations are dangerous because a student cannot easily notice them, and access to
devices and the internet is still unequal.

**Existing implementations:**
- [Khanmigo](https://www.khanmigo.ai) — Khan Academy's AI tutor and teaching assistant.
- [Duolingo Max](https://blog.duolingo.com/duolingo-max/) — a Duolingo subscription with "Explain My Answer" and role-play conversations powered by GenAI.

---

## Common patterns and conclusions

Looking at all eight use cases, the same ideas appear again and again:

1. **The LLM alone is not enough.** Useful products combine the model with company data (RAG),
   tools and integrations, and a good user interface.
2. **Hallucination is the main weakness everywhere.** Every serious product adds ways to reduce it:
   answers grounded in sources, links for checking, and a human who reviews important results.
3. **Data privacy and security are a must.** Code, customer data and medical records go through the
   model, and new attacks like prompt injection appear.
4. **The trend goes from assistants to agents.** First AI suggested text (copilot), now it completes
   whole tasks by itself, but a human-in-the-loop is still responsible for the result.

For software development this means that engineers need to learn not only how to use these tools,
but how to check their output and how to build reliable systems around them. These topics are the
next modules of this course.

See also: [Glossary of terms](glossary.md) · [Term relationship graph](term-graph.png)
