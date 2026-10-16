"""Pure text chunking and retrieval formatting functions, safe to test offline."""
import re


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    if not text or not text.strip():
        return []
    if chunk_size < 1 or not 0 <= overlap < chunk_size:
        raise ValueError("chunk_size must be positive, with 0 <= overlap < chunk_size")
    normalized = re.sub(r"[ \t]+", " ", text).strip()
    result = []
    step = chunk_size - overlap
    for start in range(0, len(normalized), step):
        piece = normalized[start : start + chunk_size]
        if not piece:
            break
        result.append(piece)
        if start + chunk_size >= len(normalized):
            break
    return result


def build_context(matches: list[dict], max_chars: int = 9000) -> tuple[str, list[str]]:
    context = []
    sources = []
    total = 0
    for match in matches:
        source = str(match.get("source", "unknown"))
        content = str(match.get("content", "")).strip()
        if not content:
            continue
        segment = f"[Source: {source}]\n{content}\n"
        if total + len(segment) > max_chars:
            break
        context.append(segment)
        total += len(segment)
        if source not in sources:
            sources.append(source)
    return "\n".join(context), sources
