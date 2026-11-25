"""Small CPU references for generic graphics interoperability fixtures."""


def composite_rgba(base, width, height, overlay, ow, oh):
    """Opaque RGBA8 destination, straight-alpha source, nearest pixel-center scale."""
    if min(width, height, ow, oh) <= 0:
        raise ValueError("invalid dimensions")
    if len(base) != width * height * 4 or len(overlay) != ow * oh * 4:
        raise ValueError("invalid buffer size")
    if any(a != 255 for a in base[3::4]):
        raise ValueError("destination must be opaque")
    result = bytearray(len(base))
    for y in range(height):
        sy = (2 * y + 1) * oh // (2 * height)
        for x in range(width):
            sx = (2 * x + 1) * ow // (2 * width)
            i, j = (y * width + x) * 4, (sy * ow + sx) * 4
            a = overlay[j + 3]
            for c in range(3):
                result[i + c] = (overlay[j + c] * a + base[i + c] * (255 - a) + 127) // 255
            result[i + 3] = 255
    return bytes(result)


def dirty_copy(previous, current, writes, page_size=65536):
    """Model page-granular copy-back of explicitly marked byte ranges.

    The caller must mark every written byte; compare with a full-copy reference
    to detect incomplete tracking. Return bytes and number of bytes copied.
    """
    if len(previous) != len(current) or page_size <= 0:
        raise ValueError("invalid buffer or page size")
    pages = set()
    for offset, length in writes:
        if offset < 0 or length < 0 or offset + length > len(current):
            raise ValueError("invalid write range")
        if length:
            pages.update(range(offset // page_size, (offset + length - 1) // page_size + 1))
    result = bytearray(previous)
    copied = 0
    for page in sorted(pages):
        start = page * page_size
        end = min(start + page_size, len(current))
        result[start:end] = current[start:end]
        copied += end - start
    return bytes(result), copied
