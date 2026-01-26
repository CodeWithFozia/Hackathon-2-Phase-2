#!/usr/bin/env python3
"""
Update Hugging Face Space to use SQLite instead of PostgreSQL.
"""
from huggingface_hub import HfApi
import sys

# Token and Space configuration
HF_TOKEN = sys.argv[1] if len(sys.argv) > 1 else None
SPACE_ID = "fouziabibi/todo"
JWT_SECRET = "58f524e598aa46bd19cb12285792ef92014b45049d1f75c57121055bd6c3779e"

# Updated environment variables with SQLite
SECRETS = {
    "DATABASE_URL": "sqlite:///./todo_app.db",
    "JWT_SECRET": JWT_SECRET,
    "JWT_ALGORITHM": "HS256",
    "JWT_EXPIRATION_MINUTES": "15",
    "JWT_REFRESH_EXPIRATION_HOURS": "168",
    "BCRYPT_ROUNDS": "12",
    "DEBUG": "false",
    "LOG_LEVEL": "info",
    "API_HOST": "0.0.0.0",
    "API_PORT": "7860",
}

def main():
    if not HF_TOKEN:
        print("[ERROR] No token provided!")
        print("Usage: python update_to_sqlite.py <HF_TOKEN>")
        sys.exit(1)

    print("Updating Hugging Face Space to use SQLite...")
    print(f"Space: {SPACE_ID}")
    print()

    try:
        api = HfApi(token=HF_TOKEN)
        user_info = api.whoami()
        print(f"[OK] Authenticated as: {user_info['name']}")

        print("\nUpdating environment variables to use SQLite...")
        for key, value in SECRETS.items():
            try:
                api.add_space_secret(
                    repo_id=SPACE_ID,
                    key=key,
                    value=value
                )
                display_value = value if key not in ["DATABASE_URL", "JWT_SECRET"] else "***HIDDEN***"
                print(f"  [OK] {key} = {display_value}")
            except Exception as e:
                print(f"  [FAIL] {key}: {str(e)}")

        print("\n[SUCCESS] Configuration updated to use SQLite!")
        print("\nThe Space will rebuild automatically.")
        print("SQLite database will be created on first run.")
        print(f"\nCheck status: https://huggingface.co/spaces/{SPACE_ID}")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
