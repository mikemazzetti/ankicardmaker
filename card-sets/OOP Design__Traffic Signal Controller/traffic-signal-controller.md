---
deck: "OOP Design::Traffic Signal Controller"
topic: "Traffic Signal Controller"
tags: [ankicardmaker, ood-traffic-signal]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Traffic Signal Controller — OOP Design

Source of truth for the `OOP Design::Traffic Signal Controller` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what are the core functional requirements to clarify for a Traffic Signal Controller system?
   **A:** 1) Control signal lights at one or more intersections. 2) Support multiple directions (N/S/E/W) with independent light states. 3) Cycle lights in a safe, timed sequence (green&rarr;yellow&rarr;red). 4) Support emergency-vehicle preemption. 5) Support manual/maintenance override (e.g. flashing red on power failure).

2. **Q:** What should you explicitly mark out of scope when designing a Traffic Signal Controller in a 45-minute interview?
   **A:** Adaptive/ML-based timing optimization, pedestrian-button hardware integration, vehicle-detection sensor hardware, and city-wide synchronization across many intersections &mdash; mention them as extensions, don't design them in depth.

3. **Q:** What is the responsibility of the <code>SignalController</code> class?
   **A:** Owns the timing loop: advances the active <code>SignalPhase</code>, tells each <code>TrafficSignal</code> to transition its light, enforces the all-red clearance interval between phases, and exposes hooks for emergency preemption and manual override.

4. **Q:** What is the responsibility of the <code>TrafficSignal</code> class, as opposed to <code>SignalController</code>?
   **A:** It represents the physical light for one direction. It only knows its own current <code>LightColor</code>/state and how to transition to the next one &mdash; it has no knowledge of other directions or the overall phase schedule.

5. **Q:** What fields does a <code>SignalPhase</code> typically hold?
   **A:** The set of <code>Direction</code>s that are GREEN during this phase, and a <code>durationSeconds</code> for how long the phase lasts before the controller advances to the next phase (optionally, which directions get a protected left-turn arrow).

6. **Q:** How does <code>Intersection</code> relate to <code>TrafficSignal</code>?
   **A:** Composition: an <code>Intersection</code> owns exactly one <code>TrafficSignal</code> per approach direction (e.g. a <code>Map&lt;Direction, TrafficSignal&gt;</code>); the signals cannot exist independently of the intersection.

7. **Q:** How does <code>SignalController</code> relate to <code>SignalPhase</code>?
   **A:** A <code>SignalController</code> holds an ordered, cyclic list of <code>SignalPhase</code> objects and steps through them one at a time, applying each phase's green directions to the intersection for its configured duration.

8. **Q:** Which design pattern best fits the light-color transitions of a single <code>TrafficSignal</code>, and why?
   **A:** The <b>State</b> pattern. Each color (Red/Yellow/Green) is a state object that knows only its own duration and which state comes next; <code>TrafficSignal.transition()</code> just delegates to <code>currentState.next()</code>. This avoids a large switch/if-else and makes adding a new state (e.g. FlashingRed) a matter of adding one class, without touching existing ones.

9. **Q:** Besides State, what secondary pattern helps notify external components (a pedestrian signal, a monitoring dashboard) when a light changes, and why?
   **A:** <b>Observer</b>. The signal maintains a list of listeners and calls <code>onLightChanged(direction, newColor)</code> on each transition, decoupling the core signal logic from whatever consumes the change event.

10. **Q:** What two methods form the minimal public API of the <code>LightState</code> interface in a State-pattern <code>TrafficSignal</code>?
   **A:** <code>getColor()</code> &mdash; returns the <code>LightColor</code> this state represents &mdash; and <code>next()</code> &mdash; returns the <code>LightState</code> to transition to once this state's duration elapses.

11. **Q:** What method does <code>SignalController</code> expose to handle an approaching emergency vehicle, and what must it do internally?
   **A:** <code>preempt(Direction direction)</code> &mdash; pauses the normal phase cycle, forces that direction's signal to GREEN and all conflicting directions to RED, then safely resumes the normal cycle (respecting all-red clearance) once preemption ends.

12. **Q:** Why must <code>SignalController</code> insert an all-red clearance interval between phases instead of switching one direction's green directly to another direction's green?
   **A:** Vehicles already in the intersection from the ending phase need time to clear before cross-traffic gets a green light &mdash; without the all-red gap, two conflicting directions could effectively be green/entering at once, causing collisions.

13. **Q:** On detecting a power failure or hardware fault, what should <code>SignalController</code> do, and why not simply turn all lights off?
   **A:** Switch every <code>TrafficSignal</code> into <code>FLASHING_RED</code> mode (each direction treated like a stop sign) rather than going dark &mdash; an unlit intersection gives drivers no cue that caution is required, which is far more dangerous than a flashing-red fail-safe.

14. **Q:** Edge case: a technician wants to force a specific phase manually from a control panel. How should the design support this without breaking the automatic cycle logic?
   **A:** Add a <code>manualOverride(SignalPhase phase)</code> entry point that pauses the controller's automatic timer loop (the same pause mechanism used for emergency preemption) and lets the operator hold a phase; resuming exits override mode and re-enters the normal cycle at a safe phase boundary (never mid-phase).

15. **Q:** (Java) Implement the <code>LightState</code> interface and its <code>GreenState</code> concrete implementation for the State-pattern <code>TrafficSignal</code>.
   **A:** <pre><code>public interface LightState {
    LightColor getColor();
    LightState next();
    int getDurationSeconds();
}

public class GreenState implements LightState {
    @Override
    public LightColor getColor() { return LightColor.GREEN; }

    @Override
    public LightState next() { return new YellowState(); }

    @Override
    public int getDurationSeconds() { return 30; }
}</code></pre>

16. **Q:** (Python) Implement <code>TrafficSignal</code> with <code>tick()</code> and <code>transition()</code> driving the State-pattern light changes.
   **A:** <pre><code>class TrafficSignal:
    def __init__(self, direction, initial_state):
        self.direction = direction
        self.state = initial_state
        self.elapsed = 0

    def tick(self, seconds=1):
        self.elapsed += seconds
        if self.elapsed &gt;= self.state.get_duration_seconds():
            self.transition()

    def transition(self):
        self.state = self.state.next()
        self.elapsed = 0

    def color(self):
        return self.state.get_color()</code></pre>

17. **Q:** (Java) Implement <code>SignalController.tick()</code>, called once per second, driving the phase cycle with an all-red clearance interval between phases.
   **A:** <pre><code>public class SignalController {
    private static final int ALL_RED_SECONDS = 2;
    private List&lt;SignalPhase&gt; phases;
    private int currentPhaseIndex = 0;
    private int elapsedInPhase = 0;
    private boolean inAllRedClearance = false;

    public void tick() {
        elapsedInPhase++;
        SignalPhase phase = phases.get(currentPhaseIndex);

        if (inAllRedClearance) {
            if (elapsedInPhase &gt;= ALL_RED_SECONDS) {
                advanceToNextPhase();
            }
            return;
        }

        if (elapsedInPhase &gt;= phase.getDurationSeconds()) {
            setAllDirectionsRed();
            inAllRedClearance = true;
            elapsedInPhase = 0;
        }
    }

    private void advanceToNextPhase() {
        currentPhaseIndex = (currentPhaseIndex + 1) % phases.size();
        inAllRedClearance = false;
        elapsedInPhase = 0;
        applyPhase(phases.get(currentPhaseIndex));
    }
}</code></pre>

18. **Q:** (Java) Implement <code>SignalController.preempt()</code> for emergency-vehicle handling, saving state so the normal cycle can resume afterward.
   **A:** <pre><code>public class SignalController {
    private SignalPhase savedPhase;
    private int savedElapsed;
    private boolean preempted = false;

    public void preempt(Direction emergencyDirection) {
        savedPhase = phases.get(currentPhaseIndex);
        savedElapsed = elapsedInPhase;
        preempted = true;

        setAllDirectionsRed();
        getSignal(emergencyDirection).forceColor(LightColor.GREEN);
    }

    public void resumeFromPreemption() {
        setAllDirectionsRed();      // all-red clearance first
        preempted = false;
        applyPhase(savedPhase);
        elapsedInPhase = savedElapsed;
    }
}</code></pre>

## Cloze cards

- The core classes in a Traffic Signal Controller design are {{c1::Intersection}} (owns the signals for a junction), {{c2::TrafficSignal}} (one per direction, holds current light state), {{c3::SignalController}} (drives the timing/phase cycle), and {{c4::SignalPhase}} (defines which directions are green together and for how long).
- The <code>LightColor</code> enum for a traffic signal is typically {{c1::RED}}, {{c2::YELLOW}}, {{c3::GREEN}}, plus a fail-safe value {{c4::FLASHING_RED}} used during power failure or maintenance.
