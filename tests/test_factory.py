from app.extractors.factory import detect_platform


def test_detect_platform_redgifs() -> None:
    assert detect_platform("https://www.redgifs.com/users/demo") == "redgifs"


def test_detect_platform_vk() -> None:
    assert detect_platform("https://vk.com/video/@creator") == "vk"


def test_detect_platform_generic() -> None:
    assert detect_platform("https://example.com/creator/videos") == "generic"
