---
deck: "Resume Prep::ETL & Data Pipelines"
topic: "ETL & Data Pipelines"
tags: [ankicardmaker, resume-prep, etl]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# ETL & Data Pipelines — Resume Prep

Source of truth for the `Resume Prep::ETL & Data Pipelines` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** ETL *(reversed — tested both ways)*
   **A:** Extract, Transform, Load — data is pulled from sources, transformed to the target format, and then loaded into the destination system.

2. **Q:** How does ELT differ from ETL?
   **A:** In ELT, raw data is loaded into the target system (e.g. a warehouse/lake) first, and transformed afterward using the target's own compute — instead of transforming before loading.

3. **Q:** What happens in the "Extract" stage of ETL?
   **A:** Raw data is pulled from one or more source systems (databases, APIs, files, etc.) into a staging area, generally with minimal transformation.

4. **Q:** What happens in the "Transform" stage of ETL?
   **A:** Extracted data is cleaned, validated, reshaped, joined, and enriched into the schema/format the destination requires.

5. **Q:** What happens in the "Load" stage of ETL?
   **A:** The transformed data is written into the target system (e.g. data warehouse or database) for downstream use.

6. **Q:** What does it mean for an ETL pipeline step to be "idempotent"?
   **A:** Running it multiple times with the same input produces the same end result as running it once — no duplicate or corrupted data from retries or re-runs.

7. **Q:** Why is idempotency important for ETL pipelines?
   **A:** Failures and retries are common in pipelines; idempotent steps can be safely re-run after a failure without creating duplicates or inconsistent state.

8. **Q:** What's the difference between batch and streaming data processing?
   **A:** Batch processes data in discrete, scheduled chunks (e.g. hourly/daily); streaming processes data continuously, record-by-record or in micro-batches, as it arrives.

9. **Q:** What is an "incremental load" in ETL?
   **A:** Loading only new or changed data since the last run (e.g. via a timestamp or change-tracking column), instead of reprocessing the full dataset every time.

10. **Q:** Why prefer incremental loads over full reloads for large datasets?
   **A:** They're much faster and cheaper — less data to extract, transform, and load, and lower load placed on source systems — than reprocessing everything on every run.

11. **Q:** Name two common data quality checks run within an ETL pipeline.
   **A:** e.g. null/missing-value checks, schema/type validation, duplicate detection, and range or referential-integrity checks.

12. **Q:** What is Microsoft Fabric, at a high level?
   **A:** A unified, end-to-end SaaS analytics platform (built on OneLake) combining data engineering, data integration/ETL pipelines, data warehousing, and Power BI reporting in one workspace.

13. **Q:** In Microsoft Fabric, what is OneLake?
   **A:** A single, unified, tenant-wide data lake (built on ADLS Gen2) underlying all Fabric workloads, so data doesn't need to be copied between engines.

14. **Q:** What role does orchestration play in a data pipeline?
   **A:** It schedules and sequences pipeline jobs, manages dependencies between them, and handles retries/failure recovery (e.g. via Airflow or Fabric/Data Factory pipelines).

15. **Q:** In the COMPLIANCE360 project, what did the Python ETL pipeline on MS Fabric do?
   **A:** Extracted and transformed compliance-related data, applied custom scoring algorithms to it, and loaded the results for a React front-end to display.

16. **Q:** What is a "scoring algorithm", in the context of the COMPLIANCE360 ETL pipeline?
   **A:** Custom logic run in the Transform stage that computes a numeric compliance/risk score for each record based on defined rules or weighted criteria.

17. **Q:** How do you express an idempotent load step as an "upsert" (insert-or-update) instead of a plain insert?
   **A:** <pre><code>INSERT INTO target (id, val)
VALUES (1, 'x')
ON CONFLICT (id) DO UPDATE SET val = EXCLUDED.val;</code></pre>

## Cloze cards

- A well-known reliability property for pipeline transactions is {{c1::ACID}}: {{c2::Atomicity}}, {{c3::Consistency}}, {{c4::Isolation}}, and {{c5::Durability}}. <!-- Back Extra: Many big-data/streaming pipelines instead trade strict ACID guarantees for eventual consistency at scale. -->
