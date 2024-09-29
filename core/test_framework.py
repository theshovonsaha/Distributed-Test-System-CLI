# core/test_framework.py

import asyncio
import pytest
from typing import List, Callable, Any

class TestCase:
    def __init__(self, name: str, test_func: Callable[[], Any]):
        self.name = name
        self.test_func = test_func

class TestSuite:
    def __init__(self, name: str):
        self.name = name
        self.tests: List[TestCase] = []

    def add_test(self, test: TestCase):
        self.tests.append(test)

class TestFramework:
    def __init__(self):
        self.suites: List[TestSuite] = []

    def add_suite(self, suite: TestSuite):
        self.suites.append(suite)

    async def run_test(self, test: TestCase):
        try:
            if asyncio.iscoroutinefunction(test.test_func):
                await test.test_func()
            else:
                test.test_func()
            print(f"Test '{test.name}' passed")
            return True
        except AssertionError as e:
            print(f"Test '{test.name}' failed: {str(e)}")
            return False

    async def run_suite(self, suite: TestSuite):
        print(f"Running test suite: {suite.name}")
        results = await asyncio.gather(*[self.run_test(test) for test in suite.tests])
        passed = sum(results)
        total = len(results)
        print(f"Suite '{suite.name}' results: {passed}/{total} tests passed")

    async def run_all(self):
        for suite in self.suites:
            await self.run_suite(suite)

# Example test function
@pytest.mark.asyncio
async def example_test():
    assert 1 + 1 == 2, "Basic addition should work"

# Setup for pytest
def pytest_generate_tests(metafunc):
    if "test_case" in metafunc.fixturenames:
        framework = TestFramework()
        suite = TestSuite("Example Suite")
        suite.add_test(TestCase("Example Test", example_test))
        framework.add_suite(suite)
        metafunc.parametrize("test_case", framework.suites[0].tests)

# Actual test function for pytest
@pytest.mark.asyncio
async def test_framework(test_case):
    framework = TestFramework()
    result = await framework.run_test(test_case)
    assert result, f"Test '{test_case.name}' failed"

if __name__ == "__main__":
    asyncio.run(example_test())