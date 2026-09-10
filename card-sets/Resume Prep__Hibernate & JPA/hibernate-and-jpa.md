---
deck: "Resume Prep::Hibernate & JPA"
topic: "Hibernate & JPA"
tags: [ankicardmaker, resume-prep, hibernate-jpa]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Hibernate & JPA — Resume Prep

Source of truth for the `Resume Prep::Hibernate & JPA` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does @Entity mark a Java class as?
   **A:** A JPA-managed persistent class whose instances map to rows in a database table.

2. **Q:** How do you code a minimal JPA entity with a database-generated primary key?
   **A:** <pre><code>@Entity
@Table(name = "eforms")
public class EForm {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    // getters/setters
}</code></pre>

3. **Q:** @GeneratedValue(strategy = GenerationType.IDENTITY) *(reversed — tested both ways)*
   **A:** Delegates primary-key generation to the database's auto-increment column; the ID is only known after the INSERT executes.

4. **Q:** What is the difference between GenerationType.IDENTITY and GenerationType.SEQUENCE?
   **A:** IDENTITY relies on the DB's auto-increment column and assigns the ID at insert time, which prevents Hibernate from batching inserts. SEQUENCE pre-fetches ID values from a database sequence before insert, which allows batching.

5. **Q:** How do you code a one-to-many / many-to-one relationship between EForm and Field entities?
   **A:** <pre><code>@Entity
public class EForm {
    @OneToMany(mappedBy = "form", fetch = FetchType.LAZY)
    private List&lt;Field&gt; fields;
}

@Entity
public class Field {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "form_id")
    private EForm form;
}</code></pre>

6. **Q:** What is the default fetch type for @ManyToOne/@OneToOne versus @OneToMany/@ManyToMany?
   **A:** @ManyToOne and @OneToOne default to EAGER; @OneToMany and @ManyToMany default to LAZY.

7. **Q:** What does LAZY fetching mean for an association, and what happens if you access it after the session is closed?
   **A:** The related entity/collection is not loaded from the database until it's actually accessed; accessing it after the persistence context/session has closed throws LazyInitializationException.

8. **Q:** What is the N+1 query problem?
   **A:** Fetching a list of N parent entities triggers 1 query for the parents plus N additional queries — one per parent — to lazily load each parent's related collection/entity, instead of one efficient query.

9. **Q:** Why does the N+1 problem typically show up when iterating over parent entities and accessing a lazy association in a loop?
   **A:** Because Hibernate only loads a LAZY association on first access, so touching that association inside a loop over N parents fires a separate SELECT for each parent individually.

10. **Q:** How do you fix N+1 for a specific repository query using JPQL JOIN FETCH?
   **A:** <pre><code>@Query("SELECT f FROM EForm f JOIN FETCH f.fields WHERE f.status = :status")
List&lt;EForm&gt; findWithFieldsByStatus(@Param("status") String status);</code></pre> This loads EForms and their fields in one SQL join instead of N extra queries.

11. **Q:** What is the key difference between a plain JPQL JOIN and a JOIN FETCH?
   **A:** A plain JOIN only affects the filter/WHERE condition and still lazily loads the association separately afterward; JOIN FETCH eagerly initializes the association within the same query, eliminating the extra round-trips.

12. **Q:** What does Hibernate's @BatchSize (or hibernate.default_batch_fetch_size) do?
   **A:** Instead of firing one SELECT per lazy association, Hibernate groups multiple pending lazy loads into a single "SELECT ... WHERE id IN (?, ?, ?...)" up to the configured batch size — cutting N+1 down to roughly N/batchSize queries when a JOIN FETCH isn't applicable.

13. **Q:** How do you apply Hibernate batch fetching to an entity's lazy collection?
   **A:** <pre><code>@Entity
public class EForm {
    @OneToMany(mappedBy = "form", fetch = FetchType.LAZY)
    @BatchSize(size = 25)
    private List&lt;Field&gt; fields;
}</code></pre> Or globally via <code>spring.jpa.properties.hibernate.default_batch_fetch_size=25</code>.

14. **Q:** At ServiceOntario, how were N+1 query bottlenecks fixed, and what was the measured impact?
   **A:** By adding JPQL JOIN FETCH for associations known to be needed on every row, and tuning Hibernate batch sizes for the remaining lazy loads — this cut read latency by 40%.

15. **Q:** When should you prefer JOIN FETCH over increasing @BatchSize, and vice versa?
   **A:** Use JOIN FETCH when you know upfront you need one (or maybe two) specific associations for every row in a query — one round trip. Use @BatchSize when several different lazy associations/collections are accessed unpredictably across many entities, since fetch-joining multiple collections at once risks a cartesian-product blowup or MultipleBagFetchException.

16. **Q:** What is the first-level cache (persistence context) in Hibernate?
   **A:** A per-Session/EntityManager cache that stores every entity loaded or saved during that session; a repeated lookup by ID within the same session returns the cached instance instead of re-querying the database.

17. **Q:** What is "dirty checking" in Hibernate?
   **A:** At flush time, Hibernate compares each managed entity's current state against the snapshot taken when it was loaded, and automatically generates UPDATE statements for any changed fields — no explicit save() call needed for a managed entity mutation.

18. **Q:** When does Hibernate flush pending SQL to the database relative to a @Transactional method's execution?
   **A:** By default (FlushMode.AUTO) it flushes automatically before the transaction commits, and also before running a JPQL/SQL query that could be affected by pending in-memory changes — not necessarily the instant an entity field is mutated.

19. **Q:** If a @Transactional method's transaction is rolled back, are SQL statements Hibernate already flushed to the database during that transaction undone?
   **A:** Yes — a rollback undoes the entire database transaction, including any statements Hibernate had already flushed (sent to the DB but not yet committed) earlier in that same transaction.

## Cloze cards

- JPQL is {{c1::object/entity-oriented}} — it queries against entity names and fields rather than table/column names — while the Criteria API builds queries {{c2::programmatically with a type-safe, object-based API}} instead of query strings, which is useful for dynamically constructed queries.
