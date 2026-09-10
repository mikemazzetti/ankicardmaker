---
deck: "Resume Prep::CI-CD"
topic: "CI-CD"
tags: [ankicardmaker, resume-prep, cicd]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# CI-CD — Resume Prep

Source of truth for the `Resume Prep::CI-CD` deck (16 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Continuous Integration (CI) *(reversed — tested both ways)*
   **A:** The practice of merging code changes into a shared branch frequently, with each merge automatically built and tested so integration errors are caught early.

2. **Q:** What's the difference between Continuous Delivery and Continuous Deployment (both abbreviated CD)?
   **A:** Continuous Delivery automatically prepares every passing change into a release-ready artifact but still requires a manual approval before it reaches production; Continuous Deployment goes further and releases to production automatically with no manual gate.

3. **Q:** What is a "build artifact" in a CI/CD pipeline?
   **A:** The immutable, versioned output of the build stage (e.g., a JAR, Docker image, or zip) that is built once and then promoted unchanged through later environments.

4. **Q:** What's the key difference between "build" and "deploy" in a pipeline?
   **A:** Build compiles and packages source code into a runnable artifact; deploy takes that already-built artifact and installs/activates it in a target environment (e.g., staging or production).

5. **Q:** What is a "rollback" in a deployment pipeline?
   **A:** Reverting a target environment to a previous known-good artifact/version after a bad deployment, to quickly restore service.

6. **Q:** What is a Jenkinsfile?
   **A:** A text file, checked into source control, written in a Groovy-based DSL that defines a Jenkins pipeline's stages and steps as code.

7. **Q:** How do you write a minimal declarative Jenkins pipeline with Build and Test stages that run Maven?
   **A:** <pre><code>pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'mvn -B compile' }
        }
        stage('Test') {
            steps { sh 'mvn -B test' }
        }
    }
}</code></pre>

8. **Q:** In a Jenkins declarative pipeline, what does the top-level `agent` directive specify?
   **A:** Where the pipeline (or an individual stage, if overridden there) executes — e.g., <code>agent any</code> runs it on any available Jenkins agent/node.

9. **Q:** What file, and in what format, defines a pipeline in Azure DevOps Pipelines?
   **A:** azure-pipelines.yml — a YAML file checked into the repo that declares triggers, stages/jobs, and steps.

10. **Q:** How do you write a minimal Azure DevOps YAML pipeline that builds a Maven project on every push to main?
   **A:** <pre><code>trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: Maven@4
  inputs:
    mavenPomFile: 'pom.xml'
    goals: 'clean install'</code></pre>

11. **Q:** What is the purpose of a project's pom.xml file in Maven?
   **A:** It's the Project Object Model — it declares the project's coordinates (groupId/artifactId/version), its dependencies, plugins, and build configuration that Maven uses to build the project.

12. **Q:** What does running `mvn clean install` actually do?
   **A:** It first removes previous build output (the `clean` phase), then runs the standard lifecycle up through `install`, compiling, testing, packaging the artifact, and copying it into the local `.m2` repository so other local projects can depend on it.

13. **Q:** How do you declare a test-scoped JUnit Jupiter dependency in pom.xml?
   **A:** <pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.junit.jupiter&lt;/groupId&gt;
    &lt;artifactId&gt;junit-jupiter&lt;/artifactId&gt;
    &lt;version&gt;5.10.0&lt;/version&gt;
    &lt;scope&gt;test&lt;/scope&gt;
&lt;/dependency&gt;</code></pre>

14. **Q:** In a Maven dependency, what's the difference between `<scope>test</scope>` and `<scope>provided</scope>`?
   **A:** `test` scope: the dependency is available only for compiling/running tests and is excluded from the final artifact; `provided` scope: available at compile time but expected to be supplied by the runtime environment (e.g., a servlet container), so it's also excluded from the packaged artifact.

## Cloze cards

- A typical CI/CD pipeline runs stages roughly in this order: {{c1::build}} -&gt; {{c2::test}} -&gt; {{c3::package/artifact}} -&gt; {{c4::deploy}}.
- Maven's default build lifecycle runs phases in order: {{c1::validate}} -&gt; {{c2::compile}} -&gt; {{c3::test}} -&gt; {{c4::package}} -&gt; {{c5::verify}} -&gt; {{c6::install}} -&gt; {{c7::deploy}}. <!-- Back Extra: Invoking a phase runs every earlier phase in the lifecycle too, e.g. `mvn install` also runs compile and test. -->
