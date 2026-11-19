# Sci-Fi Story

**Task:** with any LLM, write a 50–70 word summary of a short sci-fi story ("Circuits and Companionship")
that covers the main characters, an accurate timeline, the setting and the key plot events.
The prompt must be no longer than 17 words (the story text is not counted).

**Score:** 100 / 100 (2nd attempt)

**Technique:** Directional Stimulus Prompting — the prompt gives the model hint keywords
(characters, place, date, theme) that steer the summary toward the required content.

## Submitted solution

**Prompt:** Summarize in 60 words. Hints: Eliza Chen, ARIA, stray dog, lab, May 2185, empathy.

**Story summary:** In 2185, renowned roboticist Dr. Eliza Chen works in her high-tech lab on ARIA, a human-like
cyborg assistant lacking emotional warmth. In May 2185, a stray dog wanders in; ARIA mimics it, strokes it and begins
to play. Witnessing this on May 12, Eliza realizes empathy comes from authentic connection and integrates real social
interactions into ARIA's programming. By the end of 2185, ARIA becomes an emotionally supportive companion.

## Attempts

| # | Prompt | Score | Reviewer comment |
|---|---|---|---|
| 1 | *Summarize this story in 50-70 words, including main characters, setting, chronological timeline, and key plot events:* | 60 | The prompt was counted as 19 words (over the limit), and no Directional Stimulus Prompting was used |
| 2 | *Summarize in 60 words. Hints: Eliza Chen, ARIA, stray dog, lab, May 2185, empathy.* | **100** | — |

Lesson: keep a clear margin below the word limit (the checker counts words differently, e.g. "50-70" or "Prompt:"),
and give the model hints instead of a list of requirements.
