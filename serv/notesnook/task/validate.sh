# List of required environment variables
required_vars=(
  "ATTACHMENTS_SERVER_PUBLIC_URL"
  "AUTH_SERVER_PUBLIC_URL"
  "DISABLE_SIGNUPS"
  "INSTANCE_NAME"
  "MONOGRAPH_PUBLIC_URL"
  "NOTESNOOK_API_SECRET"
  "NOTESNOOK_APP_PUBLIC_URL"
  "SMTP_HOST"
  "SMTP_PASSWORD"
  "SMTP_PORT"
  "SMTP_USERNAME"
)

# Check each required environment variable
for var in "$${required_vars[@]}"; do
  if [ -z "$${!var}" ]; then
    echo "Error: Required environment variable $$var is not set."
    exit 1
  fi
done

echo "All required environment variables are set."
