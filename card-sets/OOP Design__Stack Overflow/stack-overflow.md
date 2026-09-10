---
deck: "OOP Design::Stack Overflow"
topic: "Stack Overflow"
tags: [ankicardmaker, ood-stack-overflow]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Stack Overflow — OOP Design

Source of truth for the `OOP Design::Stack Overflow` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What four core content classes make up the Stack Overflow domain model, from question to smallest unit of interaction?
   **A:** Question, Answer, Comment, and Vote (Question/Answer are top-level Posts; Comment and Vote attach to a Post).

2. **Q:** Why do Question and Answer often share a common abstract base class like Post?
   **A:** Both have a body, an author, a creation timestamp, a list of Comments, and a set of Votes &mdash; factoring that into a Post superclass avoids duplicating fields/logic (voting, commenting) in two places.

3. **Q:** Vote *(reversed — both ways)*
   **A:** Class recording one User's UPVOTE or DOWNVOTE on a specific Post, used both to rank content and to drive reputation changes; typically unique per (user, post) pair.

4. **Q:** What enum models whether a vote is positive or negative, and what values does it hold?
   **A:** VoteType: UPVOTE, DOWNVOTE.

5. **Q:** Which design pattern fits notifying a User when their Question gets a new Answer or Comment, and why?
   **A:** Observer: Question (the subject) maintains a list of subscribed Users (observers); posting a new Answer/Comment triggers <code>notifyObservers()</code>, decoupling the posting logic from however notifications are delivered (email, in-app, push).

6. **Q:** In the Observer-based notification design, who typically subscribes to a Question automatically?
   **A:** The question's author, anyone who answered it, and anyone who commented on it or explicitly followed/starred the question.

7. **Q:** Which design pattern fits computing reputation changes for different actions (question upvoted, answer accepted, downvote received), and why?
   **A:** Strategy: encapsulate each action's reputation delta (and rules) behind a common interface, e.g. <code>ReputationRule.apply(User)</code>, so ReputationService just looks up and applies the right rule for a given event instead of a long if/else chain.

8. **Q:** Why must self-voting be explicitly disallowed, and where should that check live?
   **A:** A User upvoting their own Question/Answer would let them farm reputation; the check belongs in the <code>vote()</code> method/service, comparing the voter's ID to the Post's author ID before recording the Vote.

9. **Q:** What must happen to a User's reputation and the Vote record when a User changes their vote from UPVOTE to DOWNVOTE on the same post?
   **A:** The system must find and update the existing Vote row (not insert a duplicate) and apply the FULL delta swing (e.g. remove the +10 from the old upvote AND apply the -2 for the new downvote) so the net reputation change is correct, not additive.

10. **Q:** Who is allowed to call acceptAnswer(), and what invariant should the system enforce?
   **A:** Only the original author of the Question. Invariant: at most one Answer per Question can be marked accepted at a time &mdash; accepting a new one un-accepts any previous one.

11. **Q:** Should a User's reputation be allowed to go negative, and how do real systems usually handle this edge case?
   **A:** No &mdash; reputation typically has a floor (e.g. minimum 1), so a barrage of downvotes can't push a user below a baseline; the ReputationService should clamp the value rather than letting it go negative.

12. **Q:** What responsibility does a BadgeService (or badge-check routine) have, and when does it typically run?
   **A:** Checks whether a User's stats (reputation, answer count, accepted-answer count, etc.) cross a threshold for a Badge (e.g. 'Great Answer' at 100 upvotes on one answer) and awards it &mdash; typically run as a side effect after a reputation-affecting event, like an Observer reacting to a Vote.

13. **Q:** What API method posts a new answer, and what should it validate before accepting it?
   **A:** <code>postAnswer(User author, String questionId, String body)</code> &mdash; should validate the Question exists and is OPEN (not CLOSED/DELETED) before allowing a new Answer.

14. **Q:** Why is Vote uniqueness per (User, Post) important to enforce at the data layer, not just in application code?
   **A:** Without a uniqueness constraint (e.g. a composite key or unique index on user_id+post_id), a race condition or bug could let the same user cast multiple votes on the same post, corrupting both the score and reputation calculations.

15. **Q:** Java: implement the Observer pattern so a <code>Question</code> notifies subscribed observers whenever a new Answer is added.
   **A:** <pre><code>import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

interface QuestionObserver {
    void onNewAnswer(Question question, Answer answer);
}

class Question {
    private final Set&lt;QuestionObserver&gt; observers = new HashSet&lt;&gt;();
    private final List&lt;Answer&gt; answers = new ArrayList&lt;&gt;();

    public void subscribe(QuestionObserver observer) {
        observers.add(observer);
    }

    public void addAnswer(Answer answer) {
        answers.add(answer);
        for (QuestionObserver observer : observers) {
            observer.onNewAnswer(this, answer);
        }
    }
}</code></pre>

16. **Q:** Python: implement <code>cast_vote(post, user, vote_type, votes_by_user)</code> that correctly handles a user changing their existing vote on a post.
   **A:** <pre><code>class VoteType:
    UPVOTE = "UPVOTE"
    DOWNVOTE = "DOWNVOTE"

VOTE_VALUE = {VoteType.UPVOTE: 1, VoteType.DOWNVOTE: -1}

def cast_vote(post, user, vote_type, votes_by_user):
    existing = votes_by_user.get((user.id, post.id))

    if existing == vote_type:
        return  # no-op, same vote already recorded

    if existing is not None:
        post.score -= VOTE_VALUE[existing]  # undo the old vote

    post.score += VOTE_VALUE[vote_type]
    votes_by_user[(user.id, post.id)] = vote_type</code></pre>

17. **Q:** Java: implement the Strategy pattern for reputation changes using an enum of ReputationEvent values, applied via a ReputationService that clamps the floor at 1.
   **A:** <pre><code>interface ReputationRule {
    int delta();
}

enum ReputationEvent implements ReputationRule {
    QUESTION_UPVOTED(5),
    ANSWER_UPVOTED(10),
    ANSWER_ACCEPTED(15),
    ANSWER_DOWNVOTED(-2);

    private final int points;
    ReputationEvent(int points) { this.points = points; }

    @Override
    public int delta() { return points; }
}

class ReputationService {
    public void apply(User user, ReputationRule event) {
        int newRep = user.getReputation() + event.delta();
        user.setReputation(Math.max(newRep, 1));
    }
}</code></pre>

18. **Q:** Python: implement a <code>vote(post, voter, vote_type, votes_by_user)</code> wrapper that raises a SelfVoteError if a user tries to vote on their own post.
   **A:** <pre><code>class SelfVoteError(Exception):
    pass

def vote(post, voter, vote_type, votes_by_user):
    if post.author_id == voter.id:
        raise SelfVoteError("Users cannot vote on their own posts")
    cast_vote(post, voter, vote_type, votes_by_user)</code></pre>

## Cloze cards

- A Question, unlike an Answer, additionally has a {{c1::title}}, a set of {{c2::Tags}}, and a reference to its {{c3::accepted Answer}} (nullable until answered).
- Typical Stack-Overflow-style reputation deltas: question upvote {{c1::+5}}, answer upvote {{c2::+10}}, answer accepted {{c3::+15}}, downvote received {{c4::-2}}. <!-- Extra: Exact numbers vary by implementation &mdash; the point is each action maps to a distinct, encapsulated rule. -->
