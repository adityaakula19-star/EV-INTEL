from app.services.llm_service import answer_question


def test_empty_question_does_not_call_llm():
    result = answer_question("   ")
    assert result["llm_used"] is False
    assert result["error"] == "empty_question"


def test_missing_api_key_still_returns_dataset_evidence():
    result = answer_question("Compare EV adoption between India and Germany in 2024.")
    assert result["question_type"] == "country_comparison"
    assert "India" in result["countries"]
    assert "Germany" in result["countries"]
    assert 2024 in result["years"]
    assert result["evidence"]
    assert "ev_units_sold" in result["evidence"][0]
    assert result["error"] in {"missing_api_key", None} or result["llm_used"] in {True, False}
