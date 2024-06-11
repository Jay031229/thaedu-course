import paramiko
import sys
import time

SERVER_FILE = "/Users/D073341/work/sre-cops/thaedu-course/linux/src/cloudserver/servers.txt"    # The file containing server details (IP, admin username, admin password)
USER_FILE = "/Users/D073341/work/sre-cops/thaedu-course/linux/src/cloudserver/user_pass.txt"    # The file containing new usernames and passwords

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

def read_users(file):
    users = []
    try:
        with open(file, 'r') as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split(',')
                    users.append((username, password))
        return users
    except FileNotFoundError:
        print(f"User file '{file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading user file: {e}")
        sys.exit(1)

def create_ssh_client(host, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password)
    return client

def run_interactive_command(ssh_client, command, password):
    try:
        channel = ssh_client.invoke_shell()
        time.sleep(1)

        if password:
            channel.send(f"echo {password} | sudo -S {command}\n")
        else:
            channel.send(f"sudo {command}\n")
        
        time.sleep(2)

        output = ""
        while channel.recv_ready():
            output += channel.recv(65535).decode('utf-8')
            time.sleep(1)

        return output
    except Exception as e:
        return f"Error running command: {e}"

def configure_sudoers(ssh_client, username, password):
    try:
        command = f'echo "{username} ALL=(ALL) NOPASSWD: /usr/sbin/useradd, /usr/sbin/chpasswd" | sudo tee /etc/sudoers.d/{username}_useradd'
        output = run_interactive_command(ssh_client, command, password)
        
        if "Error" not in output and "sudo: " not in output:
            return True, output, ""
        else:
            return False, "", output
    except Exception as e:
        print(f"Error configuring sudoers: {e}")
        return False, "", str(e)

def user_exists(ssh_client, username):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(f"id -u {username}")
        return stdout.channel.recv_exit_status() == 0
    except Exception as e:
        print(f"Error checking if user {username} exists: {e}")
        return False

def create_user(ssh_client, username, password):
    try:
        command = f"sudo useradd -m {username} && echo '{username}:{password}' | sudo chpasswd"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        
        stdout_str = stdout.read().decode()
        stderr_str = stderr.read().decode()

        if stdout.channel.recv_exit_status() == 0:
            return True, stdout_str, stderr_str
        else:
            return False, stdout_str, stderr_str
    except Exception as e:
        print(f"Error creating user {username}: {e}")
        return False, "", str(e)

def process_server(ip, admin_user, admin_password, users):
    ssh_client = None
    try:
        ssh_client = create_ssh_client(ip, admin_user, admin_password)
        
        # Configure sudoers to allow password-less execution
        print(f"Configuring sudoers on server: {ip}")
        success, stdout_str, stderr_str = configure_sudoers(ssh_client, admin_user, admin_password)
        if not success:
            print(f"Failed to configure sudoers on {ip}")
            print(f"STDOUT: {stdout_str}")
            print(f"STDERR: {stderr_str}")
            return
        
        for username, password in users:
            try:
                print(f"Checking user: {username} on server: {ip}")
                if user_exists(ssh_client, username):
                    print(f"User {username} already exists on {ip}")
                else:
                    print(f"Creating user: {username} on server: {ip}")
                    success, stdout_str, stderr_str = create_user(ssh_client, username, password)
                    if success:
                        print(f"User {username} created successfully on {ip}")
                    else:
                        print(f"Failed to create user {username} on {ip}")
                        print(f"STDOUT: {stdout_str}")
                        print(f"STDERR: {stderr_str}")
            except Exception as e:
                print(f"An error occurred with user {username} on server {ip}: {e}")
    except Exception as e:
        print(f"Failed to connect to server {ip}: {e}")
    finally:
        if ssh_client:
            ssh_client.close()

def main():
    servers = read_servers(SERVER_FILE)
    users = read_users(USER_FILE)
    
    for ip, admin_user, admin_password in servers:
        process_server(ip, admin_user, admin_password, users)

    print("Script completed.")

if __name__ == "__main__":
    main()