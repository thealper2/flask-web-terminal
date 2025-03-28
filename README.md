# Web-based Terminal Emulator

Flask application for web-based terminal emulator. Manages WebSocket connections and command execution.

## :dart: Features

1. **Secure Command Execution**:
  - Whitelist of allowed commands
  - Blacklist of dangerous commands
  - Command auditing/logging
2. **Real-time Communication**:
  - WebSocket-based terminal I/O
  - Immediate output streaming
  - Support for interactive commands
3. **Terminal UI**:
  - xterm.js for realistic terminal emulation
  - Dark theme with proper ANSI color support
  - Command history with arrow keys
  - System stats in status bar
4. **Security**:
  - Authentication requirement
  - Input validation
  - Command restrictions
  - Audit logging
5. **Performance**:
  - Efficient WebSocket communication
  - System resource monitoring
  - Responsive design

## :hammer_and_wrench: Installation

1. Clone the repository:

```bash
git clone https://github.com/thealper2/flask-web-terminal.git
cd flask-web-terminal
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Start the development server:

```bash
python main.py
```

Then open your browser to:

```bash
http://localhost:5000
```

## :handshake: Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature (git checkout -b feature/your-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Create a new Pull Request

## :scroll: License

This project is licensed under the MIT License - see the LICENSE file for details.