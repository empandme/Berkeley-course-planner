# Sources

Where to look, and how to read the fields, for the six sites. How to judge what you find is in `rubric.md`.

Collected 2026-10-07. Catalog year: 2026-2027 (shown on the catalog home page). Browse read-only: do not sign in, submit a form or accept terms on any site. Every URL below is a pattern; the part in angle brackets changes per course, term or person.

## Catalog

URL pattern: `https://undergraduate.catalog.berkeley.edu/programs?page=1&pq=<MAJOR>`

Example: `https://undergraduate.catalog.berkeley.edu/programs/25666U/requirements-krhha` (Physics, Bachelor of Arts)

How to use:
- The search results list each program as "Name, Degree" (for example "Physics Bachelor of Arts" and "Physics Minor"). Take the Major with the right degree. The page uses an opaque program id (`25666U`), so never guess it. The program list opens at `https://undergraduate.catalog.berkeley.edu/programs`.
- Open the result, then click the Requirements tab. Its address ends in a random suffix (`requirements-krhha`). Typing `/requirements` without the suffix lands on Overview.
- Under "Program Requirements", read the groups (Lower Division, Upper Division). Each group shows its rule text ("Complete at least 1 of the following Courses", "A minimum grade of C- is required") followed by course codes with titles (written without a space, for example `PHYSICS7B`). Notes under a group (for example about substitutions) apply to that group.
- "University Requirements" and "College Requirements" show requirement-set names only, collapsed. Course lists are not on that page.
- The page shows no catalog year. The year is on the catalog home page.

Verified: 2026-10-07 (built-in browser)

## Class Schedule

URL pattern: `https://classes.berkeley.edu/search/class?search=<SUBJECT>+<NUMBER>&f[]=term:<TERM_ID>`

Example: `https://classes.berkeley.edu/search/class?search=physics+7b&f[]=term:8589`

Spring 2027 status on 2026-10-07: posted

That status is a dated snapshot, so check it live on every run. A term that is not posted should show as missing from the term list on `https://classes.berkeley.edu/`, or as a search with that term filter that returns zero classes (not seen on this run).

How to use:
- Term ids are links in the left filter list on `https://classes.berkeley.edu/`. Seen: Spring 2027 = 8589, Fall 2026 = 8588, Spring 2026 = 8576, Fall 2025 = 8573. Summer terms sit between them, so read the id from the list and do not compute it.
- The search is a fuzzy keyword search ("physics 7b" returned 189 items). Look for the headings that name your course exactly, such as "Spring 2027 PHYSICS 7B 001 - LEC 001". The exact course's sections come first. Skip the rest.
- Each section card shows, in order: course title, instructor (one or more names, comma-separated; no name line when none is assigned), start and end dates, days (`Mo, We, Fr`), time (`01:00 pm - 01:59 pm`), room, `Class #`, `Units:`, instruction mode and open seats.
- Click the section heading to open `https://classes.berkeley.edu/content/<YEAR>-<season>-<subject>-<number>-<section>-lec-<section>` (lowercase). That page adds Class Notes (for example exam dates), "Requirements Class Fulfills" (for example "Meets Physical Science, L&S Breadth") and the associated lab and discussion sections.
- For an earlier year, use the same URL with the older term id.
- Seen on 2026-10-07: PHYSICS 7B 001 LEC 001 in Spring 2027 shows instructor Ronnie Spitzer, Mo We Fr 01:00 pm - 01:59 pm, Pimentel 1, 4 units, Class #22216.

Verified: 2026-10-07 (built-in browser)

## BerkeleyTime

URL pattern: `https://berkeleytime.com/grades?input=<SUBJECT>%3B<COURSE_ID>%3BP%3B<FIRST>%3A<LAST>`

Example: `https://berkeleytime.com/grades?input=PHYSICS%3B118492%3BP%3BRonnie%3ASpitzer` (PHYSICS 7B, Ronnie Spitzer, all semesters)

Other forms seen: each chart series is one `input=` value, and several join with `&input=`. Add `%3B<YEAR>%3A<SEASON>%3A1` for one term (`...%3BP%3BRonnie%3ASpitzer%3B2024%3ASpring%3A1` reloaded fine). Drop the instructor part for all instructors in all semesters, BerkeleyTime's combined view (`input=ASTRON%3B123924`).

How to use:
- `<COURSE_ID>` is an internal number (118492 is PHYSICS 7B), so build the link with the page. Open `https://berkeleytime.com/grades`, choose Class, then Instructor (or "All Instructors"), then Semester ("All Semesters" or one term), then click "Add class". The address bar now holds the link.
- The Instructor list holds only people who taught the course, and the Semester list holds only that person's terms (Ronnie Spitzer: Spring 2024, Spring 2023, Summer 2022).
- Each "Add class" adds a card (for example "Spring 2024 • Ronnie Spitzer") and a chart series. For one value per term, add each term as its own series. "All Semesters" is one series covering every term of that selection. `rubric.md` section C says which view to use for which tier.
- Read A+, A and A− by hovering those three bars. The tooltip shows "Grade: A" and one entry per series (percentage and percentile range) in card order. It repeats the course name and does not name the term. PHYSICS 7B, Spitzer, Spring 2024 read A+ 3.9%, A 15.0%, A− 11.2%.
- P/NP is already left out of the letter percentages: on ASTRON C10 the bars A+ through F add up to about 100%, and the P and NP bars are extra. The "Show P/NP" switch only hides or shows those two bars.
- The page shows percentages only, no student counts.

Verified: 2026-10-07 (built-in browser)

## RateMyProfessors

URL pattern: `https://www.ratemyprofessors.com/search/professors/1072?q=<NAME>`

Example: `https://www.ratemyprofessors.com/search/professors/1072?q=Spitzer` (loaded once on 2026-10-07 and showed no UC Berkeley match for "Spitzer")

Professor page: `https://www.ratemyprofessors.com/professor/<PROFESSOR_ID>` (found through Google; for example `https://www.ratemyprofessors.com/professor/253566` is William Golightly at UC Berkeley)

How to use:
- `1072` is UC Berkeley: the page title reads "Search professors at University of California Berkeley". `<NAME>` is a last name or a full name.
- The search page opens with a banner such as `No professors with "Spitzer" in their name at University of California Berkeley` and, under it, matches at other schools. Count a row only if its School line is University of California Berkeley.
- Each row shows: Quality (for example 2.2) with the number of ratings, the name, the department, the school, "would take again" and "level of difficulty".
- The professor page is where the individual reviews are. I could not open one on this run, so its layout is not recorded here. Read each review's date, quality rating and course code directly from the page when you reach it.
- A Google search for `William Golightly RateMyProfessors UC Berkeley` returned the professor link above as its first result.

Verified: 2026-10-07 (pattern only — page blocked: the search page loaded once in the built-in browser, then it and professor page 253566 showed "Something went wrong" in the built-in browser and in Chrome, and WebFetch was refused by robots.txt). When a page does this, follow the retry procedure in `rubric.md` section B′.

## r/berkeley

URL pattern: `https://www.reddit.com/r/berkeley/search/?q=<QUERY>&restrict_sr=1&sort=new`

Google route: `https://www.google.com/search?q=site%3Areddit.com%2Fr%2Fberkeley+<QUERY>`

How to use:
- Search the course (`PHYSICS 7B`) and the instructor's full name as separate queries. `restrict_sr=1` keeps results inside r/berkeley and `sort=new` puts recent threads first. The thread and comment layout was not seen on this run.
- reddit.com is refused here (see Verified), so use the Google route. Each result shows the thread title ("Physics 7B : r/berkeley"), "Reddit · r/berkeley", a comment count, an age ("5 comments · 2 years ago") and a text snippet. Apply `rubric.md` section B to the snippet text.
- For `reddit_urls`, use the thread URL that the Google result points to. The tool I used masked those links. If you can't get the thread URL, use the URL of the Google search that found the comment, so every entry is a full URL. Never write the short address the result displays (`www.reddit.com › r › berkeley › ...`): it is not a URL.
- An age such as "2 years ago" is coarse. When it sits near the 3-year cutoff, the "When unsure, drop the review and note it" rule in `rubric.md` section B applies.
- If the Google route yields nothing usable, treat Reddit as having no usable comments: the rubric's "Not confirmed." path.

Verified: 2026-10-07 (pattern only — page blocked: reddit.com was refused by the built-in browser and by Claude in Chrome with "not allowed due to safety restrictions", and by WebFetch as a blocked site; the Google route loaded).

## DeCal

URL pattern: `https://berkeleydecal.com/courses`

Example: `https://berkeleydecal.com/courses` (`https://decal.berkeley.edu/` redirects to `https://berkeleydecal.com/`)

Spring 2027 list on 2026-10-07: not yet posted. The Semester menu offers only Fall 2026 (selected by default) and Spring 2026.

How to use:
- Choose the term in the Semester menu. The address does not change when you do.
- Each course card shows: a category tag (Health, Cultural, Political/Social, Media, Publication, Professional/Business, Environment or Food), an enrollment status (Open, Waitlist or Full), the title, "Department • N units", and the sections with day, time and room.
- "View Details →" opens a window on the same page (the address does not change) with the term and department, "Course Details" (the description and often a website), "Enrollment Information" and "Course Sections".
- The left side has a search box and filters for Category, Units (1, 2 or 3) and Enrollment Status.

Verified: 2026-10-07 (built-in browser)
