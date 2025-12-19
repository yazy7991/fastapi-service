# This is a social media backend service

## ⚠ Development Notes & Troubleshooting
### Virtual Environment Activation (Windows)

#### Issue
While setting up the project, the Python virtual environment (venv) could not be activated when using the default Command Prompt shell. As a result, required dependencies (e.g., fastapi, uvicorn) were not available when running the application.

#### Cause
The activation command for a Python virtual environment depends on the shell being used. An incompatible shell or incorrect activation command will prevent the environment from activating correctly.

#### Solution
Switch to the appropriate shell environment and use the corresponding activation command:

- Command Prompt: `venv\Scripts\activate`


- Powershell: `.\venv\Scripts\Activate.ps1`

- GitBash/WSL: `source venv/Scripts/activate`

After activating the virtual environment correctly, all dependencies were resolved and the application ran as expected.

## 🌐 Networking Note: 0.0.0.0 vs 127.0.0.1

When running the FastAPI application with Uvicorn, the host parameter determines how the server is exposed:

- 127.0.0.1 (localhost)

    - Binds the server to the local loopback interface

    - Accessible only from the same machine

    - Recommended for standard local development

    - Does not typically trigger firewall warnings

- 0.0.0.0 (all interfaces)

    - Binds the server to all network interfaces on the machine (Wi-Fi, Ethernet, virtual adapters)

    - Allows access from other devices on the same local network (subject to firewall rules)

    - Commonly used for Docker, virtual machines, or LAN testing

    - May trigger operating system firewall prompts

### Note:
Binding to 0.0.0.0 does not automatically expose the application to the public internet. External access is still controlled by firewall settings and network configuration.