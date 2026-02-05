# Testing Guide - The Last Card NFC Platform

## Table of Contents
1. [Testing Strategy](#testing-strategy)
2. [Manual Testing Checklist](#manual-testing-checklist)
3. [Automated Testing](#automated-testing)
4. [Load Testing](#load-testing)
5. [Security Testing](#security-testing)
6. [Bug Reporting](#bug-reporting)

## Testing Strategy

### Testing Environment
- **Development**: Local machine with DEBUG=True
- **Staging**: Production-like environment with DEBUG=False
- **Production**: Live environment

### Testing Levels
1. **Unit Tests**: Individual functions and methods
2. **Integration Tests**: Multiple components working together
3. **End-to-End Tests**: Complete user workflows
4. **Performance Tests**: Load and stress testing
5. **Security Tests**: Vulnerability scanning

## Manual Testing Checklist

### 1. User Registration & Authentication

#### Registration Flow
- [ ] Navigate to registration page
- [ ] Enter valid username (letters, numbers, underscores)
- [ ] Enter valid email address
- [ ] Enter strong password (8+ chars, letters, numbers, special chars)
- [ ] Enter matching password confirmation
- [ ] Check "Accept Terms" checkbox
- [ ] Submit form
- [ ] Verify success message appears
- [ ] Check email inbox for verification email
- [ ] Click verification link in email
- [ ] Verify redirect to login or dashboard

#### Registration Validation
- [ ] Try username with spaces → Should show error
- [ ] Try username with special characters → Should show error
- [ ] Try duplicate username → Should show "already taken" error
- [ ] Try duplicate email → Should show "already exists" error
- [ ] Try mismatched passwords → Should show "passwords do not match"
- [ ] Try weak password (e.g., "12345678") → Should show password strength error
- [ ] Submit without accepting terms → Should show "must accept terms" error

#### Login Flow
- [ ] Navigate to login page
- [ ] Enter registered email
- [ ] Enter correct password
- [ ] Check "Remember Me" (optional)
- [ ] Submit form
- [ ] Verify redirect to dashboard
- [ ] Verify user name shown in navbar

#### Login Validation
- [ ] Try wrong password → Should show "invalid credentials"
- [ ] Try wrong email → Should show "invalid credentials"
- [ ] Try 5 failed attempts → Account should lock for 30 minutes
- [ ] Verify locked account shows appropriate message

#### Password Reset
- [ ] Click "Forgot Password" link
- [ ] Enter registered email
- [ ] Submit form
- [ ] Check email for password reset link
- [ ] Click reset link
- [ ] Enter new password
- [ ] Enter matching confirmation
- [ ] Submit form
- [ ] Verify success message
- [ ] Try logging in with new password → Should work
- [ ] Try using reset link again → Should show "link expired" or "already used"

#### Logout
- [ ] Click logout button
- [ ] Verify redirect to home page
- [ ] Try accessing dashboard directly → Should redirect to login

### 2. Profile Management

#### Profile Creation
- [ ] Log in to dashboard
- [ ] Navigate to "Edit Profile"
- [ ] Upload profile photo (JPG, max 5MB)
- [ ] Enter full name
- [ ] Enter job title/designation
- [ ] Write bio (max 500 characters)
- [ ] Enter company name
- [ ] Enter location
- [ ] Enter phone number
- [ ] Enter public email
- [ ] Enter website URL
- [ ] Fill shipping address (all fields)
- [ ] Add LinkedIn URL
- [ ] Add Instagram URL
- [ ] Add Twitter URL
- [ ] Add other social URLs
- [ ] Enter WhatsApp number
- [ ] Save profile
- [ ] Verify success message

#### Profile Validation
- [ ] Upload file > 5MB → Should show error
- [ ] Upload PDF as photo → Should show "invalid image" error
- [ ] Enter invalid phone (e.g., "abc") → Should show error
- [ ] Enter invalid email format → Should show error
- [ ] Enter invalid URL (e.g., "not-a-url") → Should show error
- [ ] Enter bio > 500 chars → Should show error
- [ ] Leave all contact fields empty → Should show "at least one required"
- [ ] Try very long name (200+ chars) → Should truncate or show error

#### Profile Display
- [ ] Click "View My Profile"
- [ ] Verify all information displays correctly
- [ ] Verify profile photo shows
- [ ] Verify social links work and open in new tab
- [ ] Verify save contact button appears
- [ ] Verify WhatsApp button appears (if number provided)

#### Profile Completion
- [ ] Check completion percentage in dashboard
- [ ] Verify it increases as you add more info
- [ ] Fill all fields → Should reach 100%

### 3. NFC Card Management

#### Create NFC Card
- [ ] Navigate to "My Cards" or "Create Card"
- [ ] Enter custom URL slug (e.g., "john-doe")
- [ ] Select theme (if available)
- [ ] Submit form
- [ ] Verify success message
- [ ] Verify card appears in "My Cards" list

#### Card Validation
- [ ] Try URL with uppercase → Should convert to lowercase
- [ ] Try URL with spaces → Should show error
- [ ] Try URL with special chars → Should show error
- [ ] Try URL < 3 characters → Should show error
- [ ] Try URL > 50 characters → Should show error
- [ ] Try reserved URL (e.g., "admin") → Should show "reserved" error
- [ ] Try duplicate URL → Should show "already taken" error

#### View Public Card
- [ ] Copy public URL (e.g., yourdomain.com/c/john-doe)
- [ ] Open in new incognito window
- [ ] Verify profile displays correctly
- [ ] Verify theme is applied (if selected)
- [ ] Test "Save Contact" button → vCard should download
- [ ] Test QR code displays
- [ ] Test social links work

#### QR Code
- [ ] View QR code in dashboard
- [ ] Download QR code
- [ ] Scan QR code with phone → Should open public profile
- [ ] Verify QR loads on public profile page

### 4. Order Management

#### Create Order (User Flow)
- [ ] Navigate to "Order Cards"
- [ ] Select card type: Standard PVC
- [ ] Enter quantity: 10
- [ ] Upload custom design (PNG, 2MB)
- [ ] Enter custom text: "John Doe - CEO"
- [ ] Verify shipping address auto-fills from profile
- [ ] Modify shipping address if needed
- [ ] Add order notes
- [ ] Review order summary
- [ ] Verify total price calculation (10 × ₹499 = ₹4,990)
- [ ] Submit order
- [ ] Verify success message
- [ ] Verify confirmation email received

#### Order Validation
- [ ] Try quantity = 0 → Should show error
- [ ] Try quantity = 101 → Should show error
- [ ] Try quantity = -5 → Should show error
- [ ] Upload design > 5MB → Should show error
- [ ] Upload PDF file → Should show "invalid image" error
- [ ] Leave shipping address empty → Should show error
- [ ] Enter address < 20 chars → Should show error

#### Order List
- [ ] Navigate to "My Orders"
- [ ] Verify all orders display
- [ ] Verify order details shown (card type, quantity, status, date)
- [ ] Click order to view details
- [ ] Verify all order information displays

#### Order Status Updates
- [ ] Check order status: "Pending"
- [ ] Wait for admin to update (or have admin update)
- [ ] Check status changes: Processing → Shipped → Delivered
- [ ] Verify email notification for each status change
- [ ] Verify tracking number displays when status = "Shipped"

#### Order Types
Test all 2 card types:
- [ ] Standard PVC (₹449) - Verify total = quantity × 449
- [ ] Metallic Premium (₹649) - Verify total = quantity × 649

### 5. Analytics Tracking

#### View Tracking
- [ ] Open public profile in incognito
- [ ] Wait 5 seconds
- [ ] Go back to dashboard
- [ ] Navigate to "Analytics"
- [ ] Verify view count increased by 1
- [ ] Verify today's date shows in views list

#### Interaction Tracking
- [ ] Open public profile
- [ ] Click "Save Contact" button
- [ ] Go to analytics
- [ ] Verify "Contact Saves" count increased
- [ ] Click phone number
- [ ] Verify "Phone Clicks" count increased
- [ ] Click email address
- [ ] Verify "Email Clicks" count increased
- [ ] Click website link
- [ ] Verify "Website Clicks" count increased
- [ ] Click social media link
- [ ] Verify social click tracked

#### Analytics Dashboard
- [ ] Verify total views shows correctly
- [ ] Verify unique visitors count
- [ ] Verify chart/graph displays (if implemented)
- [ ] Verify date range filter works (if implemented)
- [ ] Export analytics data (if available)

### 6. Admin Dashboard

#### User Management (Admin/Super Admin)
- [ ] Log in as admin
- [ ] Navigate to user management
- [ ] View all users list
- [ ] Search for specific user
- [ ] Click user to view details
- [ ] Change user role (User → Admin)
- [ ] Verify role change persists
- [ ] Deactivate user account
- [ ] Reactivate user account
- [ ] Reset user password

#### Order Management (Admin)
- [ ] View all orders (not just own)
- [ ] Filter orders by status
- [ ] Filter orders by date
- [ ] Filter orders by card type
- [ ] Click order to view details
- [ ] Change order status to "Processing"
- [ ] Verify customer receives email
- [ ] Add tracking number
- [ ] Change status to "Shipped"
- [ ] Verify tracking email sent
- [ ] Mark order as "Delivered"

#### Organization Management (Super Admin)
- [ ] Create new organization
- [ ] Add members to organization
- [ ] Assign organization admin
- [ ] View organization analytics
- [ ] Remove member from organization
- [ ] Delete organization

#### Analytics Overview (Admin)
- [ ] View platform-wide analytics
- [ ] See total users count
- [ ] See total orders count
- [ ] See revenue summary
- [ ] View most popular profiles
- [ ] Export reports

### 7. Responsive Design

#### Desktop (1920×1080)
- [ ] Home page looks good
- [ ] Dashboard has proper layout
- [ ] Forms are properly sized
- [ ] Images load correctly
- [ ] Navigation is accessible

#### Tablet (768×1024)
- [ ] Test in portrait mode
- [ ] Test in landscape mode
- [ ] Verify responsive layout adapts
- [ ] Verify touch interactions work
- [ ] Verify forms are usable

#### Mobile (375×667 - iPhone SE)
- [ ] Home page is mobile-friendly
- [ ] Login/register forms work
- [ ] Dashboard is accessible
- [ ] Profile editing works
- [ ] Order creation works
- [ ] Hamburger menu (if applicable) works
- [ ] All buttons are tappable
- [ ] Forms don't require horizontal scrolling

### 8. Cross-Browser Testing

#### Google Chrome (Latest)
- [ ] All features work
- [ ] Styling is correct
- [ ] No console errors
- [ ] Forms submit properly
- [ ] File uploads work

#### Mozilla Firefox (Latest)
- [ ] All features work
- [ ] Styling is correct
- [ ] No console errors
- [ ] Forms submit properly
- [ ] File uploads work

#### Safari (Latest)
- [ ] All features work
- [ ] Styling is correct
- [ ] No console errors
- [ ] Forms submit properly
- [ ] File uploads work

#### Microsoft Edge (Latest)
- [ ] All features work
- [ ] Styling is correct
- [ ] No console errors
- [ ] Forms submit properly
- [ ] File uploads work

### 9. Error Handling

#### 404 Page
- [ ] Navigate to non-existent URL (e.g., /this-does-not-exist)
- [ ] Verify custom 404 page appears
- [ ] Verify "Go Home" button works
- [ ] Verify styling matches site

#### 500 Page
- [ ] Trigger server error (if possible in staging)
- [ ] Verify custom 500 page appears
- [ ] Verify no sensitive information displayed

#### Form Errors
- [ ] Submit empty required field → See inline error
- [ ] Submit invalid email → See format error
- [ ] File upload error → See descriptive message
- [ ] Network error → See retry option

#### Permission Errors
- [ ] Try accessing admin panel as regular user → Denied
- [ ] Try viewing another user's order → Denied or 404
- [ ] Try editing another user's profile → Denied

### 10. Email Testing

#### Email Delivery
- [ ] Registration confirmation email
- [ ] Email verification email
- [ ] Password reset email
- [ ] Order confirmation email
- [ ] Order status update emails
- [ ] Welcome email (if applicable)

#### Email Content
- [ ] Verify sender name is correct
- [ ] Verify sender email is correct
- [ ] Verify subject line is clear
- [ ] Verify content is readable (not HTML source)
- [ ] Verify links work
- [ ] Verify unsubscribe link (if applicable)
- [ ] Check spam folder - emails should not be there

### 11. Performance Testing

#### Page Load Times
- [ ] Home page loads in < 3 seconds
- [ ] Dashboard loads in < 3 seconds
- [ ] Public profile loads in < 2 seconds
- [ ] Images load progressively
- [ ] No excessive re-renders

#### File Upload
- [ ] Upload 5MB image completes in < 10 seconds
- [ ] Upload shows progress (if implemented)
- [ ] Upload can be cancelled (if implemented)

#### Database Performance
- [ ] Orders list with 100+ items loads quickly
- [ ] Analytics calculations complete quickly
- [ ] Search functions respond instantly

## Automated Testing

### Running Tests

```powershell
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test orders
python manage.py test profiles
python manage.py test cards
python manage.py test analytics

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Writing Tests

Example test structure:

```python
# tests.py in each app
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
    
    def test_duplicate_email(self):
        User.objects.create_user(
            email='test@example.com',
            username='user1',
            password='pass123'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',
                username='user2',
                password='pass123'
            )
```

## Load Testing

### Tools
- **Apache Bench (ab)**: Simple load testing
- **Locust**: Python-based load testing
- **JMeter**: Comprehensive load testing

### Load Test Scenarios

#### Scenario 1: Homepage Load
```powershell
# 100 concurrent users, 1000 requests
ab -n 1000 -c 100 https://yourdomain.com/
```

Expected: < 3s average response time

#### Scenario 2: Public Profile Load
```powershell
ab -n 500 -c 50 https://yourdomain.com/c/test-profile
```

Expected: < 2s average response time

#### Scenario 3: Authentication
Test login with 50 concurrent users

Expected: No failures, < 5s average

#### Scenario 4: Order Creation
Test 20 concurrent order submissions

Expected: All succeed, database handles load

## Security Testing

### Security Checklist

#### Authentication
- [ ] Passwords are hashed (not plaintext)
- [ ] Session tokens expire after 30 minutes
- [ ] "Remember me" uses secure cookies only
- [ ] Account locks after 5 failed attempts
- [ ] Password reset links expire after 1 hour
- [ ] Password reset links are single-use

#### Authorization
- [ ] Users can only view own data
- [ ] Admins can only manage own organization
- [ ] Super admins have full access
- [ ] Direct object reference attacks fail (e.g., /orders/someone-elses-uuid)

#### Input Validation
- [ ] SQL injection attempts fail
- [ ] XSS attempts fail (HTML is escaped)
- [ ] File upload type validation works
- [ ] File size limits enforced
- [ ] CSRF tokens required on all forms

#### Security Headers
- [ ] X-Frame-Options: DENY
- [ ] X-Content-Type-Options: nosniff
- [ ] Strict-Transport-Security set (when DEBUG=False)
- [ ] CSRF cookie secure (when DEBUG=False)
- [ ] Session cookie secure (when DEBUG=False)

### Penetration Testing

#### Tools
- **OWASP ZAP**: Automated vulnerability scan
- **Burp Suite**: Manual pen testing
- **Safety**: Python dependency vulnerability check

```powershell
# Check for vulnerable dependencies
pip install safety
safety check
```

## Bug Reporting

### Bug Report Template

```
**Title**: Short description of the bug

**Severity**: Critical / High / Medium / Low

**Environment**:
- Browser: Chrome 120.0.0
- OS: Windows 11
- Screen: 1920x1080
- User Role: Admin

**Steps to Reproduce**:
1. Go to page X
2. Click button Y
3. Enter data Z
4. Click submit

**Expected Result**:
What should happen

**Actual Result**:
What actually happened

**Screenshots**:
(attach if helpful)

**Console Errors**:
(any JavaScript errors from browser console)

**Additional Notes**:
Any other relevant information
```

### Bug Tracking
- Use issue tracking system (GitHub Issues, Jira, Trello)
- Label by severity and component
- Assign to responsible developer
- Track fix and retest

## Testing Completion Criteria

Before going live, ensure:
- [ ] All critical paths tested (registration → profile → order)
- [ ] All forms validated with both valid and invalid data
- [ ] All user roles tested (User, Admin, Super Admin)
- [ ] Mobile responsive on at least 3 devices
- [ ] Cross-browser on at least 3 browsers
- [ ] No console errors on any page
- [ ] All emails deliver correctly
- [ ] All links work (no broken links)
- [ ] Load testing passes (100+ concurrent users)
- [ ] No security vulnerabilities found
- [ ] Backup and restore tested
- [ ] Monitoring and error tracking configured

---

**Remember**: Testing is ongoing! After launch, continue monitoring user feedback and error logs.

**Version**: 1.0.0  
**Last Updated**: February 3, 2026
