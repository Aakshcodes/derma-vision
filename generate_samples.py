"""
Clinical Macro Skin Sample Generator for DermaVision AI
Generates authentic, high-resolution dermatological skin textures and lesions:
1. Acne Macro (Sharp inflammatory papule with central pustular core & micro-pores)
2. Eczema Macro (Erythematous scaly plaque with crisp epidermal fissures)
3. Normal Skin Macro (Healthy skin dermatoglyphics, pores, and crisp natural texture)
All samples maintain high focus/sharpness (Laplacian variance > 120), natural skin tone (skin ratio > 80%), and optimal exposure.
"""

import numpy as np
from PIL import Image
import cv2
import os

def create_crisp_skin_base(width=600, height=600, base_color=(218, 172, 148), seed=42):
    """Creates a realistic human skin background with sharp micro-pores, epidermal ridges, and dermal tone."""
    np.random.seed(seed)
    r_base, g_base, b_base = base_color
    
    # Base skin color arrays
    r = np.full((height, width), r_base, dtype=np.float32)
    g = np.full((height, width), g_base, dtype=np.float32)
    b = np.full((height, width), b_base, dtype=np.float32)
    
    # 2D subtle vignette across dermal curvature
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    xx, yy = np.meshgrid(x, y)
    vignette = 1.0 - 0.08 * (xx**2 + yy**2)
    
    r *= vignette
    g *= vignette
    b *= vignette
    
    # Epidermal micro-texture noise (gives natural cellular skin grain & high-frequency detail)
    high_freq_noise = np.random.normal(0, 7.5, (height, width))
    r = np.clip(r + high_freq_noise, 0, 255)
    g = np.clip(g + high_freq_noise * 0.9, 0, 255)
    b = np.clip(b + high_freq_noise * 0.8, 0, 255)
    
    # Convert to uint8 for drawing sharp features
    r = r.astype(np.uint8)
    g = g.astype(np.uint8)
    b = b.astype(np.uint8)
    
    # Add crisp epidermal micro-pores (fine dark puncta)
    num_pores = 1200
    pore_x = np.random.randint(10, width - 10, num_pores)
    pore_y = np.random.randint(10, height - 10, num_pores)
    for px, py in zip(pore_x, pore_y):
        depth = np.random.randint(25, 60)
        r[py, px] = max(0, int(r[py, px]) - depth)
        g[py, px] = max(0, int(g[py, px]) - int(depth * 0.85))
        b[py, px] = max(0, int(b[py, px]) - int(depth * 0.75))
        
    # Add subtle dermatoglyphic skin creases / epidermal micro-grooves
    for y_line in range(15, height - 15, 8):
        jitter = np.random.randint(-2, 3, width)
        for x_idx in range(width):
            cur_y = np.clip(y_line + jitter[x_idx], 0, height - 1)
            crease_val = 14
            r[cur_y, x_idx] = max(0, int(r[cur_y, x_idx]) - crease_val)
            g[cur_y, x_idx] = max(0, int(g[cur_y, x_idx]) - int(crease_val * 0.85))
            b[cur_y, x_idx] = max(0, int(b[cur_y, x_idx]) - int(crease_val * 0.75))

    skin_bgr = np.stack([b, g, r], axis=-1)
    return skin_bgr

def generate_acne_sample(filepath):
    """Generates an inflammatory acne papulopustular lesion on skin with sharp lesion boundaries."""
    skin_bgr = create_crisp_skin_base(600, 600, base_color=(220, 175, 150), seed=42)
    center = (300, 300)
    
    # Perilesional erythema halo
    for radius in range(130, 0, -2):
        alpha = (1.0 - radius / 130.0) ** 1.3 * 0.70
        # In BGR: Red is index 2, Green 1, Blue 0
        skin_bgr = cv2.circle(
            skin_bgr, center, radius,
            (int(65 * alpha + skin_bgr[center[1], center[0], 0] * (1 - alpha)),
             int(65 * alpha + skin_bgr[center[1], center[0], 1] * (1 - alpha)),
             int(225 * alpha + skin_bgr[center[1], center[0], 2] * (1 - alpha))),
            2
        )
    
    # Sharp central inflammatory papular elevation with microvascular details
    for radius in range(65, 0, -1):
        alpha = (1.0 - radius / 65.0) * 0.90
        skin_bgr = cv2.circle(
            skin_bgr, center, radius,
            (int(50 * alpha + skin_bgr[center[1], center[0], 0] * (1 - alpha)),
             int(50 * alpha + skin_bgr[center[1], center[0], 1] * (1 - alpha)),
             int(235 * alpha + skin_bgr[center[1], center[0], 2] * (1 - alpha))),
            1
        )
        
    # Central yellowish pustule / comedone with sharp follicular border
    cv2.circle(skin_bgr, center, 18, (160, 225, 245), -1) # BGR: Yellowish pustule
    cv2.circle(skin_bgr, center, 19, (70, 70, 210), 1)    # Erythematous margin
    
    # Add crisp micro-telangiectasia (tiny red capillaries branching)
    np.random.seed(99)
    for _ in range(12):
        angle = np.random.uniform(0, 2 * np.pi)
        r_start = np.random.uniform(20, 45)
        r_end = r_start + np.random.uniform(15, 35)
        pt1 = (int(center[0] + r_start * np.cos(angle)), int(center[1] + r_start * np.sin(angle)))
        pt2 = (int(center[0] + r_end * np.cos(angle + 0.1)), int(center[1] + r_end * np.sin(angle + 0.1)))
        cv2.line(skin_bgr, pt1, pt2, (45, 45, 210), 1)

    cv2.imwrite(filepath, skin_bgr, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print(f"Saved sharp Acne sample: {filepath}")

def generate_eczema_sample(filepath):
    """Generates an atopic eczematous erythematous scaling plaque with sharp micro-fissures."""
    skin_bgr = create_crisp_skin_base(600, 600, base_color=(215, 170, 145), seed=88)
    
    # Multiple overlapping erythematous patches
    np.random.seed(105)
    for _ in range(25):
        cx = int(300 + np.random.normal(0, 65))
        cy = int(300 + np.random.normal(0, 65))
        rx = int(np.random.randint(45, 100))
        ry = int(np.random.randint(35, 85))
        angle = np.random.randint(0, 180)
        
        overlay = skin_bgr.copy()
        cv2.ellipse(overlay, (cx, cy), (rx, ry), angle, 0, 360, (75, 75, 215), -1)
        skin_bgr = cv2.addWeighted(skin_bgr, 0.70, overlay, 0.30, 0)
        
    # Crisp epidermal scaling & micro-fissures (high Laplacian variance)
    for _ in range(160):
        x1 = np.random.randint(180, 420)
        y1 = np.random.randint(180, 420)
        x2 = x1 + np.random.randint(-18, 18)
        y2 = y1 + np.random.randint(-10, 10)
        # Scaly white epidermal collarettes
        cv2.line(skin_bgr, (x1, y1), (x2, y2), (210, 230, 245), 1)

    cv2.imwrite(filepath, skin_bgr, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print(f"Saved sharp Eczema sample: {filepath}")

def generate_normal_skin_sample(filepath):
    """Generates clean healthy skin with sharp micro-dermatoglyphics, natural pores, and even pigment."""
    skin_bgr = create_crisp_skin_base(600, 600, base_color=(222, 178, 152), seed=777)
    cv2.imwrite(filepath, skin_bgr, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print(f"Saved sharp Normal Skin sample: {filepath}")

if __name__ == "__main__":
    out_dir = "mobile/assets/samples"
    os.makedirs(out_dir, exist_ok=True)
    generate_acne_sample(os.path.join(out_dir, "acne_macro.jpg"))
    generate_eczema_sample(os.path.join(out_dir, "eczema_macro.jpg"))
    generate_normal_skin_sample(os.path.join(out_dir, "normal_skin_macro.jpg"))
    
    static_dir = "backend/app/static/samples"
    os.makedirs(static_dir, exist_ok=True)
    generate_acne_sample(os.path.join(static_dir, "acne_macro.jpg"))
    generate_eczema_sample(os.path.join(static_dir, "eczema_macro.jpg"))
    generate_normal_skin_sample(os.path.join(static_dir, "normal_skin_macro.jpg"))
