---
deck: "System Design::Scalability & Load Balancing"
topic: "Scalability & Load Balancing"
tags: [ankicardmaker, sd-load-balancing]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Scalability & Load Balancing — System Design

Source of truth for the `System Design::Scalability & Load Balancing` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is vertical scaling?
   **A:** Increasing the capacity of a single server (more CPU, RAM, disk) rather than adding more servers.

2. **Q:** What is horizontal scaling?
   **A:** Adding more servers/nodes to distribute load, rather than upgrading a single server.

3. **Q:** Why must a service be stateless to scale horizontally behind a load balancer?
   **A:** Because any request can be routed to any instance; if session state lived only on one server, requests routed elsewhere would lose access to it.

4. **Q:** Stateless service *(reversed — both ways)*
   **A:** A service instance that stores no client session data between requests, so any instance can handle any request.

5. **Q:** What does an L4 (transport-layer) load balancer route on?
   **A:** IP address and TCP/UDP port — it does not inspect HTTP content.

6. **Q:** What does an L7 (application-layer) load balancer route on?
   **A:** HTTP-level content such as URL path, headers, cookies, or hostname.

7. **Q:** L4 load balancer *(reversed — both ways)*
   **A:** A load balancer that routes based on IP address and port at the transport layer; fast, but blind to request content.

8. **Q:** Why is an L4 load balancer generally faster than L7?
   **A:** It only inspects packet headers (IP/port), not the application payload, so there is less processing per request.

9. **Q:** When is 'least connections' a better load-balancing choice than round robin?
   **A:** When requests have highly variable processing times, so an equal request count per server doesn't mean equal server load.

10. **Q:** What property does IP-hash load balancing give you, and why is it useful?
   **A:** It routes a given client IP to the same server consistently, which gives session affinity without needing a shared session store.

11. **Q:** What is a health check in a load-balancing context?
   **A:** A periodic probe (e.g. an HTTP ping to /health) the load balancer sends to each backend to detect and stop routing to unhealthy instances.

12. **Q:** What is a 'sticky session'?
   **A:** A load-balancer configuration that routes all requests from a given client to the same backend server, typically via a cookie.

13. **Q:** What is the main downside of sticky sessions?
   **A:** They undermine even load distribution and complicate failover — if that server goes down, the client's locally stored session state is lost.

14. **Q:** Why is a single load balancer a single point of failure (SPOF)?
   **A:** If it goes down, no traffic can reach any backend server, even if all backends are healthy.

15. **Q:** How do you eliminate the load balancer itself as a single point of failure?
   **A:** Run redundant load balancers (active-passive or active-active) with a failover mechanism, e.g. DNS failover or a floating/virtual IP.

16. **Q:** What is autoscaling?
   **A:** Automatically adding or removing server instances based on real-time load (e.g. CPU, request rate) to match capacity to demand.

17. **Q:** What metrics commonly trigger autoscaling out (adding instances)?
   **A:** CPU utilization, request latency, or queue length exceeding a defined threshold.

## Cloze cards

- Vertical scaling has a hard ceiling because a single machine's {{c1::hardware capacity}} is finite, while horizontal scaling can add {{c2::more machines}} almost indefinitely.
- To make a service stateless, session data is typically moved out of server memory into {{c1::a shared store (e.g. Redis) or the client itself (e.g. a JWT token)}}.
- A load balancer's core jobs: {{c1::distribute traffic across backend servers}}, {{c2::health-check backends and route around failures}}, and {{c3::provide a single stable entry point (often handling TLS termination)}}.
- Common load-balancing algorithms: {{c1::round robin}} (cycles through servers in order), {{c2::least connections}} (sends traffic to the server with the fewest active connections), {{c3::IP hash}} (routes based on client IP for consistency), and {{c4::weighted}} (biases distribution toward more capable servers).
- A {{c1::load balancer}} distributes traffic across multiple backend servers, while a {{c2::reverse proxy}} sits in front of one or more servers handling things like caching or TLS termination — a load balancer is essentially a reverse proxy specialized for traffic distribution.
