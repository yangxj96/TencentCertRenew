import dotenv
import paramiko

import helper

dotenv.load_dotenv()
_domain = helper.get_env_var("DOMAIN")
_remote_path_prefix = helper.get_env_var("UPLOAD_PATH_PREFIX")
_deploy_nginx_container = helper.get_env_var("DEPLOY_NGINX_CONTAINER")
_service_hostname = helper.get_env_var("SERVICE_HOSTNAME")
_service_port: int = int(helper.get_env_var("SERVICE_PORT"))
_service_username = helper.get_env_var("SERVICE_USERNAME")
_service_password = helper.get_env_var("SERVICE_PASSWORD")


def deploy_nginx(temp_dir):
    """
    Nginx部署方式的上传
    :param temp_dir: 临时文件夹对象
    """
    file_crt_path = temp_dir + "/Nginx/1_{}_bundle.crt".format(_domain)
    file_key_path = temp_dir + "/Nginx/2_{}.key".format(_domain)
    upload(file_crt_path, "{}{}_bundle.crt".format(_remote_path_prefix, _domain))
    upload(file_key_path, "{}{}.key".format(_remote_path_prefix, _domain))
    # 重启下Docker下的Nginx
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(_service_hostname, _service_port, _service_username, _service_password)
    ssh.exec_command("docker restart {}".format(_deploy_nginx_container))
    ssh.close()


def upload(local_path, remote_path):
    """
    文件上传到服务器
    :param local_path: 本地文件路径
    :param remote_path: 服务器文件路径
    :return:
    """
    ssh = paramiko.Transport(_service_hostname, _service_port)
    ssh.connect(username=_service_username, password=_service_password)
    sftp = paramiko.SFTPClient.from_transport(ssh)
    sftp.put(local_path, remote_path)
    ssh.close()
