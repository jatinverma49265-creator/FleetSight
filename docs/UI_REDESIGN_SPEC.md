# FleetSight UI/UX Redesign Specification (Step 0)

> **Document Version**: 1.0.0  
> **Task**: UI-Pass (Side-task · Does not advance core loop counter)  
> **Status**: Proposed Specification (Awaiting User Approval — No application code modified)  
> **Inspiration Source**: [Orizon Wind Energy Dashboard UI (Dribbble)](https://dribbble.com/shots/26374797-Wind-Energy-Dashboard-UI-Clean-Data-Driven-Sustainable)

---

## 1. Reference Overview & Visual Analysis

### A. Observations from Reference Design
- **Visual Mood**: Serene, professional, highly analytical yet breathable. Avoids aggressive neon accents, dark harsh gradients, or busy borders.
- **Visual Density & Spacing**: Generous whitespace (24px–32px gutters) between modular widgets. Cards have substantial internal breathing room (24px padding).
- **Information Hierarchy**:
  - Top level: Crisp header with contextual breadcrumbs, status pill, user/role profile, and compact global search/actions.
  - Secondary level: High-impact KPI summary row featuring large numeric counters, delta tags (+X%), and subtle underlying sparklines/trends.
  - Core level: Asymmetric modular grid pairing a dominant visual anchor (map/spatial canvas or performance curve) with concise analytical breakdown sidebars.
- **Card Styling**: Soft rounded corners (~16px to 20px radius), hairline subtle borders (1px with low opacity), soft elevation shadows with wide blur radius and zero harsh black drop.
- **Data Presentation**: Charts use minimal horizontal gridlines, high data-ink ratio, rounded bar caps, subtle fill gradients underneath area lines, and soft tooltip pills.
- **Nature-Inspired Palette**: Leverages natural sage/moss greens, crisp sky blues, and warm earth tones on a clean, low-glare background.

### B. Observed in Reference vs. Design Assumptions
| Element | Observed in Reference (Light UI) | My Design Assumption for Dark FleetSight |
| :--- | :--- | :--- |
| **Theme Tone** | Crisp off-white & soft eggshell grey backgrounds (`#f8fafc` / `#f1f5f9`). | Deep slate-navy & obsidian surfaces (`#0a1017` / `#0f1824`) maintaining low-glare calm depth without pitch-black void. |
| **Accent Hierarchy** | Primary sage green / oceanic teal for energy efficiency. | Primary sky-cyan (`#38bdf8`) + calming teal (`#00d2b4`) with a **restrained safety orange** (`#f97316`) for hazardous road defects. |
| **Card Borders** | Barely visible translucent borders (`rgba(0,0,0,0.06)`). | Subtle hairline slate borders (`rgba(148, 163, 184, 0.12)` or `#1e2f44`). |
| **Shadows** | Soft atmospheric ambient diffuse shadows (`0 8px 30px rgba(0,0,0,0.04)`). | Layered dark glow & elevation shadows (`0 12px 32px rgba(0,0,0,0.35)`). |
| **Domain Identity** | Wind turbine telemetry, rotor speed, power generation kW/MW. | Fleet bus tracking, AI defect detection, road roughness, PWD work orders, and MoRTH safety benchmarks. |

---

## 2. Dark Theme Translation & Color Palette

The goal is a **calm, data-focused, high-contrast, non-cyberpunk dark interface** inspired by the spacious, organic composure of the reference.

### Proposed Color Tokens & Palette

```
  Surface Layers             Borders & Dividers          Semantic Accents
┌───────────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
│ BG: #080d14           │   │ Border: #1a2736       │   │ Accent: #38bdf8       │
│ Surface: #0e1722      │   │ Border Subtle: #141f2d│   │ Safety: #f97316 (Road)│
│ Elevated: #142130     │   │ Border Hover: #2b3d52 │   │ Success: #10b981      │
│ High-Elevated: #1b2c40│   │ Focus Ring: #38bdf8   │   │ Warning: #facc15      │
└───────────────────────┘   └───────────────────────┘   └───────────────────────┘
```

| Token Name | HEX Value | RGBA Equivalent | Purpose / Application |
| :--- | :--- | :--- | :--- |
| `--color-bg` | `#080d14` | `rgb(8, 13, 20)` | Root application background. |
| `--color-surface` | `#0e1722` | `rgb(14, 23, 34)` | Standard card, drawer, and table background. |
| `--color-surface-elevated` | `#142130` | `rgb(20, 33, 48)` | Floating panels, dropdowns, hovered items. |
| `--color-surface-subtle` | `#0b121b` | `rgb(11, 18, 27)` | Input fields, search bars, inset table headers. |
| `--color-border-subtle` | `#141f2d` | `rgba(255, 255, 255, 0.06)` | Hairline dividers between widgets. |
| `--color-border-default` | `#1a2736` | `rgba(148, 163, 184, 0.14)` | Card and panel outer container borders. |
| `--color-border-hover` | `#2b3d52` | `rgba(148, 163, 184, 0.28)` | Interactive card hover and active tabs. |
| `--color-text-primary` | `#f8fafc` | `rgb(248, 250, 252)` | Headings, primary KPI values, high-contrast titles. |
| `--color-text-secondary` | `#94a3b8` | `rgb(148, 163, 184)` | Body copy, table values, chart axis labels. |
| `--color-text-muted` | `#64748b` | `rgb(100, 116, 139)` | Footers, captions, inactive states, timestamp labels. |
| `--color-accent` | `#38bdf8` | `rgb(56, 189, 248)` | Sky-cyan primary active states, focus rings, interactive toggles. |
| `--color-accent-soft` | `#0c2436` | `rgba(56, 189, 248, 0.12)` | Chip backgrounds, active navigation indicator pills. |
| `--color-safety-orange` | `#f97316` | `rgb(249, 115, 22)` | **Restrained FleetSight Safety Accent** (Potholes, Road Hazards, Critical SLAs). |
| `--color-success` | `#10b981` | `rgb(16, 185, 129)` | Verified status, repaired items, online edge nodes, +trends. |
| `--color-warning` | `#facc15` | `rgb(250, 204, 21)` | Candidate status, moderate severity, pending syncs. |
| `--color-danger` | `#ef4444` | `rgb(239, 68, 68)` | High/Critical severity, SLA breaches, RBAC 403 denial. |
| `--color-info` | `#60a5fa` | `rgb(96, 165, 250)` | Corridor traffic indicators, telemetry metadata. |
| `--color-chart-grid` | `#15202e` | `rgba(255, 255, 255, 0.05)` | Minimal horizontal chart gridlines. |
| `--color-map-surface` | `#0d1520` | `rgb(13, 21, 32)` | Leaflet dark tile filter & base ocean styling. |

---

## 3. Typography & Text Hierarchy

We adopt a clean, highly legible modern geometric/humanist sans-serif pairing (`Inter` / `Plus Jakarta Sans` / `Outfit`) optimized for data-dense dashboards.

| Typographic Level | Font Family | Size (px / rem) | Weight | Line Height | Letter Spacing | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Display / Hero H1** | `Inter`, sans-serif | `32px / 2.0rem` | 800 (ExtraBold) | `1.2` | `-0.03em` | Public Portal Hero, Brand title. |
| **Section Title H2** | `Inter`, sans-serif | `22px / 1.375rem`| 700 (Bold) | `1.3` | `-0.02em` | Page headers, View section titles. |
| **Card Header H3** | `Inter`, sans-serif | `15px / 0.9375rem`| 600 (SemiBold) | `1.4` | `-0.01em` | Widget titles, drawer headers. |
| **KPI Primary Value** | `Inter`, tabular | `28px / 1.75rem` | 700 (Bold) | `1.1` | `-0.02em` | Large counters, total counts, score numerals. |
| **Body Standard** | `Inter`, sans-serif | `14px / 0.875rem` | 400 (Regular) | `1.5` | `0` | Descriptions, work order instructions. |
| **Body Medium** | `Inter`, sans-serif | `13px / 0.8125rem`| 500 (Medium) | `1.4` | `0` | Table cell data, drawer metadata values. |
| **Caption / Badge** | `Inter`, sans-serif | `11px / 0.6875rem`| 600 (SemiBold) | `1.3` | `+0.04em` | Status badges, timestamps, tags (all-caps). |
| **Mono / Telemetry** | `JetBrains Mono` | `12px / 0.75rem` | 500 (Medium) | `1.4` | `0` | GPS coords, event UUIDs, hash records. |

---

## 4. Layout Structure & Alignment System

### Reference Architecture vs FleetSight Adaptations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ NAVBAR: Brand Pill | Nav Tabs (Portal, Map, WOs, Traffic, Audit) | Sync | RBAC│
├─────────────────────────────────────────────────────────────────────────────┤
│ KPI SUMMARY ROW: 4 Streamlined Cards with Delta Badges & Spark Indicators    │
├─────────────────────────────────────────────────────────────────────────────┤
│ DEMO CONTROL STRIP: Subtle, Elevated Toolbar for Multi-Bus Scenarios        │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ MAIN CONTENT CANVAS (e.g., 65% width) │ SIDEBAR / DETAIL DRAWER (35% width)  │
│ - Interactive Leaflet GIS Map Layer  │ - Clustered Issue Inspection Card    │
│ - or Work Orders Ranked Table        │ - Explainable Priority Score Bar     │
│ - or Corridor Traffic Flow Charts    │ - Dispatch / Verify Action Buttons   │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

1. **Header / Navbar**:
   - Fixed height `64px`, sticky top, subtle `rgba(8, 13, 20, 0.85)` backdrop blur (16px).
   - Brand pill with subtle teal pulse indicator and `SIMULATED PILOT` pill.
   - Segmented pill navigation bar in center with smooth active slide indicator.
   - Right-side role selector and sync status indicator with high keyboard accessibility.
2. **KPI Summary Deck**:
   - Clean 4-column horizontal responsive grid (`gap: 16px`).
   - Cards use `border-radius: 14px`, gentle hover lift (`translateY(-2px)`), muted icon chip containers, and subtle metric comparison tags.
3. **Main Content Grid**:
   - 12-column responsive layout with 24px gutters.
   - Map tab: 8 columns (Map Canvas) + 4 columns (Issue Detail & Score Explainability Drawer).
   - Work Orders tab: Clean tabular card view with tab filters (`All`, `Pending Approval`, `Assigned`, `Closed`) and quick action buttons.
   - Traffic tab: Split view with aggregate corridor stats on top and Recharts hourly density charts below.

---

## 5. FleetSight Component Mapping

| Reference Concept (Wind Dashboard) | FleetSight Domain Equivalent | Redesign Visual Strategy |
| :--- | :--- | :--- |
| **Turbine Performance Grid** | **Active Transit Fleet (RJ14 Buses)** | Clean status chips with bus ID, speed, last GPS sync, and route. |
| **Energy Generation Curve (kW/h)** | **Corridor Traffic & Defect Rate** | Recharts AreaChart with soft gradient fill and sky-cyan stroke. |
| **Environmental Wind Map** | **Jaipur Corridor Leaflet GIS Map** | Dark custom map tiles with glowing severity pins & cluster badges. |
| **System Efficiency KPI (98.4%)** | **Bandwidth Saved (99.99%)** | High-impact card with wire comparison badge (1.6 KB vs 2.08 GB). |
| **Maintenance Work Queue** | **PWD Work Orders Pipeline** | Ranked work order cards with severity breakdown progress bars. |
| **Turbine Health Detail Panel** | **Issue Inspection Detail Drawer** | Right-hand overlay with bounding box preview, 2+ bus logs, and explainability breakdown. |
| **Facility Carbon Offset** | **MoRTH 2022 Road Safety Baseline** | Public portal statistics counter deck with clear provenance citations. |

---

## 6. Card Design System

- **Geometry**: `border-radius: 14px` (outer widgets), `10px` (nested inner containers).
- **Surface**: `background: var(--color-surface)` (`#0e1722`) with `1px solid var(--color-border-default)`.
- **Shadow**: `box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.4), 0 2px 6px -1px rgba(0, 0, 0, 0.2)`.
- **Padding**: `20px 22px` for primary widgets; `14px 16px` for compact telemetry chips.
- **Hover Micro-interaction**:
  - `transform: translateY(-2px);`
  - `border-color: var(--color-border-hover);`
  - `box-shadow: 0 12px 30px -6px rgba(0, 0, 0, 0.5);`
  - `transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);`
- **Icon Container**: `36px × 36px` rounded square (`border-radius: 8px`) with `background: rgba(56, 189, 248, 0.08)` and crisp SVG icons.

---

## 7. Chart Design (Recharts Theme)

- **Cartesian Grid**: Horizontal lines only, `stroke: #162434`, `strokeDasharray: "3 3"`, `opacity: 0.6`.
- **Axes**:
  - X-Axis & Y-Axis: `stroke: #334155`, `fontSize: 11px`, `tickLine: false`, `fill: #64748b`.
- **Tooltip Styling**:
  - `background: #142130`, `border: 1px solid #2b3d52`, `borderRadius: 8px`, `padding: 10px 14px`.
  - `boxShadow: 0 10px 25px rgba(0,0,0,0.5)`, `color: #f8fafc`.
- **Curves & Area Fills**:
  - Line stroke: `2.5px` with smooth `type="monotone"`.
  - LinearGradient defs with `stopOpacity: 0.25` at top and `stopOpacity: 0.0` at bottom.
- **Bar Charts**:
  - `radius: [6, 6, 0, 0]` (rounded top corners), `fill: #38bdf8`, hover fill `#0284c7`.

---

## 8. Leaflet Map Styling Direction

- **Basemap Direction**: Clean CartoDB Dark Matter or Stadia Alidade Smooth Dark tiles for a cohesive dark aesthetic without distracting bright roads.
- **Marker Design**:
  - Outer pulsating ring for active high-severity defects (`#f97316` or `#ef4444`).
  - Inner solid glyph pill with defect icon (Pothole, Crack, Waterlogging, Sign).
  - Selected marker: Dual ring highlight in sky-cyan (`#38bdf8`).
- **Map Popup & Overlays**:
  - Custom dark glassmorphism popup (`background: rgba(14, 23, 34, 0.95)`, `border: 1px solid #2b3d52`).
  - Floating map controls (zoom, layer filter pill) styled as unified dark rounded buttons.

---

## 9. Semantic Status & Provenance System

To ensure **accessibility and DPDP/Prototype transparency**, no status is conveyed by color alone:

| State | Color Token | Dual Cue (Icon + Label) | Text Badge Example |
| :--- | :--- | :--- | :--- |
| **Candidate** | `#facc15` (Warning Yellow) | ⚠️ Alert triangle icon | `[⚠️ CANDIDATE · 1 PASS]` |
| **Verified** | `#38bdf8` (Cyan Blue) | 📍 Double-check pin icon | `[✓✓ 2+ BUS VERIFIED]` |
| **Work Order** | `#f97316` (Safety Orange) | 🛠️ Wrench icon | `[🛠️ WO ACTIVE]` |
| **Assigned** | `#818cf8` (Indigo) | 👷 User badge | `[👷 ASSIGNED DIV-3]` |
| **Repaired** | `#10b981` (Emerald Green) | 🛡️ Shield check | `[🛡️ VERIFIED REPAIRED]` |
| **Closed** | `#64748b` (Muted Slate) | 🔒 Lock / Complete check | `[🔒 CLOSED]` |
| **Simulated Data** | `#facc15` / `#38bdf8` | 📡 Signal icon | `[SIMULATED DATA · PROTOTYPE]` |
| **Edge Privacy Blur**| `#10b981` | 👁️ Crossed-eye icon | `[DPDP ACT 2023 · BLURRED]` |

---

## 10. Preserving FleetSight's Brand Identity

1. **Safety Orange Accent**: Retain `#f97316` exclusively for roadway defects and high-priority maintenance items to preserve the civic infrastructure motif.
2. **Public Transit Motif**: Retain bus icons, corridor route indicators (e.g., `RJ14-01 · MI Road Corridor`), and speed/telemetry metrics.
3. **No Domain Leakage**: Ensure zero wind energy/turbine iconography or terminology leaks into the implementation.
4. **Data Provenance**: Keep all `data_origin="simulated"` banners and MoRTH 2022 citations intact.

---

## 11. Responsive Design Breakpoints

| Breakpoint | Target Devices | Layout Behavior |
| :--- | :--- | :--- |
| **`< 768px` (Mobile)** | Phones (360px–767px) | Single column vertical stack. Navbar collapses to menu drawer. Map view stacks drawer underneath map. |
| **`768px – 1024px` (Tablet)** | Tablets (iPad, etc.) | 2-column KPI grid. Collapsible side drawer for issue inspection. Touch-friendly target sizing (44px min). |
| **`1024px – 1440px` (Laptop/Desktop)**| Standard Displays | 4-column KPI grid. Map tab has 8-col map + 4-col persistent detail drawer. |
| **`> 1440px` (Wide Screens)** | 1080p / 2K / 4K | Max-width container (`1536px`) centered with generous gutters, high information clarity. |

---

## 12. Accessibility Requirements (WCAG 2.1 AA)

- **Contrast Ratio**: $\ge 4.5:1$ for normal text, $\ge 3.0:1$ for large text and UI components.
- **Focus Indicators**: Visible `2px solid #38bdf8` outline on all interactive buttons, tabs, dropdowns, and links with `outline-offset: 2px`.
- **Keyboard Navigation**: Full Tab/Shift+Tab, Enter/Space activation, and Escape key for modals/drawers.
- **ARIA Attributes**: `role="tablist"`, `role="tab"`, `aria-selected`, `aria-expanded`, `aria-label` on icon-only buttons.
- **Motion Reduction**: `@media (prefers-reduced-motion: reduce)` disables all transforms and pulses.

---

## 13. Proposed Design Token System (`:root`)

```css
:root {
  /* Color Palette — Surfaces */
  --color-bg: #080d14;
  --color-surface: #0e1722;
  --color-surface-elevated: #142130;
  --color-surface-subtle: #0b121b;

  /* Borders */
  --color-border-subtle: rgba(255, 255, 255, 0.06);
  --color-border-default: rgba(148, 163, 184, 0.14);
  --color-border-hover: rgba(148, 163, 184, 0.28);
  --color-focus-ring: #38bdf8;

  /* Typography Colors */
  --color-text-primary: #f8fafc;
  --color-text-secondary: #94a3b8;
  --color-text-muted: #64748b;

  /* Brand & Accents */
  --color-accent: #38bdf8;
  --color-accent-soft: rgba(56, 189, 248, 0.12);
  --color-brand-teal: #00d2b4;
  --color-safety-orange: #f97316;

  /* Semantic Status */
  --color-success: #10b981;
  --color-warning: #facc15;
  --color-danger: #ef4444;
  --color-info: #60a5fa;

  /* Typography Scale */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-size-xs: 11px;
  --font-size-sm: 13px;
  --font-size-base: 14px;
  --font-size-md: 16px;
  --font-size-lg: 20px;
  --font-size-xl: 28px;
  --font-size-2xl: 36px;

  /* Spacing Scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;

  /* Radii */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 20px;
  --radius-full: 9999px;

  /* Elevation Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.25);
  --shadow-md: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 16px 36px -6px rgba(0, 0, 0, 0.55);

  /* Micro-transitions */
  --transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-normal: 250ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 14. Review, Testing & Verification Plan

### A. Before/After Visual Review
- High-fidelity screenshots will be captured at 4 responsive viewports (`360px`, `768px`, `1280px`, `1920px`) across all primary tabs:
  - Public Portal & DPDP Charter
  - GIS Live Map & Detail Drawer
  - Ranked Work Orders Queue & Modal
  - Traffic Flow Heatmap
- Screenshots will be saved to `docs/ui-review/`.

### B. Automated Test Preservation
- **Backend Test Suite**: All 156 Pytest unit and integration tests must pass continuously without modification.
- **Browser E2E Suite**: All 6 Playwright browser tests (`frontend/test_e2e.js`) must pass with zero logic changes.

### C. Scope Enforcement & Git Verification
- Verification command: `git diff --stat` and `git status`.
- Strict check that **zero files** in `backend/`, `edge/`, `ml/`, `scripts/`, `tests/`, `pyproject.toml`, or backend schemas are modified.

---

## 15. Implementation Stages (Post-Approval Roadmap)

- **Stage A**: Core design tokens, theme variables, and global CSS reset in `frontend/src/index.css`.
- **Stage B**: App shell, header, navigation pills, and role switcher in `Navbar.jsx` & `App.jsx`.
- **Stage C**: KPI summary cards (`KPIRow.jsx`), demo control strip (`DemoControlPanel.jsx`), and traffic charts (`TrafficView.jsx`).
- **Stage D**: Leaflet GIS map styling, custom marker pins, detail drawer (`MapView.jsx`, `IssueDetailDrawer.jsx`).
- **Stage E**: Work orders queue (`WorkOrdersView.jsx`), RBAC denial modal, and audit log (`AuditView.jsx`).
- **Stage F**: Responsive layout polish, loading skeletons, and accessibility aria updates.
- **Stage G**: Public Portal (`PublicPortal.jsx`) visual refresh and final screenshot review.
