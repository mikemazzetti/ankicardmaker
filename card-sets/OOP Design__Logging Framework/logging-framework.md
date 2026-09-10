---
deck: "OOP Design::Logging Framework"
topic: "Logging Framework"
tags: [ankicardmaker, ood-logging]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Logging Framework — OOP Design

Source of truth for the `OOP Design::Logging Framework` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what are the 3 core functional requirements for a Logging Framework?
   **A:** 1) Log messages at multiple severity levels. 2) Route messages to multiple destinations (console, file, network) simultaneously. 3) Let format and filtering be configured without changing any calling code.

2. **Q:** Appender / Handler (logging framework) *(reversed — both ways)*
   **A:** A component responsible for writing a formatted log message to one specific destination — console, file, network socket, or external log service.

3. **Q:** Why is Chain of Responsibility a natural fit for handling log levels in a logging framework?
   **A:** Each handler in the chain is configured with a threshold level and decides independently whether it should process a given message, then forwards it to the next handler — decoupling the log call site from any specific handler.

4. **Q:** In a Chain-of-Responsibility log-level design, what determines whether a given handler processes a message?
   **A:** The handler compares the message's level to its own configured threshold; it processes (and typically still forwards) the message only if the message's level is >= its threshold.

5. **Q:** Why is Singleton commonly used for the LogManager (or LoggerFactory) in a logging framework?
   **A:** There should be exactly one global registry of loggers and one shared configuration (appenders, levels, formatters) so every part of the app logs consistently through a single, globally accessible access point.

6. **Q:** What is the main risk of a naive, non-thread-safe Singleton LogManager in a multi-threaded service?
   **A:** A race during lazy initialization can construct two separate LogManager instances, causing inconsistent configuration and duplicated or lost log output.

7. **Q:** Name two ways to make a Singleton LogManager thread-safe in Java.
   **A:** Eager static-field initialization, or double-checked locking with a volatile instance field (an enum-based singleton also works).

8. **Q:** What core fields should a LogMessage/LogRecord object carry?
   **A:** Timestamp, severity level, logger/source name, the message text, and optionally the thread name and an exception/stack trace.

9. **Q:** In an OOD interview, how do you cleanly support 'log to console AND file at the same time'?
   **A:** Attach multiple Appender instances to a single Logger (or to the chain of handlers); each appender independently formats and writes the same message to its own destination.

10. **Q:** Tricky edge case: what can go wrong with asynchronous (queued) logging when the process crashes?
   **A:** Messages sitting in the in-memory queue can be lost because they were never flushed to disk — mitigate with a bounded queue plus a shutdown hook that flushes pending messages before exit.

11. **Q:** Why should log-level filtering happen as early as possible in the pipeline (ideally at the Logger, before formatting)?
   **A:** It avoids the cost of building and formatting a message that will be discarded anyway — a real perf edge case when DEBUG logging is disabled in production but call sites still build expensive strings.

12. **Q:** What is log rotation, and why does a FileAppender need it?
   **A:** Rotation closes the current log file and starts a new one (by size or by time) so a single file doesn't grow unbounded; without it, disk usage keeps climbing until the disk fills up.

13. **Q:** How can each Logger instance have its own minimum level while still sharing global Appenders?
   **A:** Store a level threshold on the Logger itself, checked before the message is even constructed; surviving messages are then forwarded to the shared Appenders, which may apply their own (usually looser or equal) threshold.

14. **Q:** Implement a Chain-of-Responsibility log handler in Java: an abstract LogHandler with a next handler reference, a level threshold, and a logMessage(level, msg) method that writes locally if the level qualifies, then always forwards to the next handler.
   **A:** <pre><code>abstract class LogHandler {
    protected LogHandler next;
    protected final int level;

    LogHandler(int level) { this.level = level; }

    LogHandler setNext(LogHandler next) {
        this.next = next;
        return next;
    }

    void logMessage(int msgLevel, String msg) {
        if (msgLevel &gt;= this.level) {
            write(msg);
        }
        if (next != null) {
            next.logMessage(msgLevel, msg);
        }
    }

    protected abstract void write(String msg);
}

class ConsoleHandler extends LogHandler {
    ConsoleHandler(int level) { super(level); }
    protected void write(String msg) { System.out.println("[CONSOLE] " + msg); }
}</code></pre>

15. **Q:** Implement a thread-safe Singleton LoggerManager in Python using __new__ and a threading.Lock.
   **A:** <pre><code>import threading

class LoggerManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._loggers = {}
        return cls._instance

    def get_logger(self, name):
        if name not in self._loggers:
            self._loggers[name] = Logger(name)
        return self._loggers[name]</code></pre>

16. **Q:** Implement a common Appender interface in Java plus a FileAppender that writes each message on its own line.
   **A:** <pre><code>interface Appender {
    void write(LogMessage message);
}

class FileAppender implements Appender {
    private final BufferedWriter writer;

    FileAppender(String path) throws IOException {
        this.writer = new BufferedWriter(new FileWriter(path, true));
    }

    public synchronized void write(LogMessage message) {
        try {
            writer.write(message.format());
            writer.newLine();
            writer.flush();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}</code></pre>

17. **Q:** Implement a Python Logger.log() dispatch method that checks the logger's own threshold, then fans the message out to every attached appender.
   **A:** <pre><code>class Logger:
    def __init__(self, name, level="INFO"):
        self.name = name
        self.level = level
        self.appenders = []

    def add_appender(self, appender):
        self.appenders.append(appender)

    def log(self, level, message):
        if LEVELS[level] &lt; LEVELS[self.level]:
            return
        record = LogMessage(level, self.name, message)
        for appender in self.appenders:
            appender.write(record)

    def info(self, message):
        self.log("INFO", message)</code></pre>

## Cloze cards

- A logging framework's {{c1::Logger}} class exposes methods like debug(), info(), warn(), error(), and delegates the actual writing of each message to one or more {{c2::Appenders}} (also called Handlers).
- Standard log level severity, from least to most severe: {{c1::DEBUG}} < {{c2::INFO}} < {{c3::WARN}} < {{c4::ERROR}} < {{c5::FATAL}}.
- A {{c1::LogFormatter}} converts a raw LogMessage (timestamp, level, source, text) into the final string an Appender writes out — e.g. plain text, JSON, or a custom pattern.
