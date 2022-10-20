import logging
import os
from posixpath import basename, splitext
import random
import time
from prometheus_client import start_http_server

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "test_prom"
})
script_name = splitext(basename(__file__))[0]
loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=loglevel)
logger = logging.getLogger(script_name)
# Start Prometheus client
start_http_server(port=8001, addr="0.0.0.0")
# Initialize PrometheusMetricReader which pulls metrics from the SDK
# on-demand to respond to scrape requests
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(script_name, provider)
requests_counter = meter.create_counter(
        name="requests",
        description="number of requests",
        unit="1"
    )

requests_size = meter.create_histogram(
        name="request_size_bytes",
        description="size of requests",
        unit="byte"
    )
    
    # for (number, percent) in enumerate(print(temp)):
    #     attributes = {"cpu_number": str(number)}
    
system_cpu_time_gauge = meter.create_observable_gauge(
                name="system.cpu.time",
                callbacks=[SystemMetricsInstrumentor()._get_system_cpu_time],
                description="system cpu time",
                unit="seconds",
            )
system_cpu_utilization_gauge = meter.create_observable_gauge(
                name="system.cpu.utilization",
                callbacks=[SystemMetricsInstrumentor()._get_system_cpu_utilization],
                description=" system cpu utilization",
                unit="seconds",
            )
system_memory_usage_gauge = meter.create_observable_gauge(
                name="system.memory.usage",
                callbacks=[SystemMetricsInstrumentor()._get_system_memory_usage],
                description="System memory usage",
                unit="seconds",
            )
system_memory_utilization_gauge = meter.create_observable_gauge(
                name="system.memory.utilization",
                callbacks=[SystemMetricsInstrumentor()._get_system_memory_utilization],
                description="System memory usage",
                unit="seconds",
            )
system_swap_usage_gauge = meter.create_observable_gauge(
                name="system.swap.usage",
                callbacks=[SystemMetricsInstrumentor()._get_system_swap_usage],
                description="System memory usage",
                unit="seconds",
            )
system_swap_utilization_gauge = meter.create_observable_gauge(
                name="system.swap.utilization",
                callbacks=[SystemMetricsInstrumentor()._get_system_swap_utilization],
                description="System memory usage",
                unit="seconds",
            )
system_disk_io_gauge = meter.create_observable_gauge(
                name="system.disk.io",
                callbacks=[SystemMetricsInstrumentor()._get_system_disk_io],
                description="System memory usage",
                unit="seconds",
            )
system_disk_operations_gauge = meter.create_observable_gauge(
                name="system.disk.operations",
                callbacks=[SystemMetricsInstrumentor()._get_system_disk_operations],
                description="System memory usage",
                unit="seconds",
            )

system_disk_time_gauge = meter.create_observable_gauge(
                name="system.disk.time",
                callbacks=[SystemMetricsInstrumentor()._get_system_disk_time],
                description="System disk time",
                unit="seconds",
            )
    
system_network_dropped_packets_gauge = meter.create_observable_gauge(
                name="system.network.dropped.packets",
                callbacks=[SystemMetricsInstrumentor()._get_system_network_dropped_packets],
                description="system network dropped packets",
                unit="seconds",
            )
    
system_network_packets_gauge = meter.create_observable_gauge(
                name="system.network.packets",
                callbacks=[SystemMetricsInstrumentor()._get_system_network_packets],
                description="",
                unit="seconds",
            )
    
system_network_errors_gauge = meter.create_observable_gauge(
                name="system.network.errors",
                callbacks=[SystemMetricsInstrumentor()._get_system_network_errors],
                description="",
                unit="seconds",
            )
    
system_network_io_gauge = meter.create_observable_gauge(
                name="system.network.io",
                callbacks=[SystemMetricsInstrumentor()._get_system_network_io],
                description="",
                unit="seconds",
            )
    
system_network_connections_gauge = meter.create_observable_gauge(
                name="system.network.connections",
                callbacks=[SystemMetricsInstrumentor()._get_system_network_connections],
                description="",
                unit="seconds",
            )
    
runtime_memory_gauge = meter.create_observable_gauge(
                name="runtime.memory",
                callbacks=[SystemMetricsInstrumentor()._get_runtime_memory],
                description="",
                unit="seconds",
            )
    
runtime_cpu_time_gauge = meter.create_observable_gauge(
                name="runtime.cpu.time",
                callbacks=[SystemMetricsInstrumentor()._get_runtime_cpu_time],
                description="",
                unit="seconds",
            )
    
runtime_gc_count_gauge = meter.create_observable_gauge(
                name="runtime.gc_count",
                callbacks=[SystemMetricsInstrumentor()._get_runtime_gc_count],
                description="",
                unit="seconds",
            )
    
    
    
staging_attributes = {"environment": "staging"}
testing_attributes = {"environment": "testing"}

logger.info("starting instrumented application...")
try:
    while True:
            requests_counter.add(random.randint(0, 25), staging_attributes)
            requests_size.record(random.randint(0, 300), staging_attributes)

            requests_counter.add(random.randint(0, 35), testing_attributes)
            requests_size.record(random.randint(0, 100), testing_attributes)
            time.sleep(5)

except KeyboardInterrupt:
    logger.info("shutting down...")