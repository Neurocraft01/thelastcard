# The Last Card — Implementation Guide

Complete setup guide for Supabase, Razorpay, Cloudflare R2 Storage, Themes, and Image Restrictions.

---

## Table of Contents
1. [Supabase (PostgreSQL Database)](#1-supabase-postgresql-database)
2. [Razorpay (Payment Gateway)](#2-razorpay-payment-gateway)
3. [Cloudflare R2 (Media Storage)](#3-cloudflare-r2-media-storage)
4. [Theme Selection](#4-theme-selection)
5. [Image Upload Restrictions (500KB)](#5-image-upload-restrictions-500kb)

---

## 1. Supabase (PostgreSQL Database)

### Step 1: Create a Supabase Project
1. Go to [https://supabase.com](https://supabase.com) and create an account.
2. Click **New Project** → Choose organization → Set project name and database password.
3. Select a region close to your users (e.g., `South Asia (Mumbai)` for India).
4. Wait for the project to finish provisioning.

### Step 2: Get Connection String
1. In Supabase Dashboard → **Settings** → **Database** → Scroll to **Connection string**.
2. Select **URI** tab.
3. Copy the connection string. It looks like:
   ```
   postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
4. Replace `[YOUR-PASSWORD]` with the database password you set.

### Step 3: Configure `.env`
Open the `.env` file and set:
```env
DATABASE_URL=postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
```

> **Note:** The app also supports Neon, Railway, or any PostgreSQL provider — just set the `DATABASE_URL` accordingly. If `DATABASE_URL` is empty or removed, it falls back to local SQLite.

### Step 4: Run Migrations
```bash
python manage.py migrate
```
This creates all the required tables in your Supabase database.

### Step 5: Create Super Admin
Run:
```bash
python manage.py createsuperuser
```
- Enter email and password when prompted.
- This automatically sets the user's role to **SUPER_ADMIN** (hardcoded in the UserManager).
- The super admin can access the Django admin panel at `/admin/` and the super admin dashboard at `/superadmin/dashboard/`.

### Step 6: Create Admin Users

**Option A — Via Django Admin Panel:**
1. Log in at `/admin/` as super admin.
2. Go to **Users** → **Add User** → Fill email/password.
3. Set the **Role** field to `ADMIN`.
4. Save.

**Option B — Via Super Admin Dashboard:**
1. Log in and go to `/superadmin/dashboard/`.
2. Click **Manage Admins** → **Add New Admin**.
3. Fill in the form (name, email, password).
4. The user is automatically created with the `ADMIN` role.

**Option C — Via Django Shell:**
```bash
python manage.py shell
```
```python
from accounts.models import User
admin = User.objects.create_user(
    email='admin@example.com',
    password='securepassword123',
    first_name='Admin',
    last_name='User'
)
admin.role = User.Role.ADMIN
admin.save()
```

### Role Permissions Summary
| Role | Dashboard | Can Manage |
|------|-----------|------------|
| **SUPER_ADMIN** | `/superadmin/dashboard/` | Admins, all users, all cards, themes, settings |
| **ADMIN** | `/admin-dashboard/` | Assigned users and their cards |
| **USER** | `/user/dashboard/` | Own profile, own cards |

---

## 2. Razorpay (Payment Gateway)

### Step 1: Create Razorpay Account
1. Go to [https://dashboard.razorpay.com](https://dashboard.razorpay.com) and sign up.
2. Complete KYC verification (required for live mode).

### Step 2: Get API Keys
1. In Razorpay Dashboard → **Settings** → **API Keys** → **Generate Key**.
2. Copy the **Key ID** (starts with `rzp_test_` for test mode, `rzp_live_` for live).
3. Copy the **Key Secret** (shown only once — save it securely).

### Step 3: Configure `.env`
```env
# Test mode (for development)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxx

# Live mode (for production)
# RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxx
# RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxx
```

### Step 4: Test Payment Flow
1. Start the dev server: `python manage.py runserver`
2. Go to the orders page and place a test order.
3. Use Razorpay test card: `4111 1111 1111 1111`, any future expiry, any CVV.
4. Payment goes through `OrderCreateView` → `OrderPaymentView` → `OrderPaymentCallbackView` with signature verification.

### Payment Flow Architecture
```
User selects card → OrderCreateView (creates Razorpay order)
                  → OrderPaymentView (shows Razorpay checkout popup)
                  → Razorpay processes payment
                  → OrderPaymentCallbackView (verifies signature, updates DB)
                  → Order confirmation page
```

### Card Pricing (configured in `orders/models.py`)
| Card Type | Price |
|-----------|-------|
| White PVC | ₹449 |
| Pink PVC | ₹449 |
| Metallic | ₹649 |

### Going Live
1. Complete KYC on Razorpay Dashboard.
2. Replace test keys with live keys in `.env`.
3. Set `DEBUG=False` in `.env`.

---

## 3. Cloudflare R2 (Media Storage)

All uploaded images (profile photos, cover photos, custom designs) are stored in R2 when enabled.

### Step 1: Create R2 Bucket
1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com).
2. Go to **R2 Object Storage** → **Create Bucket**.
3. Name it `nfc-platform` (or your preferred name).
4. Select the closest location.

### Step 2: Create API Token
1. In R2 page → **Manage R2 API Tokens** → **Create API Token**.
2. Set permissions to **Object Read & Write**.
3. Scope it to your bucket.
4. Copy:
   - **Access Key ID**
   - **Secret Access Key**
5. Note your **Account ID** from the Cloudflare Dashboard URL or R2 overview page.

### Step 3: Configure `.env`
```env
USE_R2_STORAGE=True
R2_ACCOUNT_ID=your_cloudflare_account_id
R2_ACCESS_KEY_ID=your_r2_access_key_id
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key
R2_BUCKET_NAME=nfc-platform
```

### Step 4: (Recommended) Set Up Custom Domain for Public Access
Without a custom domain, R2 files are only accessible via the S3 endpoint (which requires auth). For public access:

1. In Cloudflare Dashboard → **R2** → Your bucket → **Settings** → **Public Access**.
2. **Option A — R2.dev subdomain**: Enable the R2.dev subdomain (quick but no custom domain).
3. **Option B — Custom domain**: Add a custom domain like `media.thelastcard.in`.
   - Add CNAME record pointing to your R2 bucket.
4. Update `.env`:
   ```env
   R2_CUSTOM_DOMAIN=media.thelastcard.in
   ```

### Step 5: Test Upload
1. Start the server.
2. Upload a profile photo through the onboarding flow.
3. Check your R2 bucket in Cloudflare Dashboard — the file should appear.

### How It Works
- When `USE_R2_STORAGE=True`, Django's default file storage backend switches to `S3Boto3Storage`.
- All `ImageField` and `FileField` uploads go to R2.
- Files are served via the custom domain URL or R2 endpoint.
- Configuration is in `nfc_platform/settings.py` lines 275–330.

### Disabling R2 (Local Development)
Set `USE_R2_STORAGE=False` in `.env`. Files will be stored locally in the `media/` directory.

---

## 4. Theme Selection

### How Themes Work
- Themes are defined in the `themes.Theme` model with colors (primary, secondary, accent, background, text), background types, typography, and custom CSS.
- 10 default themes are pre-loaded (Professional, Dark Mode, Gradient, Minimal, Corporate, Creative, Nature, Sunset, Ocean, Elegant).

### Loading Default Themes
```bash
python manage.py shell
```
```python
from themes.models import Theme
Theme.create_defaults()
```

### Managing Themes
- **Super Admin**: Can create/edit/delete themes via Django admin at `/admin/themes/theme/`.
- **Users**: Select a theme during onboarding (Step 3) and can change it from the dashboard card page.

### User Theme Selection Flow
1. **Onboarding**: Users pick a theme during profile setup (Theme Selection step).
2. **Dashboard**: Users can change their theme from the **My Card** page → Theme Selection section.
3. **Public Profile**: The selected theme's colors are applied as CSS variables to the public profile page.

### Creating a Custom Theme (Admin Panel)
1. Go to `/admin/themes/theme/add/`
2. Fill in:
   - **Name**: Theme name
   - **Primary/Secondary/Accent colors**: Hex color codes (e.g., `#6366f1`)
   - **Background color/Text color**: Page colors
   - **Background type**: Solid, Gradient, or Image
   - **Is premium**: Check to restrict to premium plans
   - **Is active / Is public**: Must be checked for users to see it

---

## 5. Image Upload Restrictions (500KB)

### Where Enforcement Happens

| Layer | Location | What Happens |
|-------|----------|--------------|
| **Client-side JS** | All templates with file inputs | Alert shown, file input cleared if > 500KB |
| **Django View** | `ProfileSetupView.post()` in `accounts/views.py` | Returns error message, prevents save |
| **Django Model** | `validate_image_size()` in `profiles/models.py` | `ValidationError` on `profile_photo` & `cover_photo` fields |
| **Order Form** | `clean_custom_design()` in `orders/forms.py` | Rejects custom design files > 500KB |
| **Global Setting** | `FILE_UPLOAD_MAX_MEMORY_SIZE` in `settings.py` | Hard limit at 2MB for any single upload |

### Templates with Client-Side Validation
- `templates/onboarding/profile_setup.html` — Profile photo + Cover photo
- `templates/dashboard/user/profile.html` — Profile photo + Cover photo
- `templates/accounts/profile.html` — Profile photo

### Changing the Limit
To change from 500KB to a different limit:
1. **Client-side**: Search for `512000` in templates and change the value (bytes).
2. **Server-side view**: Update the `500 * 1024` check in `accounts/views.py` → `ProfileSetupView.post()`.
3. **Model validator**: Update `512000` in `profiles/models.py` → `validate_image_size()`.
4. **Order form**: Update `512000` in `orders/forms.py` → `clean_custom_design()`.

---

## Quick Start Checklist

```
1. [ ] Set DATABASE_URL in .env (Supabase/Neon/PostgreSQL)
2. [ ] Run: python manage.py migrate
3. [ ] Run: python manage.py createsuperuser (creates Super Admin)
4. [ ] Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env
5. [ ] Set R2 credentials in .env and set USE_R2_STORAGE=True
6. [ ] Set R2_CUSTOM_DOMAIN for public media access
7. [ ] Load default themes: python manage.py shell → Theme.create_defaults()
8. [ ] Test: Upload profile photo (should enforce 500KB limit)
9. [ ] Test: Place test order with Razorpay test card
10. [ ] For production: Set DEBUG=False, use live Razorpay keys
```

---

## Environment Variables Reference

```env
# Database
DATABASE_URL=postgresql://...

# Razorpay
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...

# Cloudflare R2
USE_R2_STORAGE=True
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=nfc-platform
R2_CUSTOM_DOMAIN=media.thelastcard.in

# Django
DEBUG=True
SECRET_KEY=your-secret-key-min-50-chars
ALLOWED_HOSTS=localhost,127.0.0.1,thelastcard.in
```
