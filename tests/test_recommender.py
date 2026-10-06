from recommender import (
    COMPLETION_MAP,
    build_smart_outfit,
    color_score,
    get_cat,
    ok_persona,
)


def item(item_type, color, persona="Millennial", formality="casual", io="outdoor", **extra):
    return {
        "item_type": item_type,
        "color": color,
        "style_persona": persona,
        "formality": formality,
        "indoor_outdoor": io,
        **extra,
    }


def test_color_score_levels():
    assert color_score("Black", "black") == 2
    assert color_score("black", "white") == 1
    assert color_score("black", "yellow") == 0
    assert color_score("not-a-color", "black") == 0


def test_get_cat_keywords():
    assert get_cat("Crop Top") == "tops"
    assert get_cat("wide leg jeans") == "bottoms"
    assert get_cat("Maxi Dress") == "dresses"
    assert get_cat("Ankle Boots") == "shoes"
    assert get_cat("spaceship") == "other"


def test_ok_persona():
    assert ok_persona("anything", "All")
    assert ok_persona("Cargo pants", "Gen-Z")
    assert not ok_persona("Pearl necklace", "Gen-Z")


def test_outfit_completes_missing_categories_only():
    items = [
        item("Cargo Pants", "white", persona="Gen-Z", category_group="bottoms"),
        item("Sneakers", "black", persona="Gen-Z", category_group="shoes"),
        item("Crop Top", "black", persona="Gen-Z", category_group="tops"),
    ]
    outfit = build_smart_outfit(items, "black", "tops", "Gen-Z", "Casual", "Outdoor")
    assert set(outfit) == {"bottoms", "shoes"}  # "tops" is what was uploaded
    assert set(outfit) <= set(COMPLETION_MAP["tops"])


def test_outfit_prefers_best_colour_match():
    items = [
        item("Jeans", "yellow", category_group="bottoms"),
        item("Jeans", "white", category_group="bottoms"),
        item("Jeans", "black", category_group="bottoms"),
    ]
    outfit = build_smart_outfit(items, "black", "tops", "All", "Casual", "Outdoor")
    assert outfit["bottoms"]["color"] == "black"  # same colour beats compatible beats unknown


def test_filters_apply():
    items = [
        item("Jeans", "black", formality="formal", category_group="bottoms"),
        item("Jeans", "black", io="indoor", category_group="bottoms"),
        item("Jeans", "black", persona="Aesthetic", category_group="bottoms"),
    ]
    assert build_smart_outfit(items, "black", "tops", "Millennial", "Casual", "Outdoor") == {}


def test_no_candidates_returns_empty():
    assert build_smart_outfit([], "black", "tops", "All", "Casual", "Outdoor") == {}
