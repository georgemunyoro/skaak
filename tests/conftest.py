import pytest


def pytest_addoption(parser):
    parser.addoption("--run-movegen-test", action="store_true")


@pytest.fixture(scope='session')
def run_movegen_test(request):
    run_movegen_test_val = request.config.option.run_movegen_test
    if run_movegen_test_val is None:
        pytest.skip()
    return run_movegen_test_val

