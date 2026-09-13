#!/usr/bin/env python3
"""Substitute the Haar cascade base64 blobs into inz-visa-photo.src.html
and write index.html. Run this after editing the source."""
import base64, pathlib, sys

root = pathlib.Path(__file__).parent
src = (root / "inz-visa-photo.src.html").read_text()

face_b64 = base64.b64encode((root / "haarcascade_frontalface_default.xml").read_bytes()).decode("ascii")
# Use the tree_eyeglasses cascade — same detector API, works with and without glasses.
eye_b64  = base64.b64encode((root / "haarcascade_eye_tree_eyeglasses.xml").read_bytes()).decode("ascii")

for token in ("___BASE64_FACE___", "___BASE64_EYE___"):
    if token not in src:
        sys.exit(f"placeholder {token} missing from source")

built = src.replace("___BASE64_FACE___", face_b64).replace("___BASE64_EYE___", eye_b64)
(root / "index.html").write_text(built)
print(f"wrote index.html ({len(built):,} bytes)")
