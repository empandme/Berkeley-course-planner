# Evaluation rubric

Read this whole file on every run. Use it to score every candidate row before you write `plan.json`.

One row = one course × one instructor in the target term. If the same course and instructor would fill two requirement slots, write one row and list the other slot in `also_satisfies`. A course the student named keeps its row in `sections.personal`, even when it also fills a slot the student picked: that slot goes in its `also_satisfies` (SKILL.md, Step 6).

A label is evidence, never a choice. Never choose or rank courses for the student. The numbers behind each label always sit next to it.

## Constants

```text
REVIEW_MEAN_MIN = 4.0
MIN_KEPT_REVIEWS = 3
RECENCY_YEARS = 3
A_RANGE_GENEROUS_PCT = 40
DEFAULT_CANDIDATES_PER_SLOT = 3
MAX_SITE_TRIES = 3
```

| Constant | Meaning |
|---|---|
| `REVIEW_MEAN_MIN` | Smallest mean of kept review ratings that counts as Recommended. |
| `MIN_KEPT_REVIEWS` | Fewest kept reviews needed before reviews decide the label. |
| `RECENCY_YEARS` | How far back a review may be dated. It also sets the grade-term window in section C (two terms per year). |
| `A_RANGE_GENEROUS_PCT` | Smallest A-range percentage that counts as Generous. |
| `DEFAULT_CANDIDATES_PER_SLOT` | Candidates per requirement slot when the student gives no number. |
| `MAX_SITE_TRIES` | Most attempts to reach one web page through Google. |

The run date is `run.date` in `plan.json`. The recency cutoff is the run date minus `RECENCY_YEARS` years, same month and day. A date on or after the cutoff is recent. A date before it is old.

`build_sheet.py` rejects a plan whose `label` or `grading` contradicts `REVIEW_MEAN_MIN`, `MIN_KEPT_REVIEWS` or `A_RANGE_GENEROUS_PCT`. Write each label last, from the numbers you stored.

## A. Instructor

1. Take the instructor from the target-term Class Schedule.
2. If the schedule shows "Staff" or TBA, or the target term's schedule is not published, use the instructor who most recently taught this course in the same term of an earlier year (for Spring 2027, the most recent Spring). Add the flag "Instructor unconfirmed" to the row.
3. If the target term's schedule is not published, also add the flag "Schedule unconfirmed".
4. If you find no earlier same-term instructor either, write "Staff" as the instructor, add "Instructor unconfirmed", and treat reviews as not checked: `reviews_kept` 0, `reviews_this_course` 0, `review_score` null, `rmp_url` null, flag "Reviews not checked". Write `review_notes` from Reddit comments about this course that pass the section B filter (put their URLs in `reddit_urls`), or "Not confirmed." if none do. Grades then use the course-wide tier in section C.

Use the instructor you settle on here for sections B and C.

## B. Reviews

### Sources

- RateMyProfessors (RMP): this instructor's UC Berkeley page. Reviews of any course this instructor teaches can count.
- r/berkeley: comments that are about this course, or about this instructor in any course. Reddit supplies notes and links only (`review_notes`, `reddit_urls`). It never changes `reviews_kept` or `review_score`.

### Filter every review

Apply three tests in order. Keep a review only if it passes all three. Stop at the first test it fails. You do not need a per-review record of these decisions. The only thing you write down is the borderline-drop note described below.

1. **Recent.** The review's date is on or after the cutoff (run date minus `RECENCY_YEARS` years). A date exactly on the cutoff passes. A review with no visible date fails.
2. **About this row.** Fail a review only if it is clearly about a different instructor's section of this course, or, for a Reddit comment, clearly about a different course taught by a different instructor. Everything else passes: any review on this instructor's RMP page (any course), and any Reddit comment about this course or about this instructor in any course. The source (RMP or Reddit) decides only where a kept review is used (RMP: score and counts; Reddit: notes and links). The source alone is never a reason to drop a review.
3. **Substance.** Keep the review if at least one statement in it makes a claim about one of these five categories:
   - **workload**: homework, reading, projects, time per week.
   - **exams or grading**: exam difficulty or format, curve, how grades are given.
   - **lecture clarity**: how well lectures can be followed.
   - **course organization**: syllabus, deadlines, structure, how the course is run.
   - **instructor availability**: office hours, replies to email.

   A bare verdict counts as a claim. Statements such as "workload is heavy", "exams were really hard" and "lectures are confusing" each pass, with no number or other detail needed.

   Drop a review only if none of its statements is a claim about one of the five categories. Drop it with the reason "no specific claim". These are not claims:
   - Emotion: "hated it", "loved it", "ruined my semester".
   - Praise or insult aimed at the person or the class as a whole: "amazing professor", "10/10", "worst professor ever".
   - Anything outside the five categories: humor, kindness, textbook cost, the room.
   - A personal result that says nothing about the course: "I got an A", "I barely passed".

   A mixed review stays if one statement is a claim about a category. Ignore the rest of it, and use only that statement in `review_notes`.

**When unsure, drop the review and note it.** This covers tests 1 and 3. Test 2 fails only when the review is clearly about someone else. Add a short phrase to `review_notes`, such as "Dropped 1 borderline review." Keep it short: `review_notes` is capped at 500 characters.

### Score and counts

- Take the mean of the RMP quality ratings of the kept RMP reviews. Recompute it yourself from the kept reviews. Never copy the average RMP shows, because it includes old reviews.
- Round the mean down to one decimal place (4.0 stays 4.0, 3.96 becomes 3.9), so rounding never lifts a score over `REVIEW_MEAN_MIN`. Store it as `review_score`.
- `reviews_kept` is the number of kept RMP reviews across all of this instructor's courses. `reviews_this_course` is how many of those are for this course. The sheet shows both, for example "7 reviews (3 this course)".
- With 0 kept reviews, `review_score` is null. With 1 or 2 kept reviews, still store `review_score` (the sheet shows it), but the label comes from grades (section D).
- `review_notes` holds at most 500 characters: one or two plain sentences on the kept claims, plus any Reddit comments that passed the filter (put their URLs in `reddit_urls`). If nothing was kept, write "No kept reviews."

## B′. RateMyProfessors failure

A try fails when the RMP page does not open, is blocked or shows an error, or turns out not to be this instructor at UC Berkeley. A page that opens but has no recent reviews is not a failure. Section B simply keeps 0 reviews.

1. Open a new tab. Search Google for `<instructor> RateMyProfessors UC Berkeley` (the instructor's full name). Open the RMP result.
2. If that fails, try again. Make at most `MAX_SITE_TRIES` tries in total, then stop. Do not look for other review sites.
3. If every try fails:
   - Write `review_notes` from Reddit (r/berkeley) comments that pass the section B filter, or write "Not confirmed." if none do. Put their URLs in `reddit_urls`.
   - Set `reviews_kept` and `reviews_this_course` to 0, `review_score` to null and `rmp_url` to null.
   - Add the flag "Reviews not checked".
   - The row has 0 kept reviews, so the grade rows of the section D table decide its label.

## C. Grades

Always fetch grades from BerkeleyTime for every row except DeCals, whatever happened in section B. Use the first tier that has data:

1. This instructor teaching this course in the six most recent Fall and Spring terms that ended before the run date (two per year of `RECENCY_YEARS`; Spring ends in May, Fall in December), plus any Summer terms between them. The terms in this tier are the terms in that window in which this instructor taught this course.
2. If none, this instructor teaching this course in any earlier term. Every term in which this instructor taught this course is then in this tier.
3. If none, the course-wide distribution across all instructors and all terms.

**A-range %.** A term's A-range % is A+ % + A % + A− % exactly as BerkeleyTime displays them for that term. Use only the letter-grade bars A+, A and A−. Ignore the P and NP bars and any other non-letter entry, so P/NP never counts. BerkeleyTime shows percentages, not student counts, so do not weight terms by class size. In tiers 1 and 2 (this instructor), the tier's A-range % is the unweighted mean of its terms' A-range % values: add the values and divide by the number of terms. Do not read these tiers from BerkeleyTime's "All Semesters" view: a combined view can weight larger terms more, and its result can differ from the mean near 40. In tier 3 (course-wide), use BerkeleyTime's combined view for all instructors and all semesters, and read A+ %, A % and A− % from it. Round down to one decimal place once, at the end (52.0 stays 52.0, 39.96 becomes 39.9, so it is Strict) and store it as `a_range_pct`, a number from 0 to 100.

**Grade data scope.** Write `grade_scope` as the tier, the first and last term used, and how the terms were combined:

- Several terms averaged: `instructor, Fall 2023–Spring 2026 (mean of 4 terms)`. The number is how many terms you averaged.
- One term: `instructor, Spring 2025 (1 term)`.
- Course-wide (tier 3, every term and all instructors): `course-wide (combined view)`.

If no tier has data, set `a_range_pct` to null, `grade_scope` to "No data" and `berkeleytime_url` to null.

If BerkeleyTime cannot be reached, retry through Google: make at most `MAX_SITE_TRIES` tries in total, each in a new tab with a Google search for `<COURSE> BerkeleyTime grades` (for example "PHYSICS 7B BerkeleyTime grades"). If every try fails, treat the row as having no grade data: `a_range_pct` null, `berkeleytime_url` null, `grade_scope` "Not confirmed", and add the flag "Not confirmed".

The grading text comes from the table in section D.

## D. Label

Decide the label from the stored numbers only. A DeCal row is a row in `sections.decal`. This includes a DeCal the student asked for by name: it goes in `sections.decal`, not `sections.personal`. A DeCal row is always "Interest match". For every other row, use the table row that fits `reviews_kept`, then the mean or the A-range.

| Kept reviews | Condition | Label |
|---|---|---|
| ≥ 3 | mean ≥ 4.0 | Recommended (reviews) |
| ≥ 3 | mean < 4.0 | Below bar (reviews) |
| < 3 | A-range ≥ 40% | Recommended (grades) |
| < 3 | A-range < 40% | Below bar (grades) |
| < 3 | no grade data | No data |
| — | DeCal row | Interest match |

Kept reviews means `reviews_kept`. The mean is `review_score`. The A-range is `a_range_pct`. Write the label text exactly as shown.

Grading text (the `grading` field):

| Situation | Grading |
|---|---|
| A-range ≥ 40 | Generous |
| A-range < 40 | Strict |
| DeCal row | P/NP |
| no grade data | No data |

Check each row before you write it: the label and the grading must agree with the numbers on the same row. `build_sheet.py` rejects any that do not, and names the field.

## E. DeCal rows

A DeCal row is a row in `sections.decal`. A DeCal the student asked for by name still goes in `sections.decal`, not `sections.personal`. Do not look up RMP or BerkeleyTime for a DeCal, and do not use the section D table. Facilitators are not on RMP, and DeCals are P/NP. Fill the row like this:

- `course_number`: the DeCal's Class Schedule course number and section, if the DeCal page or the Class Schedule shows them. Otherwise write `DeCal: <title>`, with the title as the DeCal list shows it.
- `instructor`: the facilitator names, if the DeCal page shows them. Otherwise write "Student facilitators".
- `review_notes`: r/berkeley comments that pass the three tests of section B (recency uses `RECENCY_YEARS`), or "Not confirmed." if none do. Put their URLs in `reddit_urls`.
- `reviews_kept` and `reviews_this_course` are 0, and `review_score`, `a_range_pct`, `rmp_url` and `berkeleytime_url` are null.
- `grading` is "P/NP", `grade_scope` is "P/NP course" and `label` is "Interest match".
- A row taken from last year's DeCal list gets the flag "Not yet confirmed".

## Keep/drop examples

Assumed run date: 2026-10-06 (cutoff 2023-10-06). The row being scored is Prof. Rivera's section. Each review text is invented.

| # | Review text | Date | Keep/Drop | Reason |
|---|---|---|---|---|
| 1 | "Problem sets every week, about 8 hours each. Start early." | 2025-11-02 | Keep | Workload: an amount (8 hours a week). |
| 2 | "Two midterms and a final, all multiple choice. Your final score replaces your lowest midterm." | 2025-04-20 | Keep | Exams or grading: a format and a replacement policy. |
| 3 | "He derives every formula on the board from scratch, so lectures were easy to follow even if you skipped the reading." | 2024-09-18 | Keep | Lecture clarity: a concrete behavior (derives on the board). |
| 4 | "Worst semester of my life, I cried twice and I regret everything. Office hours were four days a week though." | 2025-01-22 | Keep | Mixed: the emotion is ignored, and one claim passes (instructor availability: office hours four days a week). |
| 5 | "Worst professor ever. I hated every minute and this class ruined my semester." | 2025-12-09 | Drop | No specific claim: emotion and insult only, with no category content. |
| 6 | "Amazing professor, so inspiring! Best class I have taken here. 10/10." | 2026-05-01 | Drop | No specific claim: praise only. |
| 7 | "The final was cumulative and the median was a B-. Homework was 10% of the grade." | 2022-12-15 | Drop | Older than 3 years (before the 2023-10-06 cutoff), though it makes claims about exams or grading. |
| 8 | "Syllabus was posted before the first day, and no deadline moved all semester." | 2023-10-06 | Keep | Course organization: a concrete behavior. The date is exactly on the cutoff, so it is recent. |
| 9 | "I took this with Prof. Okafor, not Rivera. Okafor gave weekly quizzes and the exams were open-book." | 2025-10-10 | Drop | About a different instructor's section. |
| 10 | "Exams were really hard and the workload is heavy." | 2026-02-11 | Keep | Exams or grading and workload: a bare verdict on a category counts as a claim, with no number or detail needed. |
