"""Standalone setup check and optional single Gemini request.

The local check imports the required libraries and reads the preparation
notebook. It does not open Jupyter, run the workshop or contact Gemini.
Credentials are accepted only through hidden interactive input.
"""

import argparse
from getpass import GetPassWarning, getpass
import importlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys
import warnings


EXPECTED_SDK = "2.28.0"
# Model and thinking levels: https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite
DEFAULT_MODEL = "gemini-3.5-flash-lite"
PREP_NOTEBOOK = "00_Sprawdz_srodowisko.ipynb"
SUPPORTED_PYTHONS = {(3, 11), (3, 12)}


def local_check():
    """Validate this preparation folder without a client, key or API request."""
    if tuple(sys.version_info[:2]) not in SUPPORTED_PYTHONS:
        return None, DEFAULT_MODEL, "python_version_unsupported"
    try:
        notebook = json.loads(
            Path(__file__).resolve().with_name(PREP_NOTEBOOK).read_text(encoding="utf-8")
        )
        if (not isinstance(notebook, dict) or notebook.get("nbformat") != 4
                or not isinstance(notebook.get("cells"), list)):
            return None, DEFAULT_MODEL, "local_setup_error"
        for module in ("jupyterlab", "ipykernel"):
            importlib.import_module(module)
        genai = importlib.import_module("google.genai")
        if version("google-genai") != EXPECTED_SDK:
            return None, DEFAULT_MODEL, "sdk_version_mismatch"
        return genai, DEFAULT_MODEL, "ok"
    except Exception:
        return None, DEFAULT_MODEL, "local_setup_error"


def read_key():
    # Stop before getpass can fall back to visible input in an unsupported terminal.
    with warnings.catch_warnings():
        warnings.simplefilter("error", GetPassWarning)
        return getpass("Wklej klucz API (znaki sa ukryte) i nacisnij Enter: ").strip()


def error_code(error):
    """Inspect status and type only; never read or return exception text."""
    status = getattr(error, "code", None)
    if type(status) is not int:
        status = getattr(getattr(error, "response", None), "status_code", None)
    if type(status) is int:
        known = {
            400: "request_rejected",
            401: "access_denied",
            402: "billing_required",
            403: "access_denied",
            404: "model_unavailable",
            429: "rate_limited",
        }
        if status in known:
            return known[status]
        if 500 <= status <= 599:
            return "service_unavailable"
    if isinstance(error, TimeoutError) or any(
        cls.__name__ in {"TimeoutException", "ReadTimeout", "ConnectTimeout",
                         "WriteTimeout", "PoolTimeout"}
        for cls in type(error).__mro__
    ):
        return "timeout"
    return "connection_or_sdk_error"


def probe(genai, model, api_key):
    """At most one synthetic request, with a 30-second request timeout and no retries."""
    client = None
    try:
        # Official SDK transport options: https://github.com/googleapis/python-genai
        client = genai.Client(api_key=api_key, vertexai=False, http_options={
            "timeout": 30_000,
            "retry_options": {"attempts": 1},
        })
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: OK",
            config={
                "automatic_function_calling": {"disable": True},
                "max_output_tokens": 512,
                "thinking_config": {"thinking_level": "MINIMAL", "include_thoughts": False},
            },
        )
        blocked = getattr(getattr(response, "prompt_feedback", None), "block_reason", None)
        if getattr(blocked, "value", blocked) not in (None, "", "BLOCK_REASON_UNSPECIFIED"):
            return "FAILED", "no_text_response"
        candidates = getattr(response, "candidates", None) or []
        if len(candidates) == 1:
            candidate = candidates[0]
            reason = getattr(candidate, "finish_reason", None)
            reason = getattr(reason, "value", reason)
            parts = getattr(getattr(candidate, "content", None), "parts", None) or []
            if any(getattr(part, "function_call", None) is not None for part in parts):
                return "FAILED", "no_text_response"
            if reason == "STOP" and any(
                isinstance(getattr(part, "text", None), str)
                and part.text.strip()
                and not getattr(part, "thought", False)
                for part in parts
            ):
                return "PASSED", "ok"
        return "FAILED", "no_text_response"
    except Exception as error:
        return "FAILED", error_code(error)
    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
                pass


def show_result(status, code):
    print(f"Gemini: {status}")
    print(f"Code: {code}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="AGH: local preparation and one optional Gemini request.")
    parser.add_argument("--local-only", action="store_true",
                        help="Check local setup only. No key and no API call.")
    args = parser.parse_args(argv)
    print(f"System: {platform.system()}")
    print(f"Python: {platform.python_version()}")
    genai, model, code = local_check()
    print(f"Model: {model}")
    print(f"Local: {'PASSED' if code == 'ok' else 'FAILED'}")
    if code != "ok":
        show_result("NOT_RUN", code)
        print("Sprawdz instalacje i tabele pomocy w README.md. Nie wysylaj klucza.")
        return 1
    print("Local PASSED: pliki i importy sa gotowe; to nie test pelnego labu ani interfejsu Jupyter.")
    if args.local_only:
        show_result("NOT_RUN", "local_only")
        return 0

    print("\nOpcjonalny test wysle jedno krotkie zadanie do Gemini.")
    print("Nie sprawdza planu rozliczen ani dostepnych limitow projektu.")
    print("Nie wlaczaj platnosci. Uzyj tylko projektu, do ktorego masz prawo.")
    request_started = False
    key = None
    try:
        consent = input("Znasz i akceptujesz zasady dostepu/rozliczenia projektu? Wpisz TAK: ")
        if consent.strip().upper() != "TAK":
            show_result("NOT_RUN", "not_confirmed")
            return 1
        key = read_key()
        if not key or len(key) > 512 or any(ch.isspace() for ch in key):
            show_result("NOT_RUN", "invalid_key_input")
            return 1
        print("Laczenie... (limit czasu zadania: 30 sekund)")
        request_started = True
        status, code = probe(genai, model, key)
        show_result(status, code)
        if status == "PASSED":
            print("Odebrano zakonczona odpowiedz tekstowa. To nie potwierdza darmowego planu ani limitow.")
            print("Teraz otworz 00_Sprawdz_srodowisko.ipynb zgodnie z README.md.")
        else:
            print("Sprawdz tabele pomocy w README.md. Nie powtarzaj testu w petli.")
        return 0 if status == "PASSED" else 1
    except GetPassWarning:
        show_result("NOT_RUN", "hidden_input_unavailable")
        return 1
    except (EOFError, KeyboardInterrupt):
        print()
        show_result("INCOMPLETE" if request_started else "NOT_RUN",
                    "interrupted_request" if request_started else "cancelled")
        return 1
    except OSError:
        show_result("INCOMPLETE" if request_started else "NOT_RUN",
                    "connection_or_sdk_error" if request_started else "hidden_input_unavailable")
        return 1
    finally:
        key = None


if __name__ == "__main__":
    raise SystemExit(main())
