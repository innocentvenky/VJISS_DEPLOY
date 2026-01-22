import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def send_brevo_email(
    to_email,
    subject,
    html_content,
    sender_email="no-reply@vjinnovative.co.in",
    sender_name="VJ Innovative Software Solutions Pvt Ltd",
    cc_emails=None,
):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = os.environ.get("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email_data = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={
            "email": sender_email,
            "name": sender_name
        },
        subject=subject,
        html_content=html_content,
        cc=[{"email": e} for e in (cc_emails or [])],

        # 🔑 THIS IS THE IMPORTANT PART
        tags=["otp", "transactional"],
        headers={
            "X-Mailin-custom": "transactional"
        },
    )

    try:
        api_instance.send_transac_email(email_data)
        return True

    except ApiException as e:
        print("BREVO EMAIL ERROR:", e)
        return False
