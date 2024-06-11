import paramiko
import time
import sys

SERVER_FILE = "/Users/D073341/work/sre-cops/thaedu-course/linux/src/cloudserver/servers.txt"    # The file containing server details (IP, username, password)
NEW_PASSWORD = "Thalassa@1234" # New password after first login

def read_servers(file):
    servers = []
    try:
        with open(file, 'r') as f:
            for line in f:
                if line.strip():
                    ip, user, password = line.strip().split(',')
                    servers.append((ip, user, password))
        return servers
    except FileNotFoundError:
        print(f"Servers file '{file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading servers file: {e}")
        sys.exit(1)

def create_ssh_client(host, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password)
    return client

def change_password_interactive(ip, username, current_password, new_password):
    try:
        ssh_client = create_ssh_client(ip, username, current_password)
        channel = ssh_client.invoke_shell()

        def send_and_receive(channel, command, wait_time=1):
            time.sleep(wait_time)
            channel.send(command + '\n')
            time.sleep(wait_time)
            output = channel.recv(65535).decode('utf-8')
            print(output)
            return output

        # Handle host key verification prompt
        output = send_and_receive(channel, 'yes', wait_time=2)

        # Send current password
        if 'password:' in output.lower():
            output = send_and_receive(channel, current_password)

        # Handle password change prompt
        if 'required to change your password' in output.lower():
            output = send_and_receive(channel, current_password)
            if 'current password' in output.lower():
                output = send_and_receive(channel, current_password)
            if 'new password' in output.lower():
                output = send_and_receive(channel, new_password)
            if 'retype new password' in output.lower():
                output = send_and_receive(channel, new_password)

        ssh_client.close()
        if 'password updated successfully' in output.lower():
            return True, output, ""
        else:
            return False, output, ""
    except Exception as e:
        return False, "", str(e)

def process_server(ip, user, password):
    try:
        print(f"Changing password for user: {user} on server: {ip}")
        success, stdout_str, stderr_str = change_password_interactive(ip, user, password, NEW_PASSWORD)
        if success:
            print(f"Password for user {user} changed successfully on {ip}")
        else:
            print(f"Failed to change password for user {user} on {ip}")
            print(f"STDOUT: {stdout_str}")
            print(f"STDERR: {stderr_str}")
    except Exception as e:
        print(f"Failed to connect to server {ip}: {e}")

def main():
    servers = read_servers(SERVER_FILE)
    
    for ip, user, password in servers:
        process_server(ip, user, password)

    print("Script completed.")

if __name__ == "__main__":
    main()
