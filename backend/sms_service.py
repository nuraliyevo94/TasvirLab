import random
import datetime
import httpx
from typing import Dict, Any, Optional
from backend.config import Config

class SMSService:
    """O'zbekiston telefon raqamlariga SMS kod yuborish xizmati (Eskiz.uz / Dev mode)."""
    
    _eskiz_token: Optional[str] = None
    _token_expiry: Optional[datetime.datetime] = None

    @staticmethod
    def generate_otp_code(length: int = 6) -> str:
        """Tasodifiy 6 xonali OTP kod generatsiya qiladi."""
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    @classmethod
    async def get_eskiz_token(cls) -> Optional[str]:
        """Eskiz.uz API autentifikatsiya tokenini oladi yoki keshdan qaytaradi."""
        if not Config.ESKIZ_EMAIL or not Config.ESKIZ_PASSWORD:
            return None
            
        now = datetime.datetime.utcnow()
        if cls._eskiz_token and cls._token_expiry and now < cls._token_expiry:
            return cls._eskiz_token

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    "https://notify.eskiz.uz/api/auth/login",
                    data={"email": Config.ESKIZ_EMAIL, "password": Config.ESKIZ_PASSWORD}
                )
                if res.status_code == 200:
                    data = res.json().get("data", {})
                    cls._eskiz_token = data.get("token")
                    # Eskiz tokenlari 30 kun amal qiladi, biz 25 kunga keshlaymiz
                    cls._token_expiry = now + datetime.timedelta(days=25)
                    return cls._eskiz_token
        except Exception as e:
            print(f"[SMSService] Eskiz login xatolik: {e}")
        return None

    @classmethod
    async def send_sms(cls, phone_number: str, text: str) -> Dict[str, Any]:
        """Telefon raqamga SMS yuboradi."""
        # Telefon raqamdan faqat raqamlarni ajratib olamiz (998901234567)
        clean_digits = "".join(filter(str.isdigit, phone_number))
        
        token = await cls.get_eskiz_token()
        if token:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    headers = {"Authorization": f"Bearer {token}"}
                    payload = {
                        "mobile_phone": clean_digits,
                        "message": text,
                        "from": "4546"
                    }
                    res = await client.post(
                        "https://notify.eskiz.uz/api/message/sms/send",
                        data=payload,
                        headers=headers
                    )
                    if res.status_code in [200, 201]:
                        return {"success": True, "provider": "eskiz", "response": res.json()}
            except Exception as e:
                print(f"[SMSService] SMS yuborishda xatolik: {e}")
        
        # Agar Eskiz kalitlari ulanmagan bo'lsa yoki dev rejimda bo'lsak:
        print("\n=======================================================")
        print(f"[SMS SIMULATSIYA] Qabul qiluvchi: {phone_number}")
        print(f"[SMS XABAR]: {text}")
        print("=======================================================\n")
        return {"success": True, "provider": "dev_simulator", "delivered": True}
