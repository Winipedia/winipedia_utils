"""Tests for winipedia_utils.resources.svgs.svg module."""

from pyrig.src.testing.assertions import assert_with_msg

from winipedia_utils.src.resources import svgs
from winipedia_utils.src.resources.svgs.svg import get_svg_path


def test_get_svg_path() -> None:
    """Test func for get_svg_path."""
    # Test with default package (svgs) - using known SVG file
    svg_name = "menu_icon"
    result_path = get_svg_path(svg_name)

    # Verify the path exists
    assert_with_msg(
        result_path.exists(),
        f"Expected SVG file to exist at {result_path}",
    )

    # Verify the path ends with the correct filename
    expected_filename = f"{svg_name}.svg"
    assert_with_msg(
        result_path.name == expected_filename,
        f"Expected filename {expected_filename}, got {result_path.name}",
    )

    # Test with explicit package parameter
    result_path_explicit = get_svg_path(svg_name, package=svgs)
    assert_with_msg(
        result_path_explicit.exists(),
        f"Expected SVG file to exist at {result_path_explicit}",
    )

    # Verify both calls return equivalent paths
    assert_with_msg(
        result_path.name == result_path_explicit.name,
        f"Expected same filename from both calls, "
        f"got {result_path.name} vs {result_path_explicit.name}",
    )

    # Test with different SVG files to ensure function works with multiple files
    test_svg_names = ["plus_icon", "play_icon", "pause_icon", "fullscreen_icon"]
    for test_svg_name in test_svg_names:
        test_result = get_svg_path(test_svg_name)
        assert_with_msg(
            test_result.exists(),
            f"Expected SVG file {test_svg_name} to exist at {test_result}",
        )
        assert_with_msg(
            test_result.name == f"{test_svg_name}.svg",
            f"Expected filename {test_svg_name}.svg, got {test_result.name}",
        )

    # Test with non-existent SVG file - function should still return a Path
    # but the file won't exist (this is expected behavior)
    non_existent_svg = "non_existent_icon"
    non_existent_result = get_svg_path(non_existent_svg)
    expected_non_existent_name = f"{non_existent_svg}.svg"
    assert_with_msg(
        non_existent_result.name == expected_non_existent_name,
        f"Expected filename {expected_non_existent_name}, "
        f"got {non_existent_result.name}",
    )

    # Test with None package parameter (should use default)
    none_package_result = get_svg_path(svg_name, package=None)
    assert_with_msg(
        none_package_result.exists(),
        f"Expected SVG file to exist with None package at {none_package_result}",
    )
    assert_with_msg(
        none_package_result.name == expected_filename,
        f"Expected filename {expected_filename} with None package, "
        f"got {none_package_result.name}",
    )
