# Styles & Design System

This document is loaded on demand when working on CSS, design tokens, or visual styling.
Return to [AGENTS.md](../AGENTS.md) for the project overview.

## Directory Structure

```text
apps/web/src/
└── styles/
    ├── globals.css     (resets, font imports, root element defaults)
    ├── tokens.css      (all CSS custom properties: colors, spacing, typography)
    └── animations.css  (shared keyframes and transition presets)
```

Component-scoped styles live next to the component file:

```text
src/components/UserCard/
├── UserCard.tsx
└── UserCard.module.css
```

## Styling Approach

- CSS Modules for component-scoped styles: `ComponentName.module.css`.
- Global styles (resets, fonts, root variables) live in `apps/web/src/styles/globals.css`.
- Design tokens are defined as CSS custom properties in `apps/web/src/styles/tokens.css`.
- Do not use inline styles except for truly dynamic values (e.g., calculated widths).
- Do not use Tailwind utility classes in JSX. Use CSS Modules.

## Design Tokens

All colors, spacing, radii, and typography are defined as CSS variables:

```css
/* tokens.css */
:root {
  /* Colors */
  --color-primary: hsl(220, 90%, 56%);
  --color-surface: hsl(0, 0%, 100%);
  --color-text: hsl(220, 15%, 10%);

  /* Spacing (4px base grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

Always use these variables. Never hardcode color values or spacing in component CSS.

## Responsive Design

- Mobile-first: base styles target mobile, use `min-width` media queries to scale up.
- Breakpoints defined in `tokens.css`:
  - `--bp-sm: 640px`
  - `--bp-md: 768px`
  - `--bp-lg: 1024px`
  - `--bp-xl: 1280px`

## Dark Mode

Dark mode is implemented via `[data-theme="dark"]` on `<html>`. Override tokens inside that selector.

```css
[data-theme="dark"] {
  --color-surface: hsl(220, 15%, 10%);
  --color-text: hsl(0, 0%, 95%);
}
```

*Referenced from: [AGENTS.md](../AGENTS.md)*
