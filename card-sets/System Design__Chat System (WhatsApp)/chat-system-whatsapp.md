---
deck: "System Design::Chat System (WhatsApp)"
topic: "Chat System (WhatsApp)"
tags: [ankicardmaker, sd-chat]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Chat System (WhatsApp) — System Design

Source of truth for the `System Design::Chat System (WhatsApp)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Should a chat system support offline message delivery (a user receives messages sent while they were offline)?
   **A:** Yes &mdash; messages sent to an offline user must be stored and delivered once they reconnect, not dropped.

2. **Q:** Why is strong consistency (not just eventual consistency) important for message ordering within a single conversation?
   **A:** Users expect messages within a chat to appear in a consistent, logical order for all participants &mdash; out-of-order messages break conversational meaning, so per-conversation ordering is a strict requirement even though other parts of the system can be eventually consistent.

3. **Q:** If 500M daily active users send 40 messages/day on average, what is the approximate write QPS for messages?
   **A:** ~230,000 QPS (500M &times; 40 / 86,400 &asymp; 231,481).

4. **Q:** If the average message is 100 bytes and 20B messages are sent per day, what is the daily storage for message content?
   **A:** ~2 TB/day (20,000,000,000 &times; 100 bytes = 2&times;10^12 bytes = 2 TB).

5. **Q:** Why must a chat system also estimate the number of concurrent open WebSocket connections, not just message QPS?
   **A:** Delivery requires a persistent connection per online user; connection count (not just message rate) determines how many connection-handling servers are needed, since each server can hold only a limited number of open sockets (e.g. ~1M per host).

6. **Q:** Write the WebSocket message format a client sends to deliver a chat message.
   **A:** <pre><code>// WS message (client -&gt; server)
{
  "type": "MESSAGE",
  "senderId": "string",
  "receiverId": "string",
  "text": "string",
  "clientMsgId": "string"
}</code></pre>

7. **Q:** Write the REST endpoint to fetch message history for a conversation.
   **A:** <pre><code>GET /api/v1/conversations/{id}/messages?cursor={cursor}&amp;limit={n}
Response: { "messages": [ {...} ], "nextCursor": "string" }</code></pre>

8. **Q:** Write a minimal schema for a <code>messages</code> table.
   **A:** <pre><code>messages(
  message_id      BIGINT,
  conversation_id BIGINT,
  sender_id       BIGINT,
  text            TEXT,
  sent_at         TIMESTAMP,
  PRIMARY KEY (conversation_id, message_id)
)</code></pre>

9. **Q:** Why is conversation_id typically the partition/shard key for the messages table rather than message_id?
   **A:** All reads for a chat fetch messages by conversation, so partitioning by conversation_id keeps a conversation's messages colocated for fast range queries, and naturally shards load across many conversations.

10. **Q:** Why can't a single application server just hold every user's WebSocket connection directly wired to the message-processing logic?
   **A:** Connections must be spread across many gateway servers for scale, so the system needs a way to route a message to whichever gateway server currently holds the recipient's connection (e.g. a connection-registry lookup, often in Redis) rather than assuming all logic is co-located.

11. **Q:** Why is WebSocket preferred over HTTP polling for real-time chat delivery?
   **A:** WebSocket keeps a single persistent, full-duplex connection open, letting the server push messages instantly with minimal overhead, whereas polling repeatedly opens/closes connections and adds latency between poll intervals plus wasted requests when there's nothing new.

12. **Q:** How does the server know which gateway server holds a given user's active WebSocket connection?
   **A:** A connection registry (e.g. in Redis) maps user_id &rarr; the gateway server/host currently holding their socket; when routing a message, the message service looks up the registry to forward it to the correct gateway.

13. **Q:** How is a message typically delivered to a recipient who is currently offline?
   **A:** It's persisted in the message store and queued; when the recipient's client reconnects and opens a WebSocket, the server pushes/syncs any undelivered messages from storage.

14. **Q:** How is online/presence status typically tracked and propagated in a chat system?
   **A:** A presence service keeps a heartbeat/TTL entry per user (e.g. in Redis) refreshed while their WebSocket is connected; when a user's status changes, the service notifies their contacts (e.g. via pub/sub) so clients can update the shown status.

15. **Q:** Why is presence status usually eventually consistent rather than strongly consistent?
   **A:** Propagating exact real-time online/offline status to every contact instantly at strong consistency would be costly at scale, and a brief lag (a second or two) in showing 'online'/'last seen' is an acceptable UX tradeoff for much lower system overhead.

16. **Q:** Why is a message queue (e.g. Kafka) often placed between the gateway and the message-persistence/delivery logic?
   **A:** It decouples ingestion from processing/fanout to group members, absorbing traffic bursts and letting the persistence and delivery services scale and retry independently without blocking the sender's connection.

17. **Q:** What is the tradeoff of storing full message history indefinitely vs. only recent messages?
   **A:** Storing full history preserves complete conversation context and search but grows storage cost indefinitely; limiting retention (e.g. archiving/cold-storing old messages) saves cost and keeps hot storage fast, at the cost of slower or unavailable access to old messages.

## Cloze cards

- Core functional requirements of a WhatsApp-like chat system include: {{c1::sending and receiving 1:1 messages}}, {{c2::group messaging}}, and {{c3::message delivery/read status}}.
- Non-functional requirements for a chat system include: {{c1::low latency message delivery (near real-time)}}, {{c2::high availability}}, and {{c3::message ordering should be preserved per conversation}}.
- The high-level architecture of a chat system typically includes: {{c1::a connection/gateway service managing WebSocket connections}}, {{c2::a message service that stores and routes messages}}, {{c3::a presence service tracking online status}}, and {{c4::a message queue (e.g. Kafka) between services}}.
- The three standard message states in a chat system's delivery/read-receipt model are: {{c1::sent (single check &mdash; left the sender's client)}}, {{c2::delivered (double check &mdash; reached the recipient's device)}}, and {{c3::read (blue double check &mdash; recipient opened it)}}.
- Scaling bottlenecks and fixes for a chat system: {{c1::a single server capping the number of concurrent WebSocket connections}} is fixed by {{c2::horizontally scaling gateway servers behind a connection registry}}; {{c3::message store write/read hotspots for very active conversations}} is fixed by {{c4::sharding messages by conversation_id and caching recent messages}}.
