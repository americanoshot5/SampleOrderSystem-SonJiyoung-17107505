def test_pytest_harness_is_wired_up():
    """CI 파이프라인(GitHub Actions)이 pytest를 정상적으로 수집/실행하는지 확인하는 smoke test.

    Phase별 기능 테스트가 추가되기 전까지, 이 테스트는 CI가 항상 최소 1개 이상의
    테스트를 수집해 실행하도록 보장한다 (pytest는 수집된 테스트가 0개면 실패 종료함).
    """
    assert True
