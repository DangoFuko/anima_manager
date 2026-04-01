import os
import difflib


def fuzzy_match(target, candidates):
    best, score = None, 0
    for c in candidates:
        s = difflib.SequenceMatcher(None, target, c).ratio()
        if s > score:
            best, score = c, s
    return best if score > 0.6 else None


def find_best_match(target, base_path):
    if not os.path.exists(base_path):
        return target

    candidates = [
        d for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d))
    ]

    return fuzzy_match(target, candidates) or target