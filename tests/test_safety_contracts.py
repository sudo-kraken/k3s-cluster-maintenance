"""Regression tests for maintenance safety invariants."""

from pathlib import Path
import unittest

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str):
    """Load a repository YAML file."""
    with (REPOSITORY_ROOT / relative_path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def walk_tasks(tasks):
    """Yield tasks recursively through Ansible block sections."""
    for task in tasks:
        yield task
        for section in ("block", "rescue", "always"):
            yield from walk_tasks(task.get(section, []))


class MaintenanceSafetyContractTests(unittest.TestCase):
    """Protect behavior that prevents cluster-wide maintenance outages."""

    def test_maintenance_runs_one_node_at_a_time_and_stops_on_failure(self):
        play = load_yaml("maintenance.yml")[0]

        self.assertEqual(play["serial"], 1)
        self.assertIs(play["any_errors_fatal"], True)

    def test_current_node_does_not_end_maintenance_for_other_nodes(self):
        tasks = load_yaml(
            "roles/k3s_node_maintenance/tasks/package_checks.yml"
        )
        meta_actions = {
            task["ansible.builtin.meta"]
            for task in tasks
            if "ansible.builtin.meta" in task
        }

        self.assertIn("end_host", meta_actions)
        self.assertNotIn("end_play", meta_actions)

    def test_drain_uses_pdb_aware_module_and_fails_closed(self):
        tasks = load_yaml(
            "roles/k3s_node_maintenance/tasks/cluster_preparation.yml"
        )
        drain_tasks = [
            task
            for task in walk_tasks(tasks)
            if task.get("kubernetes.core.k8s_drain", {}).get("state") == "drain"
        ]
        direct_pod_deletes = [
            task
            for task in walk_tasks(tasks)
            if task.get("kubernetes.core.k8s", {}).get("kind") == "Pod"
            and task["kubernetes.core.k8s"].get("state") == "absent"
        ]

        self.assertEqual(len(drain_tasks), 1)
        self.assertEqual(
            drain_tasks[0]["kubernetes.core.k8s_drain"]["state"], "drain"
        )
        self.assertNotIn("failed_when", drain_tasks[0])
        self.assertEqual(direct_pod_deletes, [])

    def test_longhorn_skip_does_not_skip_generic_state_capture(self):
        tasks = load_yaml(
            "roles/k3s_node_maintenance/tasks/cluster_preparation.yml"
        )
        capture_task = next(
            task
            for task in tasks
            if task["name"] == "Capture original scheduling state"
        )

        self.assertNotIn("longhorn", capture_task["tags"])

    def test_cluster_tag_restores_every_preparation_change(self):
        tasks = load_yaml(
            "roles/k3s_node_maintenance/tasks/cluster_restoration.yml"
        )

        self.assertTrue(tasks)
        self.assertTrue(
            all("cluster" in task.get("tags", []) for task in tasks)
        )

    def test_redhat_packages_are_upgraded(self):
        tasks = load_yaml(
            "roles/k3s_node_maintenance/tasks/redhat_updates.yml"
        )
        dnf_tasks = [
            task for task in tasks if "ansible.builtin.dnf" in task
        ]
        upgrade_task = next(
            task
            for task in dnf_tasks
            if task["ansible.builtin.dnf"].get("name") == "*"
        )

        self.assertTrue(
            any(task["ansible.builtin.dnf"].get("list") == "updates"
                for task in dnf_tasks)
        )
        self.assertEqual(upgrade_task["ansible.builtin.dnf"]["state"], "latest")
        self.assertIs(
            upgrade_task["ansible.builtin.dnf"]["update_only"], True
        )

    def test_release_archive_uses_the_project_manifest(self):
        workflow = (
            REPOSITORY_ROOT / ".github/workflows/release.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("            pyproject.toml \\", workflow)
        self.assertIn("            uv.lock \\", workflow)
        self.assertIn("            hosts.example.yml \\", workflow)
        self.assertIn("signed/release/*.bundle", workflow)
        self.assertNotIn("            requirements.txt \\", workflow)


if __name__ == "__main__":
    unittest.main()
