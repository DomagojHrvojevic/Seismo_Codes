#python biblioteka
import os
import subprocess

#prvo se lokalnim podacima ispisu nazivi velikim slovima i izbaci se .mseed nastavak
subprocess.run('./uppercase.sh /home/DATA',shell=True)

#podaci za spajanje na server
remote_host = "xxx.xx.xx.xx"
remote_user = "user"
remote_password = "password"
remote_port = 22
remote_data_folder = "/mnt/storage/podaci"

#postojeci podaci na serveru
remote_data_path = '/mnt/storage/podaci/2023/DN/DF01/HHZ.D'
scp_command = f"sshpass -p {remote_password} ssh -o StrictHostKeyChecking=no -p {remote_port} {remote_user}@{remote_host} ls {remote_data_path}"
scp_result = subprocess.run(scp_command, shell=True,capture_output=True, text=True)
output = scp_result.stdout
remote_list_files = output.split('\n')

#postojeci podaci lokalno
local_data_path = '/home/DATA'
data_files = os.listdir(local_data_path)

#brisanje lokalnih podataka koji postoje na serveru
for i in data_files:
    if i in remote_list_files:
        os.remove(local_data_path + '/' + i)
    
#rucno prebacvanje podataka na server zbog opreza