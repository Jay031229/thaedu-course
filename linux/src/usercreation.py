import paramiko
import sys

# Define variables
REMOTE_HOST = "192.168.2.134"  # Replace with the remote machine address
REMOTE_USER = "root"    # Replace with the remote machine user
PASSWORD = "Abcd@1234"          # Fixed password for new users
USER_FILE = "/Users/D073341/work/sre-cops/thaedu-course/linux/src/username.txt"    # The file containing usernames, one per line

def read_usernames(file):
    try:
        with open(file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Usernames file '{file}' not found!")
        sys.exit(1)

def create_ssh_client(host, user):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user)
    return client

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
        return stdout.channel.recv_exit_status() == 0
    except Exception as e:
        print(f"Error creating user {username}: {e}")
        return False

def main():
    usernames = read_usernames(USER_FILE)
    ssh_client = create_ssh_client(REMOTE_HOST, REMOTE_USER)
    
    for username in usernames:
        try:
            print(f"Checking user: {username}")
            if user_exists(ssh_client, username):
                print(f"User {username} already exists on {REMOTE_HOST}")
            else:
                print(f"Creating user: {username}")
                if create_user(ssh_client, username, PASSWORD):
                    print(f"User {username} created successfully on {REMOTE_HOST}")
                else:
                    print(f"Failed to create user {username} on {REMOTE_HOST}")
        except Exception as e:
            print(f"An error occurred with user {username}: {e}")
            continue

    ssh_client.close()
    print("Script completed.")

if __name__ == "__main__":
    main()
