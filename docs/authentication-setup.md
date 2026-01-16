# Authentication Setup Guide

## Quick Reference

This guide explains how to set up authentication for the Library Assistant Cloud Function when integrating with DialogFlow CX.

## Authentication Options

### Option 1: Unauthenticated (Development/Testing)

**Use Case**: Development, testing, or when you have other security measures.

**Deployment**:
```bash
cd cloud-functions
./deploy.sh
```

**Configuration**: No additional steps needed in DialogFlow CX.

**Security**: ⚠️ Less secure - anyone with the URL can call the function.

---

### Option 2: Authenticated with Service Account (Production - Recommended)

**Use Case**: Production deployments requiring security.

**Deployment**:
```bash
cd cloud-functions
./deploy-with-auth.sh
```

**Or manually**:
```bash
# 1. Create service account
gcloud iam service-accounts create dialogflow-cx-webhook \
  --display-name="DialogFlow CX Webhook Service Account"

# 2. Deploy function with authentication
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --no-allow-unauthenticated \
  --service-account=dialogflow-cx-webhook@PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars USE_MOCK_DATA=true \
  --timeout=60s \
  --memory=512MB

# 3. Grant DialogFlow CX permission
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format="value(projectNumber)")
gcloud functions add-iam-policy-binding library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

**DialogFlow CX Configuration**:

1. Go to **Fulfillment** > **Webhooks**
2. Create or edit your webhook
3. Enter the webhook URL
4. **Enable "Enable OIDC Token"**
5. Select service account: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`
6. Save

**Security**: ✅ Secure - only DialogFlow CX can call the function.

---

## Step-by-Step: Setting Up Authentication

### Step 1: Get Your Project Number

```bash
gcloud projects describe PROJECT_ID --format="value(projectNumber)"
```

Save this number - you'll need it.

### Step 2: Deploy with Authentication

Use the provided script:
```bash
cd cloud-functions
./deploy-with-auth.sh
```

### Step 3: Configure DialogFlow CX Webhook

1. **Navigate to DialogFlow CX Console**
   - Go to your agent
   - Click **Fulfillment** in left sidebar
   - Click **Webhooks**

2. **Create or Edit Webhook**
   - Click **Create** or edit existing webhook
   - **Display Name**: library-assistant-webhook
   - **URL**: Paste your Cloud Function URL

3. **Enable OIDC Token** (Critical Step!)
   - Check **"Enable OIDC Token"**
   - **Service Account**: Select `PROJECT_NUMBER-compute@developer.gserviceaccount.com`
   - Or use the service account you created

4. **Save**

### Step 4: Test Authentication

1. Go to **Test Agent** in DialogFlow CX
2. Try an intent that uses the webhook
3. Check if it works

**If you get errors**, check the logs:
```bash
gcloud functions logs read library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --limit=20
```

---

## Troubleshooting Authentication

### Error: 403 Forbidden

**Cause**: Service account doesn't have permission.

**Fix**:
```bash
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format="value(projectNumber)")
gcloud functions add-iam-policy-binding library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

### Error: 401 Unauthorized

**Cause**: OIDC token not enabled in DialogFlow CX.

**Fix**:
1. Go to DialogFlow CX > Fulfillment > Webhooks
2. Edit your webhook
3. Enable **"Enable OIDC Token"**
4. Select the correct service account
5. Save

### Error: Function not found

**Cause**: Function name or region mismatch.

**Fix**: Verify function name and region match in both:
- Cloud Functions deployment
- DialogFlow CX webhook configuration

### Error: Permission denied

**Cause**: Service account doesn't exist or has wrong permissions.

**Fix**:
```bash
# Verify service account exists
gcloud iam service-accounts list

# Grant invoker role
gcloud functions add-iam-policy-binding library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/cloudfunctions.invoker"
```

---

## Verifying Authentication is Working

### Check Function IAM Policy

```bash
gcloud functions get-iam-policy library-assistant-webhook \
  --gen2 \
  --region=us-central1
```

You should see the DialogFlow CX service account with `roles/cloudfunctions.invoker`.

### Test with curl (Unauthenticated should fail)

```bash
# This should fail with 403 if authentication is enabled
curl -X POST FUNCTION_URL \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

If you get 403, authentication is working correctly!

### Check DialogFlow CX Webhook Settings

1. Go to DialogFlow CX > Fulfillment > Webhooks
2. Verify **"Enable OIDC Token"** is checked
3. Verify service account is selected

---

## Switching Between Authenticated and Unauthenticated

### Switch to Authenticated

```bash
# Redeploy without --allow-unauthenticated
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --no-allow-unauthenticated \
  --set-env-vars USE_MOCK_DATA=true
```

Then enable OIDC token in DialogFlow CX.

### Switch to Unauthenticated

```bash
# Redeploy with --allow-unauthenticated
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars USE_MOCK_DATA=true
```

Then disable OIDC token in DialogFlow CX (or leave it - it won't hurt).

---

## Best Practices

1. **Development**: Use unauthenticated for easier testing
2. **Production**: Always use authentication
3. **Service Accounts**: Use dedicated service accounts, not default
4. **Permissions**: Follow principle of least privilege
5. **Monitoring**: Monitor authentication failures in logs
6. **Testing**: Test authentication before going to production

---

## Quick Commands Reference

```bash
# Get project number
gcloud projects describe PROJECT_ID --format="value(projectNumber)"

# List service accounts
gcloud iam service-accounts list

# Check function IAM policy
gcloud functions get-iam-policy library-assistant-webhook \
  --gen2 \
  --region=us-central1

# Grant invoker role
gcloud functions add-iam-policy-binding library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/cloudfunctions.invoker"

# View function logs
gcloud functions logs read library-assistant-webhook \
  --gen2 \
  --region=us-central1 \
  --limit=50
```

---

For more details, see the main setup guide: `docs/setup-guide.md`
