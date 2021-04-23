import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.attack_helpers import (
    GremlinAttackHelper,
    GremlinAttackTargetHelper,
    GremlinTargetHosts,
    GremlinTargetContainers,
    GremlinAttackCommandHelper,
    GremlinNetworkAttackHelper,
    GremlinResourceAttackHelper,
    GremlinCPUAttack,
    GremlinMemoryAttack,
    GremlinDiskSpaceAttack,
    GremlinDiskIOAttack,
    GremlinShutdownAttack,
    GremlinProcessKillerAttack,
    GremlinTimeTravelAttack,
    GremlinBlackholeAttack,
    GremlinDNSAttack,
    GremlinLatencyAttack,
    GremlinPacketLossAttack,
    GremlinStateAttackHelper,
)

from .util import mock_data

attack_helper_params_custom = {
    "strategy_type": "Exact",
    "exact": 1,
    # "percent": 10,
}

attack_helper_params_default = {
    "strategy_type": "Random",
    # "exact": 1,
    "percent": 10,
}


class TestAttackHelpers(unittest.TestCase):
    def test_attack_helper_api_model(self) -> None:
        # defaults
        expected_output = {
            "command": {
                "args": ["-l", "60", "-p", "100", "-c", "1"],
                "commandType": "CPU",
                "type": "cpu",
            },
            "target": {"hosts": "all", "percent": 10, "type": "Random"},
        }
        helper = GremlinAttackHelper()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_attack_helper_repr_str(self) -> None:
        # defaults
        expected_output = 'GremlinAttackHelper({\'target\': \'GremlinTargetHosts({"exact": 0, "percent": 25, "strategy_type": "Random", "target_all_hosts": true})\', \'command\': \'GremlinCPUAttack({"all_cores": false, "capacity": 90, "cores": 1, "length": 60})\'})'
        kwargs_th = {
            "exact": 0,
            "percent": 25,
            "strategy_type": "Random",
            "target_all_hosts": True,
        }
        kwargs_cpua = {"all_cores": False, "capacity": 90, "cores": 1, "length": 60}
        kwargs = {
            "target": GremlinTargetHosts(**kwargs_th),
            "command": GremlinCPUAttack(**kwargs_cpua),
        }
        helper = GremlinAttackHelper(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_target_helper_target_definition(self) -> None:
        helper = GremlinAttackTargetHelper(**attack_helper_params_custom)
        test_output = helper.target_definition()
        expected_output = {
            "strategyType": attack_helper_params_custom["strategy_type"],
            "strategy": {"count": str(attack_helper_params_custom["exact"])},
        }
        self.assertEqual(test_output, expected_output)

        helper = GremlinAttackTargetHelper()
        test_output = helper.target_definition()
        expected_output = {
            "strategyType": attack_helper_params_default["strategy_type"],
            "strategy": {"percentage": attack_helper_params_default["percent"]},
        }
        self.assertEqual(test_output, expected_output)

    def test_target_helper_target_definition_graph(self) -> None:
        helper = GremlinAttackTargetHelper(**attack_helper_params_custom)
        test_output = helper.target_definition_graph()
        expected_output = {
            "strategy_type": attack_helper_params_custom["strategy_type"],
            "strategy": {
                "count": str(attack_helper_params_custom["exact"]),
                "type": attack_helper_params_custom["strategy_type"],
            },
        }
        self.assertEqual(test_output, expected_output)

        helper = GremlinAttackTargetHelper()
        test_output = helper.target_definition_graph()
        expected_output = {
            "strategy_type": attack_helper_params_default["strategy_type"],
            "strategy": {
                "percentage": attack_helper_params_default["percent"],
                "type": "RandomPercent",
            },
        }
        self.assertEqual(test_output, expected_output)

    def test_attack_target_helper_api_model(self) -> None:
        # defaults
        expected_output = {"percent": 10, "type": "Random"}
        helper = GremlinAttackTargetHelper()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_attack_target_helper_repr_str(self) -> None:
        # defaults
        expected_output = 'GremlinAttackTargetHelper({"exact": 0, "percent": 15, "strategy_type": "Random"})'
        kwargs = {"exact": 0, "percent": 15, "strategy_type": "Random"}
        helper = GremlinAttackTargetHelper(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    @patch("requests.get")
    def test_filter_active_tags_with_decorator(self, mock_get) -> None:
        expected_output = {
            "os-type": [None],
            "os-version": [None, "test10"],
            "os_type": ["testwindows"],
        }

        def mock_json():
            return [{"tags": {"os_type": "testwindows", "os-version": "test10"}}]

        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        helper = GremlinTargetHosts()
        helper._filter_active_tags()
        self.assertEqual(helper._active_tags, expected_output)

    def test_target_hosts_api_model(self) -> None:
        # defaults
        expected_output = {"hosts": "all", "percent": 10, "type": "Random"}
        helper = GremlinTargetHosts()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_target_hosts_repr_str(self) -> None:
        # defaults
        expected_output = 'GremlinTargetHosts({"exact": 0, "percent": 25, "strategy_type": "Random", "target_all_hosts": true})'
        kwargs = {
            "exact": 0,
            "percent": 25,
            "strategy_type": "Random",
            "target_all_hosts": True,
        }
        helper = GremlinTargetHosts(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    @patch("requests.get")
    def test_filter_active_labels_with_decorator(self, mock_get) -> None:
        expected_output = {"os_type": ["testwindows"], "os-version": ["test10"]}

        def mock_json():
            return [
                {"container_labels": {"os_type": "testwindows", "os-version": "test10"}}
            ]

        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        helper = GremlinTargetContainers()
        helper._filter_active_labels()
        self.assertEqual(helper._active_labels, expected_output)

    def test_target_containers_api_model(self) -> None:
        # defaults
        expected_output = {"containers": "all", "percent": 10, "type": "Random"}
        helper = GremlinTargetContainers()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_target_containers_repr_str(self) -> None:
        # defaults
        expected_output = 'GremlinTargetContainers({"exact": 0, "percent": 35, "strategy_type": "Random", "target_all_containers": false, "ids": [], "labels": {}})'
        kwargs = {
            "exact": 0,
            "percent": 35,
            "strategy_type": "Random",
            "target_all_containers": False,
            "ids": [],
            "labels": {},
        }
        helper = GremlinTargetContainers(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_impact_definition(self) -> None:
        expected_output = {
            "commandArgs": {"cliArgs": ["memory", "-l", "100"], "length": 100},
            "commandType": "memory",
        }

        helper = GremlinAttackCommandHelper()
        helper.shortType = expected_output["commandType"]
        helper.length = expected_output["commandArgs"]["length"]

        helper_output = helper.impact_definition()
        self.assertEqual(helper_output, expected_output)

    def test_impact_definition_graph(self) -> None:
        expected_output = {
            "infra_command_args": {
                "cli_args": ["memory", "-l", "60"],
                "type": "memory",
            },
            "infra_command_type": "memory",
        }
        helper = GremlinAttackCommandHelper()
        helper.shortType = expected_output["infra_command_type"]

        helper_output = helper.impact_definition_graph()
        self.assertEqual(helper_output, expected_output)

    def test_attack_command_helper_api_model(self) -> None:
        # defaults
        expected_output = {"args": ["-l", "60"], "commandType": "", "type": ""}
        helper = GremlinAttackCommandHelper()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_attack_command_helper_repr_str(self) -> None:
        expected_output = 'GremlinAttackCommandHelper({"length": 70})'
        kwargs = {"length": 70}
        helper = GremlinAttackCommandHelper(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_resource_attack_helper_api_model(self) -> None:
        # defaults
        expected_output = {"args": ["-l", "60"], "commandType": "", "type": ""}
        helper = GremlinResourceAttackHelper()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_resource_attack_helper_repr_str(self) -> None:
        expected_output = 'GremlinResourceAttackHelper({"length": 70})'
        kwargs = {"length": 70}
        helper = GremlinResourceAttackHelper(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_state_attack_helper_repr_str(self) -> None:
        expected_output = "GremlinStateAttackHelper()"
        helper = GremlinStateAttackHelper()
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test__port_maker(self) -> None:
        expected_output = []
        helper = GremlinNetworkAttackHelper()
        helper_output = helper._port_maker()
        self.assertEqual(expected_output, helper_output)

        expected_output = ["80"]
        helper = GremlinNetworkAttackHelper()
        helper_output = helper._port_maker(80)
        self.assertEqual(expected_output, helper_output)

        expected_output = ["8080", "433", "23"]
        helper = GremlinNetworkAttackHelper()
        helper_output = helper._port_maker(expected_output)
        self.assertEqual(expected_output, helper_output)

    def test_network_attack_helper_api_model(self) -> None:
        # defaults
        expected_output = {"args": ["-l", "60"], "commandType": "", "type": ""}
        helper = GremlinNetworkAttackHelper()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_network_attack_helper_repr_str(self) -> None:
        expected_output = 'GremlinNetworkAttackHelper({"length": 65, "device": "", "ips": [], "protocol": "", "providers": [], "tags": []})'
        kwargs = {
            "length": 65,
            "device": "",
            "ips": [],
            "protocol": "",
            "providers": [],
            "tags": [],
        }
        helper = GremlinNetworkAttackHelper(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_cpu_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-p", "100", "-c", "1"],
            "commandType": "CPU",
            "type": "cpu",
        }
        helper = GremlinCPUAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_cpu_attack_repr_str(self) -> None:
        # defaults
        expected_output = 'GremlinCPUAttack({"all_cores": false, "capacity": 90, "cores": 2, "length": 60})'
        kwargs = {"all_cores": False, "capacity": 90, "cores": 2, "length": 60}
        helper = GremlinCPUAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_memory_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-p", "100"],
            "commandType": "Memory",
            "type": "memory",
        }
        helper = GremlinMemoryAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_memory_attack_repr_str(self) -> None:
        expected_output = (
            'GremlinMemoryAttack({"length": 65, "amount": 99, "amountType": "MB"})'
        )
        kwargs = {
            "length": 65,
            "amount": 99,
            "amountType": "MB",
        }
        helper = GremlinMemoryAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_disk_space_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-d", "/tmp", "-w", "1", "-b", "4", "-p", "100"],
            "commandType": "Disk",
            "type": "disk",
        }
        helper = GremlinDiskSpaceAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_disk_space_attack_repr_str(self) -> None:
        expected_output = 'GremlinDiskSpaceAttack({"length": 75, "blocksize": 4, "directory": "/tmp", "percent": 95, "workers": 1})'
        kwargs = {
            "length": 75,
            "blocksize": 4,
            "directory": "/tmp",
            "percent": 95,
            "workers": 1,
        }
        helper = GremlinDiskSpaceAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_disk_io_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": [
                "-l",
                "60",
                "-c",
                "1",
                "-d",
                "/tmp",
                "-m",
                "rw",
                "-s",
                "4",
                "-w",
                "1",
            ],
            "commandType": "IO",
            "type": "io",
        }
        helper = GremlinDiskIOAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_disk_io_repr_str(self) -> None:
        expected_output = 'GremlinDiskIOAttack({"length": 85, "blockcount": 1, "blocksize": 4, "directory": "/tmp/usr", "mode": "rw", "workers": 2})'
        kwargs = {
            "length": 85,
            "blockcount": 1,
            "blocksize": 4,
            "directory": "/tmp/usr",
            "mode": "rw",
            "workers": 2,
        }
        helper = GremlinDiskIOAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_shutdown_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-d", "1"],
            "commandType": "Shutdown",
            "type": "shutdown",
        }
        helper = GremlinShutdownAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_shutdown_attack_repr_str(self) -> None:
        expected_output = (
            'GremlinShutdownAttack({"length": 85, "delay": 20, "reboot": false})'
        )
        kwargs = {
            "length": 85,
            "delay": 20,
            "reboot": False,
        }
        helper = GremlinShutdownAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_process_killer_attack_api_model(self) -> None:
        test_process = "ls"
        kwargs = {"process": test_process}
        # defaults
        expected_output = {
            "args": ["-l", "60", "-i", "1", "-p", test_process, "-f"],
            "commandType": "Process Killer",
            "type": "process_killer",
        }
        helper = GremlinProcessKillerAttack(**kwargs)
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_process_killer_attack_repr_str(self) -> None:
        expected_output = 'GremlinProcessKillerAttack({"length": 65, "exact": false, "full_match": true, "group": "", "interval": 1, "kill_children": false, "process": "", "target_newest": false, "target_oldest": false, "user": "unittestuser"})'
        kwargs = {
            "length": 65,
            "exact": False,
            "full_match": True,
            "group": "",
            "interval": 1,
            "kill_children": False,
            "process": "",
            "target_newest": False,
            "target_oldest": False,
            "user": "unittestuser",
        }
        helper = GremlinProcessKillerAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_time_travel_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-o", "86400"],
            "commandType": "Time Travel",
            "type": "time_travel",
        }
        helper = GremlinTimeTravelAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_time_travel_attack_repr_str(self) -> None:
        expected_output = 'GremlinTimeTravelAttack({"length": 65, "block_ntp": false, "offset": 12000})'
        kwargs = {
            "length": 65,
            "block_ntp": False,
            "offset": 12000,
        }
        helper = GremlinTimeTravelAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_black_hole_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-p", "^53", "-h", "^api.gremlin.com"],
            "commandType": "Blackhole",
            "type": "blackhole",
        }
        helper = GremlinBlackholeAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_black_hole_attack_repr_str(self) -> None:
        expected_output = 'GremlinBlackholeAttack({"length": 65, "device": "", "ips": [], "protocol": "", "providers": [], "tags": [], "egress_ports": ["^533"], "hostnames": "^api2.gremlin.com", "ingress_ports": []})'
        kwargs = {
            "length": 65,
            "device": "",
            "ips": [],
            "protocol": "",
            "providers": [],
            "tags": [],
            "egress_ports": ["^533"],
            "hostnames": ["^api2.gremlin.com"],
            "ingress_ports": [],
        }
        helper = GremlinBlackholeAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_dns_attack_api_model(self) -> None:
        # defaults
        expected_output = {"args": ["-l", "60"], "commandType": "DNS", "type": "dns"}
        helper = GremlinDNSAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_dns_attack_repr_str(self) -> None:
        expected_output = 'GremlinDNSAttack({"length": 75, "device": "", "ips": [], "protocol": "", "providers": [], "tags": []})'
        kwargs = {
            "length": 75,
            "device": "",
            "ips": [],
            "protocol": "",
            "providers": [],
            "tags": [],
        }
        helper = GremlinDNSAttack(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_latency_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-m", "100", "-p", "^53", "-h", "^api.gremlin.com"],
            "commandType": "Latency",
            "type": "latency",
        }
        helper = GremlinLatencyAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_latency_attack_repr_str(self) -> None:
        expected_output = 'GremlinLatencyAttack({"length": 75, "device": "", "ips": [], "protocol": "", "providers": [], "tags": [], "delay": 100, "egress_ports": ["^533"], "hostnames": "^api2.gremlin.com", "source_ports": []})'
        kwargs = {
            "length": 75,
            "device": "",
            "ips": [],
            "protocol": "",
            "providers": [],
            "tags": [],
            "delay": 100,
            "egress_ports": ["^533"],
            "hostnames": ["^api2.gremlin.com"],
            "source_ports": [],
        }
        helper = GremlinLatencyAttack(**kwargs)
        helper_output = repr(helper)
        max_diff = self.maxDiff = None
        self.maxDiff = None
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)
        self.maxDiff = max_diff

    def test_packet_loss_attack_api_model(self) -> None:
        # defaults
        expected_output = {
            "args": ["-l", "60", "-r", "1", "-p", "^53", "-h", "^api.gremlin.com"],
            "commandType": "Packet Loss",
            "type": "packet_loss",
        }
        helper = GremlinPacketLossAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

    def test_packet_loss_attack_repr_str(self) -> None:
        expected_output = 'GremlinPacketLossAttack({"length": 85, "device": "", "ips": [], "protocol": "", "providers": [], "tags": [], "corrupt": false, "egress_ports": ["^543"], "hostnames": "^api3.gremlin.com", "percent": 1, "source_ports": []})'
        kwargs = {
            "length": 85,
            "device": "",
            "ips": [],
            "protocol": "",
            "providers": [],
            "tags": [],
            "corrupt": False,
            "egress_ports": ["^543"],
            "hostnames": ["^api3.gremlin.com"],
            "percent": 1,
            "source_ports": [],
        }
        helper = GremlinPacketLossAttack(**kwargs)
        helper_output = repr(helper)
        max_diff = self.maxDiff = None
        self.maxDiff = None
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)
        self.maxDiff = max_diff
