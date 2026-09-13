# nz-visa-photo-app

Take a photo that Immigration New Zealand's online visa system will accept. The app opens the webcam, waits for OpenCV to confirm twelve checks are green, then encodes a JPEG inside the INZ size window and downloads it. Nothing between the sensor and the file touches pixel values.

Live at https://nored.github.io/nz-visa-photo-app/

## Why this exists

Germany moved biometric passport photos into the Bürgeramt, the citizen office, to close off AI-edited and tampered submissions. That service only runs as part of a passport or ID card application; you cannot walk in for a standalone biometric photo. Since the shift the shopping-centre photo automats and the photographers who specialised in biometric photos have closed, so booking a compliant shot for a foreign visa is now hard. Consumer photo apps almost all apply AI processing to the image, which INZ does not accept. This app captures straight from a webcam under the INZ rules and never touches pixel values.

## INZ spec this targets

From immigration.govt.nz/acceptable-photos:

- JPG or JPEG, 512 KB to 3.14 MB
- 3:4 portrait aspect
- Face covers 70 to 80 percent of image height
- Neutral plain background, no shadows on face or background
- Looking straight at the camera, neutral expression, mouth closed, eyes open
- Hair not covering face or ears; ears visible unless religious or medical head covering
- Glasses only if clear, no tint, no heavy frames, no glare
- Photo taken within the last six months
- "You cannot manipulate or digitally alter your photo using Artificial Intelligence (AI) or other digital editing tools"

INZ does not publish a fixed pixel range on that page. The 900 to 2250 pixel width used in the app comes from the file-size ceiling at 3:4 with JPEG quality between 0.5 and 0.95.

## Automated checks

Face detection runs on two Haar cascades from OpenCV 4.10.0, frontal face and eye, at roughly five frames per second on a 480-pixel work canvas. Background samples come from strips outside the expanded face box.

Framing
- One face detected
- Face height between 70 and 80 percent of the crop
- Face centred horizontally within plus or minus 12 percent
- Two eyes detected inside the upper two thirds of the face
- Eye line between 55 and 65 percent up from the crop bottom
- Head tilt at most 5 degrees, from the line between eye centres

Background
- Max per-channel RGB standard deviation at most 14
- Mean grayscale brightness at least 170
- Canny edge density at most 1.5 percent

Image quality
- Laplacian variance on the face region at least 45
- Face brightness between 65 and 220
- Crop width at least 900 pixels in video coordinates

The capture button unlocks only when every check is green and the auto-computed crop fits inside the video frame. Space captures, S saves, R retakes.

## What OpenCV does not verify

Neutral expression, mouth closed, ears visible under hair, tinted glasses, head coverings, uniforms. Confirm these by eye before saving.

## Build

    python3 build.py

Reads `inz-visa-photo.src.html` and the two `haarcascade_*.xml` files, base64-encodes the cascades, substitutes the two placeholders, writes `index.html`.

## Files

- `index.html`, the built output served on GitHub Pages
- `inz-visa-photo.src.html`, the editable source carrying the two cascade placeholders
- `build.py`, the substitution script
- `haarcascade_frontalface_default.xml` and `haarcascade_eye.xml`, from OpenCV 4.10.0

## Runtime dependencies

`@techstark/opencv-js@4.10.0-release.1` from jsDelivr, an OpenCV.js build with the WASM binary inlined. IBM Plex Sans and IBM Plex Mono from Google Fonts. Everything else ships inline in `index.html`.

## Licences

Application code, MIT. Haar cascades, BSD-3-Clause from OpenCV.
