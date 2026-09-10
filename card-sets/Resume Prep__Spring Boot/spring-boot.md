---
deck: "Resume Prep::Spring Boot"
topic: "Spring Boot"
tags: [ankicardmaker, resume-prep, spring-boot]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Spring Boot — Resume Prep

Source of truth for the `Resume Prep::Spring Boot` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What problem does Inversion of Control (IoC) solve in application design?
   **A:** It removes the responsibility of creating and wiring dependencies from application classes, delegating object creation and lifecycle management to a container (the Spring IoC container), reducing tight coupling between classes.

2. **Q:** In Spring, what is a "bean"?
   **A:** An object that is instantiated, assembled, and managed by the Spring IoC container (as opposed to being created directly with <code>new</code> by application code).

3. **Q:** What is the difference between "singleton" and "prototype" bean scope in Spring?
   **A:** Singleton: one shared instance per Spring container, reused for every injection point. Prototype: a brand-new instance is created every time the bean is requested/injected.

4. **Q:** How do you code a class as a Spring REST controller that exposes a GET endpoint?
   **A:** <pre><code>@RestController
@RequestMapping("/api/eforms")
public class EFormController {
    private final EFormService service;
    public EFormController(EFormService service) {
        this.service = service;
    }
    @GetMapping("/{id}")
    public EForm getForm(@PathVariable Long id) {
        return service.findById(id);
    }
}</code></pre>

5. **Q:** What does @RestController combine, compared to plain @Controller?
   **A:** @RestController = @Controller + @ResponseBody — every handler method's return value is serialized directly into the HTTP response body (e.g. as JSON) instead of being resolved to a view template.

6. **Q:** Why annotate a class with @Service or @Repository instead of just @Component?
   **A:** Both are specializations of @Component so they're still auto-detected as beans, but they add meaning: @Service marks business-logic classes; @Repository marks data-access classes and also enables Spring's exception translation, converting persistence exceptions into Spring's DataAccessException hierarchy.

7. **Q:** Why is constructor injection generally preferred over field injection with @Autowired?
   **A:** It makes dependencies explicit and lets fields be final/immutable, allows the class to be instantiated outside Spring (easier unit testing without a container), fails fast at startup if a dependency is missing, and avoids hidden circular-dependency issues.

8. **Q:** In the ServiceOntario full-stack app (Spring Boot + React), which annotation exposes the JSON endpoints the React front-end calls?
   **A:** @RestController (combined with @RequestMapping/@GetMapping/@PostMapping etc.) — handler methods return Java objects that Spring serializes to JSON for the React client to consume over HTTP.

9. **Q:** How do you code idiomatic constructor injection for a Spring service (no Lombok)?
   **A:** <pre><code>@Service
public class EFormService {
    private final EFormRepository repository;

    public EFormService(EFormRepository repository) {
        this.repository = repository;
    }
}</code></pre>

10. **Q:** What is Spring Boot "auto-configuration"?
   **A:** A mechanism (@EnableAutoConfiguration, pulled in by @SpringBootApplication) that automatically configures beans based on the classpath contents, existing beans, and property settings — e.g. adding a DataSource bean automatically once a JDBC driver is on the classpath.

11. **Q:** What is a Spring Boot "starter" (e.g. spring-boot-starter-web)?
   **A:** A curated dependency descriptor that bundles a set of version-compatible libraries for a use case (web, JPA, security, etc.), so you don't have to manage each transitive dependency and version yourself.

12. **Q:** How do Spring profiles let you vary configuration between environments?
   **A:** You define environment-specific property files (application-dev.yml, application-prod.yml) and/or annotate beans with @Profile("dev"); activating a profile via spring.profiles.active=prod makes Spring load only the matching config and beans.

13. **Q:** How do you hook into bean initialization and cleanup using annotations?
   **A:** <pre><code>@Component
public class ConnectionPool {
    @PostConstruct
    public void init() {
        // open connections
    }
    @PreDestroy
    public void cleanup() {
        // close connections
    }
}</code></pre>

14. **Q:** What does @Transactional do when placed on a Spring service method?
   **A:** Wraps the call in a proxy that starts a database transaction before the method executes and commits it on success, rolling it back automatically if an unchecked (RuntimeException) exception propagates out.

15. **Q:** By default, does Spring's @Transactional roll back on checked exceptions?
   **A:** No — by default it only rolls back on unchecked exceptions (RuntimeException) and Error, not checked exceptions, unless rollbackFor is explicitly specified.

16. **Q:** How do you centrally handle exceptions thrown by any @RestController in a Spring Boot app?
   **A:** <pre><code>@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EFormNotFoundException.class)
    public ResponseEntity&lt;String&gt; handleNotFound(EFormNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ex.getMessage());
    }
}</code></pre>

17. **Q:** What is Spring Boot Actuator used for?
   **A:** A set of production-ready endpoints (e.g. /actuator/health, /actuator/metrics, /actuator/info) for monitoring and managing a running application — health checks, metrics, environment info — without building that infrastructure yourself.

## Cloze cards

- The default scope of a Spring bean is {{c1::singleton}} — only one shared instance is created per Spring container/application context and reused for every injection. <!-- Back Extra: Other scopes: prototype, request, session, application. -->
- Spring Boot externalizes configuration in {{c1::application.yml}} (or application.properties), letting values like {{c2::server.port}} and datasource URLs live outside compiled code. <!-- Back Extra: YAML is a hierarchical alternative to the flat .properties format. -->
- Spring bean lifecycle order: instantiate → inject dependencies → {{c1::@PostConstruct}} callback runs → bean is ready for use → {{c2::@PreDestroy}} callback runs on container shutdown.
