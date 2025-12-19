from backend.backend_endpoint import PhotoAPIClient
from PIL import Image, ImageChops


def images_equal(a, b):
    a = a.convert("RGB")
    b = b.convert("RGB")
    return a.size == b.size and ImageChops.difference(a, b).getbbox() is None

def test_backend():
    test_image_path = "./test/assets/test.png"
    image = Image.open(test_image_path)
    backend = PhotoAPIClient()

    uuid = backend.upload_pil_sync(image)
    # print(uuid)
    server_image = backend.download_image_by_id(uuid)
    # image.show()

    assert images_equal(image, server_image)
    