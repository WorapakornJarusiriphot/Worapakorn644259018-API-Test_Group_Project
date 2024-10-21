import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/users"

# ฟังก์ชันสำหรับทดสอบการสร้างผู้ใช้ใหม่
def test_create_user():
    payload = {
        "first_name": "Worapakorn",
        "last_name": "Jarusiriphot",
        "password": "111111",
        "birthday": "03/17/2003",
        "phone_number": "0623844415",
        "gender": "ชาย",
        "user_image": "a84f9cd9-3c1d-4cb2-ba88-a188c298d119.jpeg"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(BASE_URL, headers=headers, json=payload)
    
    # ตรวจสอบว่า status code เป็น 201 (สร้างสำเร็จ)
    assert response.status_code == 201, f"Status code should be 201, but got {response.status_code}"

    # ตรวจสอบว่ามีข้อความ 'User was registered successfully!'
    response_data = response.json()
    assert response_data['message'] == "User was registered successfully!"
    
    # เก็บค่า user_id เพื่อนำไปใช้ในฟังก์ชันอื่น
    user_id = response_data['id']
    print(f"Created user with id: {user_id}")
    return user_id

# ฟังก์ชันสำหรับทดสอบการดึงผู้ใช้ทั้งหมด
def test_get_users():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print(response.json())

# ฟังก์ชันสำหรับทดสอบการดึงผู้ใช้ตาม user_id
def test_get_user_by_id(user_id):
    response = requests.get(f"{BASE_URL}/{user_id}")
    assert response.status_code == 200
    print(response.json())

# ฟังก์ชันสำหรับทดสอบการอัปเดตผู้ใช้
def test_update_user(user_id):
    payload = {
        "first_name": "Updated Name",
        "last_name": "Updated Last Name",
        "gender": "หญิง",
        "user_image": "b3afd629-c2cb-4dfe-8657-157f9a567fb8.jpeg"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.put(f"{BASE_URL}/{user_id}", headers=headers, json=payload)
    assert response.status_code == 200, f"Status code should be 200, but got {response.status_code}"
    print(response.json())

# ฟังก์ชันสำหรับทดสอบการลบผู้ใช้
def test_delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/{user_id}")
    assert response.status_code == 204, f"Status code should be 204, but got {response.status_code}"
    print(f"User with id {user_id} deleted")

# เรียกใช้ฟังก์ชันทดสอบ
def run_tests():
    user_id = test_create_user()  # สร้างผู้ใช้ใหม่และเก็บ user_id
    test_get_users()  # ดึงข้อมูลผู้ใช้ทั้งหมด
    test_get_user_by_id(user_id)  # ดึงข้อมูลผู้ใช้ตาม user_id
    test_update_user(user_id)  # อัปเดตข้อมูลผู้ใช้
    test_delete_user(user_id)  # ลบผู้ใช้

# เรียกใช้การทดสอบทั้งหมด
run_tests()
