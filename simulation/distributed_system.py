# simulation/distributed_system.py

import asyncio
import random
from typing import Dict, Any

class Node:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.data: Dict[str, Any] = {}

    async def get(self, key: str) -> Any:
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate network latency
        return self.data.get(key)

    async def set(self, key: str, value: Any):
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate network latency
        self.data[key] = value

class DistributedKeyValueStore:
    def __init__(self, node_count: int):
        self.nodes = [Node(f"node_{i}") for i in range(node_count)]

    def get_node(self, key: str) -> Node:
        # Simple hash function to determine which node holds the key
        return self.nodes[hash(key) % len(self.nodes)]

    async def get(self, key: str) -> Any:
        node = self.get_node(key)
        return await node.get(key)

    async def set(self, key: str, value: Any):
        node = self.get_node(key)
        await node.set(key, value)

class NetworkSimulator:
    def __init__(self, failure_rate: float = 0.1, max_latency: float = 0.5):
        self.failure_rate = failure_rate
        self.max_latency = max_latency

    async def simulate_network_conditions(self):
        if random.random() < self.failure_rate:
            raise Exception("Network failure simulated")
        await asyncio.sleep(random.uniform(0, self.max_latency))

# Example usage
async def main():
    kv_store = DistributedKeyValueStore(3)
    network = NetworkSimulator()

    try:
        await network.simulate_network_conditions()
        await kv_store.set("key1", "value1")
        await network.simulate_network_conditions()
        value = await kv_store.get("key1")
        print(f"Retrieved value: {value}")
    except Exception as e:
        print(f"Operation failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())