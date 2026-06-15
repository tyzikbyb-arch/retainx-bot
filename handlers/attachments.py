"""
Attachment configuration for each video tool.
Defines what files each tool accepts and custom UI text.
"""

# Attachment config per tool ID
# Keys:
#   start_frame: bool - single start image
#   end_frame: bool - end image (only with start_frame)
#   img_refs: int - max image references (0 = none)
#   vid_refs: int - max video references (0 = none)  
#   aud_refs: int - max audio files (0 = none)
#   prompt_label: str - custom prompt label (None = "Enter your prompt")
#   no_prompt: bool - skip prompt entirely
#   hint: str - custom hint text (replaces default warning)
#   vid_ref_required: bool - video reference is mandatory

TOOL_ATTACHMENTS = {
    "sd20": {
        "start_frame": True, "end_frame": True,
        "img_refs": 9, "vid_refs": 3, "aud_refs": 3,
        "exclusive_startend": True,
    },
    "sd20f": {  # identical to sd20
        "start_frame": True, "end_frame": True,
        "img_refs": 9, "vid_refs": 3, "aud_refs": 3,
        "exclusive_startend": True,
    },
    "hh10": {  # Happy Horse 1.0
        "start_frame": True, "end_frame": True,
    },
    "veo31": {  # Veo 3.1
        "start_frame": True, "end_frame": True,
        "img_refs": 3,
    },
    "veo31f": {  # Veo 3.1 Fast
        "start_frame": True, "end_frame": True,
    },
    "veo31e": {  # Veo 3.1 Extend
        "vid_refs": 1, "vid_ref_required": True,
        "prompt_label": "Upload a 2-30 second video and describe what happens next",
        "hint": "Works best with videos created using Veo models",
    },
    "veo31l": {  # Veo 3.1 Lite
        "start_frame": True, "end_frame": True,
    },
    "kl30": {  # Kling 3.0
        "start_frame": True, "end_frame": True,
    },
    "kl03": {  # Kling 0.3
        "start_frame": True, "end_frame": True,
    },
    "klmc": {  # Kling Motion Control
        "img_refs": 1, "vid_refs": 1,
    },
    "hga4": {  # HeyGen Avatar 4
        "img_refs": 1, "aud_refs": 1,
        "no_prompt": True,
        "img_required": True,
        "aud_required": True,
        "hint": "Upload a character image and voice recording to make your character talk",
    },
    "grok": {  # Grok Imagine 1.5
        "start_frame": True,
    },
    "omni": {  # OmniHuman 1.5
        "img_refs": 1, "aud_refs": 1,
        "no_prompt": False,
        "img_required": True,
        "aud_required": True,
        "prompt_label": "Describe your character's expressions and gestures (optional)",
        "hint": "Upload a character image and voice recording to make your character talk",
    },
    "fab1": {},  # Removed
    "lips": {  # Lipsync v2 Pro
        "vid_refs": 1, "aud_refs": 1,
        "no_prompt": True,
        "vid_ref_required": True,
        "aud_required": True,
        "prompt_label": "Upload a video of a character talking and a voice recording to create a lip-sync",
    },
    "ltx23": {  # LTX 2.3 Pro
        "start_frame": True, "end_frame": True,
    },
    "wan27": {  # Wan 2.7
        "start_frame": True, "end_frame": True,
    },
    "sora2": {  # Sora 2 Pro
        "start_frame": True,
        "hint": "Sora 2 Pro is highly unstable. Switch to another model.",
    },
    "hail23": {  # Hailuo 2.3 Pro
        "start_frame": True,
    },
    "klve": {  # Kling 0.3 Video Edit
        "img_refs": 4, "vid_refs": 1,
        "prompt_label": "Upload a 3-10 second video and describe the edits you want to make",
    },
    "fab1": {},  # Removed
    "aur1": {  # Aurora Avatar
        "img_refs": 1, "aud_refs": 1,
        "no_prompt": False,
        "img_required": True,
        "aud_required": True,
        "prompt_label": "Describe your character's expressions and gestures (optional)",
        "hint": "Upload a character image and voice recording to make your character talk",
    },
}

def get_attach_config(tid: str) -> dict:
    return TOOL_ATTACHMENTS.get(tid, {})

def has_attachments(tid: str) -> bool:
    cfg = get_attach_config(tid)
    return bool(
        cfg.get("start_frame") or cfg.get("img_refs") or
        cfg.get("vid_refs") or cfg.get("aud_refs")
    )
