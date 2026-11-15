---
name: Obsidian Clinical HUD
colors:
  surface: '#10131a'
  surface-dim: '#10131a'
  surface-bright: '#363941'
  surface-container-lowest: '#0b0e15'
  surface-container-low: '#191b23'
  surface-container: '#1d1f27'
  surface-container-high: '#272a32'
  surface-container-highest: '#32353d'
  on-surface: '#e1e2ec'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#e1e2ec'
  inverse-on-surface: '#2d3038'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dce6'
  primary: '#e0fdff'
  on-primary: '#00373a'
  primary-container: '#00f2fe'
  on-primary-container: '#006a70'
  inverse-primary: '#00696f'
  secondary: '#43edcd'
  on-secondary: '#00382e'
  secondary-container: '#00d0b2'
  on-secondary-container: '#005346'
  tertiary: '#f7f7ff'
  on-tertiary: '#002e6a'
  tertiary-container: '#cddbff'
  on-tertiary-container: '#005cc5'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ff6ff'
  primary-fixed-dim: '#00dce6'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#57fbdb'
  secondary-fixed-dim: '#2adec0'
  on-secondary-fixed: '#00201a'
  on-secondary-fixed-variant: '#005144'
  tertiary-fixed: '#d8e2ff'
  tertiary-fixed-dim: '#adc6ff'
  on-tertiary-fixed: '#001a42'
  on-tertiary-fixed-variant: '#004395'
  background: '#10131a'
  on-background: '#e1e2ec'
  surface-variant: '#32353d'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.04em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.08em
  data-metric:
    fontFamily: JetBrains Mono
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 26px
    letterSpacing: -0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style
This design system defines an authoritative, diagnostic-grade dermatology environment optimized for high-acuity computer vision, triage, and multi-spectral skin analysis. The aesthetic balances clinical sterility with advanced optical instrumentation—merging dark, glare-reducing canvas layers with luminous optical targeting Reticles and frosted micro-HUDs.

### Personality & Emotional Tenor
- **Surgical Precision:** Every pixel, measurement scale, and confidence index conveys scientific integrity and non-speculative accuracy.
- **Calm Authority:** Eliminates clinical diagnostic anxiety through structured, ultra-legible readouts, unhurried animations, and controlled obsidian contrast.
- **Diagnostic Luminescence:** Functional glows and cyan-emerald spectral feedback represent active scanning states, lesion margins, and certainty metrics rather than decorative flourish.

### Design Movement: Precision Clinical-Tech Glassmorphism
The system combines deep obsidian slate surfaces (`#0A0D14` to `#121824`) with edge-lit micro-borders (`rgba(255, 255, 255, 0.12)`), precision optical reticles, and tactical diagnostic highlights. Camera viewports take precedence; UI controls sit in tactile glass suspension over the live feed, ensuring zero occlusion of critical tissue textures or color nuances.

## Colors
The palette is engineered for extreme contrast against human epidermal tones, minimizing eye strain during prolonged diagnostic and imaging sessions.

### Core Swatches
- **Primary (`#00F2FE` - Clinical Cyan):** Reserved for primary targeting rings, affirmative diagnostic confidence thresholds (>90%), active laser/scanner guidance, and primary actions.
- **Secondary (`#00D2B4` - Diagnostic Emerald):** Signifies healthy baseline tissue, verified benign classification, system calibration readiness, and completed captures.
- **Tertiary (`#3B82F6` - Deep Spectral Blue):** Informs secondary metadata, reference standard indicators, deep-layer cross-polarization toggles, and neutral diagnostic progress states.
- **Neutral Base (`#0A0D14` - Obsidian Surface):** Deep, non-reflective base canvas that preserves OLED efficiency and eliminates optical bleed when reviewing sensitive sub-surface imagery.

### Functional & State Distribution
- **Surface Elevation 0 (Canvas):** `#0A0D14`
- **Surface Elevation 1 (Card & HUD Base):** `#121824` with 72% opacity and `blur(24px)`
- **Surface Elevation 2 (Controls & Floating Trays):** `#182030` with 85% opacity
- **Diagnostic Warning / Dysplastic Alert:** `#FFB020` (Elevated risk index, atypical borders)
- **Clinical Urgency / Melanoma Risk:** `#FF3B30` (Immediate referral threshold, asymmetrical irregularity)
- **Micro-Border Accent:** `rgba(255, 255, 255, 0.12)` for razor-thin delineation.

## Typography
The system enforces strict split-type architecture: `Inter` anchors all structural communication, medical terminology, and diagnostic guidance, while `JetBrains Mono` governs optical calibration telemetry, AI confidence scoring, ABCDE metric tags, and anatomical coordinates.

### Typographic Discipline
- **Numeric Integrity:** `JetBrains Mono` prevents layout jitter when parsing dynamic lesion measurements, micro-meter boundaries, or streaming frame rate metrics.
- **Tabular Figures:** When displaying multi-variable risk metrics (Asymmetry, Border, Color, Diameter, Evolution), enable tabular numeral formatting to preserve vertical columnar alignment.
- **Optical Hierarchy:** Never use all-caps for clinical instructions or diagnoses. Reserve full uppercase strictly for `label-sm` technical telemetry (e.g., `POLARIZED-IR`, `FOV: 42MM`, `AI-V4.2`).

## Layout & Spacing
Designed for one-handed handheld dermatoscopy and rapid clinical charting, the system adopts a fluid vertical stack anchored to safe-area hardware perimeters.

### Grid & Ergonomic Zones
- **Vertical Partitioning:**
  - **Upper 15% (Optical Status Band):** Monospaced sensor status, lighting mode indicators, connection strength to peripheral dermatoscope hardware.
  - **Middle 55% (Diagnostic Aperture):** Unobstructed viewport housing the target reticle, segmentation masks, and real-time bounding hulls.
  - **Lower 30% (Clinical Action Stage):** Ergonomic thumb-zone housing floating glass action triggers, freeze-frame toggles, and confidence breakdown sheets.
- **Margins & Gaps:** A baseline 4px logical grid governs all spacing. Edge boundaries default to `margin-mobile` (16px) on compact handhelds, expanding to `margin` (24px) when deployed on clinic tablets or mounted diagnostic stations.
- **Safe Area Insets:** Floating HUD widgets maintain minimum `space-lg` (24px) clearance from active edge gestures and camera punch-outs.

## Elevation & Depth
Depth in this system is conveyed through optical translucency, micro-borders, and targeted spectral glows rather than traditional ambient drop shadows. Surfaces reflect the presence of medical laser and optical imaging engines.

### Optical Layer Architecture
- **Surface Elevation 0 (Base Layer):** Pure `#0A0D14`. Absolute ground plane; houses raw imaging feeds and deep canvas backgrounds.
- **Surface Elevation 1 (HUD Glass Panels):** `#121824` with 70% opacity, overlaid with a backdrop filter blur of `20px` to `30px`. Encased in a continuous 1px micro-border of `rgba(255, 255, 255, 0.12)`.
- **Surface Elevation 2 (Tactile Clinical Modals):** `#182030` at 88% opacity, `blur(32px)`, bordered by `rgba(255, 255, 255, 0.18)` with an inner specular edge highlight (`inset 0 1px 0 0 rgba(255, 255, 255, 0.2)`).

### Luminous Diagnostic Glows
To indicate system focus and risk tiers without obstructing underlying lesion morphology:
- **Scan Focus / Locked Target:** `box-shadow: 0 0 16px rgba(0, 242, 254, 0.35)`
- **Benign Verification Glow:** `box-shadow: 0 0 12px rgba(0, 210, 180, 0.3)`
- **High-Risk Threshold Perimeter:** `box-shadow: 0 0 20px rgba(255, 59, 48, 0.45)`

## Shapes
Geometry balances clinical discipline with ergonomic hand contact. Elements adhere to **Level 2 (Rounded)** specifications, maintaining smooth external corners that soften the technical nature of the software without feeling playful.

### Corner Radius System
- **Core Interactive Elements (Buttons, Inputs, Metric Badges):** `rounded` (0.5rem / 8px).
- **HUD Shells, Sheet Panels, Diagnostic Cards:** `rounded-lg` (1.0rem / 16px).
- **Detached Modal Overlays & Primary Camera Controls:** `rounded-xl` (1.5rem / 24px).
- **Targeting Brackets & Crosshair Nodes:** Strict `rounded-none` (0px) or `1px` micro-fillets to preserve the visual language of high-precision optical reticles and calibration tools.

## Components

### 1. Diagnostic Action Buttons
- **Primary Diagnostic Trigger (Capture / Analyze):** High-density cyan gradient fill (`#00F2FE` to `#00D2B4`), foreground `#0A0D14` with heavy weight (`fontWeight: 600`), 0.5rem radius, paired with an outer pulse ring on focus.
- **Secondary HUD Action:** Translucent obsidian fill (`rgba(18, 24, 36, 0.75)`), 1px border `rgba(255, 255, 255, 0.14)`, text `#00F2FE`.
- **Destructive / Abort Trigger:** Dark crimson glass background (`rgba(255, 59, 48, 0.12)`), border `rgba(255, 59, 48, 0.35)`, text `#FF3B30`.

### 2. Clinical Data Chips & Status Badges
- **Structure:** Monospaced label (`label-sm`), 4px vertical padding, 8px horizontal padding, radius 4px (`rounded-sm`).
- **Pathology Chips:**
  - *Melanocytic / High Suspicion:* Background `rgba(255, 59, 48, 0.15)`, text `#FF453A`, border `rgba(255, 59, 48, 0.4)`.
  - *Benign Keratosis:* Background `rgba(0, 210, 180, 0.12)`, text `#00D2B4`, border `rgba(0, 210, 180, 0.3)`.
  - *Indeterminate:* Background `rgba(255, 176, 32, 0.12)`, text `#FFB020`, border `rgba(255, 176, 32, 0.35)`.

### 3. Lesion Bounding Reticles (Domain-Specific)
- **Crosshair Coordinates:** Four corner brackets framing the lesion region with 1px stroke thickness (`#00F2FE`).
- **Telemetry Readout Attachment:** Directly anchored to the top-right bracket node; renders live diameter metrics in `label-sm` via JetBrains Mono (`e.g., Ø 4.2mm · CONF: 96.4%`).
- **Margin Segmentation Spline:** Translucent cyan stroke (`rgba(0, 242, 254, 0.8)`) with dynamic SVG stroke-dasharray animation when inference is computing.

### 4. Input Fields & Parameter Controls
- **Clinical Inputs:** Grounded `#121824` background, 1px border `rgba(255, 255, 255, 0.12)`. When focused: border changes to `#00F2FE` with a `0 0 8px rgba(0, 242, 254, 0.25)` cyan halo. Placeholder text sits at `rgba(255, 255, 255, 0.3)`.
- **Toggle Switches:** Track measures 44px × 24px in `#182030`. Thumb uses clinical cyan (`#00F2FE`) when active, shifting from left to right with zero overshoot easing.

### 5. Diagnostic Cards & Risk Matrices
- **Construction:** Frosted slate base (`#121824` at 80% opacity), `backdrop-filter: blur(24px)`, top edge accented with a 1px directional white highlight (`rgba(255, 255, 255, 0.15)`).
- **Metric Grids:** 2-column or 4-column structured layouts displaying ABCDE metrics. Monospaced value on top (`data-metric`), lowercase descriptor beneath (`label-sm`).