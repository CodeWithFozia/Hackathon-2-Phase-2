#!/usr/bin/env python3
"""
Script to automatically configure Hugging Face Space secrets/environment variables.
"""
from huggingface_hub import HfApi
import sys
import os

# Generated JWT secret key
JWT_SECRET = "58f524e598aa46bd19cb12285792ef92014b45049d1f75c57121055bd6c3779e"

# Space configuration
SPACE_ID = "fouziabibi/todo"

# Get token from command line argument or environment variable
HF_TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.getenv("HF_TOKEN")

# Environment variables to set
SECRETS = {
    "DATABASE_URL": "postgresql://neondb_owner:npg_Debr7jpMYk2R@ep-bitter-mode-ah28dkfm-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require",
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
    """Add secrets to Hugging Face Space."""
    print("Setting up Hugging Face Space environment variables...")
    print(f"Space: {SPACE_ID}")
    print(f"Generated JWT Secret: {JWT_SECRET}")
    print()

    if not HF_TOKEN:
        print("[ERROR] No Hugging Face token provided!")
        print("Usage: python setup_hf_secrets.py <HF_TOKEN>")
        print("Or set HF_TOKEN environment variable")
        sys.exit(1)

    try:
        # Initialize Hugging Face API with token
        api = HfApi(token=HF_TOKEN)

        # Check if user is authenticated
        try:
            user_info = api.whoami()
            print(f"[OK] Authenticated as: {user_info['name']}")
        except Exception as e:
            print(f"[ERROR] Authentication failed: {str(e)}")
            sys.exit(1)

        # Add each secret
        print("\nAdding environment variables...")
        for key, value in SECRETS.items():
            try:
                api.add_space_secret(
                    repo_id=SPACE_ID,
                    key=key,
                    value=value
                )
                # Mask sensitive values in output
                display_value = value if key not in ["DATABASE_URL", "JWT_SECRET"] else "***HIDDEN***"
                print(f"  [OK] {key} = {display_value}")
            except Exception as e:
                print(f"  [FAIL] Failed to add {key}: {str(e)}")

        print("\n[SUCCESS] Environment variables configured successfully!")
        print("\nYour Space should now rebuild automatically.")
        print(f"Check status at: https://huggingface.co/spaces/{SPACE_ID}")
        print(f"API Docs: https://fouziabibi-todo.hf.space/docs")
        print(f"Health Check: https://fouziabibi-todo.hf.space/health")

    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
