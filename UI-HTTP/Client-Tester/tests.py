import requests

# Dirección del servidor
SERVER = "http://localhost:8888"

# Almacena los resultados de las pruebas
results = []

def print_case(case, description):
    print(f"\n👉 \033[1mCase: {case}\033[0m")
    print(f"   📝 {description}")

def evaluate_response(case, expected_status, actual_status, expected_body=None, actual_body=None):
    success = actual_status == expected_status and (expected_body is None or expected_body in actual_body)
    results.append({
        "case": case,
        "status": "Success" if success else "Failed",
        "expected_status": expected_status,
        "actual_status": actual_status,
        "expected_body": expected_body,
        "actual_body": actual_body
    })
    if success:
        print(f"   ✅ \033[92mSuccess\033[0m")
    else:
        print(f"   ❌ \033[91mFailed\033[0m")

# Pruebas de métodos HTTP
print_case("GET root", "Testing a simple GET request to '/'")
response = requests.get(f"{SERVER}/")
evaluate_response("GET root", 200, response.status_code, "GET request successful", response.text)

print_case("GET with custom header", "Testing GET request with 'X-Custom-Header'")
response = requests.get(f"{SERVER}/secure", headers={"X-Custom-Header": "TestHeader"})
evaluate_response("GET with custom header", 200, response.status_code, "Custom header received", response.text)

print_case("POST with JSON body", "Testing POST request with a JSON payload")
response = requests.post(f"{SERVER}/secure", json={"key": "value"})
evaluate_response("POST with JSON body", 200, response.status_code, "JSON data received", response.text)

print_case("POST with XML body", "Testing POST request with an XML payload")
response = requests.post(f"{SERVER}/secure", headers={"Content-Type": "application/xml"}, data="<key>value</key>")
evaluate_response("POST with XML body", 200, response.status_code, "XML data received", response.text)

print_case("POST with plain text body", "Testing POST request with plain text payload")
response = requests.post(f"{SERVER}/secure", data="Hello, server!")
evaluate_response("POST with plain text body", 200, response.status_code, "Plain text", response.text)

print_case("HEAD request", "Testing a simple HEAD request")
response = requests.head(f"{SERVER}/")
evaluate_response("HEAD request", 200, response.status_code)

print_case("PUT request", "Testing a simple PUT request")
response = requests.put(f"{SERVER}/resource")
evaluate_response("PUT request", 200, response.status_code, "PUT method received", response.text)

print_case("DELETE request", "Testing a simple DELETE request")
response = requests.delete(f"{SERVER}/resource")
evaluate_response("DELETE request", 200, response.status_code, "DELETE method received", response.text)

print_case("OPTIONS request", "Testing OPTIONS request to see supported methods")
response = requests.options(f"{SERVER}/")
evaluate_response("OPTIONS request", 204, response.status_code)

print_case("TRACE request", "Testing TRACE request to echo back the request")
response = requests.request("TRACE", f"{SERVER}/")
evaluate_response("TRACE request", 200, response.status_code)

print_case("CONNECT request", "Testing CONNECT request for tunneling")
response = requests.request("CONNECT", f"{SERVER}/")
evaluate_response("CONNECT request", 501, response.status_code)

# Pruebas de autorización
print_case("GET without Authorization", "Testing GET request without Authorization header")
response = requests.get(f"{SERVER}/secure")
evaluate_response("GET without Authorization", 401, response.status_code, "Authorization header missing", response.text)

print_case("GET with invalid Authorization", "Testing GET request with an invalid Authorization header")
response = requests.get(f"{SERVER}/secure", headers={"Authorization": "Bearer invalid_token"})
evaluate_response("GET with invalid Authorization", 401, response.status_code, "Invalid or missing authorization token", response.text)

print_case("GET with valid Authorization", "Testing GET request with a valid Authorization header")
response = requests.get(f"{SERVER}/secure", headers={"Authorization": "Bearer 12345"})
evaluate_response("GET with valid Authorization", 200, response.status_code, "You accessed a protected resource", response.text)

print_case("POST with malformed body", "Testing POST request with malformed JSON payload")
response = requests.post(f"{SERVER}/secure", json='{"key":}')  # Malformed JSON
evaluate_response("POST with malformed body", 400, response.status_code)

# Resumen
print("\n🎉 \033[1mTest Summary\033[0m 🎉")
total_cases = len(results)
success_cases = sum(1 for result in results if result["status"] == "Success")
failed_cases = total_cases - success_cases

print(f"   ✅ Successful cases: {success_cases}/{total_cases}")
print(f"   ❌ Failed cases: {failed_cases}/{total_cases}")

if failed_cases > 0:
    print("\n📋 \033[1mFailed Cases Details:\033[0m")
    for result in results:
        if result["status"] == "Failed":
            print(f"   ❌ {result['case']}")
            print(f"      - Expected status: {result['expected_status']}, Actual status: {result['actual_status']}")
            if result['expected_body'] and result['actual_body']:
                print(f"      - Expected body: {result['expected_body']}")
                print(f"      - Actual body: {result['actual_body']}\n")
