---
deck: "Resume Prep::Kubernetes"
topic: "Kubernetes"
tags: [ankicardmaker, resume-prep, kubernetes]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Kubernetes — Resume Prep

Source of truth for the `Resume Prep::Kubernetes` deck (21 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is a Kubernetes Pod?
   **A:** The smallest deployable unit in Kubernetes &mdash; one or more containers that share the same network namespace (IP, port space) and storage volumes, and are always scheduled together on the same node.

2. **Q:** ReplicaSet *(reversed — tested both ways)*
   **A:** A Kubernetes controller that ensures a specified number of identical Pod replicas are running at all times, creating or deleting Pods as needed to match the desired count.

3. **Q:** What's the relationship between a Deployment and a ReplicaSet?
   **A:** A Deployment manages ReplicaSets: it creates a new ReplicaSet whenever the Pod template changes and orchestrates the rollout, scaling, and rollback. You typically create/manage Deployments, not ReplicaSets, directly.

4. **Q:** What does a Kubernetes Service of type NodePort do?
   **A:** Exposes the Service on a static port (30000-32767 by default) on every node's IP, so external traffic can reach it via &lt;NodeIP&gt;:&lt;NodePort&gt;, in addition to still getting a normal ClusterIP.

5. **Q:** What does a Kubernetes Service of type LoadBalancer do?
   **A:** Provisions an external load balancer via the cloud provider (e.g. an AWS ELB) that routes external traffic into the Service, which then load-balances across the matching Pods. Builds on top of NodePort/ClusterIP.

6. **Q:** What's the difference between a ConfigMap and a Secret in Kubernetes?
   **A:** Both inject configuration into Pods (as env vars or mounted files), but a Secret is meant for sensitive data &mdash; stored base64-encoded (not encrypted by default) with tighter access controls &mdash; while a ConfigMap holds non-sensitive plain configuration.

7. **Q:** What is a Kubernetes Namespace used for?
   **A:** A virtual partition of a single physical cluster used to isolate and organize groups of resources (e.g. per team or environment), scoping resource names and enabling per-namespace quotas and RBAC.

8. **Q:** What does the kubelet do on each node?
   **A:** An agent running on every node that makes sure the containers described in Pod specs assigned to that node are running and healthy, and reports node/Pod status back to the control plane.

9. **Q:** What does the Kubernetes scheduler do?
   **A:** Watches for newly created Pods that have no assigned node, and picks a suitable node for each based on resource requirements, affinity/anti-affinity rules, and taints/tolerations.

10. **Q:** How do you list all Pods with kubectl?
   **A:** <code>kubectl get pods</code> for the current namespace; add <code>-A</code> / <code>--all-namespaces</code> for every namespace, or <code>-n &lt;namespace&gt;</code> for a specific one.

11. **Q:** How do you view logs for one container inside a multi-container Pod?
   **A:** <code>kubectl logs &lt;pod-name&gt; -c &lt;container-name&gt;</code> &mdash; the <code>-c</code> flag is only required when the Pod has more than one container.

12. **Q:** How do you get a shell inside a running Pod's container?
   **A:** <code>kubectl exec -it &lt;pod-name&gt; -- sh</code> (or <code>bash</code>).

13. **Q:** What's the difference between a liveness probe and a readiness probe?
   **A:** A liveness probe checks whether a container is still healthy; on failure, Kubernetes restarts the container. A readiness probe checks whether a container is ready to serve traffic; on failure, the Pod is pulled from Service endpoints but NOT restarted.

14. **Q:** During a Deployment rolling update, how does Kubernetes avoid downtime by default?
   **A:** It incrementally replaces old Pods with new ones: it creates new Pods and waits for them to pass their readiness probe before terminating old ones, bounded by the <code>maxSurge</code> and <code>maxUnavailable</code> settings of the rolling update strategy.

15. **Q:** What does a HorizontalPodAutoscaler (HPA) do?
   **A:** Automatically scales the number of Pod replicas in a Deployment or ReplicaSet up or down based on observed metrics (commonly CPU or memory utilization) to track a target value.

16. **Q:** What is a Kubernetes Ingress?
   **A:** An API object that manages external HTTP/HTTPS access into cluster Services, providing host/path-based routing rules, TLS termination, and a single external entry point &mdash; it requires an Ingress controller to actually implement the routing.

17. **Q:** Write a minimal Kubernetes Deployment YAML for an nginx app with 3 replicas.
   **A:** <pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80</code></pre>

18. **Q:** How does a Kubernetes Service know which Pods to route traffic to?
   **A:** Via label selectors &mdash; the Service's <code>selector</code> field is matched against Pod labels, and any Pod with matching labels becomes an endpoint the Service load-balances across; membership is tracked continuously, not as a static list.

## Cloze cards

- A Kubernetes Service of type {{c1::ClusterIP}} (the default) exposes a stable virtual IP reachable only from inside the cluster.
- The Kubernetes control plane consists of the {{c1::API server}}, {{c2::etcd}} (the cluster state store), the {{c3::scheduler}}, and the {{c4::controller manager}}. <!-- Back Extra: Typically runs on dedicated control-plane/master nodes. -->
- <code>kubectl {{c1::apply}} -f deployment.yaml</code> declaratively creates or updates resources to match the YAML file, while <code>kubectl {{c2::delete}} -f deployment.yaml</code> removes the resources it defines.
