# Possible Features for Cribl Pipeline Visualizer (Dogfooding)

This document outlines potential features that would make the Cribl Pipeline Visualizer a valuable tool for teams managing a Cribl Stream deployment.

## 1. Observability and Metrics Overlay
*   **Live Traffic Indicators:** Integrate with Cribl's metrics API to overlay EPS (events per second) or byte throughput directly onto the edges (connections) of the graph. Thicker or differently colored lines could indicate higher volume.
*   **Health Status:** Color-code nodes (inputs/outputs/pipelines) based on their health status or error rates. For example, a pipeline dropping a high percentage of events could turn yellow or red.

## 2. Configuration Analysis and Validation
*   **Orphan Detection:** Visually flag inputs that aren't routed anywhere, or outputs that have no routes sending data to them.
*   **Disabled/Inactive Highlighting:** Show disabled routes, pipelines, or sources in a faded or grayed-out state, allowing the team to quickly see what's actually active vs. what's just sitting in the config.
*   **Complexity Scoring:** Highlight overly complex pipelines (e.g., those with too many functions) to suggest areas for refactoring.

## 3. Interactive and Navigation Features
*   **Highlight Paths:** In a large deployment, the graph can get messy. Allow a user to click an Input and highlight *only* the downstream pipelines and Outputs it connects to (and fade the rest).
*   **Search and Filter:** Add a search bar to quickly find a specific pipeline or output by name, zooming in on it within the graph.
*   **Click-to-Edit:** Make the nodes clickable hyperlinks that take the user directly to the configuration page for that specific input/pipeline/output in the Cribl Stream UI.

## 4. Versioning and Environment Comparisons
*   **Environment Diffing:** If your team manages multiple environments (Dev, Staging, Prod), allow the tool to generate a "diff" graph showing what pipelines exist in Dev but haven't been promoted to Prod yet.
*   **Git Integration (if using GitOps):** If your Cribl configs are stored in Git, the tool could show changes over time or visualize the impact of an open Pull Request before it's merged.

## 5. Documentation and Export
*   **Automated Wiki Sync:** Add a scheduled job to export the graph as an SVG/PNG and automatically update an internal Confluence page or developer portal, ensuring documentation is never out of date.
*   **Embeddable View:** Expose an iframe-friendly route so the graph can be embedded into internal dashboards (like Grafana or an internal developer portal).
