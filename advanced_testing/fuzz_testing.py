# advanced_testing/fuzz_testing.py

import random
import string
import asyncio
from simulation.distributed_system import DistributedKeyValueStore, NetworkSimulator

class FuzzTester:
    def __init__(self, kv_store: DistributedKeyValueStore, network: NetworkSimulator):
        self.kv_store = kv_store
        self.network = network

    @staticmethod
    def generate_random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    async def fuzz_set_get(self):
        key = self.generate_random_string(random.randint(1, 100))
        value = self.generate_random_string(random.randint(1, 1000))

        try:
            await self.network.simulate_network_conditions()
            await self.kv_store.set(key, value)

            await self.network.simulate_network_conditions()
            result = await self.kv_store.get(key)

            assert result == value, f"Fuzz test failed: set {key}={value}, but got {result}"
        except Exception as e:
            print(f"Fuzz test caught an exception: {str(e)}")

async def run_fuzz_tests(iterations: int = 1000):
    kv_store = DistributedKeyValueStore(3)
    network = NetworkSimulator(failure_rate=0.2, max_latency=1.0)
    fuzzer = FuzzTester(kv_store, network)

    for _ in range(iterations):
        await fuzzer.fuzz_set_get()

    print(f"Completed {iterations} fuzz tests")

if __name__ == "__main__":
    asyncio.run(run_fuzz_tests())