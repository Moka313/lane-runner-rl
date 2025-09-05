# assets.py
import os
import io
import pygame
import requests
from config import ASSET_URLS, ASSET_DIR

HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python-requests image fetch"}

def _download_to(path: str, url: str) -> bool:
    try:
        r = requests.get(url, headers=HDRS, timeout=20)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return True
    except Exception:
        return False

def _load_png(path: str) -> pygame.Surface:
    data = open(path, "rb").read()
    return pygame.image.load(io.BytesIO(data)).convert_alpha()

def _ensure(name: str, url: str) -> str:
    local = os.path.join(ASSET_DIR, name)
    if not os.path.exists(local):
        ok = _download_to(local, url)
        if not ok:
            # leave an empty file so we can detect fallback later
            with open(local, "wb") as f:
                f.write(b"")
    return local

def _make_fallback(shape: str = "rect", size=(80, 120), color=(200, 60, 60)) -> pygame.Surface:
    surf = pygame.Surface(size, pygame.SRCALPHA)
    if shape == "rect":
        pygame.draw.rect(surf, color, surf.get_rect(), border_radius=8)
    elif shape == "circle":
        r = min(size)//2
        pygame.draw.circle(surf, color, (size[0]//2, size[1]//2), r)
    return surf

def _crop_rock_cell(surf: pygame.Surface) -> pygame.Surface:
    # asteroid_01_no_moblur.png is a square spritesheet; take the first cell
    w, h = surf.get_size()
    # try an 8x8 grid first; else 10x10 fallback
    grid = 8 if w % 8 == 0 else (10 if w % 10 == 0 else 6)
    cell = w // grid
    rect = pygame.Rect(0, 0, cell, cell)
    cell_surf = pygame.Surface((cell, cell), pygame.SRCALPHA)
    cell_surf.blit(surf, (0, 0), rect)
    return cell_surf

def _crop_old_lady(surf: pygame.Surface) -> pygame.Surface:
    # take the left half (the silhouette image contains two people)
    w, h = surf.get_size()
    rect = pygame.Rect(0, 0, w//2, h)
    out = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    out.blit(surf, (0, 0), rect)
    return out

def load_assets() -> dict:
    loaded = {}
    for name, url in ASSET_URLS.items():
        path = _ensure(name, url)
        surf = None
        if os.path.getsize(path) > 0:
            try:
                surf = _load_png(path)
            except Exception:
                surf = None
        # Special post-processing
        if surf:
            if name == "rock.png":
                surf = _crop_rock_cell(surf)
            elif name == "old_lady.png":
                surf = _crop_old_lady(surf)
        if not surf:
            # fallbacks
            if name in ("car.png", "broken_car.png"):
                surf = _make_fallback("rect", (70, 120), (240, 80, 80 if name=="broken_car.png" else 80))
            elif name == "rock.png":
                surf = _make_fallback("circle", (72, 72), (150, 150, 150))
            elif name == "trashcan.png":
                surf = _make_fallback("rect", (50, 70), (120, 180, 200))
            elif name == "old_lady.png":
                surf = _make_fallback("rect", (40, 100), (60, 60, 60))
        loaded[name] = surf
    return loaded
