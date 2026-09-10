---
deck: "Resume Prep::Networking"
topic: "Networking"
tags: [ankicardmaker, networking]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Networking — Resume Prep

Source of truth for the `Resume Prep::Networking` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Which transport-layer protocol is connection-oriented and guarantees reliable, ordered delivery of data?
   **A:** TCP (Transmission Control Protocol)

2. **Q:** Which transport-layer protocol is connectionless and favors speed over guaranteed delivery, making it common for streaming, DNS, and VoIP?
   **A:** UDP (User Datagram Protocol)

3. **Q:** How many bits make up an IPv4 address?
   **A:** 32 bits (four 8-bit octets)

4. **Q:** What does a subnet mask do?
   **A:** It divides an IP address into a network portion and a host portion, determining which addresses belong to the same local subnet.

5. **Q:** In CIDR notation like 192.168.1.0/24, what does the "/24" mean?
   **A:** The first 24 bits of the address are the network portion, leaving 8 bits (256 addresses) for hosts on that subnet.

6. **Q:** What does HTTPS add on top of HTTP?
   **A:** TLS/SSL encryption of the connection, providing confidentiality, integrity, and server authentication for the HTTP traffic.

7. **Q:** What's the difference between a port and a socket?
   **A:** A port is a number (0-65535) identifying a specific application/service on a host; a socket is the combination of an IP address and a port number that identifies one endpoint of a specific network connection.

8. **Q:** What does NAT (Network Address Translation) do?
   **A:** It translates private IP addresses used on a local network into a single public IP address (and back), letting multiple devices share one public IP for internet access.

9. **Q:** What does DHCP do?
   **A:** It automatically assigns IP addresses and network configuration (subnet mask, gateway, DNS servers) to devices joining a network, without manual setup.

10. **Q:** What does ARP (Address Resolution Protocol) do?
   **A:** It resolves a known IPv4 address to the corresponding MAC (hardware) address on the local network segment.

11. **Q:** What is "latency" in networking?
   **A:** The time delay for a piece of data to travel from sender to receiver, often measured as round-trip time.

12. **Q:** What is "bandwidth" in networking?
   **A:** The maximum theoretical rate at which data could be transferred over a connection, e.g. measured in Mbps.

13. **Q:** How does "throughput" differ from "bandwidth"?
   **A:** Throughput is the actual rate of data successfully transferred over a connection in practice, which is often lower than the connection's theoretical maximum bandwidth due to congestion, overhead, or errors.

14. **Q:** How does TCP's congestion control avoid overwhelming the network?
   **A:** It starts with a small congestion window (slow start) and increases it as ACKs confirm successful delivery, then backs off (e.g., halving the window) when packet loss is detected, dynamically adapting the sending rate to available network capacity.

## Cloze cards

- The OSI model has 7 layers, from top to bottom: {{c1::Application}}, {{c2::Presentation}}, {{c3::Session}}, {{c4::Transport}}, {{c5::Network}}, {{c6::Data Link}}, {{c7::Physical}}.
- The TCP/IP model has 4 layers, from top to bottom: {{c1::Application}}, {{c2::Transport}}, {{c3::Internet}}, {{c4::Network Access (Link)}}.
- The TCP three-way handshake proceeds: client sends {{c1::SYN}}, server responds {{c2::SYN-ACK}}, client sends {{c3::ACK}}, establishing the connection.
- Resolving a domain name typically checks, in order: {{c1::browser/OS cache}}, then a {{c2::recursive resolver (e.g., ISP or 8.8.8.8)}}, then a {{c3::root server}}, then a {{c4::TLD server}} (e.g., .com), then the {{c5::authoritative name server}} for the domain.
- By default, HTTP uses port {{c1::80}} and HTTPS uses port {{c2::443}}.
- A simplified TLS handshake: client sends {{c1::ClientHello}} (supported ciphers), server replies with {{c2::ServerHello and its certificate}}, client and server perform a {{c3::key exchange}} to derive a shared session key, then both send {{c4::Finished}} messages to begin encrypted communication.
