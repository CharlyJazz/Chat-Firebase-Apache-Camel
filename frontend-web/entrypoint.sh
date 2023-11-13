#!/bin/sh

# https://dev.to/itsrennyman/manage-nextpublic-environment-variables-at-runtime-with-docker-53dl

echo "Check that we have NEXT_PUBLIC_AUTH_MICROSERVICE vars"
test -n "$NEXT_PUBLIC_AUTH_MICROSERVICE"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_AUTH_MICROSERVICE#$NEXT_PUBLIC_AUTH_MICROSERVICE#g"

echo "Check that we have NEXT_PUBLIC_CHAT_MICROSERVICE vars"
test -n "$NEXT_PUBLIC_CHAT_MICROSERVICE"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_CHAT_MICROSERVICE#$NEXT_PUBLIC_CHAT_MICROSERVICE#g"

echo "Check that we have NEXT_PUBLIC_API_KEY vars"
test -n "$NEXT_PUBLIC_API_KEY"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_API_KEY#$NEXT_PUBLIC_API_KEY#g"

echo "Check that we have NEXT_PUBLIC_AUTH_DOMAIN vars"
test -n "$NEXT_PUBLIC_AUTH_DOMAIN"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_AUTH_DOMAIN#$NEXT_PUBLIC_AUTH_DOMAIN#g"

echo "Check that we have NEXT_PUBLIC_PROJECT_ID vars"
test -n "$NEXT_PUBLIC_PROJECT_ID"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_PROJECT_ID#$NEXT_PUBLIC_PROJECT_ID#g"

echo "Check that we have NEXT_PUBLIC_STORAGE_BUCKET vars"
test -n "$NEXT_PUBLIC_STORAGE_BUCKET"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_STORAGE_BUCKET#$NEXT_PUBLIC_STORAGE_BUCKET#g"

echo "Check that we have NEXT_PUBLIC_MESSAGING_SENDER_ID vars"
test -n "$NEXT_PUBLIC_MESSAGING_SENDER_ID"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_MESSAGING_SENDER_ID#$NEXT_PUBLIC_MESSAGING_SENDER_ID#g"

echo "Check that we have NEXT_PUBLIC_APP_ID vars"
test -n "$NEXT_PUBLIC_APP_ID"

find /app/.next \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s#NEXT_PUBLIC_APP_ID#$NEXT_PUBLIC_APP_ID#g"

echo "Starting Nextjs"
exec "$@"