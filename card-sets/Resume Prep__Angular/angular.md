---
deck: "Resume Prep::Angular"
topic: "Angular"
tags: [ankicardmaker, resume-prep, angular]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Angular — Resume Prep

Source of truth for the `Resume Prep::Angular` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In Angular, what is a component?
   **A:** A TypeScript class decorated with <code>@Component</code> that controls a view via an HTML template and CSS, plus the logic behind it — Angular's basic UI building block.

2. **Q:** What is the role of an Angular <code>@NgModule</code>?
   **A:** It groups related components, directives, pipes, and services into a cohesive block, declaring what belongs to it and what it imports, exports, and provides.

3. **Q:** What is dependency injection (DI) in Angular?
   **A:** A pattern where Angular's injector supplies a class's dependencies (like services) through its constructor rather than the class creating them itself, enabling loose coupling and easy mocking in tests.

4. **Q:** How do you code an Angular service that's injectable app-wide and inject it into a component?
   **A:** <pre><code>@Injectable({ providedIn: 'root' })
export class LoanService {
  calculateMonthlyPayment(principal: number, rate: number, months: number) {
    // amortization formula
  }
}

@Component({ selector: 'app-calc' })
export class CalcComponent {
  constructor(private loanService: LoanService) {}
}</code></pre>

5. **Q:** What is a structural directive in Angular? Give an example.
   **A:** A directive that changes the DOM layout by adding or removing elements, e.g. <code>*ngIf</code> (conditionally render) and <code>*ngFor</code> (repeat a template for each item in a list).

6. **Q:** How do you code an Angular template that lists loan offers with <code>*ngFor</code> and shows a fallback when there are none?
   **A:** <pre><code>&lt;ul *ngIf="offers.length; else empty"&gt;
  &lt;li *ngFor="let o of offers"&gt;{{o.rate}}%&lt;/li&gt;
&lt;/ul&gt;
&lt;ng-template #empty&gt;No offers found&lt;/ng-template&gt;</code></pre>

7. **Q:** What Angular decorator lets a parent component pass data into a child component?
   **A:** <code>@Input()</code> — it declares a property on the child that the parent binds to via property binding, e.g. <code>[loanAmount]="amount"</code>.

8. **Q:** What Angular decorator lets a child component emit an event to its parent?
   **A:** <code>@Output()</code>, paired with an <code>EventEmitter</code>; the child calls <code>.emit(value)</code> and the parent listens via event binding, e.g. <code>(calculated)="onCalculated($event)"</code>.

9. **Q:** How do you code a child component that emits a computed loan payment up to its parent?
   **A:** <pre><code>@Component({ selector: 'app-payment' })
export class PaymentComponent {
  @Input() principal: number;
  @Output() calculated = new EventEmitter&lt;number&gt;();

  compute() {
    const payment = this.principal * 0.05;
    this.calculated.emit(payment);
  }
}</code></pre>

10. **Q:** Why does Angular favor RxJS Observables for things like <code>HttpClient</code> responses?
   **A:** Observables represent streams of async values over time and support composable operators (map, filter, switchMap, debounceTime) for transforming, combining, and cancelling async work.

11. **Q:** How do you code an Angular <code>HttpClient</code> call that fetches mortgage rates and subscribes to the result?
   **A:** <pre><code>constructor(private http: HttpClient) {}

getRates(): void {
  this.http.get&lt;Rate[]&gt;('/api/rates')
    .subscribe(rates =&gt; this.rates = rates);
}</code></pre>

12. **Q:** Which Angular lifecycle hook runs once, right after a component's inputs are first set and before the view renders?
   **A:** <code>ngOnInit()</code> — commonly used to fetch initial data or set up subscriptions.

13. **Q:** Which Angular lifecycle hook should you use to clean up subscriptions and avoid memory leaks?
   **A:** <code>ngOnDestroy()</code> — called just before the component is destroyed; typically used to call <code>.unsubscribe()</code> on RxJS subscriptions.

14. **Q:** What is Zone.js's role in Angular's change detection?
   **A:** Zone.js monkey-patches async browser APIs (setTimeout, DOM events, promises, XHR) so Angular is notified whenever async work finishes, letting it automatically trigger change detection to update the view.

15. **Q:** In Angular's default change detection strategy, what triggers a check of a component's view?
   **A:** Any async event Zone.js is aware of anywhere in the app (a DOM event, timer, HTTP response, promise resolution) causes Angular to run change detection through the whole component tree by default.

16. **Q:** What does setting <code>changeDetection: ChangeDetectionStrategy.OnPush</code> do?
   **A:** It tells Angular to only re-check that component when its <code>@Input()</code> references change, an event originates inside it, or it's marked dirty manually — reducing unnecessary checks for performance.

17. **Q:** How do you code a basic Angular route configuration for a loan calculator page?
   **A:** <pre><code>const routes: Routes = [
  { path: 'loan-calculator', component: LoanCalculatorComponent },
  { path: '', redirectTo: 'loan-calculator', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}</code></pre>

18. **Q:** In a BMO-style Mortgage & Loan Calculator built with Angular + Node.js on AWS, why use <code>debounceTime</code> on an RxJS stream of user rate-slider input before calling the calculation API?
   **A:** It waits for the user to pause dragging or typing before emitting a value, avoiding an API request on every intermediate value and cutting unnecessary calculation calls.

## Cloze cards

- Angular supports four data binding types: {{c1::interpolation}} (text via double curly braces), {{c2::property binding}} (square brackets, e.g. <code>[value]</code>), {{c3::event binding}} (parentheses, e.g. <code>(click)</code>), and {{c4::two-way binding}} ('banana in a box', e.g. <code>[(ngModel)]</code>).
