import black


def format_code(code: str) -> str:
    try:
        # Format with Black
        formatted = black.format_str(code, mode=black.FileMode(line_length=40))
        return formatted
    except Exception as e:
        raise e
