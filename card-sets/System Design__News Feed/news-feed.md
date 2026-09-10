---
deck: "System Design::News Feed"
topic: "News Feed"
tags: [ankicardmaker, sd-news-feed]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# News Feed — System Design

Source of truth for the `System Design::News Feed` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Besides posts, what other actions typically need to be reflected in a news feed's ranking?
   **A:** Engagement signals such as likes, comments, and shares, which feed into the ranking algorithm to prioritize relevant content.

2. **Q:** Why must feed-generation latency stay low even though ranking is computationally complex?
   **A:** Feed load time directly affects user engagement and retention &mdash; a slow feed causes users to abandon the app &mdash; so systems precompute/cache ranked feeds rather than ranking fully on every request.

3. **Q:** If there are 500M daily active users and each loads their feed 10 times/day, what is the approximate feed-read QPS?
   **A:** ~58,000 QPS (500M &times; 10 / 86,400 &asymp; 57,870).

4. **Q:** If each user has on average 300 friends/follows, why does fanout-on-write become expensive for a news feed system?
   **A:** Every post triggers up to 300 fanout writes (one per friend's feed), so total fanout write volume = posts/day &times; average friend count, which can be orders of magnitude larger than the raw post-write volume.

5. **Q:** Estimate storage for 100M posts/day retained for 2 years at ~1KB metadata per post.
   **A:** 100M &times; 730 days &times; 1KB &asymp; 73 TB of post metadata over 2 years.

6. **Q:** Write the REST endpoint to create a new feed post.
   **A:** <pre><code>POST /api/v1/posts
Request: { "userId": "string", "content": "string", "mediaUrls": ["string"] }
Response: { "postId": "string", "createdAt": "datetime" }</code></pre>

7. **Q:** Write the REST endpoint to fetch a user's ranked news feed.
   **A:** <pre><code>GET /api/v1/feed?userId={id}&amp;cursor={cursor}&amp;limit={n}
Response: { "posts": [ {...ranked...} ], "nextCursor": "string" }</code></pre>

8. **Q:** Write a minimal schema for a <code>feed_items</code> table storing a precomputed per-user feed.
   **A:** <pre><code>feed_items(
  user_id     BIGINT,
  post_id     BIGINT,
  rank_score  DOUBLE,
  inserted_at TIMESTAMP,
  PRIMARY KEY (user_id, post_id)
)</code></pre>

9. **Q:** Why store a rank_score alongside each feed item rather than always ranking purely by recency?
   **A:** It lets the feed service sort by relevance (predicted engagement) instead of just chronological order, and allows re-sorting without recomputing the score from scratch on every read.

10. **Q:** Where does ranking typically happen &mdash; at fanout/write time, at read time, or both?
   **A:** Both: an initial score can be computed at fanout time for pre-ranking, but feeds are often re-ranked at read time with fresh signals (recent engagement, freshness decay) before being returned to the user.

11. **Q:** Fanout-on-write (news feed context) *(reversed — both ways)*
   **A:** New posts are immediately pushed into the precomputed feed_items list of every friend/follower at post time, so feed reads are fast lookups.

12. **Q:** Fanout-on-read (news feed context) *(reversed — both ways)*
   **A:** A user's feed is assembled at read time by pulling recent posts from all friends/followed entities and ranking them on the fly, so writes stay cheap but reads are more expensive.

13. **Q:** How does the celebrity/high-degree-node problem apply to a news feed system beyond just followers?
   **A:** A single post from a page or user with millions of followers triggers a huge fanout burst; symmetrically, a user who follows an unusually large number of entities makes fanout-on-read expensive too, since their feed read must pull and rank from many sources.

14. **Q:** What is the standard hybrid fix for the celebrity problem in a news feed system?
   **A:** Push (fanout-on-write) for normal accounts with modest follower counts, and pull (fanout-on-read) for high-follower accounts &mdash; merging the precomputed feed with a live query against celebrity posts at read time.

15. **Q:** Why is ranking (not just fanout mechanism) a distinguishing deep-dive topic for news feed vs. a simple chronological timeline?
   **A:** A news feed's core value is surfacing the most relevant content, not just the newest, so the system needs a ranking/scoring model (using signals like affinity, engagement rate, recency decay) layered on top of whichever fanout strategy is used.

16. **Q:** How does sharding the social graph service help scale a news feed system?
   **A:** Friend/follow lookups (needed for fanout and feed assembly) are extremely frequent; sharding the graph store (e.g. by user_id) spreads this load across many nodes instead of bottlenecking on one graph database.

17. **Q:** What is the tradeoff of caching precomputed feeds in Redis vs. always computing feeds fresh from the database?
   **A:** Caching gives much faster reads and lower DB load, but risks showing slightly stale content and requires cache invalidation/update logic whenever new posts or engagement signals arrive.

18. **Q:** Why might a news feed system accept a ranking model that is 'good enough' rather than a fully real-time ML re-rank on every request?
   **A:** Full real-time ML inference on every feed load for every candidate post would add significant latency and compute cost; a precomputed/cached approximate ranking, refreshed periodically, is a pragmatic tradeoff between relevance quality and system performance.

## Cloze cards

- Core functional requirements of a news feed system include: {{c1::users can create posts}}, {{c2::users can see a feed of posts from friends/followed entities}}, and {{c3::the feed can be ranked, not just chronological}}.
- Non-functional requirements for a news feed system include: {{c1::low latency feed load (e.g. &lt;2s)}}, {{c2::high availability}}, and {{c3::eventual consistency is acceptable for feed freshness}}.
- The high-level architecture of a news feed system typically includes: {{c1::a post/write service}}, {{c2::a fanout service}}, {{c3::a ranking service}}, {{c4::a feed cache (e.g. Redis) storing precomputed feed items}}, and {{c5::a graph service for friend/follow relationships}}.
- Scaling bottlenecks and fixes for a news feed system: {{c1::fanout write amplification for high-degree accounts}} is fixed by {{c2::the hybrid push/pull model}}; {{c3::ranking computation being too slow at read time}} is fixed by {{c4::precomputing/caching scores and only re-ranking with lightweight fresh signals at read time}}.
