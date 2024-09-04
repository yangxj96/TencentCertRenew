import base64
import json
import os
import tempfile
import zipfile
import deploy

from tencentcloud.common import credential
from tencentcloud.ssl.v20191205 import ssl_client, models


# 环境定义
_domain = os.environ.get("DOMAIN")
_tencnet_secret_id = os.environ.get("TENCENT_SECRET_ID")
_tencnet_secret_key = os.environ.get("TENCENT_SECRET_KEY")

_deploy_type = "nginx"

# 腾讯云sdk客户端
_client = ssl_client.SslClient(credential.Credential(_tencnet_secret_id, _tencnet_secret_key), 'ap-guangzhou')


def get_list():
    """
    获取SSL证书列表
    :return: 返回第一个状态为1的证书ID
    """
    request = models.DescribeCertificatesRequest()
    # 设置参数
    request.Offset = 0
    request.Limit = 1000
    request.SearchKey = _domain
    response = _client.DescribeCertificates(request)
    _certificates = json.loads(response.to_json_string())['Certificates']
    if _certificates is None:
        return None
    else:
        if type(_certificates) is list:
            for _item in _certificates:
                if _item["Status"] == "1":
                    return _item["CertificateId"]
        return None


def get_info(_certificate_id):
    """
    获取证书详情
    :param _certificate_id: 证书ID
    :return: 证书详情
    """
    request = models.DescribeCertificateRequest()
    request.CertificateId = _certificate_id
    response = _client.DescribeCertificate(request)
    return response.to_json_string()


def create():
    """
    申请证书
    :return: 证书ID
    """
    request = models.ApplyCertificateRequest()
    request.DvAuthMethod = "DNS_AUTO"
    request.DomainName = _domain
    request.DeleteDnsAutoRecord = True
    response = _client.ApplyCertificate(request)
    return json.loads(response.to_json_string())["CertificateId"]


def download(_certificate_id):
    """
    证书下载接口,获取证书zip文件的base64编码
    :param _certificate_id:
    :return:
    """
    request = models.DownloadCertificateRequest()
    request.CertificateId = _certificate_id
    response = _client.DownloadCertificate(request)
    return response.to_json_string()


def push_server(cert_zip_file_base64):
    """
    base64转文件且上传到服务器
    :param cert_zip_file_base64: 证书zip文件的base64格式
    :return:
    """
    data = base64.b64decode(cert_zip_file_base64)
    # 临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # base64解码后放到临时文件中
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(data)
            # 解压zip文件并且放到临时文件夹中
            with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        if _deploy_type == "nginx":
            deploy.deploy_nginx(temp_dir)
