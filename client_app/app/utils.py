# from flask import current_app
# import requests

# def get_user_info():
#     try:
#         response = requests.get(f"{current_app.config['API_URL']}/api/user_info")
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         print(f"Lỗi khi lấy thông tin user: {str(e)}")
#         return None