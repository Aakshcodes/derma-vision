# DermaVision AI — Mobile UI/UX Design System & Screen Specifications

**Design Reference:** Crextio Human-Centered Dashboard ("Welcome in, Nixtio")  
**Aesthetic Theme:** *Warm Cream, Amber Gold & Charcoal Glass* (Calming Healthcare Aesthetic)

---

## 1. Visual Reference Analysis & Translation

### 1.1 Why This Aesthetic Excels in Healthcare
Traditional clinical applications rely heavily on cold clinical blues, stark whites, and harsh sterile borders, which frequently induce **"white coat anxiety"** and diagnostic distress in users inspecting potential medical issues.

The provided reference image introduces a warm, welcoming, editorial environment:
- **Calm, Human Warmth:** Gentle butter-cream and champagne gradients soften the medical context.
- **Authoritative Contrast:** Deep charcoal (`#181818`) containers provide grounding, gravitas, and high contrast for critical data.
- **Luminous Confidence:** Warm amber gold (`#F6CF4E`) is utilized for status pills, progress arcs, and affirmative action triggers.
- **Generous Curvature:** Tactile `rounded-3xl` (24–28px) cards and full pill capsules (`rounded-full`) feel organic and approachable.

---

## 2. Design Tokens & Palette

### 2.1 Color Tokens
| Token Name | Hex Code | Visual Role & Usage |
| :--- | :--- | :--- |
| `canvas-bg` | `#FAF7EE` | Primary warm ivory screen background |
| `canvas-gradient-end` | `#FEF5D7` | Soft champagne radial gradient glow in header |
| `surface-card` | `#FFFFFF` | Crisp white elevated card surface |
| `surface-dark` | `#181818` | High-contrast charcoal card container |
| `surface-dark-subtle`| `#242424` | Elevated charcoal list items & task rows |
| `accent-gold` | `#F6CF4E` | Primary brand accent, active toggles, confidence indicators |
| `accent-gold-light` | `#FDF4CE` | Subtle warm pill background for badges |
| `text-primary` | `#141414` | Deepest slate for titles and headline metrics |
| `text-secondary` | `#707070` | Muted neutral for supporting metadata and labels |
| `text-on-dark` | `#FFFFFF` | Crisp text inside charcoal cards |
| `border-subtle` | `#EFECE3` | Soft dotted or solid hairline card borders |

### 2.2 Typography Architecture
- **Primary Font Family:** `Inter` or `Plus Jakarta Sans`
  - **Display Hero:** `32px / 38px`, Bold (e.g., *"Welcome in, Jordan"*)
  - **Headline Large:** `22px / 28px`, SemiBold (*"Today's Analysis"*)
  - **Card Title:** `17px / 22px`, Medium
  - **Metric Display:** `28px / 32px`, Bold, Tabular numerals
  - **Body Text:** `14px / 20px`, Regular
  - **Caption / Badge:** `11px / 14px`, SemiBold, Tracking `0.04em`

### 2.3 Component Primitives (Extracted from Reference)
1. **Pill Action CTA:** `bg-[#181818] text-white rounded-full px-6 py-3.5 font-medium shadow-sm hover:scale-[0.98]`
2. **Circular Metric Ring:** SVG arc stroke with `#F6CF4E` fill displaying confidence or progress inside a white card.
3. **Dotted Attribute Separator:** Subtle `border-b border-dotted border-[#E8E4DA]` for anatomical location and ABCDE metrics.
4. **Charcoal Checklist Container:** Deep dark container housing scan tasks, status checks, and quality feedback badges.

---

## 3. Specification for the 12 Required Mobile Screens

```
Screen 1:  Splash Screen
           Warm cream canvas, subtle pulsing DermaVision emblem, typography fadeIn.

Screen 2:  Onboarding Carousel (3 Slides)
           1. Visual AI Screening (Camera illustration with amber reticle).
           2. Grad-CAM Explainability (Visual transparency, not a black box).
           3. Privacy First & Non-Diagnostic Disclosure (Explicit consent).

Screen 3:  Login / Signup / Guest Demo Mode
           Clean inputs with warm cream borders; prominent "Continue as Guest" pill button.

Screen 4:  Home Dashboard
           Greeting card ("Welcome in, Jordan"), prominent "Start Skin Scan" action card,
           recent analysis cards, and educational insights row.

Screen 5:  Camera Capture & Viewfinder
           Full-screen optical viewfinder with dynamic framing circle, real-time blur/lighting
           badges, flash toggle, and shutter button.

Screen 6:  Image Preview & Crop
           Allows users to verify sharpness, adjust crop boundaries, and read the pre-analysis privacy confirmation.

Screen 7:  Analysis Loading Stage
           Progress indicator cycling through: (1) Image Quality Gate -> (2) Neural Feature Extraction -> (3) Grad-CAM Heatmap Synthesis.

Screen 8:  Analysis Results
           Prediction card (e.g., "Acne - Mild Inflammatory"), Calibrated Confidence Dial (94.2%),
           Side-by-Side Dual Slider (Original vs Grad-CAM Heatmap), and Triage Recommendations.

Screen 9:  Analysis History
           Chronological list of past scans with thumbnail previews, condition chips, and delete actions.

Screen 10: Educational Hub
           Curated articles on Acne, Eczema, Sun Care, and Clinical Red Flags with category filters.

Screen 11: User Profile
           Account info, skin preferences, data export, and "Delete All My Data" button.

Screen 12: Settings & Legal Disclosures
           Notification toggles, full Medical Disclaimer, Terms of Service, and Privacy Policy.
```
