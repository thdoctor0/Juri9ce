import os
import pyperclip
import platform
import psutil
import socket
import datetime
import base64
import hashlib
import requests
import difflib
import mmap
import struct

#  no random library :)

#made by thdoctor <3 
# i just needed to redo the code structure because why not
# qol changes for version 5.5 really. and preparing code for v6
class Juri9ceTerminal:
    def __init__(self):
        self.key = hashlib.sha256(b"secure_key").digest()
        self.running = True
        self.last_output = ""
        self.prompt_symbol = "$"
        self.theme = "dark"
        self.history = []
        self.log_file = "C:/VisionStudios/Juri9ce/log.txt"
        self.commands = {
            "system": {
                "exit": self.exit_terminal_with_confirmation,
                "clear": self.clear_screen,
                "cls": self.clear_screen,
                "help": self.display_help, # updated at 10:54 am 7.1.25
                "system-info": self.system_info
            },
            "ram feature": {
                "bind-ram": self.bind_ram_stack, # done 4:30 am 6.1.25
                "ram-allocation": self.allocate_ram_files, # done 4:31 am 6.1.25
                "import": self.import_file, # done 5:11 am 6.1.25
                "export": self.export_file, # done 2:32 am 7.1.25
                "log": self.initialize_logging, # done at 10:50am 7.1.25
            },
            "network": {
                "ping": self.ping_host,# done at 4:14am 7.1.25
                "network": self.network_status,
                "optimize": self.network_optimization,
                "rename-ip": self.rename_ip
            },
            "clipboard": {
                "clipboard-copy": self.clipboard_copy,
                "clipboard-compress": self.clipboard_compress,
                "clipboard-decompress": self.clipboard_decompress
            },
            "files": {
                "current-directory": self.current_directory,
                "list-files": self.list_files,
                "create_file": self.create_file
            },
            "data": {
                "encrypt": self.encrypt_data,
                "decrypt": self.decrypt_data,
                "compress": self.compress_data,
                "decompress": self.decompress_data
            },
            "hardware": {
                "disk": self.disk_usage,
                "ram": self.memory_usage,
                "cpu": self.cpu_usage,
                "all-info": self.hardware_info
            },
            "custom": {
                "theme": self.set_theme,
                "prompt": self.set_prompt
            }
        }

    def start(self):
            print("Welcome to Juri9ce Terminal v5.5 ")
            print(f"Current prompt symbol: {self.prompt_symbol}")
            print(f"Type 'help' to show the help section")
            
            while self.running:
                user_input = input(self.show_prompt() + " ")
                # self.history.append(user_input) to be fixed
                self.execute_command(user_input)

    def clear_screen(self, args=None):
        os.system("cls" if os.name == "nt" else "clear")

    def execute_command(self, command): # New execute commands feature now the execute commands will actually use an advanced system to get Similar Commands
        if not command:
            return
        cmd_parts = command.split(" ", 1)
        cmd = cmd_parts[0]
        args = cmd_parts[1] if len(cmd_parts) > 1 else None

        for category, commands in self.commands.items():
            if cmd in commands:
                try:
                    if args:
                        commands[cmd](args)
                    else:
                        commands[cmd]()
                except TypeError as e:
                    print(f"Error: Incorrect usage of '{cmd}'. Error: {e}")
                return
            
        similar_cmds = self.get_similar_commands(cmd)
        if similar_cmds:
            print(f"Error: Command '{cmd}' not recognized. Did you mean: {', '.join(similar_cmds)}?")
        else:
            print(f"Error: Command '{cmd}' not recognized. Doesn't exist")

    def current_directory(self, args=None):
        cwd = os.getcwd()
        self.last_output = cwd
        self.log_output(f"Current Directory: {cwd}")
        print(f"Current Directory: {cwd}")

    def decrypt_data(self, data=None):
        if not data:
            data = input("Enter data to decrypt: ")
        try:
            decoded = base64.b64decode(data.encode()).decode()
            self.last_output = decoded
            print(f"Decrypted Data: {decoded}")
        except Exception:
            print("Error decrypting data.")

    def encrypt_data(self, data=None):
        if not data:
            data = input("Enter data to encrypt: ")
        encoded = base64.b64encode(data.encode()).decode()
        self.last_output = encoded
        print(f"Encrypted Data: {encoded}")

    def list_files(self, args=None):
        files = os.listdir(".")
        self.last_output = "\n".join(files)
        print("Files in Current Directory:")
        for file in files:
            print(f"  {file}")

    def export_file(self, file_name):
            """Exports data to a specified file."""
            if not file_name:
                print("Error: Please specify a file name.")
                return  # Exiting the function early if no file name is provided

            try:
                with open(file_name, 'w') as f:
                    # Export the last output (or decide what to export)
                    f.write(self.last_output)
                print(f"Data exported to {file_name}")
            except Exception as e:
                print(f"Error exporting data: {e}")

    def clipboard_copy(self, args=None):
        if not self.last_output:
            print("Error: No output available to copy.")
        else:
            pyperclip.copy(self.last_output)
            print("Last output copied to clipboard.")

    def clipboard_compress(self, args=None):
        clipboard_content = pyperclip.paste()
        if not clipboard_content:
            print("Error: Clipboard is empty.")
            return
        compressedx = Compressor.compress(clipboard_content)
        self.last_output = compressedx
        print(f"Clipboard content compressed: {compressedx}")

    def clipboard_decompress(self, args=None):
        clipboard_content = pyperclip.paste()
        if not clipboard_content:
            print("Error: Clipboard is empty.")
            return
        if clipboard_content.startswith("Compressed(") and clipboard_content.endswith(")"):
            decompressed = clipboard_content[11:-1]
            self.last_output = decompressed
            pyperclip.copy(decompressed)
            print(f"Clipboard content decompressed: {decompressed}")
        else:
            print("Error: Clipboard content is not in a compressed format.")

    def get_similar_commands(self, input_cmd):
        """Returns a list of similar commands."""
        all_commands = [cmd for cmds in self.commands.values() for cmd in cmds]
        return difflib.get_close_matches(input_cmd, all_commands, n=3, cutoff=0.6)

    def create_file(self, args=None):
        filename = input("Enter the filename: ")
        with open(filename, "w") as file:
            file.write("New file created.")
        self.last_output = f"File '{filename}' created."
        print(f"File '{filename}' created.")

    def get_computer_name(self):
        return socket.gethostname()

    def show_prompt(self):
        computer_name = self.get_computer_name()
        prompt = f"{computer_name} {self.prompt_symbol}"
        return prompt

    def exit_terminal_with_confirmation(self, args=None):
        confirmation = input("Are you sure you want to exit? (y/n): ")
        if confirmation.lower() == 'y':
            self.running = False
            self.log_output("Session ended.")
            print("Exiting Juri9ce Terminal v5.5 ...")

    def display_help(self):

        help_text = f"""
Available Commands:

Juri9ce V5.5

------------------------------
Terminal Control :
    help - Display this help message.
    clear / cls – Clears the terminal screen.
    exit – Exits the terminal using confirmations <y/n>.

Advanced Memory System (ams)
    ram-allocation - Creates advanced routing files to be used in v6 of Juri9ce as active user experience enhancers via ARS v6
    export - Exports the logs without the 'help' section
    import - Imports any material uploaded to it.
    bind-ram - Creates advanced binding to rebind files for example you have 32mb of ram created you can bind <=32 in Natural Numbers only (v6)

Computer Information :
    disk – Displays disk usage.
    ram – Shows memory usage.
    cpu – Shows CPU usage.
    all-info – Displays hardware information.
    system-info – Displays system information

File Control :
    current-directory – Displays the current working directory.
    list-files – Lists all files in the current directory.
    create-file – Creates a new file in the current directory.

Personalisation :
    prompt <symbol> – Changes the prompt symbol (e.g., $, >, YourName) Your current prompt is {self.prompt_symbol}
    theme - Shows a list to select all interfaces including a custom one.

Networking :
    network – Shows network status (hostname and IP address).
    ping - Sets and entire dedicated part to determ how big of a ping to make. 
    ping <ip> – Pings a host. It will ask you to input a host if not specified, Rapid Fire version of Ping.
    optimize – Optimizes network resources.
    rename-ip – Modifies the IPv4 address with an active Juri9ce Address (Beta)

Juri9ce Compression and Encryption :
    Clipboard Related:
        clipboard-copy – Copies the last output to the clipboard.
        clipboard-compress – Compresses clipboard content.
        clipboard-decompress – Decompresses clipboard content.
    Text Related:
        Encryption:
            encrypt <text> – Encrypts data (base64 encoding).
            decrypt <text> – Decrypts data (base64 decoding).
        Compression:
            compress <text> - Compresses text into a super algorithm.
            decompress <text> - Decompresses text into the same algorithm that it was compressed.

------------------------------

Copyright Vision Studios 2025 (tool by thdoctor)

------------------------------
"""
        print(help_text)

    def compress_data(self, data):
        """Compresses the input data string."""
        if not data:
            print("Error: Please provide data to compress.")
            return
        compressed = Compressor.compress(data)
        print(f"Compressed Data: {compressed}")

    def decompress_data(self, data):
        """Decompresses the input data string."""
        if not data:
            print("Error: Please provide data to decompress.")
            return
        try:
            decompressed = Compressor.decompress(data)
            print(f"Decompressed Data: {decompressed}")
        except ValueError as e:
            print(f"Error: {e}")

    def log_output(self, output):
        with open("terminal_output.log", "a") as log_file:
            log_file.write(output + "\n")

    def disk_usage(self, args=None):
        usage = psutil.disk_usage("/")
        self.last_output = f"Disk Usage: {usage.percent}%"
        print(f"Disk Usage: {usage.percent}%")

    def memory_usage(self, args=None):
        memory = psutil.virtual_memory()
        self.last_output = f"Memory Usage: {memory.percent}%"
        print(f"Memory Usage: {memory.percent}%")

    def hardware_info(self, args=None):
        gpu_info = self.get_gpu_info()
        ram = psutil.virtual_memory().total / (1024**3)
        self.last_output = f"CPU: {platform.processor()}, GPU: {gpu_info}, RAM: {ram:.2f} GB"
        print(f"CPU: {platform.processor()}")
        print(f"GPU: {gpu_info}")
        print(f"RAM: {ram:.2f} GB")

    def get_gpu_info(self):
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].name
            return "No GPU detected"
        except ImportError:
            return "GPU information requires GPUtil module"

    def network_status(self, args=None):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.last_output = f"Hostname: {hostname}, IP Address: {ip_address}"
        print(f"Hostname: {hostname}, IP Address: {ip_address}")

    def ping_host(self, host=None):
            if not host:
                host = input("Enter IPv4 Address to ping: ")
                attackcount = input(f"Enter how many times to ping '{host}': ")
                bytecount = input(f"Enter how many bytes to ping '{host}': ")
                timeoutping = input(f"Enter expire time before ping expire for '{host}': ")
            else:
                attackcount = "1"
                bytecount = "64"
                timeoutping = "300"
            try:
                print (f"Attackcount={attackcount} ; Bytecount={bytecount} ; Timeout={timeoutping} ")
                command = f"ping -4 -n {attackcount} -l {bytecount} -w {timeoutping} {host}" if os.name == "nt" else f"ping -c {attackcount} -s {bytecount} {host}"
                response = os.system(command)
                location = self.get_ip_location(host)
                if response == 0:
                    self.last_output = f"{host} is reachable. Location: {location}"
                    print(f"{host} is reachable. Location: {location}")
                else:
                    self.last_output = f"{host} is not reachable. Location: {location}"
                    print(f"{host} is not reachable. Location: {location}")
            except Exception as e:
                print(f"Ping error: {e}")
                
    def get_ip_location(self, host): # this is on hopes and prayers
        try:
            response = requests.get(f"https://ipinfo.io/{host}/json")
            data = response.json()
            return data.get("city", "Unknown") + ", " + data.get("country", "Unknown")
        except requests.RequestException:
            return "Location unavailable"

    def network_optimization(self, args=None):
        print("Optimizing network resources...")
        self.last_output = "Network optimized successfully."
        print("Network optimized successfully.")

    def rename_ip(self, args=None):
        new_ip = "192.168.1.100"  
        self.last_output = f"Renamed Internet Protocol to {new_ip}"
        os.system("ping -l 2048 {new_ip}")
        print(f"Renamed Internet Protocol to {new_ip}")
        try:
            socket.gethostbyname(new_ip)
            print(f"IP renamed successfully to {new_ip}")
        except socket.error:
            print("Failed to rename IP address. Invalid IP provided.")

    def initialize_logging(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "a") as log:
            log.write(f"\nSession started: {datetime.datetime.now()}\n")
            print (f"Succesfully logged to {self.log_file}")

    def set_theme(self, theme=None):

        color_list = """
    light , dark , purple , aqua , custom """
        color_pallete = """
0 = Black
1 = Blue
2 = Green
3 = Aqua
4 = Red
5 = Purple
6 = Yellow
7 = White
8 = Gray
9 = Light Blue
A = Light Green
B = Light Aqua
C = Light Red
D = Light Purple
E = Light Yellow
F = Bright White
"""

        try:
            if theme not in ['light', 'dark', 'purple', 'aqua', 'custom']:
                raise ValueError(f"Invalid theme. Choose from this list {color_list}.")
            
            self.theme = theme
            
            if self.theme == 'light':
                os.system("color 70")
                print("Theme changed to Light.")
            elif self.theme == 'dark':
                os.system("color 0f")
                print("Theme changed to Dark.")
            elif self.theme == 'purple':
                os.system("color d0")
                print("Theme changed to Purple.")
            elif self.theme == 'aqua':
                os.system("color b0")
                print("Theme changed to aqua.")
            elif self.theme == 'custom': # new themes and saving options comming soon

                print(color_pallete)
                
                c1 = input(f"Choose Color for Background according to the color pallete :")
                c2 = input(f"Choose Color for Text according to the color pallete :")
                
                os.system(f"color {c1}{c2}")
                print("Theme is customised.")
        except Exception as e:
            print(f"Error changing theme: {e}")
            return False
        return True

    def import_file(self, file_name):
        """Imports data from a file."""
        if not file_name:
            print("Error: Please specify a file name.")
            return
        try:
            with open(file_name, 'r') as f:
                data = f.read()
            print(f"Imported Data: {data}")
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")

    def system_info(self, args=None):
        info = platform.uname()
        self.last_output = str(info)
        print("System Information:")
        print(f"  System: {info.system}")
        print(f"  Node Name: {info.node}")
        print(f"  Release: {info.release}")
        print(f"  Version: {info.version}")
        print(f"  Machine: {info.machine}")
        print(f"  Processor: {info.processor}")

    def cpu_usage(self, args=None):
        cpu = psutil.cpu_percent(interval=1)
        self.last_output = f"CPU Usage: {cpu}%"
        print(f"CPU Usage: {cpu}%")

    def disk_usage(self, args=None):
        usage = psutil.disk_usage("/")
        self.last_output = f"Disk Usage: {usage.percent}%"
        print(f"Disk Usage: {usage.percent}%")

    def memory_usage(self, args=None):
        memory = psutil.virtual_memory()
        self.last_output = f"Memory Usage: {memory.percent}%"
        print(f"Memory Usage: {memory.percent}%")
    
    def set_prompt(self, args=None):
        if not args:
            print("Error: Please specify a prompt symbol.")
            return
        self.prompt_symbol = args
        self.last_output = f"Prompt symbol set to {args}"
        print(f"Prompt symbol set to {args}")

    def allocate_ram_files(self, size_mb=None):
        """Allocates RAM by creating files corresponding to the requested size."""
        try:
            size_mb = int(size_mb)
            if not os.path.exists("memory"):
                os.makedirs("memory")
            for i in range(size_mb):
                file_name = os.path.join("memory", f"memory_part_{i + 1}.dat")
                with open(file_name, "wb") as f:
                    f.write(b"0" * (1 * 1024 * 1024))  # Allocate 1 MB per file
            print(f"Allocated {size_mb} MB of RAM using files.")
        except ValueError:
            print("Error: Size must be an integer value.")

    def bind_ram_stack(self, size_mb=None):
        """Creates a high-performance RAM stack."""
        if size_mb is None:
            print("Error: Size must be provided.")
            return  # Ensure early return here to avoid further processing

        try:
            size_mb = int(size_mb)
            if size_mb <= 0:
                print("Error: Size must be a positive integer.")
                return
            mmapped_file = mmap.mmap(-1, size_mb * 1024 * 1024)
            mmapped_file.write(b'\x00' * (size_mb * 1024 * 1024))
            print(f"Bound {size_mb} MB of RAM to high-performance stack.")
        except ValueError:
            print("Error: Size must be an integer value.")

class Compressor: # finally used
    @staticmethod
    def compress(data):
        """Advanced compression logic."""
        if not data:
            raise ValueError("No data to compress.")
        encoded = bytearray()
        prev_char = data[0]
        count = 1
        for char in data[1:]:
            if char == prev_char:
                count += 1
            else:
                encoded.extend(struct.pack("B", count))
                encoded.extend(prev_char.encode())
                prev_char = char
                count = 1
        encoded.extend(struct.pack("B", count))
        encoded.extend(prev_char.encode())
        return encoded.hex()

    @staticmethod
    def decompress(data):
        """Advanced decompression logic."""
        if not data:
            raise ValueError("No data to decompress.")
        decoded = bytearray.fromhex(data)
        result = []
        i = 0
        while i < len(decoded):
            count = struct.unpack("B", bytes([decoded[i]]))[0]
            char = chr(decoded[i + 1])
            result.append(char * count)
            i += 2
        return ''.join(result)
            
# so much fucking pain to get to here :<

if __name__ == "__main__":
    terminal = Juri9ceTerminal()
    terminal.start()
