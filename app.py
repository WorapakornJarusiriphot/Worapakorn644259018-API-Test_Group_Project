from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# ตัวอย่างข้อมูลของผู้ใช้ (ในกรณีจริงควรใช้ฐานข้อมูล)
users = []

# ฟังก์ชันสำหรับสร้าง username และ email ที่ไม่ซ้ำ
def generate_unique_user():
    timestamp = int(time.time())  # ใช้ timestamp เพื่อสร้าง username และ email ที่ไม่ซ้ำ
    return {
        "username": f"WOJA{timestamp}",
        "email": f"Worapakorn{timestamp}@gmail.com"
    }

# POST: สร้างผู้ใช้ใหม่
@app.route('/api/users', methods=['POST'])
def create_user():
    required_fields = ['first_name', 'last_name', 'password', 'birthday', 'phone_number', 'gender', 'user_image']
    user_data = request.json  # รับข้อมูลจาก body

    # ตรวจสอบว่ามีข้อมูลครบถ้วนหรือไม่
    if not all(field in user_data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # สร้าง username และ email ที่ไม่ซ้ำ
    unique_user = generate_unique_user()
    user_data['username'] = unique_user['username']
    user_data['email'] = unique_user['email']

    # กำหนด user_id เป็นลำดับที่ของผู้ใช้ (ในกรณีนี้ใช้ความยาวของลิสต์)
    user_id = len(users)
    user_data['id'] = user_id  # เพิ่ม user_id ลงในข้อมูลผู้ใช้

    users.append(user_data)  # เก็บข้อมูลในลิสต์ users
    return jsonify({'message': 'User was registered successfully!', 'user': user_data, 'id': user_id}), 201

# GET: ดึงข้อมูลผู้ใช้ทั้งหมด
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET: ดึงข้อมูลผู้ใช้ตาม user_id
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if 0 <= user_id < len(users):
        return jsonify({'user': users[user_id]}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# PUT: อัปเดตข้อมูลผู้ใช้ตาม user_id
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if 0 <= user_id < len(users):
        user_data = request.json
        users[user_id].update(user_data)
        return jsonify({'message': 'User updated successfully!', 'user': users[user_id]}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# DELETE: ลบผู้ใช้ตาม user_id
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 0 <= user_id < len(users):
        del users[user_id]
        return '', 204
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
