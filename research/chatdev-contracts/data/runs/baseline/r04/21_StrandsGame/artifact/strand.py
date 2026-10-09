from dataclasses import dataclass
@dataclass(frozen=True)
class Strand:
    strand_id: int
    text: str          # display text (uppercase) — the ONLY field the UI may render
    owner_word: str    # normalized target word it belongs to (internal; never displayed)