import gc
import json
import os
from platform import python_implementation
import subprocess
from typing import Collection, Dict, Iterable, List, Optional

import psutil
import windows_tools.windows_firewall as wf
# FIXME Remove this pyling disabling line when Github issue is cleared
# pylint: disable=no-name-in-module
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.system_metrics.package import _instruments
from opentelemetry.instrumentation.system_metrics.version import __version__
from opentelemetry.metrics import CallbackOptions, Observation, get_meter
from opentelemetry.sdk.util import get_dict_as_key

_DEFAULT_CONFIG = {
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
    "system.service.state": ["STOPPED","RUNNING"]
}


class test_ut(BaseInstrumentor):
    def __init__(
        self,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, List[str]]] = None,
    ):
        super().__init__()
        if config is None:
            self._config = _DEFAULT_CONFIG
        else:
            self._config = config
        self._labels = {} if labels is None else labels
        self._meter = None
        self._python_implementation = python_implementation().lower()

        self._proc = psutil.Process(os.getpid())
        self._system_memory_usage_labels = self._labels.copy()
        self._system_service_state = self._labels.copy()
    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        # pylint: disable=too-many-branches
        meter_provider = kwargs.get("meter_provider")
        self._meter = get_meter(
            __name__,
            __version__,
            meter_provider,
        )

        # if "system.cpu.time" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.cpu.time",
        #         callbacks=[self._get_system_cpu_time],
        #         description="System CPU time",
        #         unit="seconds",
        #     )

        # if "system.cpu.utilization" in self._config:
        #     self._meter.create_observable_gauge(
        #         name="system.cpu.utilization",
        #         callbacks=[self._get_system_cpu_utilization],
        #         description="System CPU utilization",
        #         unit="1",
        #     )

        # if "system.memory.usage" in self._config:
        #     self._meter.create_observable_gauge(
        #         name="system.memory.usage",
        #         callbacks=[self._get_system_memory_usage],
        #         description="System memory usage",
        #         unit="bytes",
        #     )

        # if "system.memory.utilization" in self._config:
        #     self._meter.create_observable_gauge(
        #         name="system.memory.utilization",
        #         callbacks=[self._get_system_memory_utilization],
        #         description="System memory utilization",
        #         unit="1",
        #     )

        # if "system.swap.usage" in self._config:
        #     self._meter.create_observable_gauge(
        #         name="system.swap.usage",
        #         callbacks=[self._get_system_swap_usage],
        #         description="System swap usage",
        #         unit="pages",
        #     )

        # if "system.swap.utilization" in self._config:
        #     self._meter.create_observable_gauge(
        #         name="system.swap.utilization",
        #         callbacks=[self._get_system_swap_utilization],
        #         description="System swap utilization",
        #         unit="1",
        #     )

        # # TODO Add _get_system_swap_page_faults

        # # self._meter.create_observable_counter(
        # #     name="system.swap.page_faults",
        # #     callbacks=[self._get_system_swap_page_faults],
        # #     description="System swap page faults",
        # #     unit="faults",
        # #     value_type=int,
        # # )

        # # TODO Add _get_system_swap_page_operations
        # # self._meter.create_observable_counter(
        # #     name="system.swap.page_operations",
        # #     callbacks=self._get_system_swap_page_operations,
        # #     description="System swap page operations",
        # #     unit="operations",
        # #     value_type=int,
        # # )

        # if "system.disk.io" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.disk.io",
        #         callbacks=[self._get_system_disk_io],
        #         description="System disk IO",
        #         unit="bytes",
        #     )

        # if "system.disk.operations" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.disk.operations",
        #         callbacks=[self._get_system_disk_operations],
        #         description="System disk operations",
        #         unit="operations",
        #     )

        # if "system.disk.time" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.disk.time",
        #         callbacks=[self._get_system_disk_time],
        #         description="System disk time",
        #         unit="seconds",
        #     )

        # # TODO Add _get_system_filesystem_usage

        # # self.accumulator.register_valueobserver(
        # #     callback=self._get_system_filesystem_usage,
        # #     name="system.filesystem.usage",
        # #     description="System filesystem usage",
        # #     unit="bytes",
        # #     value_type=int,
        # # )

        # # TODO Add _get_system_filesystem_utilization
        # # self._meter.create_observable_gauge(
        # #     callback=self._get_system_filesystem_utilization,
        # #     name="system.filesystem.utilization",
        # #     description="System filesystem utilization",
        # #     unit="1",
        # #     value_type=float,
        # # )

        # # TODO Filesystem information can be obtained with os.statvfs in Unix-like
        # # OSs, how to do the same in Windows?

        # if "system.network.dropped.packets" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.network.dropped_packets",
        #         callbacks=[self._get_system_network_dropped_packets],
        #         description="System network dropped_packets",
        #         unit="packets",
        #     )

        # if "system.network.packets" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.network.packets",
        #         callbacks=[self._get_system_network_packets],
        #         description="System network packets",
        #         unit="packets",
        #     )

        # if "system.network.errors" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.network.errors",
        #         callbacks=[self._get_system_network_errors],
        #         description="System network errors",
        #         unit="errors",
        #     )

        # if "system.network.io" in self._config:
        #     self._meter.create_observable_counter(
        #         name="system.network.io",
        #         callbacks=[self._get_system_network_io],
        #         description="System network io",
        #         unit="bytes",
        #     )

        # if "system.network.connections" in self._config:
        #     self._meter.create_observable_up_down_counter(
        #         name="system.network.connections",
        #         callbacks=[self._get_system_network_connections],
        #         description="System network connections",
        #         unit="connections",
        #     )

        # if "runtime.memory" in self._config:
        #     self._meter.create_observable_counter(
        #         name=f"runtime.{self._python_implementation}.memory",
        #         callbacks=[self._get_runtime_memory],
        #         description=f"Runtime {self._python_implementation} memory",
        #         unit="bytes",
        #     )

        # if "runtime.cpu.time" in self._config:
        #     self._meter.create_observable_counter(
        #         name=f"runtime.{self._python_implementation}.cpu_time",
        #         callbacks=[self._get_runtime_cpu_time],
        #         description=f"Runtime {self._python_implementation} CPU time",
        #         unit="seconds",
        #     )

        # if "runtime.gc_count" in self._config:
        #     self._meter.create_observable_counter(
        #         name=f"runtime.{self._python_implementation}.gc_count",
        #         callbacks=[self._get_runtime_gc_count],
        #         description=f"Runtime {self._python_implementation} GC count",
        #         unit="bytes",
        #     )
        
    def str_to_class(classname):
        return getattr(sys.modules[__name__], classname)

    def _uninstrument(self, **__):
        pass

    def _get_system_memory_usage(
            self, options: CallbackOptions
        ) -> Iterable[Observation]:
            """Observer callback for memory usage"""
            virtual_memory = psutil.virtual_memory()
            for metric in self._config["system.memory.usage"]:
                self._system_memory_usage_labels["state"] = metric
                if hasattr(virtual_memory, metric):
                    yield Observation(
                        getattr(virtual_memory, metric),
                        self._system_memory_usage_labels.copy(),
                    )
                    
    # def _get_mount_info(
    #         self, options: CallbackOptions
    #     ) -> Iterable[Observation]:
    #         """Observer callback for memory usage"""
    #         test = wf.is_firewall_active()
    #         self._system_service_state["state"] = test
    #         yield Observation(test, self._system_service_state.copy())
            
            
    def _get_mount_info(
            self, options: CallbackOptions
        ) -> Iterable[Observation]:
            """Observer callback for memory usage"""
            temp = subprocess.check_output('sc query | findstr "SERVICE_NAME STATE"', shell=True).decode('utf-8')
            temp = [x.replace("\r","") for x in temp]
            test=''.join(map(str,temp))
            # test=json.loads(str(test))
            # print(test)
            # print(test.split('\n')[0])
            service=[str]
            for line in test.split('\n'):
                if 'SERVICE_NAME' in line.split(':'[0]):
                        line.split(':'[0])
                        print(service)
                else:
                    print(line.split(':'[0]))
                # print(line.split(':'))
            
            # print(service)
            for metric in self._config["system.service.state"]:
                print(metric)
                self._system_service_state["state"] = metric
                if hasattr(test, metric):
                    yield Observation(
                        getattr(test, metric),
                        self._system_service_state.copy(),
                    )
