from typing import Dict, Any, Optional, List
import requests
import time

BRIA_USER_AGENT = "BriaPlatform/Sandbox/LLMsAgent"
V2_GENERATE_URL = "https://engine.prod.bria-api.com/v2/image/generate"


def _bria_headers(api_key: str) -> Dict[str, str]:
    return {
        "api_token": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": BRIA_USER_AGENT,
    }


def _extract_image_url(payload: Dict[str, Any]) -> Optional[str]:
    res = payload.get("result")
    if isinstance(res, dict):
        url = res.get("image_url")
        if url:
            return url
    return None


def _poll_until_image(
    status_url: str,
    headers: Dict[str, str],
    interval: float = 2.0,
    timeout: float = 600.0,
) -> Dict[str, Any]:
    deadline = time.time() + timeout
    last_payload: Optional[Dict[str, Any]] = None
    while time.time() < deadline:
        resp = requests.get(status_url, headers=headers, timeout=120)
        resp.raise_for_status()
        last_payload = resp.json()
        url = _extract_image_url(last_payload)
        if url:
            return last_payload
        status = (last_payload.get("status") or "").upper()
        if status == "ERROR":
            err = last_payload.get("error") or last_payload
            raise Exception(f"Bria generation failed: {err}")
        if status == "UNKNOWN":
            raise Exception(
                f"Bria returned UNKNOWN status. If this persists, contact Bria support. Body: {last_payload}"
            )
        time.sleep(interval)
    raise TimeoutError(
        f"Timed out waiting for Bria image ({timeout}s). Last response: {last_payload}"
    )


def _generate_one_v2(
    prompt: str,
    api_key: str,
    aspect_ratio: str,
    sync: bool,
    seed: Optional[int],
    resolution: str,
    ip_signal: bool,
    prompt_content_moderation: bool,
    visual_output_moderation: bool,
    steps_num: Optional[int],
    guidance_scale: Optional[int],
) -> Dict[str, Any]:
    headers = _bria_headers(api_key)
    # 4MP + sync=true returns 422 ("sync request is not supported with 4MP resolution").
    use_sync = bool(sync) and resolution != "4MP"
    body: Dict[str, Any] = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "sync": use_sync,
        "resolution": resolution,
        "ip_signal": ip_signal,
        "prompt_content_moderation": prompt_content_moderation,
        "visual_output_content_moderation": visual_output_moderation,
        "visual_input_content_moderation": False,
    }
    if seed is not None:
        body["seed"] = seed
    if steps_num is not None:
        body["steps_num"] = max(1, min(steps_num, 50))
    if guidance_scale is not None:
        body["guidance_scale"] = max(3, min(int(round(guidance_scale)), 5))

    resp = requests.post(V2_GENERATE_URL, headers=headers, json=body, timeout=600)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        detail = resp.text[:2000] if resp.text else str(e)
        raise Exception(f"HD image generation failed ({resp.status_code}): {detail}") from e

    data = resp.json()

    status_url = data.get("status_url")
    if not _extract_image_url(data):
        if not status_url:
            rid = data.get("request_id")
            if rid:
                status_url = f"https://engine.prod.bria-api.com/v2/status/{rid}"
        if status_url:
            data = _poll_until_image(status_url, headers, timeout=900.0)
        else:
            raise Exception(f"Unexpected Bria response (no image URL): {data}")

    if not _extract_image_url(data):
        raise Exception(f"Unexpected Bria response (no image URL): {data}")

    return data


def generate_hd_image(
    prompt: str,
    api_key: str,
    model_version: str = "2.2",
    num_results: int = 1,
    aspect_ratio: str = "1:1",
    sync: bool = True,
    seed: Optional[int] = None,
    negative_prompt: str = "",
    steps_num: Optional[int] = None,
    text_guidance_scale: Optional[float] = None,
    medium: Optional[str] = None,
    prompt_enhancement: bool = False,
    enhance_image: bool = False,
    content_moderation: bool = False,
    ip_signal: bool = False,
) -> Dict[str, Any]:
    """Generate images from a text prompt via Bria ``/v2/image/generate``.

    The legacy ``/v1/text-to-image/hd/...`` path is no longer used; it commonly
    returned 500 errors. V2 is the supported API (see Bria platform docs).

    ``model_version`` is kept for call compatibility but ignored (v2 Fibo model).
    """
    if not prompt:
        raise ValueError("Prompt is required for image generation")
    if not api_key or not str(api_key).strip():
        raise ValueError("API key is required")

    full_prompt = prompt
    if negative_prompt and str(negative_prompt).strip():
        full_prompt = f"{prompt}\n\nAvoid: {negative_prompt.strip()}"
    if medium and str(medium).strip():
        full_prompt = f"{full_prompt}\n\nMedium: {medium.strip()}."

    resolution = "4MP" if enhance_image else "1MP"
    mod_prompt = bool(content_moderation)
    mod_visual = bool(content_moderation)

    guidance_int: Optional[int] = None
    if text_guidance_scale is not None:
        guidance_int = max(3, min(int(round(float(text_guidance_scale))), 5))

    urls: List[str] = []
    last_raw: Dict[str, Any] = {}

    n = max(1, min(int(num_results), 4))
    for i in range(n):
        use_seed = seed if seed is not None else None
        if n > 1 and seed is not None:
            use_seed = seed + i

        last_raw = _generate_one_v2(
            prompt=full_prompt,
            api_key=api_key,
            aspect_ratio=aspect_ratio or "1:1",
            sync=sync,
            seed=use_seed,
            resolution=resolution,
            ip_signal=bool(ip_signal),
            prompt_content_moderation=mod_prompt,
            visual_output_moderation=mod_visual,
            steps_num=steps_num,
            guidance_scale=guidance_int,
        )
        u = _extract_image_url(last_raw)
        if u:
            urls.append(u)

    if not urls:
        raise Exception("Bria returned no image URLs")

    out: Dict[str, Any] = dict(last_raw)
    if len(urls) == 1:
        out["result_url"] = urls[0]
    else:
        out["result_urls"] = urls
    return out
