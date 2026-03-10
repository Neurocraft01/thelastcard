# Admin Guide - The Last Card NFC Platform

## Table of Contents
1. [Admin Dashboard Overview](#admin-dashboard-overview)
2. [User Management](#user-management)
3. [Order Management](#order-management)
4. [Organization Management](#organization-management)
5. [Analytics & Reporting](#analytics--reporting)
6. [System Administration](#system-administration)
7. [Daily Operations](#daily-operations)
8. [Troubleshooting](#troubleshooting)

## Admin Dashboard Overview

### Access Levels

**Super Admin** - Platform Owner
- Full system access
- Manage all organizations
- User role assignments
- System settings
- Global analytics

**Admin** - Organization Manager
- Organization scope only
- Member management
- Organization orders
- Team analytics
- Limited settings

### Dashboard Sections
- **Overview**: Key metrics at a glance
- **Users**: Member management
- **Orders**: Physical card orders
- **Analytics**: Detailed insights
- **Organizations**: Company/team management
- **Settings**: Platform configuration

## User Management

### Creating New Users

**Manual Creation:**
1. Go to **Dashboard → Users → Add User**
2. Enter email, name, role
3. System sends invitation email
4. User sets password on first login

**Bulk Import:**
```bash
# Use Django admin for bulk operations
python manage.py createsuperuser
```

### User Roles Assignment

**Changing User Role:**
1. Navigate to **Users → All Users**
2. Click user name
3. Edit role field:
   - USER (default)
   - ADMIN (organization manager)
   - SUPER_ADMIN (platform owner)
4. Save changes

### User Verification
- New users: unverified by default
- Manually verify: User details → Mark as verified
- Email verification: Auto-verifies on email click

### Handling Locked Accounts
- Auto-lock after 5 failed login attempts
- Duration: 30 minutes
- Manual unlock: User details → Clear failed attempts
- Reset password: Send password reset link

## Order Management

### Order Workflow

**1. Order Received (Pending)**
- Customer places order
- Payment confirmation needed
- Review order details
- Check custom design requirements

**2. Design Approval (Processing)**
- Create design proof
- Send to customer for approval
- Wait for customer confirmation
- Make requested changes

**3. Production (Processing)**
- Send to manufacturer
- Production time: 3-5 business days
- Quality check upon completion

**4. Shipment (Shipped)**
- Package order
- Generate shipping label
- Update tracking number in system
- Send tracking email to customer

**5. Completion (Delivered)**
- Confirm delivery
- Request customer feedback
- Archive order

### Managing Orders

**View All Orders:**
```
Dashboard → Orders → All Orders
```

**Filter Orders:**
- By status (pending/processing/shipped/delivered)
- By date range
- By customer
- By card type

**Update Order Status:**
1. Click order number
2. Change status dropdown
3. Add internal notes
4. Save changes
5. Customer receives automatic email

**Add Tracking Number:**
1. Go to order details
2. Click "Add Tracking"
3. Enter courier and tracking number
4. Save - customer gets email notification

**Cancel Order:**
1. Open order details
2. Click "Cancel Order"
3. Enter cancellation reason
4. Confirm cancellation
5. Refund if payment received

### Order Priority

**Rush Orders:**
- Mark as priority in order notes
- Highlight in daily production list
- Expedite with manufacturer
- Use express shipping

**Bulk Orders:**
- Orders >50 cards need approval
- Check stock availability
- Confirm production timeline
- Provide bulk discount if applicable

## Organization Management

### Creating Organizations

1. **Dashboard → Organizations → Add New**
2. Enter organization details:
   - Name
   - Domain (optional)
   - Admin user
   - Billing information
3. Set member limit
4. Save organization

### Managing Organization Members

**Add Member:**
1. Go to organization page
2. Click "Add Member"
3. Enter user email
4. Assign role (User/Admin)
5. Send invitation

**Remove Member:**
1. Organization members list
2. Click member name
3. "Remove from Organization"
4. Confirm removal

**Transfer Ownership:**
1. Organization settings
2. "Transfer Admin"
3. Select new admin user
4. Confirm transfer
5. Previous admin becomes regular member

## Analytics & Reporting

### Available Reports

**User Analytics:**
- Total registered users
- Active users (last 30 days)
- User growth trends
- Most viewed profiles
- Engagement rates

**Order Analytics:**
- Total orders by status
- Revenue tracking
- Popular card types
- Average order value
- Order fulfillment time

**Organization Analytics:**
- Organization count
- Average members per org
- Organization growth
- Bulk order trends

### Generating Reports

**Profile Views Report:**
```bash
Dashboard → Analytics → Profile Views
Select date range → Export CSV
```

**Revenue Report:**
```bash
Dashboard → Analytics → Orders → Financial
Select month → Download PDF
```

**User Activity Report:**
```bash
Dashboard → Analytics → Users → Activity
Filter by date → Export
```

### Key Metrics to Monitor

Daily:
- New user registrations
- Pending orders (>24 hours)
- Failed login attempts
- System errors

Weekly:
- Order completion rate
- Average delivery time
- Customer satisfaction
- Profile completion rate

Monthly:
- Revenue vs target
- User retention
- Popular features
- Growth trends

## System Administration

### Django Admin Panel

**Access:**
```
https://yourdomain.com/admin
```

**Use Cases:**
- Bulk operations
- Database queries
- Advanced user management
- Direct model editing
- System logs review

### Database Management

**Backups:**
```bash
# Daily automated backups
# Manual backup command:
python manage.py dumpdata > backup.json
```

**Migrations:**
```bash
# Apply new migrations:
python manage.py migrate

# Check migration status:
python manage.py showmigrations
```

### Security Settings

**Password Policy:**
- Minimum 8 characters
- Must include letters and numbers
- Cannot be commonly used password
- Cannot be too similar to username

**Session Management:**
- Auto logout: 30 minutes inactive
- Force logout: User settings → Sessions
- Clear all sessions: Django admin

**Two-Factor Authentication:**
- Enable in user settings
- QR code generation
- Backup codes provided

### Email Configuration

**Test Email Delivery:**
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@email.com', ['to@email.com'])
```

**Email Templates:**
- Located in: `templates/email/`
- Customize branding
- Edit content carefully
- Test before deploying

## Daily Operations

### Morning Checklist
- [ ] Review new orders from last 24 hours
- [ ] Check pending orders for >24 hours
- [ ] Respond to support emails
- [ ] Review analytics dashboard
- [ ] Check system health

### Order Processing Routine
1. **9:00 AM** - Review new orders
2. **10:00 AM** - Send design proofs
3. **2:00 PM** - Process approved designs
4. **4:00 PM** - Update tracking numbers
5. **5:00 PM** - Follow up on pending approvals

### Weekly Tasks
- [ ] Generate revenue report
- [ ] Review user feedback
- [ ] Plan production schedule
- [ ] Stock inventory check
- [ ] System updates check

### Monthly Tasks
- [ ] Financial reconciliation
- [ ] Performance review
- [ ] Database cleanup
- [ ] Backup verification
- [ ] Security audit

## Troubleshooting

### Common User Issues

**"I can't access my account"**
1. Check if email verified
2. Check if account locked
3. Reset password
4. Clear failed login attempts
5. Verify email in system

**"My order hasn't moved"**
1. Check order status
2. Verify payment received
3. Check for design approval needed
4. Contact manufacturer
5. Update customer

**"Profile not showing"**
1. Verify profile is published
2. Check username is set
3. Clear cache
4. Check for errors in profile data

### System Issues

**Slow Performance**
```bash
# Check database size
python manage.py dbshell
.databases

# Optimize database
python manage.py optimize_db

# Clear cache
python manage.py clear_cache
```

**Email Not Sending**
1. Check SMTP credentials
2. Test connection
3. Review email logs
4. Check spam folder
5. Verify email service status

**File Upload Errors**
1. Check disk space
2. Verify file permissions
3. Check max upload size
4. Review error logs
5. Test with small file

### Emergency Procedures

**Site Down**
1. Check server status
2. Review error logs
3. Verify database connection
4. Contact hosting support
5. Restore from backup if needed

**Data Loss**
1. Don't panic - backups exist
2. Identify what was lost
3. Check backup timestamps
4. Restore from most recent
5. Verify data integrity

**Security Breach**
1. Immediately disable affected accounts
2. Change all admin passwords
3. Review access logs
4. Contact security team
5. Notify affected users
6. Document incident

## Best Practices

### Order Management
- Process orders within 24 hours
- Update tracking numbers same day
- Communicate delays proactively
- Keep detailed notes
- Archive completed orders monthly

### Customer Communication
- Respond within 4 hours (business hours)
- Use professional, friendly tone
- Always confirm understanding
- Set realistic expectations
- Follow up on issues

### Data Management
- Regular backups (daily automated)
- Clean old analytics (>1 year)
- Archive inactive users (>6 months)
- Monitor database size
- Document all major changes

### Security
- Use 2FA on your account
- Never share admin credentials
- Log out when leaving workstation
- Review user permissions quarterly
- Keep software updated

## Useful Commands

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# List all users
python manage.py shell
from accounts.models import User
User.objects.all()
```

### Order Management
```bash
# Export orders to CSV
python manage.py export_orders --start=2026-01-01 --end=2026-01-31

# Order statistics
python manage.py order_stats
```

### Analytics
```bash
# Generate analytics report
python manage.py generate_analytics_report --days=30

# Popular profiles
python manage.py top_profiles --limit=10
```

### Maintenance
```bash
# Database optimization
python manage.py optimize_db

# Clear old sessions
python manage.py clearsessions

# Collect static files
python manage.py collectstatic --noinput
```

## Support & Resources

### Internal Resources
- [Deployment Guide](DEPLOYMENT.md)
- [User Guide](USER_GUIDE.md)
- [README](README.md)

### External Support
- Django Documentation: https://docs.djangoproject.com
- Django REST Framework: https://www.django-rest-framework.org
- WhiteNoise: https://whitenoise.readthedocs.io

### Getting Help
- Email: admin-support@yourdomain.com
- Priority Response: Within 4 hours
- Emergency: Phone support

---

**Version**: 1.0.0  
**Last Updated**: February 3, 2026  
**Maintained By**: Platform Admin Team
