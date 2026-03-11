"""
Custom storage backends for Cloudflare R2 (S3-compatible).

Cloudflare R2 is S3-compatible but differs from AWS S3 in key ways:
- No ACL support (bucket-level public access via R2 dashboard)
- Uses 'auto' region
- Requires S3v4 signing
- Endpoint format: https://{account_id}.r2.cloudflarestorage.com
"""

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class R2MediaStorage(S3Boto3Storage):
    """
    Storage backend for user-uploaded media files stored in Cloudflare R2.

    Files are stored under the 'media/' prefix in the R2 bucket.
    Public access is served via the custom domain (if configured) or the
    R2 public bucket URL.
    """

    location = "media"
    file_overwrite = False   # Preserve existing files; append suffix on conflict
    default_acl = None       # R2 does not support per-object ACLs


class R2StaticStorage(S3Boto3Storage):
    """
    Optional storage backend for static files stored in Cloudflare R2.

    Only use this if you prefer serving static assets from R2 instead of
    WhiteNoise (the default). Files are stored under 'static/' in the bucket.
    """

    location = "static"
    default_acl = None
