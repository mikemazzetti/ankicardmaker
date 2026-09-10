---
deck: "OOP Design::Meeting Scheduler"
topic: "Meeting Scheduler"
tags: [ankicardmaker, ood-meeting-scheduler]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Meeting Scheduler — OOP Design

Source of truth for the `OOP Design::Meeting Scheduler` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What five core classes typically make up a meeting scheduler system?
   **A:** Meeting, Room, User/Participant, Calendar, and TimeSlot (Interval) &mdash; Meeting ties a TimeSlot to a Room and a set of Participants; Calendar aggregates a User's Meetings.

2. **Q:** What is the responsibility of the TimeSlot (Interval) class?
   **A:** Holds a start and end timestamp and exposes an <code>overlaps(other)</code> method &mdash; the core reusable building block for all conflict-detection logic (room booking, participant double-booking, free-slot search).

3. **Q:** Why is the interval-overlap check typically written with strict '&lt;' rather than '&lt;=' at the boundaries?
   **A:** So a meeting ending exactly when another starts (e.g. 10:00-11:00 and 11:00-12:00) is NOT treated as a conflict &mdash; using '&lt;=' would incorrectly flag back-to-back, non-overlapping meetings as conflicting.

4. **Q:** Calendar *(reversed — both ways)*
   **A:** Per-User class holding that user's Meetings, used to answer 'is this user free at time T' and to compute free slots for scheduling.

5. **Q:** What enum models how a Meeting repeats, and what values does it hold?
   **A:** RecurrenceType: NONE, DAILY, WEEKLY, MONTHLY (sometimes CUSTOM with an explicit rule).

6. **Q:** What is the core algorithmic technique for detecting a room double-booking against N existing bookings efficiently, rather than a full O(n) linear scan each time?
   **A:** Keep each Room's bookings in a sorted structure ordered by start time (e.g. a TreeMap/balanced BST or interval tree); to check a new [start, end), look up the closest existing bookings around start and only compare against those neighbors &mdash; O(log n) instead of O(n).

7. **Q:** What data structure gives true O(log n) overlap queries for arbitrary insert/delete of many intervals, and why is it better than a simple sorted list for a busy scheduler?
   **A:** An interval tree (each node stores an interval plus the max endpoint in its subtree) &mdash; unlike a sorted-by-start list, it supports efficient overlap queries even when intervals have very different lengths, without scanning past every interval that starts before the query but ends after it starts.

8. **Q:** Which design fits expanding a recurring Meeting (WEEKLY, ends after N occurrences) into concrete Meeting instances, and why?
   **A:** Strategy pattern for recurrence expansion: each RecurrenceType (DAILY/WEEKLY/MONTHLY) implements a common <code>RecurrenceStrategy.nextOccurrences(start, rule)</code> interface, so SchedulerService doesn't need type-specific branching to generate instances.

9. **Q:** Why can't a recurring Meeting simply be stored as N separate Meeting rows generated once and forgotten?
   **A:** Individual occurrences can be modified independently (one instance moved, cancelled, or renamed without affecting the series) &mdash; the classic 'edit this event / this and following / all events' problem, requiring either exception records per-instance or storing the recurrence rule and materializing occurrences on read with an override list.

10. **Q:** What edge case makes finding a common free slot among N participants harder than checking one person's calendar?
   **A:** You must intersect the free time of ALL participants &mdash; a slot is only valid if it doesn't overlap ANY participant's existing meetings, so the algorithm merges each participant's busy intervals, then finds gaps common to every participant's free-time list (an intersection of free intervals, not a union).

11. **Q:** Why must all Meeting start/end times be normalized to a single reference (e.g. stored in UTC) rather than each participant's local time?
   **A:** Participants may be in different timezones; comparing raw local times without a common reference would misclassify overlaps/conflicts. Store timestamps in UTC internally and convert to each participant's local timezone only for display.

12. **Q:** Should a User be allowed to be double-booked (two overlapping meetings on their own calendar), and how should the design decide?
   **A:** It's a policy decision, not purely technical: tentative meetings may be allowed to overlap so the user can choose later, but the SchedulerService should expose the conflict via <code>hasConflict(user, timeslot)</code> so the caller (UI) can warn or block, rather than silently allowing or silently rejecting.

13. **Q:** What API method would a client call to schedule a new meeting, and what should it check before creating it?
   **A:** <code>scheduleMeeting(User organizer, List&lt;User&gt; participants, Room room, TimeSlot slot)</code> &mdash; must check the Room isn't already booked for an overlapping slot AND that no required participant already has a conflicting Meeting (or degrade gracefully to a warning for optional attendees).

14. **Q:** What API method finds open slots for a group, and what parameters does it need?
   **A:** <code>findAvailableSlots(List&lt;User&gt; participants, Duration duration, DateRange searchWindow)</code> &mdash; returns a list of TimeSlots of at least <code>duration</code> where every participant is free within <code>searchWindow</code>.

15. **Q:** When cancelling one occurrence of a recurring Meeting, what should the system NOT do?
   **A:** It should not cancel the entire recurring series &mdash; it must create/mark an exception for just that single occurrence, leaving the rest of the recurrence rule and its future/past instances untouched.

16. **Q:** Java: implement a <code>TimeSlot.overlaps(other)</code> method using the strict-inequality interval overlap check.
   **A:** <pre><code>import java.time.LocalDateTime;

class TimeSlot {
    private final LocalDateTime start;
    private final LocalDateTime end;

    public TimeSlot(LocalDateTime start, LocalDateTime end) {
        this.start = start;
        this.end = end;
    }

    public LocalDateTime getStart() { return start; }
    public LocalDateTime getEnd() { return end; }

    public boolean overlaps(TimeSlot other) {
        return this.start.isBefore(other.end) &amp;&amp; other.start.isBefore(this.end);
    }
}</code></pre>

17. **Q:** Python: write <code>find_free_slots(busy_intervals, window_start, window_end, min_duration)</code> that returns gaps of at least min_duration between sorted busy intervals.
   **A:** <pre><code>def find_free_slots(busy_intervals, window_start, window_end, min_duration):
    intervals = sorted(busy_intervals)
    free_slots = []
    cursor = window_start

    for start, end in intervals:
        if start &gt; cursor and (start - cursor) &gt;= min_duration:
            free_slots.append((cursor, start))
        cursor = max(cursor, end)

    if window_end &gt; cursor and (window_end - cursor) &gt;= min_duration:
        free_slots.append((cursor, window_end))

    return free_slots</code></pre>

18. **Q:** Java: implement a <code>Room</code> class backed by a TreeMap of bookings that checks only its nearest neighbors for an overlap in <code>isAvailable(requested)</code>.
   **A:** <pre><code>import java.time.LocalDateTime;
import java.util.Map;
import java.util.TreeMap;

class Room {
    private final TreeMap&lt;LocalDateTime, TimeSlot&gt; bookingsByStart = new TreeMap&lt;&gt;();

    public boolean isAvailable(TimeSlot requested) {
        Map.Entry&lt;LocalDateTime, TimeSlot&gt; before = bookingsByStart.floorEntry(requested.getStart());
        Map.Entry&lt;LocalDateTime, TimeSlot&gt; after = bookingsByStart.ceilingEntry(requested.getStart());

        if (before != null &amp;&amp; before.getValue().overlaps(requested)) return false;
        if (after != null &amp;&amp; after.getValue().overlaps(requested)) return false;
        return true;
    }

    public void book(TimeSlot slot) {
        bookingsByStart.put(slot.getStart(), slot);
    }
}</code></pre>

19. **Q:** Python: write <code>expand_weekly(first_start, first_end, occurrences)</code> that generates the (start, end) tuples for a weekly recurring meeting.
   **A:** <pre><code>from datetime import timedelta

def expand_weekly(first_start, first_end, occurrences):
    meetings = []
    for i in range(occurrences):
        offset = timedelta(weeks=i)
        meetings.append((first_start + offset, first_end + offset))
    return meetings</code></pre>

## Cloze cards

- Two time intervals [start1, end1) and [start2, end2) overlap if and only if {{c1::start1 &lt; end2}} AND {{c2::start2 &lt; end1}}.
