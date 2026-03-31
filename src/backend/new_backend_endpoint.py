from __future__ import annotations
import base64
import io
import asyncio
import threading
from typing import Tuple
from uuid import UUID
import httpx
from PIL import Image
from urllib.parse import urljoin
import logging

# NOT PROUD OF THE FOLLOWING CODE, i created a new file just to pplay with it with calm later

# Use logger configured in main (coherent name)
logger = logging.getLogger("photobooth.upload")


class PhotoAPIClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        client_id: str = "agent",
        client_secret: str = None,
        timeout: Tuple[float, float] = (5.0, 30.0),
    ):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret

        # httpx requires all four fields or a single default
        self.timeout = httpx.Timeout(
            connect=timeout[0],
            read=timeout[1],
            write=timeout[1],
            pool=timeout[0],
        )

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        # logger.info("PhotoAPIClient initialized with base_url=%s", self.base_url)

    async def login(self):
        """Perform login to get JWT Bearer token."""
        logger.info("Attempting login to backend...")
        payload = {"client_id": self.client_id, "client_secret": self.client_secret}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                r = await client.post(f"{self.base_url}/oauth/token", json=payload)
                r.raise_for_status()
                token = r.json()["access_token"]
                self.headers["Authorization"] = f"Bearer {token}"
                logger.info("Login successful")
            except Exception as e:
                logger.error(f"Login failed: {e}")
                raise

    async def upload_pil(self, img: Image.Image, photo_name: str) -> UUID:
        """
        Send a PIL image as PNG base64 to POST /photos and return the new photo UUID (async).
        """
        # --- LOG 1: START UPLOAD ---
        logger.info(f"Uploading '{photo_name}' started")

        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")

        # logger.debug("Starting async upload_pil, image mode=%s", img.mode)
        # (commented: debug log removed)

        b64 = await asyncio.to_thread(self._to_b64, img)

        if not self.headers.get("Authorization") and self.client_secret:
            await self.login()

        async with httpx.AsyncClient(
            timeout=self.timeout, headers=self.headers
        ) as client:
            try:
                # logger.info("POST %s/photos (async)", self.base_url)  # removed
                r = await client.post(f"{self.base_url}/photos", json={"data": b64})

                if r.status_code == 401 and self.client_secret:
                    logger.warning(
                        f"401 Unauthorized for '{photo_name}', retrying login"
                    )
                    await self.login()
                    # Re-create client with new headers (token refreshed)
                    async with httpx.AsyncClient(
                        timeout=self.timeout, headers=self.headers
                    ) as retry_client:
                        r = await retry_client.post(
                            f"{self.base_url}/photos", json={"data": b64}
                        )

                r.raise_for_status()

                photo_id = UUID(r.json()["id"])

                # --- LOG 2: SUCCESS ---
                logger.info(f"Upload OK '{photo_name}' -> {photo_id}")

                return photo_id

            except httpx.TimeoutException:
                # --- LOG 3: HANDLED FAILURE ---
                logger.error(f"Upload FAILED (timeout) for '{photo_name}'")
                raise

            except httpx.ConnectError:
                # --- LOG 3: HANDLED FAILURE ---
                logger.error(
                    f"Upload FAILED (backend unreachable) for '{photo_name}'. Connection Error"
                )
                raise

            except httpx.ReadError:
                logger.error(
                    f"Upload FAILED (backend unreachable) for '{photo_name}'. Read Error"
                )
                raise

            except Exception:
                # Unhandled → real stacktrace
                logger.exception(f"Unhandled error while uploading '{photo_name}'")
                raise

    # ---------- BACKGROUND ----------
    def upload_pil_background(self, img: Image.Image, photo_name: str) -> None:
        """Fire-and-forget upload that never blocks the caller."""

        def _worker():
            not_sent = True

            while not_sent:
                try:
                    # logger.info("Background upload started")  # removed
                    asyncio.run(self.upload_pil(img, photo_name))
                    # logger.info("Background upload finished OK")  # removed
                    not_sent = False

                except httpx.ConnectError:
                    # handled: backend unreachable — log without traceback
                    logger.info(
                        f"The upload of '{photo_name}' will be retried in 5 seconds"
                    )
                    import time

                    time.sleep(5)
                except httpx.TimeoutException:
                    logger.info(
                        f"The upload of '{photo_name}' will be retried in 5 seconds"
                    )
                    import time

                    time.sleep(5)
                except httpx.ReadError:
                    logger.info(
                        f"The upload of '{photo_name}' will be retried in 5 seconds"
                    )
                    import time

                    time.sleep(5)
                except Exception:
                    # real unexpected errors: print stacktrace
                    logger.exception(
                        f"[PhotoAPIClient] Background upload failed for '{photo_name}'"
                    )
                    not_sent = False

        threading.Thread(target=_worker, daemon=True).start()

    # ---------- SYNC VERSION ----------
    def upload_pil_sync(self, img: Image.Image, photo_name: str) -> UUID:
        """Blocking version (no asyncio)."""

        # --- LOG 1: START UPLOAD ---
        logger.info(f"Uploading '{photo_name}' started")

        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")

        # logger.debug("Starting sync upload_pil_sync, image mode=%s", img.mode)  # removed

        b64 = self._to_b64(img)

        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            try:
                # logger.info("POST %s/photos (sync)", self.base_url)  # removed
                r = client.post(f"{self.base_url}/photos", json={"data": b64})

                # logger.debug("Response status (sync): %s", r.status_code)  # removed
                r.raise_for_status()

                photo_id = UUID(r.json()["id"])

                # --- LOG 2: SUCCESS ---
                logger.info(f"Upload OK '{photo_name}' → {photo_id}")

                return photo_id

            except httpx.TimeoutException:
                logger.error(f"Upload FAILED (timeout) for '{photo_name}'")
                raise

            except httpx.ConnectError:
                logger.error(f"Upload FAILED (backend unreachable) for '{photo_name}'")
                raise

            except Exception:
                logger.exception(f"Unhandled error while uploading '{photo_name}'")
                raise

    # just for test purpose
    def download_image_by_id(self, photo_id: UUID):
        # logger.info("Downloading image, id=%s", photo_id)  # removed
        with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
            r = client.get(f"{self.base_url}/photos/{photo_id}")
            # logger.debug("GET metadata status: %s", r.status_code)  # removed
            r.raise_for_status()

            raw_url = r.json()["url"]
            raw_url = urljoin(self.base_url, raw_url)

            # logger.info("GET raw image %s", raw_url)  # removed
            r = client.get(raw_url)
            # logger.debug("GET raw status: %s", r.status_code)  # removed
            r.raise_for_status()

        img = Image.open(io.BytesIO(r.content))
        img.load()
        # logger.info("Image downloaded and decoded")  # removed
        return img

    def _to_b64(self, img: Image.Image) -> str:
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")

        # Detach from the file & ensure all pixels are in memory
        # it seems that sometimes pillow works lazily and can break stuff here
        img.load()
        img = img.copy()

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode("ascii")

        # logger.debug("Image converted to base64 (%d chars)", len(encoded))  # removed
        return encoded
