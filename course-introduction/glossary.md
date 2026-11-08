# Glossary of GenAI Terms

Terms that appear in the [GenAI applications report](genai-applications-report.md),
explained in my own words. The [term graph](term-graph.html) shows how often each term is used
in the report and which terms appear together.

| # | Term | My explanation |
|---|---|---|
| 1 | **Generative AI (GenAI)** | AI that creates something new (text, code, pictures, sound) instead of only choosing a category or a number. It learns patterns from a lot of examples and then produces content that follows these patterns. |
| 2 | **Large Language Model (LLM)** | A very big neural network trained on huge amounts of text. Its main skill is to guess the next piece of text, and from this simple skill it learns to answer questions, write code and translate. |
| 3 | **Token** | The small piece of text a model works with: a word, part of a word or a symbol. Models read and write tokens, and the price and limits of a model are counted in tokens. |
| 4 | **Context window** | The "short-term memory" of a model: the maximum number of tokens it can look at in one request (instructions, documents, chat history and the answer together). What does not fit is simply not seen. |
| 5 | **Prompt** | The text we give to the model to tell it what to do: a question, an instruction, examples, data. A system prompt is a hidden prompt that sets the role and rules of an assistant. |
| 6 | **Prompt engineering** | The skill of writing prompts so that the model gives a better and more predictable result: clear instructions, examples, the needed format, step-by-step reasoning. |
| 7 | **Hallucination** | When a model confidently says something false or invented, for example a function, a fact or a link that does not exist. It happens because the model generates likely text, not checked facts. |
| 8 | **Retrieval-Augmented Generation (RAG)** | A way to give the model fresh or private knowledge: first search the documents for relevant pieces, then put them into the prompt and ask the model to answer only from them. |
| 9 | **Embedding** | A list of numbers that represents the meaning of a text. Texts with similar meaning get similar numbers, so the computer can find "similar by meaning", not only by exact words. |
| 10 | **Vector database** | A database that stores embeddings and can quickly find the ones closest to a query. It is the search part of most RAG systems. |
| 11 | **Fine-tuning** | Additional training of an already trained model on a smaller special dataset, so that it gets better at one task, style or domain. |
| 12 | **Inference** | Using an already trained model to get an answer. Training happens once and is very expensive; inference happens on every request and must be fast and cheap. |
| 13 | **AI agent** | A program where an LLM does not only answer but decides what to do next: makes a plan, uses tools, looks at the results and continues until the goal is reached. |
| 14 | **Agentic workflow** | A process where one or several AI agents complete a task in many steps (plan → act → check → repeat) instead of giving one answer. |
| 15 | **Tool calling** | The ability of a model to ask the application to run a function for it (search, run a command, call an API) and then use the result. This is how agents act in the real world. |
| 16 | **Copilot** | An AI assistant built into an existing tool (IDE, office apps) that suggests and helps, while the person stays in control and decides what to accept. |
| 17 | **Multimodal model** | A model that works with several kinds of data at once, for example text and images, or text, audio and video. |
| 18 | **Guardrails** | Rules and checks around a model that keep it safe and on-topic: filters for input and output, limits on what it may do, checks of the answer before it is shown. |
| 19 | **Prompt injection** | An attack where hidden or malicious instructions are placed in text the model reads (a web page, a document, an e-mail) to make it ignore its rules or do something harmful. |
| 20 | **Human-in-the-loop** | A design where a person checks or approves the AI's result at important points, for example reviews generated code before merge or a doctor signs a generated note. |
