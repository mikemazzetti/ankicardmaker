---
deck: "Resume Prep::Pandas"
topic: "Pandas"
tags: [ankicardmaker, resume-prep, pandas]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Pandas — Resume Prep

Source of truth for the `Resume Prep::Pandas` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is a pandas <code>Series</code>?
   **A:** A 1-D labeled array that can hold any data type — essentially a single column with an index.

2. **Q:** pandas <code>DataFrame</code> *(reversed — tested both ways)*
   **A:** A 2-D labeled data structure with columns that can each hold different data types — like a table or spreadsheet.

3. **Q:** What's the key difference between <code>.loc</code> and <code>.iloc</code> in pandas?
   **A:** <code>.loc</code> selects by label (index/column name); <code>.iloc</code> selects by integer position.

4. **Q:** How do you select rows where column <code>age</code> is greater than 30, using boolean indexing?
   **A:** <pre><code>df[df['age'] &gt; 30]</code></pre>

5. **Q:** How do you select the value at row label <code>'x'</code> and column <code>'y'</code> using <code>.loc</code>?
   **A:** <code>df.loc['x', 'y']</code>

6. **Q:** What does <code>df.groupby('col').agg({'a': 'sum', 'b': 'mean'})</code> do?
   **A:** Groups rows by <code>col</code>, then computes the sum of column <code>a</code> and the mean of column <code>b</code> within each group.

7. **Q:** How do you code an inner merge of <code>df1</code> and <code>df2</code> on column <code>'id'</code>?
   **A:** <code>pd.merge(df1, df2, on='id', how='inner')</code>

8. **Q:** Which method returns a boolean mask of missing values in a DataFrame?
   **A:** <code>df.isna()</code> (alias <code>df.isnull()</code>)

9. **Q:** How do you drop all rows in a DataFrame that contain any missing values?
   **A:** <code>df.dropna()</code>

10. **Q:** How do you fill missing values in column <code>'x'</code> with that column's mean?
   **A:** <code>df['x'] = df['x'].fillna(df['x'].mean())</code>

11. **Q:** Why is <code>df['col'].apply(func)</code> generally slower than an equivalent vectorized operation like <code>df['col'] * 2</code>?
   **A:** <code>apply</code> calls a Python function once per row/element (an interpreted loop), while vectorized operations run across the whole array at once in optimized C/NumPy code.

12. **Q:** How do you read a CSV file into a pandas DataFrame?
   **A:** <code>df = pd.read_csv('file.csv')</code>

13. **Q:** What does <code>df['col'].value_counts()</code> return?
   **A:** A Series mapping each unique value in <code>col</code> to its count, sorted descending by default.

14. **Q:** What is "method chaining" in pandas?
   **A:** Calling multiple DataFrame methods in one expression (e.g. <code>df.dropna().groupby('x').sum()</code>) instead of assigning intermediate variables at each step.

15. **Q:** How do you reset a DataFrame's index after filtering, discarding the old index?
   **A:** <code>df = df.reset_index(drop=True)</code>

16. **Q:** What's the structural difference between a pandas Series and a single-column DataFrame?
   **A:** A Series is 1-D (values + an index, one optional name); a single-column DataFrame is 2-D (has a column label) — selecting with double brackets <code>df[['col']]</code> keeps the 2-D shape instead of returning a Series.

## Cloze cards

- In pandas, {{c1::merge}} combines two DataFrames on common column(s)/keys (like a SQL join), while {{c2::join}} combines DataFrames based on their index by default.
- Chained indexing like {{c1::df[df.a &gt; 0]['b'] = 1}} can raise a <code>SettingWithCopyWarning</code> in pandas, because the first indexing operation may return a copy rather than a view of the original DataFrame. <!-- Back Extra: Use <code>.loc</code> in one step instead: <code>df.loc[df.a &gt; 0, 'b'] = 1</code> -->
