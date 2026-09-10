---
deck: "Resume Prep::SQL"
topic: "SQL"
tags: [ankicardmaker, resume-prep, sql]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# SQL — Resume Prep

Source of truth for the `Resume Prep::SQL` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In query execution order, does <code>WHERE</code> filter rows before or after <code>GROUP BY</code> forms groups?
   **A:** Before — <code>WHERE</code> filters individual rows first, then the survivors are grouped by <code>GROUP BY</code>.

2. **Q:** Which SQL clause filters groups after aggregation, and why can't <code>WHERE</code> do this?
   **A:** <code>HAVING</code>. <code>WHERE</code> runs before grouping/aggregation, so it can't reference aggregate results like <code>COUNT(*)</code> or <code>SUM(x)</code>.

3. **Q:** INNER JOIN *(reversed — tested both ways)*
   **A:** Returns only rows that have matching values in both joined tables.

4. **Q:** LEFT JOIN *(reversed — tested both ways)*
   **A:** Returns all rows from the left table, plus matched rows from the right table (NULLs where there's no match).

5. **Q:** RIGHT JOIN *(reversed — tested both ways)*
   **A:** Returns all rows from the right table, plus matched rows from the left table (NULLs where there's no match).

6. **Q:** FULL OUTER JOIN *(reversed — tested both ways)*
   **A:** Returns all rows from both tables, with NULLs on whichever side has no match.

7. **Q:** Write a SQL query returning each customer_id and total order amount from <code>orders</code>, including only customers with more than 5 orders.
   **A:** <pre><code>SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING COUNT(*) &gt; 5;</code></pre>

8. **Q:** What distinguishes a correlated subquery from a regular (uncorrelated) subquery?
   **A:** A correlated subquery references columns from the outer query and is logically re-evaluated per outer row; a regular subquery runs once, independently of the outer query.

9. **Q:** Write a SQL query using a subquery to find employees earning more than their own department's average salary.
   **A:** <pre><code>SELECT e.name
FROM employees e
WHERE e.salary &gt; (
  SELECT AVG(salary) FROM employees e2
  WHERE e2.department_id = e.department_id
);</code></pre>

10. **Q:** What can a window function do that plain <code>GROUP BY</code> cannot?
   **A:** Compute an aggregate or ranking value per row while keeping every row in the result — <code>GROUP BY</code> collapses rows into one row per group.

11. **Q:** Write a SQL query using a window function to rank employees by salary within each department.
   **A:** <pre><code>SELECT name, department_id, salary,
  RANK() OVER (PARTITION BY department_id
               ORDER BY salary DESC) AS rnk
FROM employees;</code></pre>

12. **Q:** What's the key difference between DDL and DML?
   **A:** DDL defines or modifies the schema's structure (tables, columns, constraints); DML manipulates the data stored within that structure.

13. **Q:** Write SQL to insert a new row into <code>users</code> with columns id, username, created_at.
   **A:** <pre><code>INSERT INTO users (id, username, created_at)
VALUES (1, 'alice', NOW());</code></pre>

14. **Q:** Write SQL to update a user's email where id = 5.
   **A:** <pre><code>UPDATE users SET email = 'new@x.com'
WHERE id = 5;</code></pre>

15. **Q:** Write SQL to delete all orders older than 1 year.
   **A:** <pre><code>DELETE FROM orders
WHERE order_date &lt; NOW() - INTERVAL '1 year';</code></pre>

16. **Q:** Name three common SQL aggregate functions besides <code>COUNT</code>.
   **A:** <code>SUM</code>, <code>AVG</code>, and <code>MIN</code>/<code>MAX</code>.

17. **Q:** A Discord bot does CRUD against a SQL back-end. What SQL statement type handles a "delete this reminder" command?
   **A:** <code>DELETE</code> — a DML statement that removes the matching row(s).

## Cloze cards

- In SQL, the {{c1::GROUP BY}} clause groups rows that share a column value so aggregate functions can be applied per group.
- The core DDL statements are {{c1::CREATE}}, {{c2::ALTER}}, {{c3::DROP}}, and {{c4::TRUNCATE}}.
- The core DML statements are {{c1::SELECT}}, {{c2::INSERT}}, {{c3::UPDATE}}, and {{c4::DELETE}}.
