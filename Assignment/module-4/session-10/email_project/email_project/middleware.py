from django.shortcuts import redirect


class BlockExpiredOTPAccessMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response


    def __call__(self, request):

        # Only check OTP verification page
        if request.path == '/verify-otp/':

            # Get OTP from session
            otp = request.session.get('otp')


            # OTP missing means expired/not generated
            if not otp:

                return redirect(
                    'forgot_password'
                )


        # Continue request
        response = self.get_response(request)


        return response