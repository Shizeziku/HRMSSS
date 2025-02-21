from django.contrib.auth.hashers import check_password
from department.models import Employe_User

def custom_authenticate(email, password):
    try:
        user = Employe_User.objects.get(email=email)
        print(f"✅ Found User: {user.email}")  # Debugging

        if check_password(password, user.password):  # Check hashed password
            print("✅ Password Matched")
            return user
        else:
            print("❌ Password Incorrect")
    except Employe_User.DoesNotExist:
        print("❌ No User Found with this Email")

    return None
