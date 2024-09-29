# advanced_testing/property_based.py

from hypothesis import given, strategies as st
from simulation.distributed_system import DistributedKeyValueStore
import asyncio

@given(key=st.text(), value=st.text())
async def test_set_get_property(key, value):
    kv_store = DistributedKeyValueStore(3)
    await kv_store.set(key, value)
    result = await kv_store.get(key)
    assert result == value, f"Expected {value}, got {result}"

@given(keys=st.lists(st.text(), min_size=1), value=st.text())
async def test_multiple_sets_property(keys, value):
    kv_store = DistributedKeyValueStore(3)
    for key in keys:
        await kv_store.set(key, value)
    
    results = await asyncio.gather(*[kv_store.get(key) for key in keys])
    assert all(result == value for result in results), "Not all keys had the expected value"

if __name__ == "__main__":
    asyncio.run(test_set_get_property())
    asyncio.run(test_multiple_sets_property())