import shlex
import subprocess
from typing import Any, Dict, Generator

import psutil

from security import CommandSecurity, log_command


class TerminalHandler:
    """
    Manages command execution and system resource monitoring.
    Provides secure and efficient command processing.
    """

    @staticmethod
    def execute_command(command: str) -> Dict[str, Any]:
        """
        Execute a shell command with enhanced security and output handling.

        Args:
            command (str): Command to execute

        Returns:
            Dict[str, Any]: Dict containing execution status and output
        """
        # Sanitize command
        safe_command = CommandSecurity.sanitize_command(command)

        if not safe_command:
            return {"status": "error", "message": "Unsafe or blocked command"}

        log_command(safe_command)

        try:
            # Use shlex to handle command arguments safely
            process = subprocess.Popen(
                shlex.split(safe_command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
                close_fds=True,
            )

            def output_generator(proc) -> Generator[str, None, None]:
                """
                Generator to stream command output
                """
                for line in proc.stdout:
                    yield line.strip()

                for line in proc.stderr:
                    yield line.strip()

                proc.wait()

            return {
                "status": "success",
                "pid": process.pid,
                "output_generator": output_generator(process),
            }

        except Exception as e:
            log_command(safe_command, f"Error: {str(e)}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_system_resources() -> Dict[str, float]:
        """
        Retrieve current system resource usage.

        Returns:
            Dict[str, float]: Dict with CPU and RAM usage percentages
        """
        return {
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory().percent,
        }
