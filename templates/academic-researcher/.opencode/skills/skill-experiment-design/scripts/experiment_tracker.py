#!/usr/bin/env python3
"""
Experiment Tracker - Track experiment versions, configurations, and results.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List


class ExperimentTracker:
    """Manage experiment tracking database."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.getcwd()
        self.exp_dir = os.path.join(self.base_dir, "exp")
        self.db_path = os.path.join(self.exp_dir, ".experiment_tracker.json")

    def load_db(self) -> Dict[str, Any]:
        """Load tracking database or initialize if missing."""
        if not os.path.exists(self.db_path):
            return {"experiments": {}}

        with open(self.db_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_db(self, data: Dict[str, Any]) -> None:
        """Save tracking database to disk."""
        os.makedirs(self.exp_dir, exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def init_experiment(self, name: str, description: str = "") -> Dict[str, Any]:
        """Initialize a new experiment."""
        data = self.load_db()
        if name in data["experiments"]:
            raise ValueError(f"Experiment already exists: {name}")

        timestamp = self._timestamp()
        data["experiments"][name] = {
            "description": description,
            "created_at": timestamp,
            "status": "initialized",
            "versions": [],
        }
        self.save_db(data)
        return {"name": name, "description": description, "timestamp": timestamp}

    def log_config(self, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Log a configuration snapshot for an experiment."""
        data = self.load_db()
        experiment = self._get_experiment(data, name)

        version_number = len(experiment["versions"]) + 1
        entry = {
            "version": version_number,
            "timestamp": self._timestamp(),
            "config": config,
            "metrics": None,
            "notes": "",
        }
        experiment["versions"].append(entry)
        experiment["status"] = "running"
        self.save_db(data)
        return entry

    def log_result(self, name: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Record metrics for the latest version."""
        data = self.load_db()
        experiment = self._get_experiment(data, name)
        if not experiment["versions"]:
            raise ValueError("No configuration logged yet. Use 'log' first.")

        latest = experiment["versions"][-1]
        latest["metrics"] = metrics
        experiment["status"] = "completed"
        self.save_db(data)
        return latest

    def status(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Return status summary for experiments."""
        data = self.load_db()
        if name:
            experiment = self._get_experiment(data, name)
            return {name: experiment}
        return data["experiments"]

    def history(self, name: str) -> Dict[str, Any]:
        """Return full history for an experiment."""
        data = self.load_db()
        return self._get_experiment(data, name)

    def _get_experiment(self, data: Dict[str, Any], name: str) -> Dict[str, Any]:
        if name not in data["experiments"]:
            raise ValueError(f"Experiment not found: {name}")
        return data["experiments"][name]

    def _timestamp(self) -> str:
        return datetime.utcnow().isoformat(timespec="seconds")


class ExperimentTrackerCLI:
    """CLI interface for experiment tracker."""

    def __init__(self, tracker: ExperimentTracker):
        self.tracker = tracker

    def run(self, argv: List[str]) -> None:
        if not argv:
            self._print_usage()
            return

        command = argv[0]
        if command == "init":
            self._handle_init(argv[1:])
        elif command == "log":
            self._handle_log(argv[1:])
        elif command == "result":
            self._handle_result(argv[1:])
        elif command == "status":
            self._handle_status(argv[1:])
        elif command == "history":
            self._handle_history(argv[1:])
        else:
            self._print_usage()

    def _handle_init(self, args: List[str]) -> None:
        if not args:
            self._print_usage()
            return

        name = args[0]
        description = self._extract_flag(args[1:], "--description") or ""
        info = self.tracker.init_experiment(name, description)
        self._print_header("EXPERIMENT TRACKER")
        print(f"[init] Created experiment: {info['name']}")
        print(f"Description: {info['description']}")
        print(f"Timestamp: {info['timestamp']}")
        self._print_footer()

    def _handle_log(self, args: List[str]) -> None:
        if not args:
            self._print_usage()
            return

        name = args[0]
        config_json = self._extract_flag(args[1:], "--config")
        if not config_json:
            raise ValueError("Missing --config JSON for log command.")
        config = json.loads(config_json)
        entry = self.tracker.log_config(name, config)
        self._print_header("EXPERIMENT TRACKER")
        print(f"[log] Updated experiment: {name}")
        print(f"Version: {entry['version']}")
        print(f"Timestamp: {entry['timestamp']}")
        self._print_footer()

    def _handle_result(self, args: List[str]) -> None:
        if not args:
            self._print_usage()
            return

        name = args[0]
        metrics_json = self._extract_flag(args[1:], "--metrics")
        if not metrics_json:
            raise ValueError("Missing --metrics JSON for result command.")
        metrics = json.loads(metrics_json)
        entry = self.tracker.log_result(name, metrics)
        self._print_header("EXPERIMENT TRACKER")
        print(f"[result] Recorded metrics for: {name}")
        print(f"Version: {entry['version']}")
        print(f"Timestamp: {entry['timestamp']}")
        self._print_footer()

    def _handle_status(self, args: List[str]) -> None:
        name = args[0] if args else None
        data = self.tracker.status(name)
        self._print_header("EXPERIMENT STATUS")

        if name:
            self._print_single_status(name, data[name])
        else:
            self._print_status_table(data)

        self._print_footer()

    def _handle_history(self, args: List[str]) -> None:
        if not args:
            self._print_usage()
            return

        name = args[0]
        history = self.tracker.history(name)
        self._print_header("EXPERIMENT HISTORY")
        print(f"Experiment: {name}")
        print(f"Description: {history['description']}")
        print(f"Status: {history['status']}")
        print("")

        for version in history.get("versions", []):
            print(f"Version {version['version']} - {version['timestamp']}")
            print(f"  Config: {json.dumps(version['config'], ensure_ascii=False)}")
            print(
                f"  Metrics: {json.dumps(version['metrics'], ensure_ascii=False) if version['metrics'] else 'None'}"
            )
            print("")

        self._print_footer()

    def _print_status_table(self, data: Dict[str, Any]) -> None:
        print("Name              | Status      | Versions | Last Updated")
        print("------------------|-------------|----------|------------------")
        for name, exp in data.items():
            versions = len(exp.get("versions", []))
            last_updated = self._last_updated(exp)
            status = exp.get("status", "unknown")
            print(
                f"{name[:17].ljust(17)} | {status.ljust(11)} | {str(versions).ljust(8)} | {last_updated}"
            )

    def _print_single_status(self, name: str, exp: Dict[str, Any]) -> None:
        versions = len(exp.get("versions", []))
        last_updated = self._last_updated(exp)
        status = exp.get("status", "unknown")
        print(f"Name: {name}")
        print(f"Status: {status}")
        print(f"Versions: {versions}")
        print(f"Last Updated: {last_updated}")

    def _last_updated(self, exp: Dict[str, Any]) -> str:
        if exp.get("versions"):
            timestamp = exp["versions"][-1]["timestamp"]
        else:
            timestamp = exp.get("created_at", "N/A")
        return timestamp.replace("T", " ")

    def _extract_flag(self, args: List[str], flag: str) -> Optional[str]:
        if flag not in args:
            return None
        index = args.index(flag)
        if index + 1 >= len(args):
            return None
        return args[index + 1]

    def _print_header(self, title: str) -> None:
        print("====================================")
        print(title)
        print("====================================")
        print("")

    def _print_footer(self) -> None:
        print("")
        print("====================================")

    def _print_usage(self) -> None:
        print("Usage:")
        print(
            '  python experiment_tracker.py init <experiment-name> [--description "..."]'
        )
        print(
            "  python experiment_tracker.py log <experiment-name> --config '{"
            "model"
            ": "
            "bert"
            ", "
            "lr"
            ": 0.001}'"
        )
        print(
            "  python experiment_tracker.py result <experiment-name> --metrics '{"
            "accuracy"
            ": 0.95}'"
        )
        print("  python experiment_tracker.py status [experiment-name]")
        print("  python experiment_tracker.py history <experiment-name>")


def main() -> None:
    tracker = ExperimentTracker()
    cli = ExperimentTrackerCLI(tracker)

    try:
        cli.run(sys.argv[1:])
    except Exception as error:
        print("====================================")
        print("EXPERIMENT TRACKER ERROR")
        print("====================================")
        print(str(error))


if __name__ == "__main__":
    main()
