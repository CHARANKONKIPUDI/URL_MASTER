from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from .models import ShortURL

import requests
import speedtest
import qrcode
import io
import string
import secrets
from urllib.parse import urlparse

# ----------------- Speedtest setup (safe) ----------------- #

try:
    speed = speedtest.Speedtest()
except Exception as e:
    print("Speedtest initialization failed:", e)
    speed = None


def home(request):
    """Render the home page with the URL input form."""
    return render(request, "index.html")


def result(request):
    """Handle URL submission, shortening, checking, speed test, and show result."""
    if request.method == "POST":
        url = request.POST.get("url", "").strip()

        if not url:
            return render(request, "index.html", {"error": "Please enter a URL."})

        # Parse URL to extract hostname and path
        parsed = urlparse(url)
        host_name = parsed.hostname
        path = parsed.path

        # Check original URL (not shortened) – you can keep or remove this
        check = check_url(url)

        # Create our own short code and save in DB
        short_code = generate_short_code()
        short_obj = ShortURL.objects.create(
            original_url=url,
            short_code=short_code,
        )

        # Build full short URL for display (e.g., http://127.0.0.1:8000/s/Ab12Xy)
        short_link = request.build_absolute_uri(
            reverse("redirect_short", args=[short_code])
        )

        # Run speed tests (may return "N/A" if speedtest failed)
        download_speed = get_download_speed()
        upload_speed = get_upload_speed()

        return render(
            request,
            "result.html",
            {
                "short_url": short_link,
                "check": check,
                "download_speed": download_speed,
                "upload_speed": upload_speed,
                "host_name": host_name,
                "path": path,
            },
        )

    # If method is GET, just show the input form
    return render(request, "index.html")


def qr_code_view(request):
    """Return a PNG QR code image for the given URL (short URL)."""
    url = request.GET.get("url")
    if url is None:
        return HttpResponseBadRequest("Missing URL parameter")

    img = generate_qr_code(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type="image/png")


def redirect_short(request, code):
    """Redirect from short code to the original URL."""
    short_obj = get_object_or_404(ShortURL, short_code=code)
    return redirect(short_obj.original_url)


# ----------------- Helper functions ----------------- #

def generate_short_code(length: int = 6) -> str:
    """Generate a unique random short code."""
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(secrets.choice(chars) for _ in range(length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code


def check_url(url: str) -> str:
    """Check if a URL is reachable using a HEAD request."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return "URL is good."
        else:
            return "URL is bad."
    except requests.exceptions.RequestException:
        return "URL is bad."


def generate_qr_code(data: str):
    """Generate a QR code PIL image for the given data."""
    qr = qrcode.QRCode(version=1, box_size=5, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def get_download_speed() -> str:
    """Return download speed in Mb/s as string or 'N/A' if not available."""
    try:
        if speed is None:
            return "N/A"
        return "{:.2f} Mb/s".format(speed.download() / 1024 / 1024)
    except Exception:
        return "N/A"


def get_upload_speed() -> str:
    """Return upload speed in Mb/s as string or 'N/A' if not available."""
    try:
        if speed is None:
            return "N/A"
        return "{:.2f} Mb/s".format(speed.upload() / 1024 / 1024)
    except Exception:
        return "N/A"
