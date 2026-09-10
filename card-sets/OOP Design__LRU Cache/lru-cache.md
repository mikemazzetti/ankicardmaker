---
deck: "OOP Design::LRU Cache"
topic: "LRU Cache"
tags: [ankicardmaker, ood-lru-cache]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# LRU Cache — OOP Design

Source of truth for the `OOP Design::LRU Cache` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the functional requirement an LRU Cache design must satisfy?
   **A:** A fixed-capacity key-value store where both <code>get</code> and <code>put</code> run in O(1) time, and when capacity is exceeded, the Least Recently Used entry is evicted.

2. **Q:** Why does an efficient LRU Cache combine a HashMap with a doubly linked list instead of using just one of them?
   **A:** The HashMap gives O(1) key lookup but no ordering; the doubly linked list gives O(1) reordering (move-to-front) and O(1) removal-from-middle — the HashMap maps keys directly to their list nodes so both operations stay O(1).

3. **Q:** Why must the linked list be doubly linked rather than singly linked for O(1) LRU operations?
   **A:** Removing an arbitrary node (the one being accessed or evicted) requires updating its neighbor's pointers; without a prev pointer you'd need O(n) traversal to find the predecessor.

4. **Q:** What does each Node in the LRU Cache's linked list store?
   **A:** The key, the value, and prev/next pointers — storing the key (not just the value) lets you evict from the HashMap in O(1) when you evict the tail node.

5. **Q:** Where in the doubly linked list do the most-recently-used and least-recently-used entries live, by convention?
   **A:** Most-recently-used is kept at the head; least-recently-used sits at the tail — so eviction removes the tail and every access moves the touched node to the head.

6. **Q:** What are the two sentinel (dummy) nodes commonly used in an LRU Cache implementation, and why?
   **A:** A dummy head and dummy tail — they eliminate null-checks when inserting/removing at the boundaries, since every real node always has a non-null neighbor on each side.

7. **Q:** What steps does <code>get(key)</code> perform in an O(1) LRU Cache?
   **A:** Look up the node in the HashMap (return -1/not-found if absent), detach it from its current position in the list, move it to the head, and return its value.

8. **Q:** What steps does <code>put(key, value)</code> perform when the key already exists?
   **A:** Update the existing node's value, then detach and move it to the head — the same recency update as a get, just with a value overwrite first.

9. **Q:** What steps does <code>put(key, value)</code> perform when the key is new and the cache is at capacity?
   **A:** Evict the tail node (remove it from both the list and the HashMap), then insert a new node for the key at the head and add it to the HashMap.

10. **Q:** How does the HashMap's value type differ between a plain cache and an LRU cache?
   **A:** A plain cache maps key to value directly; an LRU cache maps key to Node (the linked-list node), so the map can both fetch the value and manipulate the node's position in O(1).

11. **Q:** Edge case: what should <code>put</code> do when capacity is 0?
   **A:** Reject the insert immediately (no-op or explicit error) rather than evicting — with zero capacity there is no tail node to evict, so eviction logic must special-case this.

12. **Q:** Edge case: calling <code>put</code> on an existing key with a new value — does this count as an eviction-candidate reset?
   **A:** Yes: updating an existing key must still move it to the head (most-recently-used), even though no new slot was consumed — recency is about access, not just insertion.

13. **Q:** Edge case: is <code>get</code> alone enough to change eviction order, or does only <code>put</code> affect it?
   **A:** Get alone changes eviction order — reading a key is itself a 'use', so a successful get must also move that node to the head, not just return the value.

14. **Q:** Edge case: how would you extend a single-threaded O(1) LRU Cache to be safe under concurrent access?
   **A:** Guard the map and list mutations with a single lock (coarse-grained) around get/put, or use a concurrent map plus a separate synchronized recency structure — naive lock-free reordering of a doubly linked list under concurrent writers is unsafe.

15. **Q:** LRU (Least Recently Used) eviction policy *(reversed — both ways)*
   **A:** A cache-replacement policy that discards the entry that hasn't been accessed for the longest time when the cache is full, on the assumption that recently used items are more likely to be reused soon.

16. **Q:** Implement a complete O(1) LRU Cache in Java using a HashMap and a doubly linked list with sentinel nodes.
   **A:** <pre><code>import java.util.HashMap;
import java.util.Map;

public class LRUCache {
    private class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }

    private final int capacity;
    private final Map&lt;Integer, Node&gt; map = new HashMap&lt;&gt;();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertAtHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        insertAtHead(node);
        return node.value;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            remove(map.get(key));
        }
        Node node = new Node(key, value);
        map.put(key, node);
        insertAtHead(node);
        if (map.size() &gt; capacity) {
            Node lru = tail.prev;
            remove(lru);
            map.remove(lru.key);
        }
    }
}
</code></pre>

17. **Q:** Implement a complete O(1) LRU Cache in Python using a dict and a doubly linked list with sentinel nodes.
   **A:** <pre><code>class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -&gt; int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._insert_at_head(node)
        return node.value

    def put(self, key: int, value: int) -&gt; None:
        if key in self.map:
            self._remove(self.map[key])
        node = Node(key, value)
        self.map[key] = node
        self._insert_at_head(node)
        if len(self.map) &gt; self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
</code></pre>

18. **Q:** Implement an O(1) LRU Cache in Java using <code>LinkedHashMap</code>'s built-in access-order mode instead of a hand-rolled linked list.
   **A:** <pre><code>import java.util.LinkedHashMap;
import java.util.Map;

public class LRUCache extends LinkedHashMap&lt;Integer, Integer&gt; {
    private final int capacity;

    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    public int get(int key) {
        return super.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        super.put(key, value);
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry&lt;Integer, Integer&gt; eldest) {
        return size() &gt; capacity;
    }
}
</code></pre>

19. **Q:** Implement an O(1) LRU Cache in Python using <code>collections.OrderedDict</code> instead of a hand-rolled linked list.
   **A:** <pre><code>from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -&gt; int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -&gt; None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) &gt; self.capacity:
            self.cache.popitem(last=False)
</code></pre>

## Cloze cards

- In an LRU Cache backed by a HashMap and doubly linked list, get and put both run in {{c1::O(1)}} time, and the cache evicts the {{c2::least recently used}} entry when it exceeds capacity.
