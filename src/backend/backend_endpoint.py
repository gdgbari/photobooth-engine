from __future__ import annotations
import base64, io, asyncio, threading
from typing import Tuple
from uuid import UUID
import httpx
from PIL import Image
import time
from urllib.parse import urljoin

class PhotoAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: Tuple[float, float] = (5.0, 30.0)):
        self.base_url = base_url.rstrip("/")
        # httpx requires all four fields or a single default
        self.timeout = httpx.Timeout(
            connect=timeout[0],
            read=timeout[1],
            write=timeout[1],
            pool=timeout[0],
        )
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async def upload_pil(self, img: Image.Image) -> UUID:
        """Send a PIL image as PNG base64 to POST /photos and return the new photo UUID (async)."""
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")
        b64 = await asyncio.to_thread(self._to_b64, img)
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            r = await client.post(f"{self.base_url}/photos", json={"data": b64})
            r.raise_for_status()
            return UUID(r.json()["id"])

    def upload_pil_background(self, img: Image.Image) -> None:
        """Fire-and-forget upload that never blocks the caller."""
        def _worker():
            try:
                asyncio.run(self.upload_pil(img))
            except Exception as e:
                # Replace with your logger if you have one
                print(f"[PhotoAPIClient] Upload failed: {e}")
        threading.Thread(target=_worker, daemon=True).start()

    # ---------- SYNC ----------
    def upload_pil_sync(self, img: Image.Image) -> UUID:
        """Blocking version (no asyncio)."""
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")
        b64 = self._to_b64(img)
        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            r = client.post(f"{self.base_url}/photos", json={"data": b64})
            r.raise_for_status()
            return UUID(r.json()["id"])
        
    # just for test purpose
    def download_image_by_id(self, photo_id : UUID):
        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            # First get the signed/raw URL from metadata
            r = client.get(f"{self.base_url}/photos/{photo_id}")
            r.raise_for_status()
            raw_url = r.json()["url"]

            # Now fetch the actual image bytes
            raw_url = urljoin(self.base_url, raw_url)
            r = client.get(raw_url)
            r.raise_for_status()

        img = Image.open(io.BytesIO(r.content))
        img.load()  # fully decode so the BytesIO can close
        return img


    def _to_b64(self, img: Image.Image) -> str:
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")

        # Detach from the file & ensure all pixels are in memory
        # it seems that sometimes it pillow work in a lazy way and can break stuff here
        img.load()
        img = img.copy()

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("ascii")


