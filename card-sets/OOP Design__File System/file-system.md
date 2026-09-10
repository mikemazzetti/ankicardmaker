---
deck: "OOP Design::File System"
topic: "File System"
tags: [ankicardmaker, ood-file-system]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# File System — OOP Design

Source of truth for the `OOP Design::File System` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the two concrete node types in a Composite-pattern file system model, and what do they represent?
   **A:** File (leaf &mdash; holds actual content/size, no children) and Directory (composite &mdash; holds a collection of child FileSystemNode objects, which may themselves be Files or Directories).

2. **Q:** What common interface/abstract class do File and Directory both implement in the Composite pattern, and what methods does it declare?
   **A:** FileSystemNode (or Node), declaring at minimum <code>getName()</code>, <code>getSize()</code>, and often <code>getParent()</code> &mdash; so client code can treat files and directories uniformly.

3. **Q:** Why does Directory need a reference to its parent node?
   **A:** To support operations like computing the absolute path, moving up the tree, or validating a move doesn't create a cycle (can't move a directory into its own descendant).

4. **Q:** Composite pattern *(reversed — both ways)*
   **A:** Structural pattern that lets you compose objects into tree structures and treat individual objects (leaves) and compositions of objects (composites) uniformly through a shared interface.

5. **Q:** In the File System design, which class owns the list of child nodes, and what data structure is typical?
   **A:** Directory owns the children, typically a <code>Map&lt;String, FileSystemNode&gt;</code> keyed by name for O(1) lookup, or a List if insertion order matters.

6. **Q:** Why is the Composite pattern the natural fit for a file system's File/Directory relationship?
   **A:** Operations like <code>getSize()</code>, <code>delete()</code>, or <code>print()</code> need to work identically whether called on a single file or an entire directory subtree &mdash; Composite lets Directory's implementation just delegate to each child polymorphically, without the caller knowing which type it's dealing with.

7. **Q:** Besides Composite, what pattern would you add to support new cross-cutting operations (search, compress, count-by-extension) without modifying File/Directory classes?
   **A:** The Visitor pattern: define a FileSystemVisitor interface with visit(File) and visit(Directory) methods, and have each node call <code>accept(visitor)</code> &mdash; new operations become new Visitor implementations instead of new methods on every node class.

8. **Q:** How would the Decorator pattern apply to a file system that supports optional compression or encryption on files?
   **A:** Wrap a File in a CompressedFile or EncryptedFile decorator implementing the same FileSystemNode interface, so behavior (e.g. read/write transforms the bytes) is added transparently without subclassing every combination.

9. **Q:** What is the classic recursive-size edge case for a Directory.getSize() implementation, and why does naive recursion risk infinite loops?
   **A:** Symbolic links (symlinks) that point back up the tree (or to themselves) create cycles; naive recursion following every child recurses forever. Fix: track visited node IDs/inodes and skip already-visited nodes, or don't follow symlinks by default.

10. **Q:** Why should deleting a non-empty Directory require either a recursive/force flag or fail by default?
   **A:** Silently deleting all descendants is destructive and surprising; APIs typically mirror real file systems by requiring an explicit recursive=true flag (like <code>rm -r</code>) or throwing an exception if the directory isn't empty.

11. **Q:** What edge case arises from case sensitivity when adding a child to a Directory (e.g. adding 'Notes.txt' when 'notes.txt' exists)?
   **A:** Behavior differs by target OS: case-sensitive file systems (Linux) allow both to coexist as distinct files, case-insensitive ones (Windows/macOS default) must treat them as the same name and reject/overwrite &mdash; the design should make this policy explicit and configurable.

12. **Q:** Should FileSystem.getSize(directory) compute size eagerly (cached, updated on every write) or lazily (recomputed on each call)? What's the tradeoff?
   **A:** Eager/cached: O(1) reads but every write must propagate size deltas up to every ancestor. Lazy: O(1) writes but O(n) reads (full subtree walk). Most designs cache and propagate deltas upward since size reads are far more frequent than the propagation cost.

13. **Q:** What API method would let a client move a directory, and what validation must it perform before allowing the move?
   **A:** <code>move(FileSystemNode node, Directory newParent)</code> &mdash; must reject the move if <code>newParent</code> is <code>node</code> itself or a descendant of <code>node</code> (that would detach the tree into a cycle).

14. **Q:** What API method lists a directory's immediate contents, and why should it not recurse by default?
   **A:** <code>List&lt;FileSystemNode&gt; listChildren(Directory dir)</code> &mdash; returning only immediate children (not the full recursive tree) keeps the call cheap and predictable; recursive listing should be a separate, explicit operation (e.g. via a Visitor).

15. **Q:** Java: implement the Composite pattern with an abstract FileSystemNode, a File leaf, and a Directory composite whose <code>getSize()</code> sums its children.
   **A:** <pre><code>import java.util.HashMap;
import java.util.Map;

abstract class FileSystemNode {
    protected String name;
    protected Directory parent;

    public FileSystemNode(String name) { this.name = name; }
    public abstract long getSize();
    public String getName() { return name; }
}

class File extends FileSystemNode {
    private long sizeInBytes;

    public File(String name, long sizeInBytes) {
        super(name);
        this.sizeInBytes = sizeInBytes;
    }

    @Override
    public long getSize() { return sizeInBytes; }
}

class Directory extends FileSystemNode {
    private final Map&lt;String, FileSystemNode&gt; children = new HashMap&lt;&gt;();

    public Directory(String name) { super(name); }

    public void add(FileSystemNode node) {
        node.parent = this;
        children.put(node.getName(), node);
    }

    @Override
    public long getSize() {
        long total = 0;
        for (FileSystemNode child : children.values()) {
            total += child.getSize();
        }
        return total;
    }
}</code></pre>

16. **Q:** Python: write a recursive <code>get_size(node, visited=None)</code> function that computes a directory tree's total size while avoiding infinite recursion from symlink cycles.
   **A:** <pre><code>def get_size(node, visited=None):
    if visited is None:
        visited = set()
    if id(node) in visited:
        return 0
    visited.add(id(node))

    if node.is_file:
        return node.size_bytes

    return sum(get_size(child, visited) for child in node.children.values())</code></pre>

17. **Q:** Java: implement a depth-first <code>findByName(Directory root, String targetName)</code> search over a file system tree, returning the first matching node or null.
   **A:** <pre><code>public FileSystemNode findByName(Directory root, String targetName) {
    if (root.getName().equals(targetName)) {
        return root;
    }
    for (FileSystemNode child : root.getChildren()) {
        if (child.getName().equals(targetName)) {
            return child;
        }
        if (child instanceof Directory) {
            FileSystemNode found = findByName((Directory) child, targetName);
            if (found != null) {
                return found;
            }
        }
    }
    return null;
}</code></pre>

18. **Q:** Python: implement <code>Directory.add_child(node)</code> that raises if a child with the same name already exists.
   **A:** <pre><code>class Directory(FileSystemNode):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}

    def add_child(self, node):
        if node.name in self.children:
            raise FileExistsError(f"'{node.name}' already exists in '{self.name}'")
        node.parent = self
        self.children[node.name] = node</code></pre>

## Cloze cards

- A file system's core requirements include: {{c1::create}} files/directories, {{c2::delete}} them, {{c3::move/rename}} them, {{c4::list}} a directory's contents, and compute {{c5::size}} recursively.
- The {{c1::NodeType}} enum distinguishes {{c2::FILE}} from {{c3::DIRECTORY}} when Composite polymorphism alone isn't enough (e.g. for serialization or a switch in client code).
