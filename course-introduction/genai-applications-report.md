# Generative AI Applications: Research Report

**Author:** Dariya Moldash
**Course:** Generative AI for Software Development 2026-2027 (TechOrda), Course Introduction

## Introduction

Generative AI (GenAI) is a class of models that produce new content (text, code, images, audio)
instead of only classifying or predicting a number. Most modern GenAI products are built on top of a
Large Language Model (LLM): a neural network trained on a huge amount of text that predicts the next
token of a sequence. Users control the model with a prompt, and the amount of text the model can
"see" at once is limited by its context window.

This report looks at eight areas where GenAI is already used in practice. For every use case it
describes the business value, the technical challenges, the weaknesses, and real products that
implement it.

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

An assistant built into the IDE that suggests the next lines of code, explains code, writes
documentation and answers questions about the project in a chat. This is the classic copilot
pattern: the developer stays in control, the AI only proposes changes.

**Business value**
- Developers spend less time on boilerplate, typical patterns and searching documentation.
- New team members understand an unfamiliar codebase faster, because they can ask questions about it.
- Consistent quality of routine work: unit tests, comments, simple refactoring.

**Technical challenges**
- The model must get the right part of the project into its context window: the open file,
  related classes, project conventions. Large repositories do not fit completely.
- Suggestions must appear in a fraction of a second, so the inference has to be fast and cheap.
- Code is sent to an external model provider, so the company has to control data privacy
  and licences.

**Weaknesses**
- The model sometimes produces code that looks correct but calls functions that do not exist
  (hallucination) or contains subtle bugs and security vulnerabilities.
- Developers may accept suggestions without reading them carefully ("automation bias").
- Quality depends on the language: popular languages work much better than rare ones.

**Examples**

| Name | Link | Description |
|---|---|---|
| GitHub Copilot | https://github.com/features/copilot | Code completion, chat and code review inside VS Code, JetBrains IDEs and GitHub. Students of this course get an educational licence. |
| Cursor | https://cursor.com | An AI-native code editor (a fork of VS Code) where chat and multi-file edits are the main way of working. |
| Tabnine | https://www.tabnine.com | A coding assistant that can run on the company's own servers, focused on privacy. |
| Amazon Q Developer | https://aws.amazon.com/q/developer/ | AWS assistant for writing code, upgrading Java versions and working with AWS services. |

---

## 2. Autonomous coding agents

A step further than a copilot: an AI agent receives a task in natural language ("fix this failing
test", "add an endpoint") and completes it by itself. It reads files, runs commands, runs tests,
looks at the results and repeats until the task is done. This is called an agentic workflow, and it
is possible because the model can use tools (tool calling).

**Business value**
- Whole tasks, not just single lines, are automated: bug fixes, migrations, dependency updates.
- An engineer can run several tasks in parallel and act as a reviewer instead of a typist.
- Routine maintenance work becomes much cheaper.

**Technical challenges**
- The agent needs a safe environment (sandbox), because it executes real commands.
- Long tasks require planning and memory: the context window fills up and old information has to be
  summarised or dropped.
- It is hard to evaluate the result automatically: the agent must know when the task is really finished.

**Weaknesses**
- A small mistake early in the plan can grow into a large wrong change.
- Agents can be manipulated through text in files or web pages they read (prompt injection).
- Running many steps costs many tokens, so complex tasks can be expensive.
- A human-in-the-loop review is still needed before the change is merged.

**Examples**

| Name | Link | Description |
|---|---|---|
| Claude Code | https://www.anthropic.com/claude-code | An agentic coding tool from Anthropic that works in the terminal and IDE, edits files and runs commands. |
| OpenAI Codex | https://openai.com/codex/ | A coding agent that works in a cloud sandbox and in the CLI, and can prepare pull requests. |
| Gemini CLI | https://github.com/google-gemini/gemini-cli | An open-source command-line agent from Google. |
| EPAM AI/Run CodeMie CLI | https://github.com/codemie-ai/codemie-code | EPAM's open-source CLI that runs its own coding agent and manages other agents (Claude Code, Codex, Gemini CLI) from one place; CodeMie is available to students of this course. |

---

## 3. Customer support chatbots

A chatbot answers customer questions 24/7: order status, refunds, how to use the product. Modern
bots do not use fixed scripts. They find the answer in the company's help articles (RAG) and write it
in natural language, and they hand the conversation to a person when they are not sure.

**Business value**
- Most simple requests are solved instantly, without waiting in a queue.
- Support costs drop, while human agents focus on complex and emotional cases.
- Support is available in many languages without hiring for each language.

**Technical challenges**
- Answers must be based only on current company documents, so the knowledge base has to be kept
  up to date and well indexed.
- Integration with internal systems (orders, payments, CRM) through APIs.
- Guardrails must prevent the bot from promising things the company does not offer.

**Weaknesses**
- When the bot invents a policy that does not exist, the company can be held responsible for it.
- Customers get frustrated when the bot does not understand them and does not pass them to a person.
- Personal data of customers goes through the model, which creates privacy risks.

**Examples**

| Name | Link | Description |
|---|---|---|
| Intercom Fin | https://fin.ai | An AI agent for customer service that answers from the company's help center content. |
| Zendesk AI | https://www.zendesk.com/service/ai/ | AI agents and assistant features inside the Zendesk support platform. |
| Klarna AI assistant | https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ | A well-known case: in its first month the assistant handled two thirds of Klarna's customer service chats. |

---

## 4. Enterprise knowledge search

Employees ask questions in natural language and get an answer collected from internal documents:
wikis, Confluence, SharePoint, tickets, e-mails. The documents are split into chunks, converted to
embeddings and stored in a vector database. For each question the system retrieves the most similar
chunks and gives them to the LLM. This is Retrieval-Augmented Generation (RAG). It is usually
preferred over fine-tuning the model on company documents, because the index can be updated every
day, while retraining a model is slow and expensive.

**Business value**
- People spend less time searching for information and asking colleagues.
- Knowledge does not get lost when employees leave.
- Answers contain links to sources, so they can be checked.

**Technical challenges**
- Access rights: a user must only see answers built from documents they are allowed to read.
- Choosing how to split documents and which embedding model to use strongly affects quality.
- The index has to be updated when documents change.

**Weaknesses**
- If the retrieval step finds the wrong documents, the model confidently gives a wrong answer.
- Old or contradictory documents lead to outdated answers.
- Costs of indexing and storage grow with the amount of data.

**Examples**

| Name | Link | Description |
|---|---|---|
| Glean | https://www.glean.com | An enterprise search and assistant platform that connects to many company tools. |
| Microsoft 365 Copilot | https://www.microsoft.com/microsoft-365/copilot | An assistant in Word, Outlook, Teams etc. that uses the user's company data. |
| Notion AI | https://www.notion.com/product/ai | Q&A and writing assistant over a team's Notion workspace. |
| EPAM AI DIAL | https://dialx.ai | EPAM's open-source platform that gives access to different LLMs and lets companies build RAG applications on top of them. |

---

## 5. Automated software testing

GenAI writes unit tests, generates test data, turns test cases written in plain English into
automated tests and explains why a test failed.

**Business value**
- Higher test coverage for legacy code that had no tests.
- QA engineers write tests in natural language instead of fragile scripts.
- Faster feedback in CI/CD pipelines.

**Technical challenges**
- Generated tests must really check behaviour and not just repeat what the current code does.
- Tests need to compile and run, so the tool must understand the build system and dependencies.
- UI tests must survive changes of the page layout.

**Weaknesses**
- The model may write tests that always pass, which gives a false feeling of safety.
- If the code has a bug, the generated test may "lock in" the wrong behaviour.
- Generated tests still need review, otherwise the test suite becomes large and hard to maintain.

**Examples**

| Name | Link | Description |
|---|---|---|
| Diffblue Cover | https://www.diffblue.com | Automatically writes Java unit tests for existing code. |
| Qodo | https://www.qodo.ai | AI for code review and test generation in the IDE and in pull requests. |
| testRigor | https://testrigor.com | End-to-end tests written in plain English and executed automatically. |

---

## 6. Marketing and creative content

Multimodal models create texts, images, video and voice for advertising, social media, product
descriptions and design drafts.

**Business value**
- Content is produced many times faster and in many variants for A/B testing.
- Personalised messages for different customer segments and languages.
- Small companies get access to design and copywriting quality that used to be expensive.

**Technical challenges**
- Keeping a consistent brand style and voice across thousands of generated pieces.
- Controlling the result precisely (layout, exact text on images, product details).
- Generating images and video needs a lot of computing power.

**Weaknesses**
- Copyright questions: training data and ownership of generated content.
- Generic, repetitive "AI-looking" content.
- Risk of deepfakes and misleading content, so many companies require labelling.

**Examples**

| Name | Link | Description |
|---|---|---|
| Adobe Firefly | https://www.adobe.com/products/firefly.html | Image and video generation integrated into Photoshop and other Adobe tools. |
| Canva Magic Studio | https://www.canva.com/magic/ | AI design and writing tools inside Canva. |
| Jasper | https://www.jasper.ai | An AI platform for marketing texts with brand voice settings. |
| Midjourney | https://www.midjourney.com | A popular image generation service. |

---

## 7. Healthcare clinical documentation

During an appointment the system listens to the conversation between the doctor and the patient
(with consent), turns speech into text and writes a structured clinical note. The doctor checks and
signs it.

**Business value**
- Doctors spend much less time on paperwork and more time with patients.
- Less burnout of medical staff.
- More complete and standardised medical records.

**Technical challenges**
- Medical terminology, accents and noisy rooms make speech recognition difficult.
- Strict regulations for medical data (for example HIPAA in the USA, GDPR in Europe).
- Integration with electronic health record systems.

**Weaknesses**
- A small error in a medicine name or dose can harm the patient, so the doctor must always
  review the note.
- The model may add details that were never said.
- High cost of mistakes means slow adoption and legal risks.

**Examples**

| Name | Link | Description |
|---|---|---|
| Microsoft Dragon Copilot | https://www.microsoft.com/en-us/health-solutions/clinical-workflow/dragon-copilot | Clinical voice assistant that creates documentation from the conversation (formerly Nuance DAX). |
| Abridge | https://www.abridge.com | Generates clinical notes from patient-doctor conversations. |

---

## 8. Personalized education

An AI tutor explains topics, asks guiding questions, checks answers and adapts to the level of each
student. Good tutors are instructed through a carefully designed system prompt not to give the final
answer immediately, but to help the student think.

**Business value**
- Every student gets something close to a personal tutor at low cost.
- Teachers save time on preparing materials and checking routine tasks.
- Learning languages becomes more interactive: conversation practice at any time.

**Technical challenges**
- Prompt engineering and guardrails so that the tutor teaches instead of just solving the task.
- Adapting explanations to age and knowledge level.
- Protecting the data of children.

**Weaknesses**
- Students can use GenAI to cheat instead of learning.
- Wrong explanations are dangerous, because a student cannot easily notice them.
- Unequal access to devices and internet.

**Examples**

| Name | Link | Description |
|---|---|---|
| Khanmigo | https://www.khanmigo.ai | Khan Academy's AI tutor and teaching assistant. |
| Duolingo Max | https://blog.duolingo.com/duolingo-max/ | Duolingo subscription with "Explain My Answer" and role-play conversations powered by GenAI. |

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
