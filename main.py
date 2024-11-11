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
        seconds = int(time_diff.total_seconds())
        print("剩余时间:{}秒".format(seconds))
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
            _cert = cert.get_info(certificate_id)
            # 如果证书申请下来了,则跳出死循环,进入下一步,进行证书部署
            if int(_cert["Status"]) == 1:
                break
            time.sleep(5 * 1000)
    if _deploy:
        print("部署证书")
        b64 = json.loads(cert.download(certificate_id))["Content"]
        cert.push_server(b64)
    print("脚本执行结束")
