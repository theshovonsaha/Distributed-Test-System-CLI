# monitoring/performance.py

import time
import asyncio
from typing import Dict, List
import matplotlib.pyplot as plt
from simulation.distributed_system import DistributedKeyValueStore, NetworkSimulator

class PerformanceMonitor:
    def __init__(self):
        self.operation_times: Dict[str, List[float]] = {"get": [], "set": []}
        self.error_counts: Dict[str, int] = {"get": 0, "set": 0}

    async def measure_operation(self, operation: str, func, *args):
        start_time = time.time()
        try:
            result = await func(*args)
            elapsed_time = time.time() - start_time
            self.operation_times[operation].append(elapsed_time)
            return result
        except Exception:
            self.error_counts[operation] += 1
            raise

    def generate_report(self):
        report = "Performance Report\n"
        report += "==================\n\n"

        for operation in ["get", "set"]:
            times = self.operation_times[operation]
            if times:
                avg_time = sum(times) / len(times)
                report += f"{operation.capitalize()} Operations:\n"
                report += f"  Average time: {avg_time:.4f} seconds\n"
                report += f"  Total operations: {len(times)}\n"
                report += f"  Error rate: {self.error_counts[operation] / (len(times) + self.error_counts[operation]):.2%}\n\n"

        return report

    def generate_charts(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

        operations = ["get", "set"]
        colors = ["blue", "green"]

        for operation, color in zip(operations, colors):
            times = self.operation_times[operation]
            if times:
                ax1.plot(range(len(times)), times, color=color, label=f"{operation} time")
                ax2.hist(times, bins=20, color=color, alpha=0.7, label=f"{operation} distribution")

        ax1.set_xlabel("Operation number")
        ax1.set_ylabel("Time (seconds)")
        ax1.set_title("Operation Times")
        ax1.legend()

        ax2.set_xlabel("Time (seconds)")
        ax2.set_ylabel("Frequency")
        ax2.set_title("Operation Time Distribution")
        ax2.legend()

        plt.tight_layout()
        plt.savefig("performance_charts.png")
        plt.close()

async def run_performance_test(num_operations: int = 1000):
    kv_store = DistributedKeyValueStore(3)
    network = NetworkSimulator(failure_rate=0.05, max_latency=0.5)  # Reduced failure rate
    monitor = PerformanceMonitor()

    for i in range(num_operations):
        key = f"key_{i}"
        value = f"value_{i}"

        try:
            await network.simulate_network_conditions()
            await monitor.measure_operation("set", kv_store.set, key, value)
            
            await network.simulate_network_conditions()
            await monitor.measure_operation("get", kv_store.get, key)
        except Exception as e:
            print(f"Operation failed: {str(e)}")

    print(monitor.generate_report())
    monitor.generate_charts()

if __name__ == "__main__":
    asyncio.run(run_performance_test())