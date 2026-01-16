# Library Assistant - Deployment Guide

## Overview

This guide covers deploying the professional Library Assistant to production, including best practices, monitoring, and maintenance.

## Pre-Deployment Checklist

- [ ] All flows configured and tested
- [ ] Intents created with sufficient training phrases
- [ ] Entities configured with synonyms
- [ ] Webhook deployed and tested
- [ ] Knowledge base configured (if using)
- [ ] Rich responses tested
- [ ] Error handling verified
- [ ] Authentication flow working
- [ ] All integrations tested

## Deployment Steps

### 1. Production Environment Setup

```bash
# Create production project (if separate)
gcloud projects create library-assistant-prod --name="Library Assistant Production"

# Set project
gcloud config set project library-assistant-prod

# Enable billing
# (Do this in GCP Console)

# Enable APIs
gcloud services enable dialogflow.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### 2. Deploy Cloud Functions (Production)

```bash
cd cloud-functions

# Set production environment variables
export LIBRARY_API_URL="https://api.library.production.com"
export LIBRARY_API_KEY="production-api-key"
export USE_MOCK_DATA="false"

# Deploy with production settings
gcloud functions deploy library-assistant-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=handle_webhook \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars LIBRARY_API_URL=$LIBRARY_API_URL,LIBRARY_API_KEY=$LIBRARY_API_KEY,USE_MOCK_DATA=false \
  --timeout=60s \
  --memory=512MB \
  --max-instances=100 \
  --min-instances=1 \
  --service-account=library-assistant@PROJECT_ID.iam.gserviceaccount.com
```

### 3. Configure DialogFlow CX Agent (Production)

1. **Create Production Agent**
   - Use separate agent for production
   - Configure with production settings
   - Set appropriate location and timezone

2. **Import/Configure Flows**
   - Import flows from development
   - Update webhook URLs to production
   - Verify all configurations

3. **Set Up Knowledge Base**
   - Configure production knowledge base
   - Test knowledge connector
   - Verify FAQ responses

4. **Configure Rich Responses**
   - Test all card responses
   - Verify list responses
   - Test quick replies

### 4. Security Configuration

#### 4.1 Authentication

```bash
# Create service account
gcloud iam service-accounts create library-assistant \
  --display-name="Library Assistant Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:library-assistant@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/dialogflow.client"
```

#### 4.2 API Security

- Enable API key restrictions
- Configure CORS if needed
- Set up rate limiting
- Enable audit logging

#### 4.3 Data Privacy

- Ensure PII handling compliance
- Configure data retention policies
- Set up data encryption
- Enable access logging

### 5. Monitoring Setup

#### 5.1 Cloud Functions Monitoring

```bash
# Set up alerting
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Library Assistant Error Rate" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

#### 5.2 DialogFlow CX Analytics

1. Enable conversation analytics
2. Set up custom metrics
3. Configure dashboards
4. Set up alerts

#### 5.3 Application Monitoring

- Set up error tracking
- Monitor response times
- Track user satisfaction
- Monitor API usage

### 6. Testing in Production

#### 6.1 Smoke Tests

```bash
# Test webhook endpoint
curl -X POST https://PRODUCTION_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "sessionInfo": {
      "session": "test-session",
      "parameters": {}
    },
    "intentInfo": {
      "displayName": "Greeting"
    }
  }'
```

#### 6.2 Integration Tests

- Test all flows end-to-end
- Verify webhook responses
- Test error scenarios
- Verify authentication

#### 6.3 Load Testing

- Test concurrent users
- Verify performance under load
- Check resource utilization
- Monitor response times

### 7. Go-Live Checklist

- [ ] Production webhook deployed
- [ ] Production agent configured
- [ ] All flows tested
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Documentation updated
- [ ] Team trained
- [ ] Rollback plan ready
- [ ] Support channels ready

## Post-Deployment

### 1. Monitor Initial Usage

- Watch error rates
- Monitor response times
- Track user interactions
- Review logs

### 2. Gather Feedback

- Collect user feedback
- Monitor satisfaction metrics
- Track common issues
- Identify improvement areas

### 3. Iterate and Improve

- Add more training phrases
- Improve responses
- Fix identified issues
- Add requested features

## Maintenance

### Regular Tasks

1. **Weekly**
   - Review error logs
   - Check performance metrics
   - Review user feedback

2. **Monthly**
   - Update training phrases
   - Add new intents if needed
   - Review and optimize flows
   - Update knowledge base

3. **Quarterly**
   - Comprehensive testing
   - Performance optimization
   - Security review
   - Documentation update

### Monitoring Metrics

- **Response Time**: Target < 2 seconds
- **Error Rate**: Target < 1%
- **User Satisfaction**: Track via feedback
- **Intent Recognition**: Monitor accuracy
- **Webhook Success Rate**: Target > 99%

## Troubleshooting

### Common Production Issues

1. **High Error Rate**
   - Check Cloud Functions logs
   - Verify API connectivity
   - Check resource limits

2. **Slow Response Times**
   - Optimize webhook code
   - Check API response times
   - Consider caching

3. **Intent Recognition Issues**
   - Add more training phrases
   - Review entity matching
   - Check intent priority

4. **Webhook Failures**
   - Verify webhook URL
   - Check authentication
   - Review function logs

## Rollback Plan

### If Issues Occur

1. **Immediate Actions**
   - Disable problematic flows
   - Revert to previous version
   - Notify users if needed

2. **Rollback Steps**
   ```bash
   # Rollback Cloud Function
   gcloud functions deploy library-assistant-webhook \
     --gen2 \
     --region=us-central1 \
     --source=. \
     --entry-point=handle_webhook \
     --trigger-http \
     --allow-unauthenticated
   ```

3. **Agent Rollback**
   - Restore previous agent version
   - Or disable specific flows
   - Update webhook if needed

## Best Practices

1. **Version Control**
   - Use version control for configurations
   - Tag releases
   - Maintain changelog

2. **Testing**
   - Test in staging first
   - Use canary deployments
   - Monitor closely after deployment

3. **Documentation**
   - Keep documentation updated
   - Document changes
   - Maintain runbooks

4. **Communication**
   - Notify team of deployments
   - Communicate changes to users
   - Provide support channels

## Resources

- [DialogFlow CX Deployment Guide](https://cloud.google.com/dialogflow/cx/docs)
- [Cloud Functions Best Practices](https://cloud.google.com/functions/docs/best-practices)
- Project documentation in `docs/` directory

---

**Ready for Production!** Follow this guide to ensure a smooth deployment and ongoing operation.
