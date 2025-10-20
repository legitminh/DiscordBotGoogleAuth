# from flask import Flask, request, redirect
# from linkToken.nonce_manager import validate_nonce, cleanup_nonces
# from supabase import create_client
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)

# # You can use a service role key to verify/session exchange server-side if needed
# supabase = None
# if SUPABASE_URL and SUPABASE_SERVICE_KEY:
#     supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


# @app.route('/auth/callback')
# def callback():
#     # Validate the nonce
#     nonce = request.args.get('nonce')
#     if not nonce or not validate_nonce(nonce):
#         return "Invalid or expired token.", 400

#     # Optionally, handle the Supabase OAuth code exchange here if you receive a code.
#     # For now, just show success and redirect to a friendly page.
#     cleanup_nonces()
#     return "Sign-in validated. You can close this window.", 200


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
