from __future__ import annotations
import base64, io, asyncio, threading
from typing import Tuple
from uuid import UUID
import httpx
from PIL import Image

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

    def _to_b64(self, img: Image.Image) -> str:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("ascii")




test_image_path = "./test/assets/test.png"
image = Image.open(test_image_path)

client = PhotoAPIClient()
client.upload_pil_background(image)

"""
for i in range(10):
    print("sending")
    output = client.upload_pil_background(image)
    """

print("done")