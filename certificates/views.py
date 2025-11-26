import os

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv

load_dotenv()


@require_http_methods(["GET"])
def home(request):
    """Render the homepage that embeds the ChatKit widget."""
    return render(request, "home.html")


@csrf_exempt
@require_http_methods(["POST"])
def create_chatkit_session(request):
    """Backend endpoint used by ChatKit to obtain a client_secret.

    This mirrors the ChatKit docs: it creates a session bound to the
    workflow ID from your Agent Builder and returns the client_secret
    to the browser, which then uses it to start the chat.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    workflow_id = os.getenv("WORKFLOW_ID")

    if not api_key or not workflow_id:
        return JsonResponse(
            {"error": "Server missing OPENAI_API_KEY or WORKFLOW_ID."},
            status=500,
        )

    try:
        resp = requests.post(
            "https://api.openai.com/v1/chatkit/sessions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "chatkit_beta=v1",
            },
            json={
                "workflow": {"id": workflow_id},
                "user": "web-user",
            },
            timeout=30,
        )
        data = resp.json()
        if resp.status_code != 200:
            return JsonResponse(
                {"error": data},
                status=resp.status_code,
            )

        client_secret = data.get("client_secret")
        if not client_secret:
            return JsonResponse(
                {"error": "chatkit/sessions response missing client_secret."},
                status=500,
            )

        return JsonResponse({"client_secret": client_secret})
    except Exception as exc:  # noqa: BLE001
        return JsonResponse(
            {"error": f"Failed to create ChatKit session: {exc}"},
            status=500,
        )

