# # from gcm import *
# #
# #
# # APIKey = "AIzaSyBwp1_iKvFIH9FFTSv65sRUQejTh0TkqnY"
# # reg_id = "cywq8GyZDP0:APA91bHD46xaSwKXVIyX0OEQApnqKIUTC9-8UltNDIfE2ocvHLpq4jK0yROYfVvAuW5veeFHYO8XTABZrpWrlO3vwLbciSNxzXuuJG1GvheqibqWdUEZeJtSlof3KyS8vuLap3HQUf8Y"
# # # reg_id = 'eprzyGWpkZQ:APA91bEbPwEhK2mMnkpHY9MR3oLcH4MXF38VLgglpNePHjceathTOiOyYXg-Khu5Ryp5-PbFU9B3Gf8FdE23Tn_yDGFQdFDGm3dljhtFnznylU3Ndw3zCB6r3pldjdlGSAiRP1D6kU-J'
# # data = {'message': 'You have a new order', 'param2': 'value2'}
# #
# #
# # def sendNotification(APIKey, redToken, JSONstr):
# #     gcm = GCM(APIKey)
# #     gcm.plaintext_request(registration_id=reg_id, data=JSONstr)
# #
# # # sendNotification(APIKey, reg_id, data)
# #
# #
#
# from oauth2client import client, crypt
#
# # (Receive token by HTTPS POST)
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNmYjJhYTUyZjlmZDdmYTRiZGIyOTE0ZDA3ODEyNGUyZjM0MGM2MDYifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhdWQiOiIxMjM5NDU4MDE2MTEtazJzcW1qdWtpZ3Z1YTl0Mm5oc2I2YTBsZmx1cW5ldGguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDE0NzI2OTcwMzAzNDg0OTIzOTQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMTIzOTQ1ODAxNjExLTRsZ29nZGJhbzdicHM0azFrcWhpZG4zYjI3dDMwYmJvLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiZW1haWwiOiJyYXR1bGphaW4xOTkxQGdtYWlsLmNvbSIsImlhdCI6MTQ1NjkzODk4NiwiZXhwIjoxNDU2OTQyNTg2LCJuYW1lIjoiUmF0dWwgSmFpbiIsImdpdmVuX25hbWUiOiJSYXR1bCIsImZhbWlseV9uYW1lIjoiSmFpbiIsImxvY2FsZSI6ImVuIn0.mlJQtyySqis5CtRTPV8Cgi-gHO65e61DRLwMlkNlh7luiNdax-rlKtJerrFvtZV1f__T-wOFIosc3aAlFb1MrdJ2MKVFuFCCkx6XrWpDysl7KsIMM3HtbTb36PwlA0Shb3d5uMH77cQHxvxmuTtNtfMIV98MdC1b0EMxgc0KQWBOqr2CcJ5s2m9TY6Ed35JyaQQtwhpce6I3Yvt-TsLiJtlunpZ5zLjNjq6I0ZhbWO5ScPc4lQIcwh-KiqtNUeK4yZOBxCJSDjVdJrXtDOndTZR3RCVFBS_lqwWEMQV5g6JR85H7o0aQN1QulWCYzroBK6xhbknQL7BA9qerdJ9x2Q"
#
#
# data = {"idToken" : token}
#
#
#

ANDROID_CLIENT_ID = "123945801611-4lgogdbao7bps4k1kqhidn3b27t30bbo.apps.googleusercontent.com"
WEB_CLIENT_ID = "123945801611-k2sqmjukigvua9t2nhsb6a0lfluqneth.apps.googleusercontent.com"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ1ZTRiMzE0NzllNmE2NmE1YzQyZjk2ZTI5MDFiYzkwOWY1M2NhY2EifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhdWQiOiIxMjM5NDU4MDE2MTEtazJzcW1qdWtpZ3Z1YTl0Mm5oc2I2YTBsZmx1cW5ldGguYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDE0NzI2OTcwMzAzNDg0OTIzOTQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMTIzOTQ1ODAxNjExLXV1czBmNGJidWwwcDVnOTVzNWw1ZTlzZm5ubXRmNXNzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiZW1haWwiOiJyYXR1bGphaW4xOTkxQGdtYWlsLmNvbSIsImlhdCI6MTQ1ODk5NDgyMCwiZXhwIjoxNDU4OTk4NDIwLCJuYW1lIjoiUmF0dWwgSmFpbiIsImdpdmVuX25hbWUiOiJSYXR1bCIsImZhbWlseV9uYW1lIjoiSmFpbiIsImxvY2FsZSI6ImVuIn0.qli0bjnxI1VxvI7lfgylHEkBz_JrNb7VhVXIGodRRv9U8lHp1_wZC1B4BWHaXxhWx0iMLgrvpQyXDf2b9xcnJCQCQcFOhRXZEWhaCXoxhKM3HF1esdfgkDnWUGD7be0oR4lr200nlo-SD3uTsaORKxVsNFtgyVeMmU3sXjYwuXrYejnSQXDMkD1ILY4DrateQPnrbGuLbb-KBC2MHq-xo9dxqxCEzLr7U3H6yHQwrw_nKCaiSvk_MEPYlxc7IDhWpya03vnAC-LVMQdRgZOhwopyN_mzR0iRZj2GPQ82O7uMtlqx9Uc_NWE2UjXaIrO2RVcZn4i8rV2TVIr8__iFfg"
from oauth2client import client, crypt

# (Receive token by HTTPS POST)
def googleTokenValidation(token, WEB_CLIENT_ID, ANDROID_CLIENT_ID):
    try:
        idinfo = client.verify_id_token(token, WEB_CLIENT_ID)
        # print idinfo
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [ANDROID_CLIENT_ID, WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        return idinfo
    except crypt.AppIdentityError:
        print "The token is invalid"
#
# userid = idinfo['sub']
# print googleTokenValidation(token, WEB_CLIENT_ID, ANDROID_CLIENT_ID)