---
deck: "Resume Prep::PySpark"
topic: "PySpark"
tags: [ankicardmaker, resume-prep, pyspark]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# PySpark — Resume Prep

Source of truth for the `Resume Prep::PySpark` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** RDD (Spark) *(reversed — tested both ways)*
   **A:** Resilient Distributed Dataset — Spark's low-level, immutable collection of objects partitioned and distributed across a cluster.

2. **Q:** Why do most PySpark applications prefer DataFrames over raw RDDs?
   **A:** DataFrames carry a schema and run through Spark's Catalyst optimizer and Tungsten execution engine, giving much better performance than RDDs' unoptimized, low-level operations.

3. **Q:** What does "lazy evaluation" mean in Spark?
   **A:** Spark builds up a logical execution plan from transformations but doesn't actually run any computation until an action is called.

4. **Q:** Give two examples of Spark transformations.
   **A:** e.g. <code>filter()</code>, <code>select()</code>, <code>withColumn()</code>, <code>groupBy()</code> — each returns a new DataFrame/RDD lazily, without triggering computation.

5. **Q:** Give two examples of Spark actions.
   **A:** e.g. <code>collect()</code>, <code>count()</code>, <code>show()</code>, <code>write()</code> — these trigger execution of the accumulated transformation plan.

6. **Q:** What is a "partition" in Spark?
   **A:** A chunk of a distributed dataset that lives on one node/executor; Spark processes partitions in parallel as its basic unit of parallelism.

7. **Q:** How do you filter a Spark DataFrame for rows where <code>age &gt; 30</code> and select just <code>name</code> and <code>age</code>?
   **A:** <code>df.filter(df.age &gt; 30).select('name', 'age')</code>

8. **Q:** How do you add a new column <code>bonus</code> equal to <code>salary * 0.1</code> on a Spark DataFrame?
   **A:** <code>df = df.withColumn('bonus', df.salary * 0.1)</code>

9. **Q:** How do you group a Spark DataFrame by <code>dept</code> and compute the average <code>salary</code> per group?
   **A:** <code>df.groupBy('dept').agg(avg('salary'))</code>

10. **Q:** What is a "shuffle" in Spark, and why is it expensive?
   **A:** Redistributing data across partitions/nodes over the network (needed for operations like <code>groupBy</code>, joins, or <code>repartition</code>) — expensive due to network I/O, disk spills, and serialization.

11. **Q:** Name three Spark operations that typically trigger a shuffle.
   **A:** <code>groupBy</code>, joins, <code>distinct</code>, <code>repartition</code>, and <code>orderBy</code>/<code>sortBy</code>.

12. **Q:** How do you run a SQL query against a Spark DataFrame?
   **A:** <pre><code>df.createOrReplaceTempView('t')
spark.sql('SELECT * FROM t WHERE age &gt; 30')</code></pre>

13. **Q:** Why use Spark instead of pandas for big data processing?
   **A:** Spark distributes both data and computation across a cluster of machines, so it can handle datasets far larger than one machine's memory — pandas runs single-node, in-memory only.

14. **Q:** How does <code>df.repartition(n)</code> differ from <code>df.coalesce(n)</code>?
   **A:** <code>repartition(n)</code> does a full shuffle to produce exactly n partitions (can increase or decrease count); <code>coalesce(n)</code> merges existing partitions without a full shuffle, so it's cheaper but can only decrease the count.

15. **Q:** If all Spark transformations are lazy, what actually triggers execution?
   **A:** Calling an action, e.g. <code>.collect()</code>, <code>.count()</code>, <code>.show()</code>, or <code>.write()</code>.

16. **Q:** What does <code>df.cache()</code> (or <code>.persist()</code>) do, and when is it useful?
   **A:** It materializes the DataFrame/RDD and keeps it in memory (or memory+disk) after the first computation, avoiding recomputation when the same DataFrame is reused across multiple actions.

17. **Q:** In Spark SQL, what is the Catalyst optimizer responsible for?
   **A:** Analyzing and rewriting logical query plans — predicate pushdown, column pruning, join reordering, etc. — into an efficient physical execution plan.

## Cloze cards

- Spark builds a {{c1::DAG (directed acyclic graph)}} of stages from a chain of transformations, then schedules {{c2::tasks}} to run that DAG on executors, one task per partition.
