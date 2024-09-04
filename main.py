import json
import time
from datetime import datetime

import cert

# 最小剩余时间,最小剩余多少天了需要重新部署
_countdown = 1

if __name__ == '__main__':
    print("开始进行证书有效期校验")
    # 是否申请证书
    _apply = False
    # 是否部署证书
    _deploy = True
    # 获取证书ID,如果没获取到,或者证书的到期时间快到了,则要进行申请新的且部署
    certificate_id = cert.get_list()
    if certificate_id is None:
        _apply = True
    else:
        details = json.loads(cert.get_info(certificate_id))
        time_end = datetime.strptime(details["CertEndTime"], "%Y-%m-%d %H:%M:%S")
        time_diff = time_end - datetime.now()
        if time_diff.total_seconds() <= (_countdown * 86400):
            # 快到期了 重新申请后重新部署
            _apply = True
        else:
            # 还没到期呢 不用重复部署
            _deploy = False
    if _apply:
        print("申请证书")
        certificate_id = cert.create()
        while True:
            _cert = cert.get_info(certificate_id)
            # 如果证书申请下来了,则跳出死循环,进入下一步,进行证书部署
            if int(_cert["Status"]) == 1:
                break
            time.sleep(15)
    if _deploy:
        print("部署证书")
        b64 = json.loads(cert.download(certificate_id))["Content"]
        cert.push_server(b64)
    print("脚本执行结束")
