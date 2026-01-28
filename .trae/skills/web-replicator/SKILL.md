---
name: "web-replicator"
description: "Replicates web pages from descriptions or images. Invoke when user wants to clone, copy, or recreate a website design/functionality."
---

# Web Replicator

This skill is designed to help users quickly replicate web pages.

## Workflow

1.  **Analyze Requirements**:
    *   Ask for the target website URL, image, or detailed description if not provided.
    *   Identify the key sections (Header, Hero, Features, Footer, etc.).
    *   Identify the design style (colors, fonts, layout).

2.  **Determine Tech Stack**:
    *   If simple static page: HTML + Tailwind CSS (via CDN) or plain CSS.
    *   If complex/interactive: React or Vue (using Vite).
    *   Ask user for preference if unsure.

3.  **Implementation Steps**:
    *   **Structure**: Create the HTML structure or Component hierarchy.
    *   **Style**: Apply styles to match the visual design. Use Tailwind CSS for speed if applicable.
    *   **Assets**: Use placeholders (like `https://placehold.co/600x400`) if actual assets aren't available.
    *   **Interactivity**: Add necessary JavaScript for menus, sliders, etc.

4.  **Verification**:
    *   If running a local server, use `OpenPreview` to show the result.
    *   Self-correct any visual discrepancies.

## Tips for Success

*   **Mobile First**: Ensure the design is responsive.
*   **Modern Practices**: Use Flexbox and Grid for layouts.
*   **Clean Code**: Keep the code modular and readable.
