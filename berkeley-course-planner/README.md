# Berkeley Course Planner

A Claude plugin that helps UC Berkeley undergraduates plan one semester. It checks which campus, college and major requirements you still have, researches course candidates for the ones you choose, and builds an Excel workbook with the evidence for each course.

**You make every choice.** The planner never picks courses for you, never proposes a "best" schedule, and never enrolls you in anything. It gathers the information and lays it out side by side; you decide.

> This is an independent student project. It is not affiliated with or endorsed by UC Berkeley. Requirements can change. Always confirm your plan with your adviser and the official [Berkeley Academic Guide](https://undergraduate.catalog.berkeley.edu/).

---

## What you get

An Excel workbook named like `Course_Plan_Spring2027_Physics.xlsx`, with three tabs:

| Tab | What it shows |
|---|---|
| **Candidates** | Course candidates in four sections: Breadth Courses, Major Requirements, Personally Intended Courses, Recommended DeCal Courses. Each row has the instructor, lecture time, units, a label, a review score, review notes, a grading summary, flags, and links to the sources. |
| **Requirements** | Your campus, college and major requirements, each marked Done, Remaining or Chosen option, with a source link. |
| **Run Info** | When and how the plan was made, the catalog year of the data used, and a list of every course that was left out, with the reason. |

There is a **Pick?** column: type `Y` next to the courses you want, and the **Units picked** cell at the top adds up their units for you.

### What the labels mean

Each candidate gets one label, always shown next to the numbers behind it:

| Label | Meaning |
|---|---|
| Recommended (reviews) | At least 3 recent, specific reviews, averaging 4.0/5 or higher |
| Below bar (reviews) | At least 3 recent, specific reviews, averaging below 4.0 |
| Recommended (grades) | Not enough reviews; at least 40% of students got an A+, A or A− (BerkeleyTime) |
| Below bar (grades) | Not enough reviews; under 40% got an A-range grade |
| No data | No usable reviews and no grade data |
| Interest match | A DeCal that matches the interests you gave (DeCals are P/NP, so they have no grade data) |

"Recent" means within the last 3 years. Reviews that contain only emotion ("worst class ever!!") are ignored; a review must say something about workload, exams or grading, lectures, course organization, or the instructor's availability. The full rules are in [`references/rubric.md`](plugin/skills/berkeley-course-planner/references/rubric.md).

A label is evidence, not advice. You can disagree with it using the same numbers.

---

## Requirements

- A Claude plan with **Cowork**. The planner is designed for the **Claude in Chrome side panel**, and it also works in the Claude desktop app.
- A browser the planner can use: Claude in Chrome, or the Claude desktop app's built-in browser. It reads the Berkeley Class Schedule, the Academic Guide, BerkeleyTime, RateMyProfessors and r/berkeley.
- Optional: a folder from your computer connected to the session, so the workbook can be saved there. Without one, you get it as a download in the chat.

---

## Install

1. Download [`dist/berkeley-course-planner.plugin`](dist/berkeley-course-planner.plugin) from this repository.
2. Open a Cowork session in the Claude desktop app and drag the `.plugin` file into the chat.
3. Click the install button on the plugin card.

Installed plugins also work in the Claude in Chrome side panel.

---

## How to use it

Start a conversation with something like:

- "Help me plan my Spring 2027 semester."
- "Which classes should I take next semester? I'm a Cognitive Science major."
- "I need two breadth courses and a DeCal."

The planner then walks through nine steps. At the three steps marked ★ it **stops and waits for your answer**:

1. **Intake.** It asks, in one message, for your intended major, the semester, your unit target, the credit you already have (a typed list, or your Academic Progress Report PDF from CalCentral), your interests (optional), any courses you already want (optional), and how many candidates per requirement to research (default 3).
2. **Requirements.** It reads your major's page in the Academic Guide and loads your college's rules.
3. ★ **Confirm.** It shows what you have done, what is left, and every place where your major or college lets you choose between options. You pick an option for each, or ask it to research all of them.
4. ★ **Choose slots.** It lists the requirements you could work on this semester. You choose which ones to research.
5. ★ **Cost check.** It tells you how big the research job is (about 6–8 page lookups per course) before it starts. You can cut it down.
6. **Find candidates** from the Class Schedule for that term.
7. **Evaluate** each candidate with the rules above.
8. **Build** the workbook.
9. **Hand-off.** A short summary: what was found, time conflicts, anything it couldn't confirm, and any courses it found but didn't research.

If you ask it to "just pick for me", it won't. It shows you the evidence again and offers to check any combination you name for time conflicts and total units.

**Tip for your unit target:** if you don't give one, the planner uses your college's minimum and tells you so. If you ask for more than your college's maximum, it tells you the limit and asks what you want to do. It never changes the number by itself.

---

## Good to know (current limitations)

- **Reviews are often unavailable.** RateMyProfessors frequently blocks automated browsers, and reddit.com is often reached only through Google search. When that happens, the row says "Reviews not checked" and the label comes from BerkeleyTime grade data instead.
- **Prerequisites are rarely shown** on the Class Schedule, so many rows carry a "Check prerequisite" flag. Check those yourself.
- **DeCals for a semester are usually posted near its start.** Before then, the planner uses last year's same-term DeCals and marks them "Not yet confirmed".
- **The requirements data is from the 2026–27 catalog**, collected in October 2026 and checked rule by rule against its sources. If you plan for a later catalog year, the planner warns you and asks whether to re-check the live pages.
- **The Haas School of Business publishes no per-semester unit maximum**, so for Haas students the planner asks instead of assuming one.
- Covered colleges: Letters & Science, Engineering, Chemistry, Rausser Natural Resources, Environmental Design, Computing Data Science & Society, Haas, and the School of Education.

---

## Privacy

- The planner only reads public pages. It never logs in anywhere, never fills in forms, and never touches CalCentral or enrollment.
- If you give it your Academic Progress Report, it is used only in your own Claude session.
- Your workbook stays in your session or your own folder. If a workbook with the same name already exists, it saves a new copy (`_2`, `_3`, …) instead of overwriting your marked-up file.

---

## Repository layout

```
plugin/                          the plugin
  .claude-plugin/plugin.json     manifest
  skills/berkeley-course-planner/
    SKILL.md                     the workflow and the "never decide" rules
    references/                  requirements data, rating rules, source guide
      campus.md, colleges/*.md   campus and college requirements, every rule sourced
      rubric.md                  how reviews and grades become labels
      sources.md                 where to look on each site and how to read it
    scripts/                     builds the Excel workbook (Python 3.10+, openpyxl, jsonschema)
dist/berkeley-course-planner.plugin   ready-to-install package
```

To update the requirements data, edit the files in `plugin/skills/berkeley-course-planner/references/colleges/`. Every rule must end with a `[src: https://…]` link to the page that states it, and each file records its catalog year and collection date.

---

## Feedback

Found a wrong requirement, a broken link, or a case the planner handles badly? Please open an issue, and include the source page if it's about a requirement.
