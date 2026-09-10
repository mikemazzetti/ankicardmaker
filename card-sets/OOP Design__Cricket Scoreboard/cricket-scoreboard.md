---
deck: "OOP Design::Cricket Scoreboard"
topic: "Cricket Scoreboard"
tags: [ankicardmaker, ood-cricket-scoreboard]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Cricket Scoreboard — OOP Design

Source of truth for the `OOP Design::Cricket Scoreboard` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements to clarify for a Cricket Scoreboard OOD interview?
   **A:** 1) Track runs, wickets, and overs bowled per innings, live, ball by ball. 2) Record how a batsman got out (dismissal type). 3) Handle extras (wide, no-ball, bye, leg-bye) correctly. 4) Rotate strike between batsmen. 5) Progress the match through innings and end states (completed/abandoned) and expose live updates to a display.

2. **Q:** What should you explicitly mark out of scope when designing a Cricket Scoreboard in an interview?
   **A:** Duckworth&ndash;Lewis-style rain-adjusted target calculation, full tournament/league standings, and video-referral (DRS) workflow &mdash; model the match/innings/ball state machine and scoring rules, not these extensions.

3. **Q:** What is the responsibility of the <code>Match</code> class?
   **A:** Owns the two (or four, for Tests) <code>Innings</code> in order, the two competing <code>Team</code>s, and the overall <code>MatchState</code>; delegates each incoming <code>Ball</code> to the current innings via its state object and decides when to move to the next innings or end the match.

4. **Q:** What is the responsibility of the <code>Innings</code> class?
   **A:** Tracks the batting/bowling team, total runs, wickets fallen, overs bowled (as a list of <code>Over</code>, each a list of <code>Ball</code>s), and which two batsmen are currently at the crease (striker/non-striker); applies each ball's effect via <code>applyBall()</code> and reports <code>isComplete()</code>.

5. **Q:** What is the responsibility of the <code>Scoreboard</code> class?
   **A:** Acts purely as a publisher: it holds no scoring logic itself, just a list of observers (live display, mobile push, commentary feed) that it notifies whenever a ball is bowled or the match state changes.

6. **Q:** How does <code>Match</code> relate to <code>Innings</code>?
   **A:** Composition with strict sequencing: a <code>Match</code> owns an ordered list of <code>Innings</code> objects and only one is ever "current" at a time; an innings only starts once the previous one is marked complete.

7. **Q:** Which design pattern fits the match/innings lifecycle, and why?
   **A:** <b>State</b>. States like NotStarted, InProgress, InningsBreak, Completed, and Abandoned each know which ball-handling/transition behavior is legal; <code>Match.recordBall()</code> delegates to <code>state.recordBall(match, ball)</code>, so e.g. balls arriving during an innings break are simply invalid for that state rather than needing ad hoc guard checks scattered around.

8. **Q:** Which design pattern fits pushing live score updates to displays/apps, and why?
   **A:** <b>Observer</b>. <code>Scoreboard</code> (the subject) notifies every registered listener &mdash; a stadium display, a mobile app, a commentary system &mdash; on each ball, so new consumers of live score data can be added without touching the scoring logic.

9. **Q:** What is the shape of <code>Match.recordBall()</code>'s API and what does it return/update?
   **A:** <code>recordBall(Ball ball)</code> delegates to <code>currentState.recordBall(this, ball)</code>, which applies the ball to the current innings, decides whether the innings/match has ended, and returns the new <code>MatchState</code> to assign &mdash; keeping all transition logic out of <code>Match</code> itself.

10. **Q:** What does <code>Innings.isComplete()</code> check?
   **A:** Whether all ten wickets have fallen (<code>wickets &gt;= 10</code>) or the maximum overs for the format have been bowled (<code>overs.size() &gt;= maxOvers</code>) &mdash; either condition alone ends the innings.

11. **Q:** Edge case: how do WIDE and NO_BALL extras affect scoring differently from a normal run?
   **A:** Both add at least 1 extra run to the team total that is credited to neither batsman's individual tally, and the ball does not count toward the 6-ball over. A NO_BALL additionally grants the batting side a "free hit" on the next legal delivery, during which the batsman cannot be dismissed except by run-out.

12. **Q:** Edge case: when does strike rotate between the striker and non-striker batsman?
   **A:** After any ball where the batsmen complete an odd number of runs (1 or 3), and automatically at the end of every completed over (6 legal balls) &mdash; unless that same last ball of the over was also an odd-run ball, in which case the two swaps cancel out (no net rotation).

13. **Q:** Edge case: a match is interrupted by rain partway through an innings. How should the state machine represent this, and what should it explicitly avoid doing?
   **A:** Introduce a distinct <code>ABANDONED</code>/<code>INTERRUPTED</code> state separate from <code>COMPLETED</code>, so downstream consumers (results, stats) can tell a rain-shortened match apart from a normally finished one. It should NOT attempt to compute a revised target itself &mdash; Duckworth&ndash;Lewis-style recalculation is explicitly out of scope and left to a separate pluggable component.

14. **Q:** (Java) Implement the <code>MatchState</code> interface and an <code>InProgressState</code> that handles a ball and detects innings completion.
   **A:** <pre><code>public interface MatchState {
    MatchState recordBall(Match match, Ball ball);
}

public class InProgressState implements MatchState {
    @Override
    public MatchState recordBall(Match match, Ball ball) {
        match.getCurrentInnings().applyBall(ball);
        if (match.getCurrentInnings().isComplete()) {
            return match.hasSecondInningsRemaining()
                ? new InningsBreakState()
                : new CompletedState();
        }
        return this;
    }
}</code></pre>

15. **Q:** (Python) Implement an Observer-pattern <code>Scoreboard</code> subject and a <code>LiveScoreDisplay</code> listener.
   **A:** <pre><code>class Scoreboard:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify_ball(self, ball, innings):
        for observer in self._observers:
            observer.on_ball_bowled(ball, innings)


class LiveScoreDisplay:
    def on_ball_bowled(self, ball, innings):
        print(f"{innings.team.name}: {innings.total_runs}/{innings.wickets} "
              f"({innings.overs_bowled} ov) - {ball.outcome}")</code></pre>

16. **Q:** (Java) Implement <code>Innings.applyBall()</code> and <code>isComplete()</code>, handling wides/no-balls and wickets.
   **A:** <pre><code>public class Innings {
    private int totalRuns = 0;
    private int wickets = 0;
    private List&lt;Over&gt; overs = new ArrayList&lt;&gt;();

    public void applyBall(Ball ball) {
        totalRuns += ball.getRuns();
        if (ball.getExtraType() == ExtraType.WIDE || ball.getExtraType() == ExtraType.NO_BALL) {
            totalRuns += 1;
        }
        if (ball.isWicket()) {
            wickets++;
        }
        getCurrentOver().addBall(ball);
    }

    public boolean isComplete() {
        return wickets &gt;= 10 || overs.size() &gt;= maxOvers();
    }
}</code></pre>

17. **Q:** (Python) Implement strike rotation on <code>Innings</code> for odd runs and end-of-over.
   **A:** <pre><code>class Innings:
    def __init__(self, batting_team, max_overs):
        self.striker, self.non_striker = batting_team.opening_pair()
        self.max_overs = max_overs

    def apply_ball(self, ball):
        if ball.runs % 2 == 1:
            self._swap_strike()
        if ball.is_last_of_over and not ball.is_wicket:
            self._swap_strike()

    def _swap_strike(self):
        self.striker, self.non_striker = self.non_striker, self.striker</code></pre>

## Cloze cards

- The core classes in a Cricket Scoreboard design are {{c1::Match}}, {{c2::Innings}}, {{c3::Team}}, {{c4::Player}}, {{c5::Ball}} (a single delivery), and {{c6::Scoreboard}} (the live display/publisher).
- The <code>DismissalType</code> enum includes {{c1::BOWLED}}, {{c2::CAUGHT}}, {{c3::LBW}}, {{c4::RUN_OUT}}, {{c5::STUMPED}}, and {{c6::HIT_WICKET}}.
- The <code>ExtraType</code> enum for a delivery includes {{c1::WIDE}}, {{c2::NO_BALL}}, {{c3::BYE}}, and {{c4::LEG_BYE}}.
