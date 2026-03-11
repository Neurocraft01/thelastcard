# Pre-Launch Checklist - The Last Card NFC Platform

## Critical Priority (Must Complete Before Launch)

### Security ✅ CRITICAL
- [ ] Change `DEBUG=False` in production `.env`
- [ ] Generate new SECRET_KEY (50+ characters)
- [ ] Update `ALLOWED_HOSTS` with production domain
- [ ] Remove `.env` from repository (check .gitignore)
- [ ] Change all default admin passwords
- [ ] Enable HTTPS/SSL certificate
- [ ] Verify `SECURE_SSL_REDIRECT=True` when SSL active
- [ ] Set `SECURE_HSTS_SECONDS=31536000`
- [ ] Configure CSRF_TRUSTED_ORIGINS with production URLs
- [ ] Review all user permissions and roles
- [ ] Disable or secure Django admin panel (`/admin`)
- [ ] Remove any test/demo accounts
- [ ] Verify email credentials are production (not Gmail app password)

### Database 🔥 CRITICAL
- [ ] Backup current SQLite database
- [ ] Set up production PostgreSQL/Neon database
- [ ] Update DATABASE_URL in production `.env`
- [ ] Run `python manage.py migrate` on production
- [ ] Create production superuser account
- [ ] Verify all 23 migrations applied
- [ ] Set up automated daily backups
- [ ] Test database connection from application

### Static Files & Media 📦 CRITICAL
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Verify WhiteNoise is serving static files correctly
- [ ] Test static file loading on production URL
- [ ] Set up media file storage (R2/S3 or local with backups)
- [ ] Verify logo uploads work
- [ ] Test QR code generation
- [ ] Check profile photo uploads
- [ ] Test custom card design uploads

### Email Configuration 📧 CRITICAL
- [ ] Configure production SMTP server (not Gmail)
- [ ] Update EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
- [ ] Test order confirmation emails
- [ ] Test password reset emails
- [ ] Test new user registration emails
- [ ] Verify email FROM address is professional
- [ ] Check spam folder for test emails
- [ ] Set up email sending limits/quotas

## High Priority (Complete During Launch Day)

### Testing & Validation
- [ ] **User Registration Flow**
  - [ ] Register new account
  - [ ] Verify email received
  - [ ] Confirm email verification works
  - [ ] Complete profile setup

- [ ] **Profile Creation & Editing**
  - [ ] Upload profile photo
  - [ ] Add all contact information
  - [ ] Add social media links
  - [ ] Save and verify changes persist
  - [ ] View public profile URL

- [ ] **Order Processing**
  - [ ] Create test order (all 4 card types)
  - [ ] Verify order total calculation
  - [ ] Test custom design upload
  - [ ] Verify order confirmation email
  - [ ] Test order status updates

- [ ] **Authentication & Permissions**
  - [ ] Test User role access (can only see own data)
  - [ ] Test Admin role access (organization scope)
  - [ ] Test Super Admin access (full platform)
  - [ ] Verify login/logout works
  - [ ] Test password reset flow
  - [ ] Test "Remember Me" functionality

- [ ] **Analytics Tracking**
  - [ ] Visit public profile
  - [ ] Verify view is tracked
  - [ ] Check analytics dashboard updates
  - [ ] Test "Save Contact" tracking
  - [ ] Test social link click tracking

- [ ] **Mobile Responsiveness**
  - [ ] Test on iPhone Safari
  - [ ] Test on Android Chrome
  - [ ] Test on tablet
  - [ ] Verify QR code scanning works
  - [ ] Check mobile dashboard layout

- [ ] **Cross-Browser Testing**
  - [ ] Google Chrome (latest)
  - [ ] Mozilla Firefox (latest)
  - [ ] Safari (latest)
  - [ ] Microsoft Edge (latest)

### Performance Optimization
- [ ] Run `python manage.py check --deploy` (0 issues expected)
- [ ] Test page load speed (<3 seconds)
- [ ] Verify images are optimized
- [ ] Check database query performance
- [ ] Enable gzip compression
- [ ] Configure CDN if using R2/S3
- [ ] Set up Redis cache (optional but recommended)
- [ ] Test under load (100+ concurrent users)

### Content & Branding
- [ ] Replace all placeholder text
- [ ] Verify company logo appears correctly
- [ ] Check footer links work
- [ ] Update "About Us" page
- [ ] Update "Contact" page with real info
- [ ] Verify pricing page is accurate
- [ ] Check terms of service
- [ ] Verify privacy policy is updated
- [ ] Test contact form submission

## Medium Priority (Complete Within First Week)

### Monitoring & Analytics
- [ ] Set up error tracking (Sentry recommended)
- [ ] Configure uptime monitoring (UptimeRobot/Pingdom)
- [ ] Set up Google Analytics or similar
- [ ] Configure email alerts for errors
- [ ] Set up server resource monitoring
- [ ] Create admin alert for pending orders >24hrs
- [ ] Set up database size monitoring

### Documentation
- [ ] Review and finalize USER_GUIDE.md
- [ ] Review and finalize ADMIN_GUIDE.md
- [ ] Create video tutorial for users (optional)
- [ ] Document custom admin procedures
- [ ] Create FAQ page
- [ ] Write customer support scripts
- [ ] Document order fulfillment workflow

### Business Operations
- [ ] Set up payment processing (if not manual)
- [ ] Configure invoice generation
- [ ] Set up accounting integration
- [ ] Create order fulfillment checklist
- [ ] Establish SLA (Service Level Agreement)
- [ ] Create customer support email
- [ ] Set up feedback collection system

### Marketing & SEO
- [ ] Add meta descriptions to all pages
- [ ] Verify Open Graph tags for social sharing
- [ ] Create sitemap.xml
- [ ] Submit to Google Search Console
- [ ] Set up Google My Business
- [ ] Create social media accounts
- [ ] Prepare launch announcement

## Low Priority (Can Complete Post-Launch)

### Nice-to-Have Features
- [ ] Set up two-factor authentication for admins
- [ ] Add bulk user import tool
- [ ] Create automated monthly reports
- [ ] Set up A/B testing
- [ ] Add live chat support
- [ ] Create mobile app (future)
- [ ] Add payment gateway integration
- [ ] Set up referral program

### Advanced Analytics
- [ ] Heatmap tracking
- [ ] User session recordings
- [ ] Conversion funnel analysis
- [ ] Cohort analysis
- [ ] Advanced reporting dashboard

## Pre-Launch Testing Scenarios

### Scenario 1: New User Journey
1. Land on homepage
2. Click "Register"
3. Fill registration form
4. Verify email
5. Complete profile
6. View public profile
7. Share profile link
8. Check analytics

### Scenario 2: Order Flow
1. Login as user
2. Navigate to "Order Cards"
3. Select card type
4. Enter quantity
5. Upload custom design
6. Fill shipping information
7. Place order
8. Receive confirmation email
9. Admin reviews order
10. Admin updates status
11. User receives tracking email

### Scenario 3: Admin Operations
1. Login as admin
2. View all orders
3. Filter pending orders
4. Update order status
5. Add tracking number
6. View organization analytics
7. Export report
8. Manage team members

## Launch Day Checklist

### 2 Hours Before Launch
- [ ] Final database backup
- [ ] Verify all environment variables
- [ ] Clear test data
- [ ] Run final migrations
- [ ] Collect static files
- [ ] Test production URL works
- [ ] Verify SSL certificate active

### 1 Hour Before Launch
- [ ] Create monitoring dashboard
- [ ] Test critical user flows
- [ ] Verify email sending works
- [ ] Check error logging active
- [ ] Test from different networks
- [ ] Have rollback plan ready

### At Launch (Go-Live Moment)
- [ ] Switch DNS to production server
- [ ] Verify site loads on production domain
- [ ] Test registration immediately
- [ ] Monitor error logs in real-time
- [ ] Have team on standby
- [ ] Send launch announcement

### 1 Hour After Launch
- [ ] Monitor server resources
- [ ] Check for any errors
- [ ] Test all critical features
- [ ] Verify emails are sending
- [ ] Monitor user registrations
- [ ] Check analytics tracking

### 24 Hours After Launch
- [ ] Review error logs
- [ ] Check user feedback
- [ ] Monitor order volume
- [ ] Verify backups ran
- [ ] Review performance metrics
- [ ] Plan next improvements

## Rollback Plan

If critical issues occur within first 24 hours:

1. **Immediate Actions**
   - Put up maintenance page
   - Stop accepting new orders
   - Document the issue

2. **Assessment** (5-10 minutes)
   - Identify severity
   - Determine if fixable quickly
   - Check data integrity

3. **Decision Point**
   - **Fix Forward**: If issue is minor and fixable <30 min
   - **Rollback**: If issue is critical or unfixable quickly

4. **Rollback Procedure**
   ```bash
   # Restore database backup
   pg_restore -d database_name backup.dump
   
   # Revert to previous code version
   git revert HEAD
   
   # Deploy previous version
   git push production previous-stable-branch
   
   # Verify rollback successful
   curl https://yourdomain.com
   ```

5. **Post-Rollback**
   - Notify users via email
   - Fix issue in staging
   - Re-test thoroughly
   - Schedule re-launch

## Support Contacts

### Technical Team
- **Developer**: your-email@domain.com
- **DevOps**: devops@domain.com (if separate)
- **Database Admin**: dba@domain.com (if separate)

### Hosting/Infrastructure
- **Hosting Provider**: Railway/Render/VPS provider support
- **DNS Provider**: Your DNS provider support
- **SSL Certificate**: Certbot/Let's Encrypt support

### Third-Party Services
- **Email Provider**: SMTP service support
- **Storage Provider**: R2/S3 support (if used)
- **Monitoring**: Sentry/Uptime Robot support

## Success Criteria

Launch is successful when:
- ✅ Site loads without errors
- ✅ New users can register and create profiles
- ✅ Orders can be placed and processed
- ✅ Emails are sending correctly
- ✅ Analytics tracking works
- ✅ No critical security issues
- ✅ Performance is acceptable (<3s load time)
- ✅ Mobile experience is good
- ✅ 0 critical bugs in first 24 hours

## Post-Launch Monitoring (First Week)

### Daily Checks
- [ ] Review error logs every morning
- [ ] Check pending orders status
- [ ] Monitor server resources (CPU, memory, disk)
- [ ] Respond to user feedback
- [ ] Track registration rate

### Metrics to Watch
- New user registrations per day
- Order placement rate
- Average order value
- Page load times
- Error rate
- Email delivery rate
- Mobile vs desktop traffic
- Most viewed profiles

---

## Final Verification Commands

Run these on production server before launch:

```bash
# System check
python manage.py check --deploy

# Migration status
python manage.py showmigrations

# Collect static files
python manage.py collectstatic --noinput --clear

# Test database connection
python manage.py dbshell
\q

# Test email
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Production test', 'from@domain.com', ['to@domain.com'])
exit()
```

All checks should pass with 0 errors (warnings about HSTS/SSL are OK if DEBUG=False).

---

**Remember**: Better to delay launch by a day than launch with critical issues!

**Good luck with your launch! 🚀**

---

**Version**: 1.0.0  
**Last Updated**: February 3, 2026
