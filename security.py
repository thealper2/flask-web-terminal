import logging
import re
from typing import Optional


class CommandSecurity:
    """
    Manages security checks for terminal commands.
    Provides methods to validate and filter potentially dangerous commands.
    """

    BLOCKED_COMMANDS = [
        "sudo",
        "rm",
        "reboot",
        "shutdown",
        "poweroff",
        "mkfs",
        "dd",
        "kill",
        "exec",
        "eval",
        "wget",
        "curl --upload-file",
        "nc",
        "telnet",
    ]

    ALLOWED_PREFIXES = [
        "ls",
        "cat",
        "echo",
        "pwd",
        "whoami",
        "date",
        "cal",
        "top",
        "ps",
        "ping",
        "grep",
        "awk",
        "sed",
        "head",
        "tail",
    ]

    @classmethod
    def sanitize_command(cls, command: str) -> Optional[str]:
        """
        Sanitize and validate the command.

        Args:
            command (str): Command to sanitize

        Returns:
            Optional[str]: Sanitized command or None if unsafe
        """
        command = command.strip()

        # Check for blocked commands
        if any(blocked in command for blocked in cls.BLOCKED_COMMANDS):
            logging.warning(f"Blocked potentially dangerous command: {command}")
            return None

        # Enforce allowed command prefixes
        if not any(command.startswith(prefix) for prefix in cls.ALLOWED_PREFIXES):
            logging.warning(f"Unauthorized command prefix: {command}")
            return None

        # Remove potential shell injection characters
        command = re.sub(r"[;&|`]", "", command)

        return command


def log_command(command: str, status: str = "executed") -> None:
    """
    Log executed commands for audit purposes.

    Args:
        command (str): Command executed
        status (str): Status of command execution
    """
    logging.basicConfig(
        filename="terminal_audit.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )
    logging.info(f"Command: {command} - Status: {status}")
