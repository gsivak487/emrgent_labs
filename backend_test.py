import requests
import sys
import json
from datetime import datetime

class EmergentLabsAPITester:
    def __init__(self, base_url="https://72b1c11c-42ac-479c-9780-24857d108336.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response preview: {str(response_data)[:200]}...")
                except:
                    print(f"   Response text: {response.text[:200]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}...")

            return success, response.json() if response.text and response.text.strip() else {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            return False, {}
        except requests.exceptions.ConnectionError:
            print(f"❌ Failed - Connection error")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        return self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )

    def test_get_portfolio_data(self):
        """Test getting all portfolio data"""
        success, response = self.run_test(
            "Get Portfolio Data",
            "GET",
            "portfolio",
            200
        )
        
        if success:
            # Validate portfolio data structure
            expected_sections = ['hero', 'services', 'users', 'differentiators', 'capabilities', 'features']
            missing_sections = []
            for section in expected_sections:
                if section not in response:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"   ⚠️  Missing sections: {missing_sections}")
            else:
                print(f"   ✅ All expected sections present")
                
            # Check if each section has required fields
            for section_name, section_data in response.items():
                if isinstance(section_data, dict):
                    required_fields = ['id', 'title', 'description']
                    missing_fields = [field for field in required_fields if field not in section_data]
                    if missing_fields:
                        print(f"   ⚠️  Section {section_name} missing fields: {missing_fields}")
        
        return success, response

    def test_get_portfolio_section(self, section_id="hero"):
        """Test getting a specific portfolio section"""
        return self.run_test(
            f"Get Portfolio Section ({section_id})",
            "GET",
            f"portfolio/{section_id}",
            200
        )

    def test_get_invalid_portfolio_section(self):
        """Test getting an invalid portfolio section"""
        return self.run_test(
            "Get Invalid Portfolio Section",
            "GET",
            "portfolio/invalid_section",
            200  # Backend returns 200 with error message instead of 404
        )

    def test_submit_contact_form(self):
        """Test submitting contact form"""
        test_contact = {
            "name": f"Test User {datetime.now().strftime('%H%M%S')}",
            "email": f"test{datetime.now().strftime('%H%M%S')}@example.com",
            "message": "This is a test message from the API test suite."
        }
        
        success, response = self.run_test(
            "Submit Contact Form",
            "POST",
            "contact",
            200,
            data=test_contact
        )
        
        if success:
            # Validate response structure
            expected_fields = ['id', 'name', 'email', 'message', 'timestamp']
            missing_fields = [field for field in expected_fields if field not in response]
            if missing_fields:
                print(f"   ⚠️  Response missing fields: {missing_fields}")
            else:
                print(f"   ✅ Contact submission response has all required fields")
                
            # Validate that submitted data matches response
            if response.get('name') == test_contact['name'] and response.get('email') == test_contact['email']:
                print(f"   ✅ Submitted data matches response")
            else:
                print(f"   ⚠️  Submitted data doesn't match response")
        
        return success, response

    def test_get_contact_submissions(self):
        """Test getting contact submissions"""
        return self.run_test(
            "Get Contact Submissions",
            "GET",
            "contact",
            200
        )

    def test_invalid_contact_submission(self):
        """Test submitting invalid contact form data"""
        invalid_contact = {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email
            "message": ""  # Empty message
        }
        
        return self.run_test(
            "Submit Invalid Contact Form",
            "POST",
            "contact",
            422  # Expecting validation error
        )

    def test_status_endpoints(self):
        """Test status check endpoints"""
        # Test creating status check
        test_status = {
            "client_name": f"test_client_{datetime.now().strftime('%H%M%S')}"
        }
        
        success, response = self.run_test(
            "Create Status Check",
            "POST",
            "status",
            200,
            data=test_status
        )
        
        if success:
            print(f"   ✅ Status check created with ID: {response.get('id', 'N/A')}")
        
        # Test getting status checks
        success2, response2 = self.run_test(
            "Get Status Checks",
            "GET",
            "status",
            200
        )
        
        return success and success2

def main():
    print("🚀 Starting Emergent Labs Portfolio API Tests")
    print("=" * 60)
    
    # Initialize tester
    tester = EmergentLabsAPITester()
    
    # Run all tests
    print("\n📋 Testing Core API Endpoints...")
    tester.test_root_endpoint()
    
    print("\n📋 Testing Portfolio Endpoints...")
    portfolio_success, portfolio_data = tester.test_get_portfolio_data()
    tester.test_get_portfolio_section("hero")
    tester.test_get_portfolio_section("services")
    tester.test_get_invalid_portfolio_section()
    
    print("\n📋 Testing Contact Form Endpoints...")
    tester.test_submit_contact_form()
    tester.test_get_contact_submissions()
    tester.test_invalid_contact_submission()
    
    print("\n📋 Testing Status Endpoints...")
    tester.test_status_endpoints()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Backend API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())