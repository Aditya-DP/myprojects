from distutils.command.config import config
from logging import Logger
from posixpath import basename, splitext
import time
from test_lib import test_ut
from opentelemetry.instrumentation.system_metrics.package import _instruments as instrumentmetrics
from opentelemetry.metrics import set_meter_provider, Observation, CallbackOptions
import opentelemetry.metrics as metrics
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

configuration = {
        "system.cpu.time": ["idle", "user", "system", "irq"],
        "system.cpu.utilization": ["idle", "user", "system", "irq"],
        "system.memory.usage": ["used", "free", "cached"],
        "system.memory.utilization": ["used", "free", "cached"],
        "system.swap.usage": ["used", "free"],
        "system.swap.utilization": ["used", "free"],
        "system.disk.io": ["read", "write"],
        "system.disk.operations": ["read", "write"],
        "system.disk.time": ["read", "write"],
        "system.network.dropped.packets": ["transmit", "receive"],
        "system.network.packets": ["transmit", "receive"],
        "system.network.errors": ["transmit", "receive"],
        "system.network.io": ["transmit", "receive"],
        "system.network.connections": ["family", "type"],
        "runtime.memory": ["rss", "vms"],
        "runtime.cpu.time": ["user", "system"],
        "runtime.gc_count": None,   
    }



if __name__ == '__main__':
    script_name = splitext(basename(__file__))[0]
    # test_ut()

    set_meter_provider(MeterProvider(
        metric_readers= [PeriodicExportingMetricReader(exporter= ConsoleMetricExporter(), export_interval_millis=5000)]))
    # metrics are collected asynchronously
    # input("...")
    # to configure custom metrics
    # SystemMetricsInstrumentor(config=configuration).instrument()
    # test_ut(config=configuration).instrument()

    
    # for (number, percent) in enumerate(print(temp)):
    #     attributes = {"cpu_number": str(number)}
    meter = metrics.get_meter(script_name)
    
    system_cpu_time_gauge = meter.create_observable_gauge(
                name="system.service.state",
                callbacks=[test_ut()._get_mount_info],
                description="firewall status",
                unit="Boolean",
            )
