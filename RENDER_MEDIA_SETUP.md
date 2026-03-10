# Render Media Files Setup Guide

## Problem
Render uses **ephemeral filesystems** - uploaded files (profile photos, QR codes) are deleted on each deployment or restart.

## Solution: Cloudflare R2 Storage

Cloudflare R2 is S3-compatible object storage with **zero egress fees** and generous free tier (10GB storage, 1M reads/month).

### Step 1: Create Cloudflare R2 Bucket

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **R2 Object Storage**
3. Click **Create bucket**
   - Bucket name: `thelastcard-media`
   - Location: Choose closest to your users
4. Click **Create bucket**

### Step 2: Generate R2 API Tokens

1. In R2 dashboard, click **Manage R2 API Tokens**
2. Click **Create API Token**
   - Token name: `thelastcard-render`
   - Permissions: **Object Read & Write**
   - Bucket: Select `thelastcard-media`
3. Save these credentials (you won't see them again):
   - **Access Key ID**
   - **Secret Access Key**
   - **Account ID** (found in R2 dashboard URL or settings)

### Step 3: Configure R2 Bucket CORS (Important!)

1. Open your bucket → **Settings** → **CORS Policy**
2. Add this JSON:

```json
[
  {
    "AllowedOrigins": [
      "https://your-render-app.onrender.com",
      "https://yourdomain.com"
    ],
    "AllowedMethods": [
      "GET",
      "PUT",
      "POST",
      "DELETE",
      "HEAD"
    ],
    "AllowedHeaders": [
      "*"
    ],
    "ExposeHeaders": [
      "ETag"
    ],
    "MaxAgeSeconds": 3600
  }
]
```

### Step 4: (Optional) Setup Custom Domain

1. In bucket settings, click **Connect Domain**
2. Add your subdomain: `media.yourdomain.com`
3. Add the CNAME record to your DNS:
   ```
   CNAME media -> [R2 endpoint]
   ```

### Step 5: Configure Render Environment Variables

Go to your Render dashboard → Your service → **Environment** and add:

```
USE_R2_STORAGE=True
R2_ACCOUNT_ID=your_r2_account_id
R2_ACCESS_KEY_ID=your_access_key_id  
R2_SECRET_ACCESS_KEY=your_secret_access_key
R2_BUCKET_NAME=thelastcard-media
R2_CUSTOM_DOMAIN=media.yourdomain.com  (optional, leave blank to use R2 URL)
```

### Step 6: Deploy

1. Commit your changes:
   ```bash
   git add render.yaml
   git commit -m "Configure R2 storage for media files"
   git push
   ```

2. Render will automatically redeploy

### Step 7: Verify

1. Upload a profile photo
2. Check that the image URL points to R2 (e.g., `https://media.yourdomain.com/profiles/...`)
3. Redeploy your app - images should persist

---

## Alternative: AWS S3 (If you prefer)

If you prefer AWS S3 instead of R2:

### Environment Variables:
```
USE_R2_STORAGE=False
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Settings Update Required:
Update `nfc_platform/settings.py` to support standard S3:

```python
if USE_R2_STORAGE:
    # Existing R2 config...
else:
    # Standard AWS S3
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    }
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
```

---

## Temporary Workaround (Not Recommended)

If you can't set up R2/S3 immediately, you can use Render's **persistent disks** (paid feature).

Add to `render.yaml`:
```yaml
services:
  - type: web
    # ...existing config...
    disk:
      name: media-storage
      mountPath: /opt/render/project/src/media
      sizeGB: 10
```

**Note**: This costs $0.25/GB/month and files persist across deploys, but not across region failures.

---

## Pricing Comparison

| Service | Free Tier | Cost After Free Tier |
|---------|-----------|---------------------|
| **Cloudflare R2** | 10GB storage, 1M reads/month, ZERO egress | $0.015/GB/month storage, $0 egress |
| **AWS S3** | 5GB for 12 months | $0.023/GB/month + egress fees |
| **Render Disk** | None | $0.25/GB/month |

**Recommended**: Cloudflare R2 for zero egress costs

---

## Troubleshooting

### Images not loading after R2 setup:
1. Check CORS policy is configured correctly
2. Verify env vars are set in Render dashboard
3. Check bucket is public or credentials are correct
4. Look at Render logs for boto3 errors

### QR codes not generating:
1. Check `media/qrcodes/` directory is being written to
2. Verify R2 has write permissions
3. Check Render logs for PIL/qrcode errors

### Profile photos not uploading:
1. Check file size limits in settings.py
2. Verify R2 bucket has sufficient storage
3. Check Django logs for upload errors
