---
deck: "Resume Prep::Docker"
topic: "Docker"
tags: [ankicardmaker, resume-prep, docker]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Docker — Resume Prep

Source of truth for the `Resume Prep::Docker` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the key difference between a Docker image and a Docker container?
   **A:** An image is a read-only, immutable template (layered filesystem + metadata) used to create containers. A container is a running (or stopped) instance of an image, with a thin writable layer added on top of the image's read-only layers.

2. **Q:** What are Docker image layers, and why do they enable build caching?
   **A:** Each Dockerfile instruction (FROM, RUN, COPY, etc.) produces a new read-only layer stacked on the previous ones. Docker caches each layer keyed by its instruction and inputs; if nothing changed, it reuses the cached layer instead of re-executing the instruction.

3. **Q:** What does the <code>FROM</code> instruction do in a Dockerfile?
   **A:** Specifies the base image the new image is built on, e.g. <code>FROM node:20-alpine</code>. It must be the first instruction (aside from an optional <code>ARG</code> before it).

4. **Q:** What's the difference between <code>RUN</code> and <code>CMD</code> in a Dockerfile?
   **A:** <code>RUN</code> executes a command at build time and commits the result as a new image layer (e.g. installing packages). <code>CMD</code> specifies the default command a container runs at start time; it does not execute during the build.

5. **Q:** What's the difference between <code>CMD</code> and <code>ENTRYPOINT</code> in a Dockerfile?
   **A:** <code>ENTRYPOINT</code> sets the fixed executable the container always runs. <code>CMD</code> supplies default arguments, which are overridden if arguments are passed to <code>docker run</code>. If both are set, CMD's values become ENTRYPOINT's default args.

6. **Q:** What's the difference between <code>COPY</code> and <code>ADD</code> in a Dockerfile?
   **A:** <code>COPY</code> only copies files/directories from the build context into the image. <code>ADD</code> does that plus extra features: it auto-extracts local tar archives and can fetch remote URLs. Best practice: prefer <code>COPY</code> unless you specifically need ADD's extraction or URL behavior.

7. **Q:** What does <code>EXPOSE 8080</code> do in a Dockerfile, and what does it NOT do?
   **A:** It documents that the container listens on port 8080 (metadata used by tools and <code>docker run -P</code>). It does NOT publish the port to the host &mdash; that requires <code>-p</code> on <code>docker run</code>.

8. **Q:** Write a multi-stage Dockerfile for a Node.js/TypeScript app that builds the code then ships only the compiled output.
   **A:** <pre><code>FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]</code></pre>

9. **Q:** What does <code>docker run -d -p 8080:80 --name web nginx</code> do?
   **A:** Runs a container from the <code>nginx</code> image in detached mode (<code>-d</code>), maps host port 8080 to container port 80 (<code>-p</code>), and names the container <code>web</code>.

10. **Q:** How do you build an image from a Dockerfile in the current directory and tag it <code>myapp:1.0</code>?
   **A:** <code>docker build -t myapp:1.0 .</code> &mdash; the trailing <code>.</code> is the build context sent to the Docker daemon.

11. **Q:** What does <code>docker ps -a</code> show that plain <code>docker ps</code> doesn't?
   **A:** <code>docker ps</code> lists only running containers. <code>docker ps -a</code> lists all containers, including stopped/exited ones.

12. **Q:** How do you get an interactive shell inside a running container?
   **A:** <code>docker exec -it &lt;container&gt; sh</code> (or <code>bash</code> if available) &mdash; <code>-i</code> keeps STDIN open, <code>-t</code> allocates a TTY.

13. **Q:** What's the difference between a named volume and a bind mount in Docker?
   **A:** A named volume is created and managed by Docker in its own storage area (<code>docker volume create</code>), portable across hosts. A bind mount maps a specific host filesystem path directly into the container, tying the container to that host's layout.

14. **Q:** By default, how do containers on the same user-defined Docker network reach each other?
   **A:** By container name &mdash; Docker's embedded DNS resolves container names to their IPs on that network, so one container can reach another using its name as the hostname.

15. **Q:** What does the <code>-p 8080:80</code> flag mean in <code>docker run -p 8080:80 myapp</code>?
   **A:** Maps host port 8080 to the container's port 80, in the form <code>-p host:container</code>, forwarding traffic that hits the host on 8080 into the container on port 80.

16. **Q:** What is <code>.dockerignore</code> for?
   **A:** Lists files/paths (e.g. <code>node_modules</code>, <code>.git</code>) to exclude from the build context sent to the Docker daemon, keeping builds faster and images from accidentally including secrets or bloat.

17. **Q:** Why does chaining multiple install commands into one <code>RUN ... &amp;&amp; ...</code> reduce image size compared to separate <code>RUN</code> lines?
   **A:** Each <code>RUN</code> creates a new layer; a separate update layer can go stale and any intermediate package caches persist in their own layer. Chaining into a single <code>RUN</code> (and cleaning caches in that same instruction) keeps it to one layer with no leftover cache data.

## Cloze cards

- In a Dockerfile, once a layer's cache is invalidated (its instruction or inputs changed), {{c1::every layer after it}} must be rebuilt, even if their own instructions didn't change. <!-- Back Extra: This is why you order instructions from least- to most-frequently-changing (e.g. install deps before copying source). -->
- A multi-stage Dockerfile uses multiple {{c1::FROM}} statements in one file so build artifacts from an earlier stage can be copied into a final, {{c2::smaller}} runtime image, leaving build-only tools and dependencies behind. <!-- Back Extra: Keeps compilers/dev dependencies out of the shipped image. -->
- To shrink Docker image size: use a {{c1::minimal/alpine}} base image, {{c2::combine RUN commands}} to reduce layer count, use {{c3::multi-stage builds}} to drop build-only tools, and add a {{c4::.dockerignore}} to avoid copying unneeded files. <!-- Back Extra: All reduce the final image's footprint. -->
