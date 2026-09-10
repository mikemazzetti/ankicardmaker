---
deck: "System Design::Networking & Protocols (for SD)"
topic: "Networking & Protocols (for SD)"
tags: [ankicardmaker, sd-networking]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Networking & Protocols (for SD) — System Design

Source of truth for the `System Design::Networking & Protocols (for SD)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the main limitation of HTTP/1.1 that motivated HTTP/2?
   **A:** Head-of-line blocking: only one request per TCP connection can be effectively in flight at a time, forcing browsers to open many parallel connections.

2. **Q:** What key feature does HTTP/2 introduce to fix HTTP/1.1's per-connection limitation?
   **A:** Multiplexing — multiple requests and responses can be in flight concurrently over a single TCP connection.

3. **Q:** What transport protocol does HTTP/3 use instead of TCP, and why?
   **A:** QUIC, built on UDP — it avoids TCP-level head-of-line blocking and supports faster connection setup.

4. **Q:** What architectural style does REST rely on for resources and semantics?
   **A:** Resources identified by URLs, manipulated via standard HTTP methods (GET/POST/PUT/DELETE), typically with JSON payloads.

5. **Q:** What is the main advantage of gRPC over REST for internal service-to-service calls?
   **A:** It uses HTTP/2 with binary Protobuf serialization, giving lower latency and smaller payloads than JSON over HTTP/1.1.

6. **Q:** What problem does GraphQL solve that plain REST often doesn't?
   **A:** Over-fetching and under-fetching: clients specify exactly which fields they need in one query, instead of being locked to fixed REST endpoint shapes.

7. **Q:** What is a key downside of gRPC for public/browser-facing APIs?
   **A:** Limited native browser support and less human-readable payloads (binary Protobuf) compared to JSON/REST.

8. **Q:** What is long polling?
   **A:** The client repeatedly sends HTTP requests that the server holds open until new data is available (or a timeout), then the client immediately reconnects.

9. **Q:** What is Server-Sent Events (SSE)?
   **A:** A one-way, persistent HTTP connection where the server pushes a stream of text-based events to the client.

10. **Q:** What is the key advantage of WebSockets over long polling and SSE?
   **A:** WebSockets provide full-duplex (bidirectional) communication over a single persistent connection, not just server-to-client or repeated request/response.

11. **Q:** Why would you choose UDP over TCP for a service?
   **A:** When low latency matters more than guaranteed delivery and ordering — e.g. video/voice streaming or real-time gaming — since UDP skips TCP's handshake, retransmission, and ordering overhead.

12. **Q:** Why is TCP preferred over UDP for most web services?
   **A:** It guarantees reliable, ordered delivery with congestion control, which most application logic (e.g. API calls, file transfer) depends on.

13. **Q:** What is the primary role of an API gateway?
   **A:** A single entry point that routes client requests to backend services, and can centralize concerns like auth, rate limiting, and logging.

14. **Q:** Forward proxy *(reversed — both ways)*
   **A:** A proxy that sits in front of clients, forwarding their requests outward and hiding the client's identity from the destination server.

15. **Q:** Reverse proxy *(reversed — both ways)*
   **A:** A proxy that sits in front of servers, forwarding client requests to the appropriate backend and hiding the backend's identity from the client.

16. **Q:** What does 'TLS termination' at a load balancer or proxy mean?
   **A:** The proxy decrypts incoming HTTPS traffic and forwards plain HTTP to backend servers, so backends don't need to manage TLS certificates themselves.

17. **Q:** Is the HTTP GET method idempotent?
   **A:** Yes — repeating the same GET request multiple times has the same effect as making it once (no side effects).

## Cloze cards

- DNS resolution for a request typically flows: browser cache → {{c1::OS resolver cache}} → {{c2::recursive resolver (ISP or public DNS)}} → {{c3::root, TLD, and authoritative nameservers}} → IP address returned to the client.
- HTTP version progression: {{c1::HTTP/1.1}} (one request effectively in flight per connection), {{c2::HTTP/2}} (multiplexed streams over one TCP connection), {{c3::HTTP/3}} (multiplexed over QUIC/UDP, avoiding TCP-level head-of-line blocking).
- REST, {{c1::gRPC}}, and {{c2::GraphQL}} are three API styles for service communication: REST is simple and cacheable, gRPC is fast and binary for internal services, and GraphQL lets clients query exactly the fields they need.
- For real-time updates, options of increasing capability are: {{c1::long polling}} (repeated requests held open by the server), {{c2::SSE}} (persistent one-way server-to-client stream), and {{c3::WebSockets}} (persistent full-duplex connection).
- Among standard HTTP methods, {{c1::GET, PUT, and DELETE}} are idempotent (repeating them has the same effect as once), while {{c2::POST}} is generally not idempotent (repeating it can create duplicate resources).
