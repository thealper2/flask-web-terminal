document.addEventListener('DOMContentLoaded', () => {
    // Socket.IO connection
    const socket = io({
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000
    });

    const terminalEl = document.getElementById('terminal');
    const commandInput = document.getElementById('command-input');
    const executeBtn = document.getElementById('execute-btn');
    const cpuUsage = document.getElementById('cpu-usage');
    const ramUsage = document.getElementById('ram-usage');

    // xterm.js setup
    const term = new Terminal({
        cursorBlink: true,
        theme: {
            background: '#121212',
            foreground: '#00ff00'
        }
    });
    term.open(terminalEl);

    // Command execution function
    function executeCommand() {
        const command = commandInput.value.trim();
        if (command === '') return;

        console.log('Executing command:', command);
        term.writeln(`\x1b[1;33m$ ${command}\x1b[0m`);

        socket.emit('execute_command', { command }, (response) => {
            console.log('Server response:', response);
        });

        commandInput.value = '';
    }

    // Connecting event listeners
    executeBtn.addEventListener('click', executeCommand);
    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') executeCommand();
    });

    // Output and error event handlers
    socket.on('command_output', (data) => {
        console.log('Received output:', data);
        if (data.output) {
            term.writeln(data.output);
        }
    });

    socket.on('command_error', (error) => {
        console.error('Command error:', error);
        term.writeln(`\x1b[1;31mError: ${error.message || 'Unknown error'}\x1b[0m`);
    });

    // Connection status event listeners
    socket.on('connect', () => {
        console.log('Connected to WebSocket');
        term.writeln('\x1b[1;32mWebSocket Connected\x1b[0m');
    });

    socket.on('connect_error', (error) => {
        console.error('Connection Error:', error);
        term.writeln(`\x1b[1;31mConnection Error: ${error}\x1b[0m`);
    });

    // Periodically update system resources
    function updateSystemResources() {
        socket.emit('get_resources');
    }

    socket.on('system_resources', (resources) => {
        cpuUsage.textContent = `CPU: ${resources.cpu_usage}%`;
        ramUsage.textContent = `RAM: ${resources.ram_usage}%`;
    });

    // Update resource information every 5 seconds
    setInterval(updateSystemResources, 5000);
});