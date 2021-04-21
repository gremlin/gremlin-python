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

    def test_dns_attack_api_model(self) -> None:
        # defaults
        expected_output = {"args": ["-l", "60"], "commandType": "DNS", "type": "dns"}
        helper = GremlinDNSAttack()
        helper_output = helper.api_model()
        self.assertEqual(helper_output, expected_output)

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
