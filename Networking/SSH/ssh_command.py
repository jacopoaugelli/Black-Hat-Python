import paramiko
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('[*] Output:')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    try:
        import getpass
# user = getpass.getuser()
        user = input('Username: ')
        password = getpass.getpass()
        ip = input('Server IP: ')
        port = input('Port: ')
        cmd = input('Command: ') or 'id'
        ssh_command(ip, port, user, password, cmd)
    except KeyboardInterrupt:
        print("\n[!] Process terminated by user")
    except Exception as e:
        print("[!!] An error occured:\n", e)