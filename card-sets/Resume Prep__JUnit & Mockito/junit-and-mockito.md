---
deck: "Resume Prep::JUnit & Mockito"
topic: "JUnit & Mockito"
tags: [ankicardmaker, resume-prep, junit-mockito]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# JUnit & Mockito — Resume Prep

Source of truth for the `Resume Prep::JUnit & Mockito` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What annotation marks a method as a JUnit 5 test?
   **A:** <code>@Test</code>

2. **Q:** What does <code>@BeforeEach</code> do in a JUnit 5 test class?
   **A:** Runs the annotated method before <em>every</em> test method in the class &mdash; used for per-test setup (e.g. re-creating fixtures).

3. **Q:** What does <code>@AfterEach</code> do in a JUnit 5 test class?
   **A:** Runs the annotated method after <em>every</em> test method &mdash; used for per-test cleanup (e.g. closing resources).

4. **Q:** Write a JUnit 5 test asserting that 2 + 2 equals 4.
   **A:** <pre><code>@Test
void addsTwoNumbers() {
    assertEquals(4, 2 + 2);
}</code></pre>

5. **Q:** Write a JUnit 5 test asserting that <code>calc.divide(1, 0)</code> throws <code>ArithmeticException</code>.
   **A:** <pre><code>@Test
void divideByZeroThrows() {
    Calculator calc = new Calculator();
    assertThrows(ArithmeticException.class,
        () -&gt; calc.divide(1, 0));
}</code></pre>

6. **Q:** What does JUnit's <code>assertThrows(...)</code> return, and why is that useful?
   **A:** It returns the caught exception instance, so you can chain further assertions on it (e.g. <code>assertEquals("bad input", ex.getMessage())</code>) instead of only checking the type.

7. **Q:** Write a JUnit 5 parameterized test that checks every int in {1, 2, 3, 4} is positive.
   **A:** <pre><code>@ParameterizedTest
@ValueSource(ints = {1, 2, 3, 4})
void isPositive(int number) {
    assertTrue(number &gt; 0);
}</code></pre>

8. **Q:** In Mockito, what does the <code>@Mock</code> annotation create?
   **A:** A fake implementation of the annotated type whose methods return default/empty values (null, 0, empty collection, etc.) until you stub them &mdash; it does not call any real logic.

9. **Q:** In Mockito, what does <code>@InjectMocks</code> do?
   **A:** Creates a real instance of the class under test and injects the fields annotated <code>@Mock</code> (or <code>@Spy</code>) into it via constructor, setter, or field injection.

10. **Q:** Write Mockito code to stub <code>userRepository.findById(1L)</code> so it returns <code>Optional.of(user)</code>.
   **A:** <pre><code>when(userRepository.findById(1L))
    .thenReturn(Optional.of(user));</code></pre>

11. **Q:** Why must you use <code>doReturn(x).when(mock).method()</code> instead of <code>when(mock.method()).thenReturn(x)</code> when stubbing a Mockito <strong>spy</strong>?
   **A:** <code>when(...)</code> first actually calls <code>mock.method()</code> to resolve the argument; on a spy that wraps a real object, that invokes the real method (possibly with side effects) before the stub is applied. <code>doReturn()</code> never calls the real method.

12. **Q:** How do you verify with Mockito that <code>emailService.send(...)</code> was called exactly once?
   **A:** <pre><code>verify(emailService, times(1)).send(any());</code></pre> (<code>times(1)</code> is the default, so <code>verify(emailService).send(any());</code> is equivalent.)

13. **Q:** What is the rule for mixing Mockito argument matchers (like <code>anyString()</code>) with raw literal values in the same stub or verify call?
   **A:** If <em>any</em> argument in the call uses a matcher, <em>all</em> arguments in that call must be matchers &mdash; you cannot mix raw values and matchers in one invocation (use <code>eq(value)</code> for the raw ones instead).

14. **Q:** Mockito <strong>spy</strong> *(reversed — tested both ways)*
   **A:** A test double that wraps a real object; unless explicitly stubbed, calling a method on it runs the real implementation &mdash; unlike a mock, which returns defaults for every unstubbed call.

15. **Q:** What do the three parts of the AAA pattern stand for when structuring a unit test?
   **A:** Arrange (set up objects/data), Act (call the method under test), Assert (check the result) &mdash; keeping these visually separated makes tests easier to read.

16. **Q:** Write a JUnit 5 + Mockito test for a Spring <code>OrderService</code> that mocks its <code>OrderRepository</code> dependency, without starting the Spring context.
   **A:** <pre><code>@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository repo;
    @InjectMocks OrderService service;

    @Test
    void savesOrder() {
        when(repo.save(any())).thenReturn(new Order());
        assertNotNull(service.createOrder());
    }
}</code></pre>

## Cloze cards

- In JUnit 5, {{c1::@BeforeAll}} runs once before all tests in the class, and {{c2::@AfterAll}} runs once after all tests; both must be <code>static</code> methods unless the class uses <code>@TestInstance(Lifecycle.PER_CLASS)</code>.
- A JUnit 5 parameterized test uses {{c1::@ParameterizedTest}} instead of <code>@Test</code>, plus a source annotation such as {{c2::@ValueSource}}, {{c3::@CsvSource}}, or {{c4::@MethodSource}} to supply the argument values.
