import socket
import subprocess
import sys

ip = "127.0.0.1"
port = 3306


def check_port(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=3):
            print(f"Port {port} is OPEN on {ip}.")

            if sys.platform == "win32":
                result = subprocess.run(
                    ["netstat", "-ano", "-p", "tcp"],
                    capture_output=True,
                    text=True
                )

                found = False

                for line in result.stdout.splitlines():
                    parts = line.split()

                    if len(parts) >= 5:
                        local_address = parts[1]
                        state = parts[3]
                        pid = parts[4]

                        if (
                            local_address.endswith(f":{port}")
                            and state == "LISTENING"
                        ):
                            print(f"Status: LISTENING")
                            print(f"Process ID (PID): {pid}")

                            process = subprocess.run(
                                ["tasklist", "/FI", f"PID eq {pid}"],
                                capture_output=True,
                                text=True
                            )

                            print("Process information:")
                            print(process.stdout)
                            found = True

                if not found:
                    print("Could not identify the listening process.")

            else:
                print(
                    "To identify the process, run: "
                    f"lsof -nP -iTCP:{port} -sTCP:LISTEN"
                )

    except ConnectionRefusedError:
        print(f"Port {port} is CLOSED on {ip}.")

    except socket.timeout:
        print(f"Connection to port {port} TIMED OUT.")

    except OSError as error:
        print(f"Connection error: {error}")


check_port(ip, port)
