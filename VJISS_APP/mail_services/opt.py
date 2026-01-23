from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from django.core.cache import cache
from VJISS_APP.models import Create_User
from . import brevo_service   # 👈 correct usage


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

        if not Create_User.objects.filter(email=email).exists():
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

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

        sent = brevo_service.send_brevo_email(   # ✅ FIX
            to_email=email,
            subject=subject,
            html_content=html_content,
            cc_emails=None   # OTP must NOT use CC
        )

        if sent:
            return Response(
                {"message": "OTP sent successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Failed to send OTP. Try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
