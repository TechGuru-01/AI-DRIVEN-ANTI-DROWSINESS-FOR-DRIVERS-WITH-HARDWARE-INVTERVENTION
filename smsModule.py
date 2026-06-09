from moceansdk import Client, Basic

class SMSNotifier:
    @staticmethod
    def send_sms():
        mocean = Client(Basic(api_token="apit-wt5XD6WyIPecXXXeGYxNPlrxckTZdJux-0nkrh"))
        sender_name = "LUMINA ALERT"
        message = "[LUMINA ALERT]\nWARNING: DROWSINESS DETECTED! PLEASE CHECK ON YOUR DRIVER."
        recipients="639459929446, 639217239974, 639568794775, 639917870087"
        try:
            res = mocean.sms.create({
                "mocean-from": sender_name,
                "mocean-to": recipients,
                "mocean-text": message
            }).send()
            return res
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return None