from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None


def optimize_uploaded_image(uploaded_file, max_size=(1600, 1600), quality=82):
    if Image is None:
        return uploaded_file

    uploaded_file.seek(0)
    with Image.open(uploaded_file) as image:
        image = image.convert("RGB")
        image.thumbnail(max_size)

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=quality, optimize=True)
        buffer.seek(0)

        stem = Path(getattr(uploaded_file, "name", "upload.jpg")).stem
        optimized_name = f"{stem}.jpg"
        return ContentFile(buffer.read(), name=optimized_name)
