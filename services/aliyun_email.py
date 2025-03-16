# -*- coding: utf-8 -*-
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from config import ALIYUN_DM_CONFIG

class AliyunEmailService:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dm20151123Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=ALIYUN_DM_CONFIG['access_key_id'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=ALIYUN_DM_CONFIG['access_key_secret'],
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dm
        config.endpoint = f'dm.aliyuncs.com'
        return Dm20151123Client(config)

    @staticmethod
    def single_send_mail(
        recipient_email: str,
        subject: str,
        html_body: str
    ) -> None:
        client = AliyunEmailService.create_client()
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name=ALIYUN_DM_CONFIG['account_name'],
            address_type=ALIYUN_DM_CONFIG['address_type'],
            tag_name=ALIYUN_DM_CONFIG['tag_name'],
            reply_to_address=True,
            to_address=recipient_email,
            subject=subject,
            html_body=html_body,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.single_send_mail_with_options(single_send_mail_request, runtime)
            return True
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            return False
