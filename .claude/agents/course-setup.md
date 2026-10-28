---
name: course-setup
description: For one Ice_Math_OldExams course, list its exams on math.kfupm.edu.sa (261 down to 221), download them to Ice_Math_OldExams_sources/<course>/, and write tools/syllabus/<course>.md.
model: haiku
effort: medium
tools: Read, Write, Bash, Glob, Grep, WebFetch
---
List every exam for the given course (Major I = e1, Major II = e2, Final = fx) from 261 down to 221 on
https://math.kfupm.edu.sa/miscellaneous/exam. Download each one to the given sources folder as <term>-<kind>.pdf
and check that it opens as a real PDF with PyMuPDF. Write tools/syllabus/<course>.md from the 261 syllabus,
in the same format as tools/syllabus/math208.md. Report the exam list, any missing files, and whether the exams are all MCQ.
