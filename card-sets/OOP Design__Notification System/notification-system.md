---
deck: "OOP Design::Notification System"
topic: "Notification System"
tags: [ankicardmaker, ood-notification]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Notification System — OOP Design

Source of truth for the `OOP Design::Notification System` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what are the 3 core functional requirements for a Notification System?
   **A:** 1) Send notifications through multiple channels (email, SMS, push). 2) Respect per-user channel preferences/opt-outs. 3) Let new channels or event types be added without rewriting existing sending logic.

2. **Q:** NotificationChannel (Notification System) *(reversed — both ways)*
   **A:** An interface/strategy representing one delivery mechanism (email, SMS, push) with a send(user, message) method; each concrete channel encapsulates its own transport logic.

3. **Q:** Why is the Observer pattern a natural fit for how a Notification System reacts to domain events (e.g. 'order shipped')?
   **A:** The event source (e.g. OrderService) doesn't need to know who cares about it — it just publishes an event; the NotificationService subscribes as an observer and is notified automatically, decoupling triggering logic from notification logic.

4. **Q:** Why is Strategy a good fit for per-channel sending logic in a Notification System?
   **A:** Email, SMS, and push all need very different transport code (SMTP client, SMS gateway API, push provider SDK) but share the same send(user, message) contract — Strategy lets the NotificationService pick and swap the algorithm at runtime without conditionals.

5. **Q:** Why use a Factory to create channel-specific notification objects instead of `new EmailNotification()` scattered through the codebase?
   **A:** A NotificationFactory centralizes the mapping from NotificationType to the concrete class, so adding a new channel means adding one factory branch/registration instead of hunting down every call site that constructs notifications.

6. **Q:** How do Factory and Strategy typically combine in a Notification System's design?
   **A:** The Factory creates the right NotificationChannel (Strategy) implementation for a given NotificationType; the NotificationService then calls that strategy's send() method without knowing which concrete channel it got.

7. **Q:** What core fields does a Notification/Message object typically carry?
   **A:** Recipient (User), channel type, subject/title, body content, priority, timestamp, and delivery status.

8. **Q:** How does an Observer-based design let a user 'subscribe' to updates on a specific entity, e.g. a price drop on a product?
   **A:** The entity (Subject) keeps a list of observers; subscribe(user) adds the user (or their notification handler) to that list, and when the entity's state changes it calls notify(), which invokes update() on each registered observer.

9. **Q:** Edge case: a push notification send fails due to a transient network error. How should the system handle it?
   **A:** Retry with exponential backoff up to a max attempt count, and after exhausting retries, move the notification to a dead-letter store/queue for later inspection rather than silently dropping it or retrying forever.

10. **Q:** Edge case: how should the system behave if a user has opted out of email for a given event type?
   **A:** The NotificationService should check NotificationPreference before dispatching and simply skip the email channel for that user/event — it should not fall back to another channel unless the user separately enabled that one.

11. **Q:** Edge case: what problem does batching solve for a notification system with high-frequency events (e.g. 50 likes on a post in a minute)?
   **A:** Without batching, the user gets 50 separate notifications (spam); a batching/debounce window aggregates events over a short interval into a single summarized notification.

12. **Q:** Why should NotificationChannel.send() be designed as idempotent (or paired with a delivery-id dedup check)?
   **A:** Retries after a timeout can cause the same notification to be sent twice even though the first attempt actually succeeded; an idempotency key lets the channel or provider recognize and drop the duplicate.

13. **Q:** What's the tradeoff of sending notifications synchronously inside the request that triggers them, versus asynchronously via a queue?
   **A:** Synchronous sending is simpler but couples request latency/availability to the (possibly slow or flaky) notification provider; asynchronous sending via a queue keeps the triggering request fast and isolates notification failures, at the cost of added infrastructure and eventual-consistency delay.

14. **Q:** Implement a NotificationChannel Strategy interface in Java plus an EmailNotificationChannel implementation.
   **A:** <pre><code>interface NotificationChannel {
    void send(User user, Notification notification);
}

class EmailNotificationChannel implements NotificationChannel {
    private final EmailClient emailClient;

    EmailNotificationChannel(EmailClient emailClient) {
        this.emailClient = emailClient;
    }

    public void send(User user, Notification notification) {
        emailClient.sendMail(
            user.getEmail(),
            notification.getSubject(),
            notification.getBody()
        );
    }
}</code></pre>

15. **Q:** Implement a NotificationFactory in Python that maps a NotificationType to the right channel strategy.
   **A:** <pre><code>class NotificationFactory:
    _channels = {
        "EMAIL": EmailNotificationChannel,
        "SMS": SMSNotificationChannel,
        "PUSH": PushNotificationChannel,
    }

    @classmethod
    def create(cls, channel_type, **deps):
        if channel_type not in cls._channels:
            raise ValueError(f"Unknown channel: {channel_type}")
        return cls._channels[channel_type](**deps)</code></pre>

16. **Q:** Implement a minimal Observer pattern in Java: a Subject interface and a concrete OrderTracker that notifies subscribed observers when the order ships.
   **A:** <pre><code>interface Observer {
    void update(String eventType, Object payload);
}

class OrderTracker {
    private final List&lt;Observer&gt; observers = new ArrayList&lt;&gt;();

    void subscribe(Observer o) { observers.add(o); }
    void unsubscribe(Observer o) { observers.remove(o); }

    void markShipped(Order order) {
        order.setStatus("SHIPPED");
        for (Observer o : observers) {
            o.update("ORDER_SHIPPED", order);
        }
    }
}</code></pre>

17. **Q:** Implement a Python NotificationService.notify() method that checks user preferences, resolves a channel via the factory, and sends with basic retry.
   **A:** <pre><code>class NotificationService:
    def __init__(self, preferences, factory, max_retries=3):
        self.preferences = preferences
        self.factory = factory
        self.max_retries = max_retries

    def notify(self, user, event_type, notification):
        for channel_type in self.preferences.enabled_channels(user, event_type):
            channel = self.factory.create(channel_type)
            self._send_with_retry(channel, user, notification)

    def _send_with_retry(self, channel, user, notification):
        for attempt in range(self.max_retries):
            try:
                channel.send(user, notification)
                return
            except TransientError:
                continue
        raise DeliveryFailed(notification)</code></pre>

## Cloze cards

- A {{c1::NotificationService}} is the central entry point apps call to trigger notifications; it looks up user preferences and delegates actual delivery to channel-specific {{c2::NotificationChannel}} implementations.
- NotificationType is typically an enum with values {{c1::EMAIL}}, {{c2::SMS}}, and {{c3::PUSH}}.
- A {{c1::NotificationPreference}} object stores, per user and per event type, which channels are opted into — letting the NotificationService skip channels the user disabled.
