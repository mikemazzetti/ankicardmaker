---
deck: "Resume Prep::Concurrency & Resilience"
topic: "Concurrency & Resilience"
tags: [ankicardmaker, resume-prep, concurrency-resilience]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Concurrency & Resilience — Resume Prep

Source of truth for the `Resume Prep::Concurrency & Resilience` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does Spring's @Async annotation do to a method call?
   **A:** Causes the method to execute on a separate thread from a configured TaskExecutor instead of the caller's thread, so the caller doesn't block waiting for it. Requires @EnableAsync on a configuration class.

2. **Q:** How do you code an asynchronous Spring service method that returns a result?
   **A:** <pre><code>@Service
public class ValidationService {
    @Async
    public CompletableFuture&lt;Boolean&gt; validateAsync(EForm form) {
        boolean valid = runValidation(form);
        return CompletableFuture.completedFuture(valid);
    }
}</code></pre>

3. **Q:** Why does an @Async method typically return CompletableFuture<T> (or void) rather than T directly?
   **A:** Because the method runs on another thread and the caller returns immediately; CompletableFuture gives the caller a handle to later retrieve the result or compose further async work, while void is used for fire-and-forget calls.

4. **Q:** What happens if you call an @Async method from another method in the same class (self-invocation)?
   **A:** The @Async annotation is ignored — Spring's proxy-based AOP only intercepts calls made through the external bean reference, so an internal call bypasses the proxy and executes synchronously on the caller's thread.

5. **Q:** What is a thread pool (Executor), and why use one instead of spawning a new thread per task?
   **A:** A managed pool of reusable worker threads that pull tasks from a queue; reusing threads avoids the overhead of constantly creating/destroying OS threads and lets you bound concurrency to avoid exhausting system resources.

6. **Q:** How do you configure a custom thread pool for @Async tasks in Spring?
   **A:** <pre><code>@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(8);
        executor.setMaxPoolSize(16);
        executor.setQueueCapacity(100);
        return executor;
    }
}</code></pre>

7. **Q:** What does "non-blocking I/O" mean, and why did the Gov of Ontario eForm validation microservice use it with @Async?
   **A:** The thread that issues an I/O operation (network/DB call) isn't left idle waiting for it — it's freed to do other work while the I/O completes in the background. Combined with Spring @Async, this kept worker threads from blocking on slow validation calls in a ~10GB/day pipeline, cutting latency by 40%.

8. **Q:** What is CompletableFuture used for in Java concurrency?
   **A:** A Future implementation that lets you compose, chain, and combine asynchronous computations (thenApply, thenCompose, allOf, thenCombine, etc.) without manually blocking a thread to wait for a result.

9. **Q:** How do you run two independent tasks concurrently and combine their results with CompletableFuture?
   **A:** <pre><code>CompletableFuture&lt;Integer&gt; f1 = CompletableFuture.supplyAsync(() -&gt; slowLookup());
CompletableFuture&lt;Integer&gt; f2 = CompletableFuture.supplyAsync(() -&gt; anotherLookup());
CompletableFuture&lt;Integer&gt; combined = f1.thenCombine(f2, Integer::sum);
combined.thenAccept(System.out::println);</code></pre>

10. **Q:** What is a race condition?
   **A:** A bug where a program's correctness depends on the relative timing/interleaving of multiple threads accessing shared mutable state, producing incorrect results under certain thread orderings.

11. **Q:** Name two standard ways to prevent a race condition on shared mutable state in Java.
   **A:** Synchronize access (the synchronized keyword or explicit locks) so only one thread mutates the state at a time, or use atomic/concurrent-safe types (e.g. AtomicInteger, ConcurrentHashMap) that are designed for lock-free thread-safe updates.

12. **Q:** What is the circuit breaker pattern used for in a microservice architecture?
   **A:** It stops a service from repeatedly calling a downstream dependency that is failing or slow, by "tripping" after a failure threshold and short-circuiting further calls (failing fast) instead of piling up latency and exhausting resources.

13. **Q:** How do you apply a Resilience4j circuit breaker with a fallback to a method in Spring Boot?
   **A:** <pre><code>@CircuitBreaker(name = "eformValidation", fallbackMethod = "fallback")
public ValidationResult callValidationService(EForm form) {
    return restTemplate.postForObject(url, form, ValidationResult.class);
}

public ValidationResult fallback(EForm form, Throwable t) {
    return ValidationResult.unavailable();
}</code></pre>

14. **Q:** What is the difference between Resilience4j's retry and bulkhead patterns?
   **A:** Retry automatically re-attempts a failed call a configured number of times (often with backoff), aiming to survive transient failures. Bulkhead limits the number of concurrent calls to a dependency (via a semaphore or fixed thread pool), isolating it so its slowness/failures can't exhaust resources the rest of the app needs.

15. **Q:** What does a rate limiter do in Resilience4j, and why pair one with a downstream call?
   **A:** It caps how many calls are allowed to a resource within a time window, rejecting or delaying calls beyond that limit — protecting both the caller and the downstream service from being overwhelmed by traffic spikes.

16. **Q:** What is Caffeine, and what problem does it solve?
   **A:** A high-performance, in-memory Java caching library; it avoids recomputing or refetching expensive/repeated results (e.g. DB lookups) by storing them in memory with configurable size limits and eviction policies.

17. **Q:** How do you cache a Spring service method's result with @Cacheable (Caffeine-backed)?
   **A:** <pre><code>@Service
public class LookupService {
    @Cacheable(value = "eformTypes", key = "#formId")
    public EFormType getFormType(Long formId) {
        return expensiveLookup(formId);
    }
}</code></pre> Backed by a CaffeineCacheManager bean configured with cache names, TTL, and max size.

18. **Q:** Name two eviction policies Caffeine supports for bounding cache size or lifetime.
   **A:** Size-based eviction (maximumSize, evicting least-recently-used entries once a cap is reached) and time-based eviction (expireAfterWrite / expireAfterAccess, evicting entries after a fixed duration).

19. **Q:** What's a common gotcha with @Cacheable and self-invocation, similar to @Async?
   **A:** Calling a @Cacheable method from another method in the same class bypasses Spring's proxy (just like with @Async), so the caching logic never runs and the method executes uncached every time.

## Cloze cards

- A Resilience4j circuit breaker has three core states: {{c1::CLOSED}} (calls pass through normally while failures are counted), {{c2::OPEN}} (calls are short-circuited immediately without reaching the downstream service), and {{c3::HALF_OPEN}} (a limited number of trial calls are let through to test if the dependency has recovered). <!-- Back Extra: OPEN transitions to HALF_OPEN after a configured wait duration; HALF_OPEN moves to CLOSED on success or back to OPEN on failure. -->
