import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
import cv2
import numpy as np

from ..core.config import settings


class StorageService:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or settings.STORAGE_DIR
        self.orig_dir = self.base_dir / "originals"
        self.heat_dir = self.base_dir / "heatmaps"
        self.over_dir = self.base_dir / "overlays"

        # Create subdirectories
        for d in [self.orig_dir, self.heat_dir, self.over_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def save_analysis_images(
        self,
        analysis_id: str,
        original_rgb: np.ndarray,
        heatmap_rgb: np.ndarray,
        overlay_rgb: np.ndarray,
    ) -> Tuple[str, str, str]:
        """
        Saves original, heatmap, and overlay images as JPEGs.
        Returns paths relative to the storage base directory.
        """
        file_stem = f"{analysis_id}.jpg"

        orig_path = self.orig_dir / file_stem
        heat_path = self.heat_dir / file_stem
        over_path = self.over_dir / file_stem

        # OpenCV expects BGR for imwrite
        cv2.imwrite(str(orig_path), cv2.cvtColor(original_rgb, cv2.COLOR_RGB2BGR))
        cv2.imwrite(str(heat_path), cv2.cvtColor(heatmap_rgb, cv2.COLOR_RGB2BGR))
        cv2.imwrite(str(over_path), cv2.cvtColor(overlay_rgb, cv2.COLOR_RGB2BGR))

        return (
            f"originals/{file_stem}",
            f"heatmaps/{file_stem}",
            f"overlays/{file_stem}",
        )

    def delete_analysis_images(
        self,
        raw_path: Optional[str] = None,
        heat_path: Optional[str] = None,
        over_path: Optional[str] = None,
    ):
        for rel_path in [raw_path, heat_path, over_path]:
            if rel_path:
                full_path = self.base_dir / rel_path
                if full_path.exists():
                    try:
                        full_path.unlink()
                    except Exception:
                        pass
