import requests
import json
import time

BASE_URL = "https://dicedreams-backend-deploy-to-render.onrender.com/api"
LOGIN_URL = f"{BASE_URL}/auth"


# ฟังก์ชันเพื่อดึง AUTH_TOKEN โดยการ login สำหรับ User
def get_auth_token():
    payload = json.dumps(
        {
            "identifier": "WOJA2",  # ระบุ identifier ของ User
            "password": "111111",  # ระบุรหัสผ่านของ User
        }
    )

    headers = {"Content-Type": "application/json"}

    response = requests.post(LOGIN_URL, headers=headers, data=payload)

    # ตรวจสอบว่าการ login สำเร็จ
    if response.status_code == 200:
        data = response.json()
        # คืนค่า access_token ที่ได้จากการ login
        return data.get("access_token")
    else:
        raise Exception(f"Failed to authenticate, status code: {response.status_code}")


# ฟังก์ชันเพื่อดึง AUTH_TOKEN โดยการ login สำหรับ Admin
def get_auth_token2():
    payload = json.dumps(
        {
            "identifier": "WOJA555",  # ระบุ identifier ของ Admin
            "password": "123456",  # ระบุรหัสผ่านของ Admin
        }
    )

    headers = {"Content-Type": "application/json"}

    response = requests.post(LOGIN_URL, headers=headers, data=payload)

    # ตรวจสอบว่าการ login สำเร็จ
    if response.status_code == 200:
        data = response.json()
        # คืนค่า access_token ที่ได้จากการ login
        return data.get("access_token")
    else:
        raise Exception(f"Failed to authenticate, status code: {response.status_code}")


# ฟังก์ชันทั่วไปสำหรับการเรียก API โดยใช้ AUTH_TOKEN ของผู้ใช้ทั่วไป
def call_api_with_auth_token(method, endpoint, data=None):
    auth_token = get_auth_token()  # ดึง token ของผู้ใช้ทั่วไป
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    # ประกอบ URL สำหรับการเรียก API
    url = f"{BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")

    # คืนค่าผลลัพธ์ที่ได้จาก API
    return response


# ฟังก์ชันทั่วไปสำหรับการเรียก API โดยใช้ AUTH_TOKEN ของ Admin
def call_api_with_auth_token2(method, endpoint, data=None):
    auth_token = get_auth_token2()  # ดึง token ของ Admin
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    # ประกอบ URL สำหรับการเรียก API
    url = f"{BASE_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")

    # คืนค่าผลลัพธ์ที่ได้จาก API
    return response


# ทดสอบการสร้างและลบผู้ใช้ผ่านการส่ง request แบบ chain
def test_create_and_delete_user():
    # สร้างผู้ใช้ใหม่
    user_data = {
        "first_name": "TestFirstName",
        "last_name": "TestLastName",
        "username": f"TestUser{int(time.time())}",
        "password": "test123",
        "email": f"test{int(time.time())}@mail.com",
        "birthday": "04/13/2006",
        "phone_number": "0123456789",
        "gender": "ชาย",
    }

    response = call_api_with_auth_token("POST", "/users", user_data)

    # ตรวจสอบว่าการตอบสนองสำเร็จ
    assert (
        response.status_code == 201
    ), f"Expected status code 201, but got {response.status_code}"
    response_data = response.json()

    # ตรวจสอบว่าข้อความที่ได้รับตรงตามความคาดหวัง
    assert (
        response_data.get("message") == "User was registered successfully!"
    ), "User creation failed or unexpected response message"

    # ดึงข้อมูลของผู้ใช้ที่สร้างใหม่เพื่อรับ users_id
    new_username = user_data["username"]
    users_response = call_api_with_auth_token("GET", "/users")
    assert users_response.status_code == 200, "Failed to retrieve users list"

    # ค้นหา users_id ของผู้ใช้ที่สร้างใหม่
    users_list = users_response.json()
    new_user = next(
        (user for user in users_list if user["username"] == new_username), None
    )
    assert new_user is not None, "Newly created user not found in users list"

    new_user_id = new_user["users_id"]

    # ลบผู้ใช้ที่เพิ่งสร้าง โดยล็อกอินในฐานะ admin
    delete_response = call_api_with_auth_token2("DELETE", f"/users/{new_user_id}")
    assert (
        delete_response.status_code == 200
    ), f"Expected status code 200, but got {delete_response.status_code}"
    assert delete_response.json()["message"] == "User was deleted successfully!"


# ทดสอบ API GET /users
def test_get_users():
    response = call_api_with_auth_token("GET", "/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# ทดสอบ API POST /users (การสร้างผู้ใช้ใหม่)
def test_create_user():
    user_data = {
        "first_name": "Worapakorn",
        "last_name": "Jarusiriphot",
        "username": f"WOJA{int(time.time())}",
        "password": "111111",
        "email": f"Worapakorn{int(time.time())}@gmail.com",
        "birthday": "03/17/2003",
        "phone_number": "0623844415",
        "gender": "ชาย",
        "user_image": "a84f9cd9-3c1d-4cb2-ba88-a188c298d119.jpeg",
    }

    response = call_api_with_auth_token("POST", "/users", user_data)
    assert response.status_code == 201
    assert response.json()["message"] == "User was registered successfully!"


# ทดสอบ API POST /auth (Login)
def test_login_user():
    payload = {"identifier": "WOJA2", "password": "111111"}
    response = call_api_with_auth_token("POST", "/auth", payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


# ทดสอบ API GET /users/{users_id}
def test_get_user_by_id():
    user_id = "5e3f5b48-0389-436c-a801-9ff5ec625284"
    response = call_api_with_auth_token("GET", f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["users_id"] == user_id
    assert data["first_name"] == "Worapakorn70"


# ทดสอบ API PUT /users/{users_id} (Update User)
def test_update_user():
    user_id = "674d68b7-28e6-447b-b220-daa032c5281d"
    user_data = {
        "first_name": "Worapakorn",
        "last_name": "Jarusiriphot",
        "username": f"WOJA{int(time.time())}",
        "password": "111111",
        "email": f"Worapakorn{int(time.time())}@gmail.com",
        "birthday": "03/17/2003",
        "phone_number": "0623844415",
        "gender": "หญิง",
        "role": "store",
        "user_image": "b3afd629-c2cb-4dfe-8657-157f9a567fb8.jpeg",
        "bio": "รักการเล่นบอร์ดเกมและชอบพบปะผู้คนใหม่ๆ",
    }

    response = call_api_with_auth_token("PUT", f"/users/{user_id}", user_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User was updated successfully."
