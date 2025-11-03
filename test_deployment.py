import sys
import json
import requests
from jose import jwt
import argparse

# --- Configuration ---
BASE_URL = ""

# --- JWT Generation ---
def generate_dummy_jwt() -> str:
    """Generates a dummy JWT with sub='test_user'."""
    # The payload contains the claims. We only need 'sub' for this test.
    payload = {"sub": "test_user"}

    # The secret and algorithm are required to sign the token.
    # Since the server does not verify the signature, these can be any string.
    secret = "dummy-secret-key-that-is-not-used-for-verification"
    algorithm = "HS256"

    dummy_token = jwt.encode(payload, secret, algorithm=algorithm)
    return dummy_token


# --- Main Functions ---

def make_request(endpoint: str, token: str):
    """Makes a GET request to a specific endpoint and prints the response."""
    print(f"--- Testing {endpoint} ---")
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        print(json.dumps(response.json(), indent=2))
        print("Status: OK\n")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}", file=sys.stderr)
        print(f"Response Body: {response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.", file=sys.stderr)
        print(f"Response Text: {response.text}", file=sys.stderr)
        sys.exit(1)


def make_unauthenticated_request(endpoint: str):
    """Makes a GET request to a specific endpoint without a token and expects a 401."""
    print(f"--- Testing unauthenticated access to {endpoint} ---")
    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.get(url)

        if response.status_code == 401:
            print(f"Status: 401 Unauthorized (Expected)")
            print(f"Response Body: {json.dumps(response.json(), indent=2)}\n")
            assert response.json() == {"detail": "Not authenticated"}
        else:
            print(
                f"Error: Expected 401, but got {response.status_code}", file=sys.stderr
            )
            print(f"Response Body: {response.text}", file=sys.stderr)
            sys.exit(1)

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.", file=sys.stderr)
        print(f"Response Text: {response.text}", file=sys.stderr)
        sys.exit(1)


def main():
    global BASE_URL

    parser = argparse.ArgumentParser(description="Test deployed application endpoints.")
    parser.add_argument("--env", type=str, default="deployed",
                        help="Specify the environment: 'local' or 'deployed' (default). If 'local', uses http://localhost:8080. Otherwise, uses the deployed Cloud Run URL.")
    args = parser.parse_args()

    if args.env == "local":
        BASE_URL = "http://localhost:8080"
        print("Running tests against LOCAL environment (http://localhost:8080)\n")
    else:
        BASE_URL = "https://money-note-api-6j7ycme5ya-uc.a.run.app" # Updated deployed URL
        print(f"Running tests against DEPLOYED environment ({BASE_URL})\n")

    print("Generating a dummy JWT for testing...\n")
    jwt_token = generate_dummy_jwt()

    endpoints_to_test = [
        "/api/v1/version",
        "/api/v1/test3",
        "/api/v1/currencies/all",
        "/api/v1/book-templates/all",
    ]

    for endpoint in endpoints_to_test:
        make_request(endpoint, jwt_token)

    # Test for /initState expecting a 404 (user not found in empty database)
    print("\n--- Testing /api/v1/users/initState (expecting 404 for non-existent user) ---")
    url_init_state = f"{BASE_URL}/api/v1/users/initState"
    headers_auth = {"Authorization": f"Bearer {jwt_token}"}
    try:
        response = requests.get(url_init_state, headers=headers_auth)
        if response.status_code == 404:
            print(f"Status: 404 Not Found (Expected)")
            print(f"Response Body: {json.dumps(response.json(), indent=2)}\n")
            assert response.json() == {"detail": "User not found"}
        else:
            print(f"Error: Expected 404 for /initState, but got {response.status_code}", file=sys.stderr)
            print(f"Response Body: {response.text}", file=sys.stderr)
            sys.exit(1)
            
    except requests.exceptions.RequestException as err:
        print(f"An error occurred during /initState test: {err}", file=sys.stderr)
        sys.exit(1)

    print("\n--- Running Unauthenticated Tests ---")
    make_unauthenticated_request("/api/v1/currencies/all")

    print("--- All tests completed successfully! ---")


if __name__ == "__main__":
    # Check if requests library is installed
    try:
        import requests
    except ImportError:
        print("Error: The 'requests' library is not installed.", file=sys.stderr)
        print("Please install it using: pip install requests", file=sys.stderr)
        sys.exit(1)
    main()

