from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import os
from django.core.cache import cache
from VJISS_APP.models import Create_User

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


class SendOtp(APIView):

    def generate_otp(self, length=6):
        return "".join(str(random.randint(0, 9)) for _ in range(length))

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = Create_User.objects.filter(email=email).exists()
        print(user, email)

        otp = self.generate_otp()

        # Store OTP for 5 minutes
        cache_key = f"otp_{email}"
        cache.set(cache_key, otp, timeout=300)

        subject = "🔐 OTP Verification Code"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>OTP Verification</h2>

            <p>Your verification code is:</p>

            <div style="
                font-size: 40px;
                font-weight: bold;
                letter-spacing: 8px;
                color: #1e90ff;
                background-color: #f0f6ff;
                padding: 18px 28px;
                border-radius: 8px;
                display: inline-block;
            ">
                {otp}
            </div>

            <p style="margin-top: 20px;">
                This OTP is valid for <b>5 minutes</b>.
                Do not share this OTP with anyone.
            </p>

            <p>If this request was not made by you, please ignore this email.</p>

            <p>Regards,<br><b>Support Team</b></p>
        </body>
        </html>
        """

        # Brevo API config
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = os.environ.get("BREVO_API_KEY")

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        email_data = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            sender={
                "email": "no-reply@vjinnovative.co.in",
                "name": "VJ Innovative Software Solutions Pvt Ltd"
            },
            subject=subject,
            html_content=html_content,
             tags=["otp", "transactional"],
             headers={
            "X-Mailin-custom": "transactional"
    }
        )

        try:
            api_instance.send_transac_email(email_data)
            return Response(
                {"message": "OTP sent successfully"},
                status=status.HTTP_200_OK
            )

        except ApiException as e:
            print("BREVO API ERROR:", e)
            return Response(
                {"error": "Failed to send OTP. Try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
