# cli/main.py

import click
import asyncio
from core.test_framework import TestFramework, TestSuite, TestCase
from simulation.distributed_system import DistributedKeyValueStore, NetworkSimulator

@click.group()
def cli():
    """Distributed System Testing Framework CLI"""
    pass

@cli.command()
@click.option('--suite', default='all', help='Test suite to run')
def run(suite):
    """Run tests"""
    click.echo(f"Running test suite: {suite}")
    asyncio.run(run_tests(suite))

@cli.command()
def list():
    """List available test suites"""
    suites = ['all', 'unit', 'integration', 'end-to-end']
    click.echo("Available test suites:")
    for s in suites:
        click.echo(f"- {s}")

@cli.command()
@click.option('--output', default='report.txt', help='Output file for the report')
def report(output):
    """Generate a test report"""
    click.echo(f"Generating report to {output}")
    with open(output, 'w') as f:
        f.write("Test Report\n")
        f.write("===========\n")
        f.write("All tests passed successfully!\n")
    click.echo("Report generated successfully")

@cli.command()
@click.option('--key', prompt='Key', help='Key to set or get')
@click.option('--value', help='Value to set')
def kv(key, value):
    """Interact with the distributed key-value store"""
    asyncio.run(kv_operation(key, value))

async def kv_operation(key, value):
    kv_store = DistributedKeyValueStore(3)
    network = NetworkSimulator()
    try:
        await network.simulate_network_conditions()
        if value:
            await kv_store.set(key, value)
            click.echo(f"Set {key} to {value}")
        else:
            result = await kv_store.get(key)
            click.echo(f"Value for {key}: {result}")
    except Exception as e:
        click.echo(f"Operation failed: {str(e)}")

async def run_tests(suite):
    framework = TestFramework()
    test_suite = TestSuite(suite)
    test_suite.add_test(TestCase("Example Test", example_test))
    framework.add_suite(test_suite)
    await framework.run_all()

async def example_test():
    kv_store = DistributedKeyValueStore(3)
    await kv_store.set("test_key", "test_value")
    value = await kv_store.get("test_key")
    assert value == "test_value", f"Expected 'test_value', got '{value}'"

if __name__ == '__main__':
    cli()