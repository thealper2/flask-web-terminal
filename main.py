from typing import Dict

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

from terminal import TerminalHandler


class WebTerminalApp:
    """
    Main Flask application for web-based terminal emulator.
    Manages WebSocket connections and command execution.
    """

    def __init__(self):
        self.app = Flask(__name__)

        # CORS and SocketIO configuration
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.socketio = SocketIO(
            self.app, cors_allowed_origins="*", logger=True, engineio_logger=True
        )

        self.terminal_handler = TerminalHandler()
        self.register_routes()
        self.register_socket_events()

    def register_routes(self):
        """
        Define application routes.
        """

        @self.app.route("/")
        def index():
            return render_template("index.html")

    def register_socket_events(self):
        """
        Set up WebSocket event handlers.
        """

        @self.socketio.on("execute_command")
        def handle_command(data: Dict[str, str]):
            print("Received command:", data)

            command = data.get("command", "")
            result = self.terminal_handler.execute_command(command)

            if result["status"] == "success":

                def stream_output():
                    try:
                        for line in result["output_generator"]:
                            self.socketio.emit("command_output", {"output": line})
                    except Exception as e:
                        self.socketio.emit("command_error", {"message": str(e)})

                self.socketio.start_background_task(stream_output)
            else:
                self.socketio.emit("command_error", result)

        @self.socketio.on("get_resources")
        def handle_resources():
            resources = self.terminal_handler.get_system_resources()
            self.socketio.emit("system_resources", resources)

    def run(self, debug: bool = True):
        """
        Start the Flask application.

        Args:
            debug (bool): Enable debug mode
        """
        self.socketio.run(self.app, host="0.0.0.0", port=5000, debug=debug)

if __name__ == "__main__":
    web_terminal = WebTerminalApp()
    web_terminal.run(debug=True)
