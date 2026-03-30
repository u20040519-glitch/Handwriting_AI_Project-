import requests

API_URL = "http://127.0.0.1:8000"

def test_connection():
    """Test if AI Tool is running"""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✅ AI Tool is connected!")
            print(f"Response: {response.json()}")
            return True
        else:
            print("❌ AI Tool responded with error")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to AI Tool: {e}")
        return False

def test_signup(username="testuser", password="testpass"):
    """Test user signup"""
    try:
        response = requests.post(
            f"{API_URL}/signup",
            json={"username": username, "password": password}
        )
        print(f"Signup Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Signup Error: {e}")
        return None

def test_login(username="testuser", password="testpass"):
    """Test user login"""
    try:
        response = requests.post(
            f"{API_URL}/login",
            data={"username": username, "password": password}
        )
        print(f"Login Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Login Error: {e}")
        return None

if __name__ == "__main__":
    print("🔗 Testing API Connection...\n")
    test_connection()
    print("\n🔗 Testing Signup...")
    test_signup()
    print("\n🔗 Testing Login...")
    test_login()
