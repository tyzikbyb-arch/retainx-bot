"""
Static catalog of Artlist Voice Catalog voices used to fulfil voiceover
orders. Sourced from a one-time export of toolkit.artlist.io's Voice
Catalog API (see retainx-worker/voice_catalog_export.py +
voice_catalog_slim.py). Mirrors the same "data lives in a Python const"
convention as config.py's IMAGE_TOOLS — the catalog rarely changes and
doesn't need its own DB table.

`languages` from the slim export is intentionally dropped: all 73 voices
support essentially the same ~74-language multilingual TTS model, so it
is not a useful filter for telling voices apart.
"""

CATEGORIES = [
    "Social", "Tutorials", "Documentaries", "Trailers",
    "Explainers", "Characters", "Commercials", "Health & Wellness",
]

GENDERS = ["MALE", "FEMALE", "NEUTRAL"]

AGE_ORDER = ["CHILD", "TEEN", "YOUNG_ADULT", "ADULT", "MIDDLE_AGED", "SENIOR"]

VOICE_CATALOG = [
    {"id": 1, "name": "Secrets", "description": "Soft whispers to relax and unwind", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Health & Wellness"]},
    {"id": 2, "name": "Views", "description": "A distinct grit-meets-artisanal edge with a touch of stoicism", "gender": "MALE", "age": "ADULT", "categories": ["Social"]},
    {"id": 3, "name": "Tattle", "description": "A bold, sharp, and mischievous youthful British voice", "gender": "FEMALE", "age": "TEEN", "categories": ["Characters", "Social"]},
    {"id": 5, "name": "Paradigm", "description": "Deliver information at eye level", "gender": "MALE", "age": "ADULT", "categories": ["Explainers", "Tutorials"]},
    {"id": 6, "name": "Esteem", "description": "Narrate with warmth and wisdom", "gender": "MALE", "age": "ADULT", "categories": ["Documentaries", "Explainers"]},
    {"id": 7, "name": "Obsession", "description": "Casual Gen Z style narration", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Explainers", "Social"]},
    {"id": 10, "name": "Anchor", "description": "Steady, strong and quietly adventurous", "gender": "MALE", "age": "ADULT", "categories": ["Documentaries", "Explainers"]},
    {"id": 13, "name": "All-Rounder", "description": "A reassuring voice you can depend on", "gender": "MALE", "age": "ADULT", "categories": ["Commercials", "Explainers"]},
    {"id": 16, "name": "Hype", "description": "Infuse your video with energy and excitement", "gender": "MALE", "age": "ADULT", "categories": ["Characters", "Social"]},
    {"id": 17, "name": "Persuasion", "description": "Speak clearly and directly to your audience", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Social"]},
    {"id": 18, "name": "Sleek", "description": "A charismatic voice to sell your product", "gender": "MALE", "age": "ADULT", "categories": ["Commercials", "Tutorials"]},
    {"id": 19, "name": "Bulletin", "description": "Convey information with warmth", "gender": "FEMALE", "age": "ADULT", "categories": ["Characters", "Trailers"]},
    {"id": 20, "name": "Jackpot", "description": "Sell anything with enthusiasm", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Characters", "Commercials"]},
    {"id": 23, "name": "Explore", "description": "Educate and entertain with a voice that inspires curiosity", "gender": "MALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 24, "name": "Shadow", "description": "Add depth with raspy hoarse tones", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Characters", "Trailers"]},
    {"id": 25, "name": "Wit", "description": "A touch of cheekiness paired with sarcasm", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Commercials", "Social"]},
    {"id": 26, "name": "Mono", "description": "Make complex ideas sound simple", "gender": "MALE", "age": "ADULT", "categories": ["Documentaries", "Explainers"]},
    {"id": 27, "name": "Revelation", "description": "Inspire audiences with a voice of knowledge", "gender": "MALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 28, "name": "Hushed", "description": "Soothe your audience with a voice of tranquility", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Health & Wellness"]},
    {"id": 29, "name": "Serenity", "description": "Soothe and calm your senses", "gender": "FEMALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 30, "name": "Mentor", "description": "Motivate and empower your audience", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Social", "Tutorials"]},
    {"id": 31, "name": "Unfiltered", "description": "Stir up emotions with a bold young voice", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Commercials", "Social"]},
    {"id": 32, "name": "Bright", "description": "Narrate with a friendly, welcoming voice", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Social", "Tutorials"]},
    {"id": 33, "name": "Guidance", "description": "An approachable voice for any video", "gender": "FEMALE", "age": "ADULT", "categories": ["Social", "Tutorials"]},
    {"id": 34, "name": "Rural", "description": "Transport your audience with a raspy Southern drawl", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Commercials", "Trailers"]},
    {"id": 35, "name": "Gloss", "description": "Influence your audience with sassy confidence", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Commercials", "Social"]},
    {"id": 36, "name": "Polished", "description": "Communicate with clarity and optimism", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Tutorials"]},
    {"id": 38, "name": "Edge", "description": "Share your message with a raw voice", "gender": "MALE", "age": "ADULT", "categories": ["Characters", "Social"]},
    {"id": 39, "name": "Charmed", "description": "Tell your story with childlike wonder", "gender": "FEMALE", "age": "SENIOR", "categories": ["Characters", "Trailers"]},
    {"id": 40, "name": "Pixel", "description": "Excite your viewers with a young and energetic voice", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Characters", "Social"]},
    {"id": 41, "name": "Trail", "description": "A steady voice to accompany every journey", "gender": "MALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 42, "name": "Gloom", "description": "Express empathy and raw emotion in your video", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Commercials", "Social"]},
    {"id": 43, "name": "Mild", "description": "Infuse your video with a young, clear and relatable voice.", "gender": "MALE", "age": "YOUNG_ADULT", "categories": ["Explainers", "Social"]},
    {"id": 44, "name": "Assistance", "description": "A futuristic voice for guiding and educating users", "gender": "FEMALE", "age": "MIDDLE_AGED", "categories": ["Commercials", "Social"]},
    {"id": 46, "name": "Balance", "description": "A composed voice that reflects calm and sensibility", "gender": "MALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 47, "name": "Curiosity", "description": "Spark wonder and childlike adventure in your video", "gender": "MALE", "age": "CHILD", "categories": ["Characters", "Explainers"]},
    {"id": 64, "name": "Flair", "description": "Spread your message with a trendy, friendly voice", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Explainers", "Tutorials"]},
    {"id": 73, "name": "Aspire", "description": "A bold and determined voice with a touch of empathy", "gender": "FEMALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 75, "name": "Professor", "description": "Craft a sense of trust and wisdom", "gender": "MALE", "age": "SENIOR", "categories": ["Documentaries", "Explainers"]},
    {"id": 77, "name": "Insight", "description": "Bring a sense of enthusiasm to facts", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Commercials", "Explainers"]},
    {"id": 78, "name": "Resonance", "description": "Create genuine and relatable content", "gender": "FEMALE", "age": "ADULT", "categories": ["Explainers", "Tutorials"]},
    {"id": 79, "name": "Initiative", "description": "A bright and energetic tone to inspire your audience", "gender": "MALE", "age": "ADULT", "categories": ["Explainers", "Social"]},
    {"id": 80, "name": "Keen", "description": "Relay facts with confident professionalism", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Explainers", "Tutorials"]},
    {"id": 82, "name": "Everyday", "description": "Engage and reassure your listeners", "gender": "FEMALE", "age": "ADULT", "categories": ["Health & Wellness", "Social"]},
    {"id": 83, "name": "Precision", "description": "Clarity and elegance in every word", "gender": "FEMALE", "age": "ADULT", "categories": ["Documentaries", "Explainers"]},
    {"id": 85, "name": "Grounded", "description": "Engage your audience with a down-to-earth British accent", "gender": "FEMALE", "age": "ADULT", "categories": ["Characters", "Social"]},
    {"id": 86, "name": "Chipper", "description": "A high dosage of friendly enthusiasm", "gender": "MALE", "age": "ADULT", "categories": ["Commercials", "Explainers"]},
    {"id": 87, "name": "Cupcake", "description": "Uplift your audience with the sweet, innocent voice of a child", "gender": "FEMALE", "age": "CHILD", "categories": ["Characters", "Explainers"]},
    {"id": 113, "name": "Posh", "description": "Give your video a refined touch with a young British accent", "gender": "FEMALE", "age": "TEEN", "categories": ["Characters", "Social"]},
    {"id": 114, "name": "Showtime", "description": "Tell epic stories with a deep, cinematic voice", "gender": "MALE", "age": "ADULT", "categories": ["Commercials", "Trailers"]},
    {"id": 115, "name": "Focus", "description": "A grounded, confident voice to communicate with purpose", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Explainers", "Health & Wellness"]},
    {"id": 116, "name": "Deadpan", "description": "A cool, laidback voice with a touch of attitude", "gender": "FEMALE", "age": "ADULT", "categories": ["Characters", "Social"]},
    {"id": 117, "name": "Essence", "description": "A calm and understated voice to subtly inspire your audience.", "gender": "FEMALE", "age": "ADULT", "categories": ["Documentaries", "Explainers"]},
    {"id": 118, "name": "League", "description": "Deliver thrilling, high-stakes energy with a booming British voice", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Characters", "Commercials"]},
    {"id": 119, "name": "Alpha", "description": "Invigorate your audience with a booming, charismatic voice", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Commercials", "Trailers"]},
    {"id": 129, "name": "Candid", "description": "Raw and intimate authenticity", "gender": "FEMALE", "age": "TEEN", "categories": ["Commercials", "Social"]},
    {"id": 131, "name": "Vision", "description": "An authentic, articulate voice that motivates viewers", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Characters", "Documentaries"]},
    {"id": 133, "name": "Quest", "description": "Dive into an imaginative tale with wit and youthful curiosity", "gender": "MALE", "age": "TEEN", "categories": ["Social", "Tutorials"]},
    {"id": 134, "name": "Vibes", "description": "Lighten things up with an cool, energetic, optimistic voice", "gender": "MALE", "age": "TEEN", "categories": ["Commercials", "Social"]},
    {"id": 135, "name": "Pep", "description": "Effortlessly delightful, with a fun and inviting energy", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Explainers"]},
    {"id": 136, "name": "Horizon", "description": "Establish trust, authority, and a clear vision of the future", "gender": "MALE", "age": "ADULT", "categories": ["Commercials", "Explainers"]},
    {"id": 137, "name": "Nourish", "description": "Graceful, composed and effortlessly confident", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Explainers"]},
    {"id": 138, "name": "Primetime", "description": "A smooth, confident voice that's always ready for the spotlight", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Trailers"]},
    {"id": 141, "name": "Santa", "description": "A rich, resonant voice full of warmth, wonder and timeless cheer", "gender": "MALE", "age": "SENIOR", "categories": ["Characters", "Commercials"]},
    {"id": 143, "name": "Grace", "description": "A dreamy, delicate voice that brings a sense of peace and wonder", "gender": "FEMALE", "age": "YOUNG_ADULT", "categories": ["Characters", "Commercials"]},
    {"id": 148, "name": "Neutral", "description": "A non-binary voice that's soft, calm and understated", "gender": "NEUTRAL", "age": "ADULT", "categories": ["Explainers", "Social"]},
    {"id": 149, "name": "Stride", "description": "A composed voice with quiet strength and steady purpose", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Health & Wellness"]},
    {"id": 264, "name": "Sunny", "description": "A sweet, high-spirited voice that radiates a bubbly, bright energy", "gender": "FEMALE", "age": "ADULT", "categories": ["Commercials", "Social"]},
    {"id": 265, "name": "Boss", "description": "Street-wise, tough, with a threatening authority", "gender": "MALE", "age": "ADULT", "categories": ["Characters", "Trailers"]},
    {"id": 113128, "name": "Suburb", "description": "A dependable, friendly, and approachable everyman.", "gender": "MALE", "age": "ADULT", "categories": ["Social", "Tutorials"]},
    {"id": 113129, "name": "Path", "description": "Insightful and articulate with soulful depth", "gender": "FEMALE", "age": "ADULT", "categories": ["Documentaries", "Explainers"]},
    {"id": 113130, "name": "Gravity", "description": "Deeply resonant with a soulful, textured tone", "gender": "MALE", "age": "MIDDLE_AGED", "categories": ["Documentaries", "Trailers"]},
    {"id": 113132, "name": "Twinkle", "description": "A singsong warmth that sparks curiosity with a young audience", "gender": "FEMALE", "age": "ADULT", "categories": ["Characters", "Social"]},
]

_BY_ID = {v["id"]: v for v in VOICE_CATALOG}


def get_voice(voice_id: int) -> dict | None:
    return _BY_ID.get(voice_id)


def list_genders(category: str) -> list[str]:
    present = {v["gender"] for v in VOICE_CATALOG if category in v["categories"]}
    return [g for g in GENDERS if g in present]


def list_ages(category: str, gender: str) -> list[str]:
    present = {
        v["age"] for v in VOICE_CATALOG
        if category in v["categories"] and v["gender"] == gender
    }
    return [a for a in AGE_ORDER if a in present]


def list_voices(category: str, gender: str, age: str) -> list[dict]:
    return sorted(
        (v for v in VOICE_CATALOG
         if category in v["categories"] and v["gender"] == gender and v["age"] == age),
        key=lambda v: v["name"],
    )
