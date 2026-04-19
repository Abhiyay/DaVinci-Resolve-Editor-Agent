"""AI engine using local llama.cpp model."""

from __future__ import annotations

import json
from typing import Any

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None  # type: ignore


class AIEngine:
    """Local AI model for command generation."""

    def __init__(self, model_path: str | None = None):
        if Llama is None:
            raise ImportError(
                "llama-cpp-python not installed. "
                "Install with: pip install llama-cpp-python"
            )
        self.model_path = model_path
        self.model = None

    def load_model(self) -> None:
        """Load llama.cpp model."""
        if self.model_path is None:
            raise ValueError("Model path not set.")

        self.model = Llama(
            model_path=self.model_path,
            n_ctx=2048,
            n_threads=8,
        )

    def generate_command(self, user_text: str) -> dict[str, Any]:
        """Generate command from user text."""
        if self.model is None:
            raise RuntimeError("Model not loaded.")

        system_prompt = (
            "You are a video editing AI assistant for DaVinci Resolve. "
            "Convert user text to a JSON command with actions. "
            "Valid actions: add_marker, rename_clip, set_clip_enabled, cut_split_at_timecode, "
            "set_in_point, set_out_point, move_trim_clip, insert_transition, "
            "add_color_node, set_exposure, set_contrast, set_saturation, set_temperature, "
            "set_lift_gamma_gain, apply_lut, enable_disable_node, remove_node, set_color_label. "
            "Return ONLY valid JSON with fields: timeline_id, actions[]."
        )

        prompt = f"{system_prompt}\n\nUser request: {user_text}\n\nJSON Command:"

        response = self.model(
            prompt,
            max_tokens=1024,
            temperature=0.2,
            stop=["\n\n"],
        )

        text = response["choices"][0]["text"]
        # Parse JSON from response
        try:
            cmd_dict = json.loads(text)
            return cmd_dict
        except json.JSONDecodeError:
            # Try to extract JSON from response
            start_idx = text.find("{")
            end_idx = text.rfind("}") + 1
            if start_idx >= 0 and end_idx > start_idx:
                return json.loads(text[start_idx:end_idx])
            raise ValueError(f"Could not parse command from AI response: {text}")
