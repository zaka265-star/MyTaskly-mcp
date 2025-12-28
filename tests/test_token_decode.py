"""Test script to verify JWT token generation and decoding."""

import sys
import jwt
from datetime import datetime, timezone, timedelta

# Default values matching config.py
SECRET_KEY = "change-this-secret-key-in-production"
ALGORITHM = "HS256"
AUDIENCE = "mcp://mytaskly-mcp-server"
ISSUER = "https://api.mytasklyapp.com"


def test_token(token_string: str):
    """Test decoding a JWT token."""
    print("=" * 70)
    print("JWT TOKEN DECODE TEST")
    print("=" * 70)
    print()

    # Print token info
    print(f"Token (full): {token_string}")
    print(f"Token length: {len(token_string)}")

    # Check format
    parts = token_string.split('.')
    print(f"Token parts count: {len(parts)}")

    if len(parts) != 3:
        print("\n❌ ERROR: JWT must have exactly 3 parts (header.payload.signature)")
        print(f"   Found {len(parts)} parts")
        return False

    print(f"\nPart 1 (Header) length: {len(parts[0])}")
    print(f"Part 2 (Payload) length: {len(parts[1])}")
    print(f"Part 3 (Signature) length: {len(parts[2])}")

    # Try to decode
    print("\n" + "=" * 70)
    print("DECODING TOKEN...")
    print("=" * 70)

    try:
        # First, decode without verification to see the payload
        unverified = jwt.decode(
            token_string,
            options={"verify_signature": False}
        )

        print("\n✅ Token structure is valid (decoded without verification)")
        print("\nPayload content:")
        import json
        print(json.dumps(unverified, indent=2))

        # Now decode with full verification
        print("\n" + "=" * 70)
        print("VERIFYING SIGNATURE AND CLAIMS...")
        print("=" * 70)

        payload = jwt.decode(
            token_string,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": True,
                "require": ["sub", "aud", "exp", "iat"]
            }
        )

        print("\n✅ TOKEN IS VALID!")
        print("\nVerified payload:")
        print(json.dumps(payload, indent=2))

        # Check expiration
        exp_timestamp = payload.get('exp')
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            remaining = exp_datetime - now

            print(f"\nExpiration: {exp_datetime}")
            print(f"Now: {now}")
            print(f"Remaining time: {remaining}")

            if remaining.total_seconds() > 0:
                print(f"✅ Token is still valid for {int(remaining.total_seconds() / 60)} minutes")
            else:
                print("❌ Token has EXPIRED!")

        return True

    except jwt.ExpiredSignatureError:
        print("\n❌ ERROR: Token has expired")
        return False

    except jwt.InvalidAudienceError as e:
        print(f"\n❌ ERROR: Invalid audience - {e}")
        print(f"   Expected audience: {AUDIENCE}")
        return False

    except jwt.InvalidSignatureError:
        print("\n❌ ERROR: Invalid signature")
        print("   The token was not signed with the correct secret key")
        return False

    except jwt.DecodeError as e:
        print(f"\n❌ ERROR: Token decode error - {e}")
        return False

    except Exception as e:
        print(f"\n❌ ERROR: Unexpected error - {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_and_test_token(user_id: int = 123):
    """Generate a new token and test it."""
    print("=" * 70)
    print("GENERATING NEW TOKEN")
    print("=" * 70)

    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "aud": AUDIENCE,
        "iss": ISSUER,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=30)).timestamp()),
        "scope": "tasks:read tasks:write categories:read categories:write notes:read notes:write"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    print(f"\nGenerated token for user_id={user_id}:")
    print(token)
    print()

    # Test it
    return test_token(token)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test provided token
        token = sys.argv[1]

        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        success = test_token(token)
    else:
        # Generate and test a new token
        print("No token provided, generating a new one...\n")
        success = generate_and_test_token(user_id=123)

    print("\n" + "=" * 70)
    if success:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ TESTS FAILED")
    print("=" * 70)

    sys.exit(0 if success else 1)
