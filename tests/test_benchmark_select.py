import pytest
import time


def select_query(client):
    cursor = client
    cursor.execute("SELECT * FROM oxlafunctions;")
    results = cursor.fetchall()
    return len(results)


@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=False,
    warmup=True,
)
def test_benchmark_select_on_oxla(benchmark, setup_oxla):
    results = benchmark(select_query, setup_oxla)
    assert results == 99


@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    timer=time.time,
    disable_gc=False,
    warmup=True,
)
def test_benchmark_select_on_pg(benchmark, setup_pg):
    results = benchmark(select_query, setup_pg)
    assert results == 99
