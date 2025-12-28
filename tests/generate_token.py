"""Generate JWT tokens for testing MyTaskly MCP Server.

This script creates valid JWT tokens that can be used to authenticate
with the MCP server when connecting from external clients like ChatGPT.

Usage:
    python tests/generate_token.py --user-id 123
    python tests/generate_token.py --user-id 456 --expires 60
    python tests/generate_token.py --help
"""

import argparse
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional


def generate_jwt_token(
    user_id: int,
    secret_key: str,
    audience: str = "mcp://mytaskly-mcp-server",
    issuer: str = "https://api.mytasklyapp.com",
    expires_minutes: int = 30,
    algorithm: str = "HS256"
) -> str:
    """
    Generate a JWT token for MCP server authentication.

    Args:
        user_id: User ID to encode in the token
        secret_key: Secret key for signing the token (must match MCP server)
        audience: Token audience (resource indicator)
        issuer: Token issuer (authorization server)
        expires_minutes: Token expiration time in minutes
        algorithm: JWT signing algorithm

    Returns:
        JWT token string ready to use with MCP server
    """
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),  # Subject: user identifier
        "aud": audience,      # Audience: MCP server resource identifier
        "iss": issuer,        # Issuer: authorization server
        "iat": int(now.timestamp()),  # Issued at
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),  # Expiration
        "scope": "tasks:read tasks:write categories:read categories:write notes:read notes:write"
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def main():
    """CLI entry point for token generation."""
    parser = argparse.ArgumentParser(
        description="Generate JWT tokens for MyTaskly MCP Server authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate token for user 123 (expires in 30 minutes)
  python tests/generate_token.py --user-id 123

  # Generate token with custom expiration (60 minutes)
  python tests/generate_token.py --user-id 456 --expires 60

  # Generate token with custom secret key
  python tests/generate_token.py --user-id 789 --secret "my-custom-secret"

  # Show token info and usage instructions
  python tests/generate_token.py --user-id 123 --verbose
        """
    )

    parser.add_argument(
        "--user-id",
        type=int,
        required=True,
        help="User ID to encode in the token"
    )

    parser.add_argument(
        "--secret",
        type=str,
        default="change-this-secret-key-in-production",
        help="JWT secret key (must match MCP server config, default: from config.py)"
    )

    parser.add_argument(
        "--audience",
        type=str,
        default="mcp://mytaskly-mcp-server",
        help="Token audience (default: mcp://mytaskly-mcp-server)"
    )

    parser.add_argument(
        "--issuer",
        type=str,
        default="https://api.mytasklyapp.com",
        help="Token issuer (default: https://api.mytasklyapp.com)"
    )

    parser.add_argument(
        "--expires",
        type=int,
        default=30,
        help="Token expiration in minutes (default: 30)"
    )

    parser.add_argument(
        "--algorithm",
        type=str,
        default="HS256",
        help="JWT signing algorithm (default: HS256)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed token information and usage instructions"
    )

    args = parser.parse_args()

    # Generate token
    token = generate_jwt_token(
        user_id=args.user_id,
        secret_key=args.secret,
        audience=args.audience,
        issuer=args.issuer,
        expires_minutes=args.expires,
        algorithm=args.algorithm
    )

    # Output
    print("=" * 70)
    print("JWT TOKEN GENERATED SUCCESSFULLY")
    print("=" * 70)
    print()
    print(f"User ID:    {args.user_id}")
    print(f"Expires:    {args.expires} minutes")
    print(f"Audience:   {args.audience}")
    print(f"Issuer:     {args.issuer}")
    print()
    print("=" * 70)
    print("ACCESS TOKEN (copy this):")
    print("=" * 70)
    print(token)
    print("=" * 70)
    print()

    if args.verbose:
        print("USAGE INSTRUCTIONS:")
        print("=" * 70)
        print()
        print("1. Copy the token above")
        print()
        print("2. In ChatGPT MCP connection interface, paste it in the")
        print("   'Access token / API key' field")
        print()
        print("3. The token will be sent as:")
        print(f"   Authorization: Bearer {token[:20]}...")
        print()
        print("4. Test the connection with curl:")
        print()
        print(f"   curl -X POST https://mcp.mytasklyapp.com/sse/mcp/get_tasks \\")
        print(f"     -H 'Authorization: Bearer {token[:30]}...' \\")
        print(f"     -H 'Content-Type: application/json'")
        print()
        print("=" * 70)
        print("TOKEN DETAILS:")
        print("=" * 70)

        # Decode token to show payload
        decoded = jwt.decode(
            token,
            args.secret,
            algorithms=[args.algorithm],
            audience=args.audience
        )

        import json
        print(json.dumps(decoded, indent=2))
        print("=" * 70)

    print()
    print("NOTE: Keep this token secret! It provides full access to user data.")
    print()


if __name__ == "__main__":
    main()
