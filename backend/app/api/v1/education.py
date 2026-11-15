from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/education", tags=["Education"])

ARTICLES = [
    {
        "id": "1",
        "slug": "understanding-acne-causes-and-care",
        "title": "Understanding Acne: Causes, Types, and Evidence-Based Care",
        "category": "Acne",
        "read_time_minutes": 4,
        "summary": "Learn what triggers follicular inflammation and how to care for acne-prone skin without causing scarring.",
        "content_markdown": """# Understanding Acne Vulgaris

Acne is one of the most common dermatological conditions globally. It occurs when hair follicles become plugged with sebum and keratinized skin cells.

### Common Types:
- **Comedones (Non-inflammatory):** Blackheads (open comedones) and whiteheads (closed comedones).
- **Inflammatory Papules & Pustules:** Small, erythematous, tender bumps that may contain visible purulent fluid.
- **Nodulocystic Lesions:** Deeper, painful lesions that pose a high risk of scarring and require prompt dermatological care.

### Core Care Principles:
1. **Gentle Cleansing:** Use a balanced pH 5.5 foaming cleanser twice daily.
2. **Do Not Pick:** Squeezing or picking lesions ruptures the follicular wall and spreads inflammation into the dermis.
3. **Non-Comedogenic Products:** Always check labels for 'non-comedogenic' to ensure products do not clog pores.
""",
    },
    {
        "id": "2",
        "slug": "eczema-management-and-skin-barrier",
        "title": "Eczema & Atopic Dermatitis: Restoring the Epidermal Barrier",
        "category": "Eczema",
        "read_time_minutes": 5,
        "summary": "How to soothe itching, avoid common irritant triggers, and repair skin barrier function using ceramides.",
        "content_markdown": """# Managing Eczema (Atopic Dermatitis)

Eczema involves dysfunction in the stratum corneum skin barrier, leading to heightened transepidermal water loss and sensitivity to environmental allergens.

### Cardinal Signs:
- Erythematous, dry, flaky patches with pruritus (intense itching).
- Lichenification (thickened skin) from chronic scratching.

### Best Practices:
1. **Moisturize Within 3 Minutes:** Apply thick ointment or cream immediately after bathing to seal in hydration.
2. **Avoid Fragrance & Harsh Detergents:** Fragrances are the leading trigger for contact dermatitis flare-ups.
3. **Temperature Control:** Hot water strips natural lipid bilayers; use lukewarm water instead.
""",
    },
    {
        "id": "3",
        "slug": "when-to-see-a-dermatologist",
        "title": "When Should You Consult a Dermatologist Immediately?",
        "category": "Clinical Triage",
        "read_time_minutes": 3,
        "summary": "Red flags that require urgent or professional in-person medical evaluation.",
        "content_markdown": """# Dermatological Red Flags

While DermaVision AI provides educational triage assistance, the following symptoms require immediate in-person medical review:

1. **Rapidly Changing Lesions:** Any mole that changes size, shape, color, or elevation over a matter of weeks.
2. **Spontaneous Bleeding or Ulceration:** Lesions that ooze, bleed without trauma, or fail to heal after 3–4 weeks.
3. **Severe Pain or Systemic Symptoms:** Spreading redness accompanied by fever, chills, or streaking lymphatics.
4. **Suspected Drug Eruptions:** Widespread rash appearing shortly after starting a new oral medication.
""",
    },
]


@router.get("/articles")
def list_articles(category: Optional[str] = None):
    if category:
        return [a for a in ARTICLES if a["category"].lower() == category.lower()]
    return ARTICLES


@router.get("/articles/{slug}")
def get_article(slug: str):
    for a in ARTICLES:
        if a["slug"] == slug:
            return a
    raise HTTPException(status_code=404, detail="Article not found.")
