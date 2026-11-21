from src.knowledge import load_articles, search_articles


def test_articles_have_required_fields():
    articles = load_articles()
    assert len(articles) >= 5
    for article in articles:
        assert article["id"]
        assert article["title"]
        assert article["content"]


def test_finds_the_return_policy():
    results = search_articles("how do i return an item", load_articles())
    assert results[0]["id"] == "returns"


def test_finds_shipping_times():
    results = search_articles("how long does shipping take", load_articles())
    assert results[0]["id"] == "shipping"


def test_unrelated_question_returns_nothing():
    assert search_articles("tell me about the weather on mars", load_articles()) == []


def test_empty_query_returns_nothing():
    assert search_articles("", load_articles()) == []


def test_respects_the_limit():
    results = search_articles("order shipping returns refund", load_articles(), k=2)
    assert len(results) == 2
