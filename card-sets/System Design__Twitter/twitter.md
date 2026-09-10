---
deck: "System Design::Twitter"
topic: "Twitter"
tags: [ankicardmaker, sd-twitter]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Twitter — System Design

Source of truth for the `System Design::Twitter` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Should a Twitter-like system support near real-time delivery of new tweets to followers' feeds?
   **A:** Yes &mdash; near real-time feed updates are expected as a functional requirement, typically within a few seconds of posting.

2. **Q:** Why does a Twitter-like system favor availability and eventual consistency over strong consistency?
   **A:** Feeds are read-heavy and users tolerate a few seconds of staleness in seeing new tweets, but not downtime &mdash; so the system is designed AP under CAP, using eventual consistency for feed propagation.

3. **Q:** If a system has 200M daily active users posting 2 tweets/day on average, what is the approximate tweet-write QPS?
   **A:** ~4,600 QPS (200M &times; 2 / 86,400 &asymp; 4,630).

4. **Q:** If each user checks their timeline 5 times/day and there are 200M DAU, what is the approximate read QPS for timeline requests?
   **A:** ~11,600 QPS (200M &times; 5 / 86,400 &asymp; 11,574).

5. **Q:** Why is the read:write ratio for a social feed system typically very high (e.g. 100:1 or more)?
   **A:** Far more users scroll/read feeds than post content, so read traffic (timeline fetches) vastly outweighs write traffic (new tweets).

6. **Q:** Write the REST endpoint to post a new tweet.
   **A:** <pre><code>POST /api/v1/tweets
Request: { "userId": "string", "text": "string", "mediaUrls": ["string"] }
Response: { "tweetId": "string", "createdAt": "datetime" }</code></pre>

7. **Q:** Write the REST endpoint to fetch a user's home timeline.
   **A:** <pre><code>GET /api/v1/timeline?userId={id}&amp;cursor={cursor}&amp;limit={n}
Response: { "tweets": [ {...} ], "nextCursor": "string" }</code></pre>

8. **Q:** Write a minimal schema for the <code>tweets</code> table.
   **A:** <pre><code>tweets(
  tweet_id   BIGINT PRIMARY KEY,
  user_id    BIGINT,
  text       VARCHAR(280),
  media_urls TEXT[],
  created_at TIMESTAMP
)</code></pre>

9. **Q:** Write a minimal schema for the <code>follows</code> table modeling the social graph.
   **A:** <pre><code>follows(
  follower_id BIGINT,
  followee_id BIGINT,
  created_at  TIMESTAMP,
  PRIMARY KEY (follower_id, followee_id)
)</code></pre>

10. **Q:** Why is it useful to also index <code>follows</code> by followee_id (a reverse index)?
   **A:** The fanout-on-write process needs to quickly find all followers of a user who just tweeted, which requires querying by followee_id &mdash; a forward-only index on follower_id can't serve that efficiently.

11. **Q:** Why is a message queue placed between tweet creation and the fanout service?
   **A:** It decouples ingestion from fanout so tweet writes return quickly, and lets the fanout service process work asynchronously and absorb bursts without blocking writers.

12. **Q:** Fanout-on-write (push model) *(reversed — both ways)*
   **A:** When a user tweets, the tweet is immediately pushed into the precomputed timeline/inbox of every follower, so reads are fast (just fetch the precomputed list).

13. **Q:** Fanout-on-read (pull model) *(reversed — both ways)*
   **A:** A user's timeline is assembled at read time by querying and merging tweets from everyone they follow, so writes are cheap but reads are more expensive.

14. **Q:** What is the main tradeoff between fanout-on-write and fanout-on-read?
   **A:** Fanout-on-write makes reads fast but writes expensive (and wastes work fanning out to inactive followers); fanout-on-read makes writes cheap but reads slow/expensive, especially for users who follow many people.

15. **Q:** What is the 'celebrity problem' in feed fanout design?
   **A:** A user with millions of followers (e.g. a celebrity) triggers fanout-on-write to millions of inboxes per tweet, creating a massive write spike and hot-key pressure that can overwhelm the fanout system.

16. **Q:** What is the standard hybrid solution to the celebrity problem?
   **A:** Use fanout-on-write for regular users, but fanout-on-read (pull) for celebrities/high-follower accounts &mdash; at read time, merge the follower's precomputed timeline with a live query of tweets from any celebrities they follow.

17. **Q:** How does caching precomputed timelines in Redis help scale feed reads?
   **A:** It avoids recomputing/merging tweets from all followees on every read, serving most timeline requests directly from an in-memory cache, cutting database load and latency dramatically.

18. **Q:** Why does a Twitter-like system accept eventual consistency for the timeline instead of strong consistency?
   **A:** Strong consistency across a globally distributed, fanned-out feed system would add significant write latency and reduce availability; a few seconds of delay before a tweet appears in followers' feeds is an acceptable UX tradeoff for much higher throughput and availability.

## Cloze cards

- Core functional requirements of a Twitter-like system include: {{c1::users can post tweets (text, optionally media)}}, {{c2::users can follow other users}}, and {{c3::users can view a timeline/feed of tweets from people they follow}}.
- Non-functional requirements for Twitter-scale systems include: {{c1::high availability}}, {{c2::low read latency for feed generation}}, and {{c3::eventual consistency is acceptable (a slightly stale feed is fine)}}.
- The high-level architecture of a Twitter-like system typically includes: {{c1::a tweet/write service}}, {{c2::a fanout/timeline-generation service}}, {{c3::a cache (e.g. Redis) storing precomputed timelines}}, and {{c4::a message queue between the write and fanout services}}.
- Scaling bottlenecks and fixes for a Twitter-like feed system: {{c1::the tweets table growing huge}} is fixed by {{c2::sharding by user_id or tweet_id}}; {{c3::fanout write amplification for celebrities}} is fixed by {{c4::the hybrid push/pull model}}.
