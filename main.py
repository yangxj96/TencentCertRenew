import json
import os
import time
import cert
import dotenv
from datetime import datetime

dotenv.load_dotenv()
# 最小剩余时间,最小剩余多少天了需要重新部署
_countdown: int = int(os.getenv("COUNTDOWN", 1))

if __name__ == '__main__':
    print("开始进行证书有效期校验")
    # 是否申请证书
    _apply = False
    # 是否部署证书
    _deploy = False
    # 获取证书ID,如果没获取到,或者证书的到期时间快到了,则要进行申请新的且部署
    certificate_id = cert.get_list()
    if certificate_id is None:
        print("找不到相关证书ID,进行重新申请")
        _apply = True
    else:
        details = json.loads(cert.get_info(certificate_id))
        time_end = datetime.strptime(details["CertEndTime"], "%Y-%m-%d %H:%M:%S")
        time_diff = time_end - datetime.now()
        seconds = time_diff.total_seconds()
        print(f"剩余时间:{time.strftime('%d天%H时%M分%S秒', time.gmtime(seconds))}")
        if time_diff.total_seconds() <= (_countdown * 86400):
            _apply = True
            _deploy = True
            print("快到期了 重新申请后重新部署")
        else:
            print("还没到期呢 不用重复部署")
    if _apply:
        print("申请证书")
        certificate_id = cert.create()
        while True:
            _cert = json.loads(cert.get_info(certificate_id))
            _status = int(_cert["Status"])
            _msg = _cert["StatusMsg"]
            if _status != 0 and _status != 1:
                print(f"证书审核状态异常,请控制台查看具体情况,状态码:${_status},具体消息:${_msg}")
                exit(-1)
            if _status == 0:
                print("证书审核中,请等待...")
            # 如果证书申请下来了,则跳出死循环,进入下一步,进行证书部署
            if _status == 1:
                print(f"验证通过,证书ID:${certificate_id}")
                break
            time.sleep(5)

    if _deploy:
        print("部署证书")
        b64 = json.loads(cert.download(certificate_id))["Content"]
        cert.push_server(b64)
    print("脚本执行结束")
