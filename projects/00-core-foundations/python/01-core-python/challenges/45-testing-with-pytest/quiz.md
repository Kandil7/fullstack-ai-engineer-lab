# Challenge 45 — Quiz: Testing with pytest

1. pytest discovers functions whose names:
   - A) start with `test_`  (B) contain "test"  (C) end with `_test_`  (D) are decorated
2. To assert an exception is raised, use:
   - A) `assert raises(...)`  (B) `with pytest.raises(...):`  (C) `try/except`  (D) `assert_called`
3. `@pytest.mark.parametrize`:
   - A) runs tests in parallel  (B) feeds many cases into one test body  (C) skips tests  (D) adds markers
4. `tmp_path` provides:
   - A) a session temp dir  (B) a per-test temp dir  (C) the repo root  (D) a fake filesystem
5. Mocking the LLM API in tests:
   - A) is cheating  (B) makes tests free and deterministic  (C) requires a GPU  (D) is deprecated
6. `Mock(side_effect=[e, "ok"])` means:
   - A) raise always  (B) first call raises, second returns "ok"  (C) random results  (D) returns a list
7. For float comparisons use:
   - A) `==`  (B) `pytest.approx`  (C) `is`  (D) `math.eq`
8. AAA stands for:
   - A) Assert-Assign-Apply  (B) Arrange-Act-Assert  (C) Always-Avoid-Asserts  (D) Analyze-Act-Agree

**Answers:** 1-A, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
