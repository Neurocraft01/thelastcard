# Admin Roles & Permissions Documentation

## Overview
This NFC Card platform has a 3-tier role-based access control system:
1. **Super Admin** - Platform owner with full system access
2. **Admin** - Organization manager who manages team members
3. **User** - Regular user who manages their own profile/card

---

## 🔐 User Roles Explained

### 1. SUPER ADMIN (Platform Owner)
**Who:** You, the platform owner/developer
**Access Level:** Complete system control across all organizations

**Current Permissions:**
✅ **VIEW Operations Available:**
- Dashboard: System overview (total users, admins, organizations, cards)
- View all Admins across the platform
- View all Organizations
- View all Users (across all organizations)
- System Analytics
- Global Settings

❌ **MISSING Operations (TO BE ADDED):**
- CREATE new Admin accounts
- UPDATE Admin details
- DELETE Admin accounts
- CREATE new Organizations
- UPDATE Organization details (name, limits, branding)
- DELETE Organizations
- ASSIGN Admin to Organization
- CHANGE user roles (User ↔ Admin ↔ Super Admin)
- SUSPEND/ACTIVATE Admins and Organizations
- EXPORT system-wide reports

**Dashboard Location:** `/accounts/superadmin/dashboard/`

---

### 2. ADMIN (Organization Manager)
**Who:** Company owner or manager who purchased the NFC card service
**Access Level:** Full control over their organization and team members only

**Current Permissions:**
✅ **VIEW Operations Available:**
- Dashboard: Organization overview (team members, cards, analytics)
- View team members (users in their organization)
- View team member details
- View all cards in organization
- View individual card details
- View QR codes for each user
- Export individual card data (PDF)
- Export all cards (bulk PDF)
- Print cards view
- Organization Analytics
- Organization Settings

❌ **MISSING Operations (TO BE ADDED):**
- CREATE new team member (User) accounts
- UPDATE team member details (name, email, role)
- DELETE team members
- ACTIVATE/DEACTIVATE users
- RESET user password
- CREATE new cards for team members
- UPDATE card details
- DELETE/DEACTIVATE cards
- UPDATE organization settings (logo, colors, limits)
- INVITE users by email
- MANAGE user permissions within organization

**Dashboard Location:** `/accounts/admin-dashboard/`

---

### 3. USER (Regular Team Member)
**Who:** Employee/team member created by Admin
**Access Level:** Can only manage their own profile and card

**Current Permissions:**
✅ **Available Operations:**
- Dashboard: Personal overview
- UPDATE own profile (name, photo, bio, contact info, social links)
- VIEW own card
- VIEW analytics for own card (views, taps, link clicks)
- UPDATE settings (password, notifications)
- LIVE PREVIEW while editing profile

❌ **Cannot Access:**
- Other users' profiles
- Organization settings
- Team member management
- System settings

**Dashboard Location:** `/accounts/user/dashboard/`

---

## 🏢 What is "Organization"?

### Concept
An **Organization** is a company/business/team that purchases NFC card services.

### Structure
```
Organization (e.g., "TechCorp Inc")
├── 1 Admin (Organization Owner/Manager)
└── Multiple Users (Team Members/Employees)
    ├── User 1: John Doe
    ├── User 2: Jane Smith
    └── User 3: Mike Johnson
```

### Organization Features
- **Name & Branding:** Logo, primary color, secondary color
- **Subscription Tier:** FREE, STARTER, PROFESSIONAL, ENTERPRISE
- **Limits:**
  - `max_users`: Maximum team members (default: 5)
  - `max_cards`: Maximum NFC cards (default: 10)
- **Custom Domain:** Optional branded domain
- **Settings:**
  - `allow_custom_themes`: Can users customize card themes?
  - `allow_analytics`: Enable analytics tracking?
  - `allow_password_protection`: Enable password-protected profiles?

### Use Case Example
**Scenario:** A company "TechCorp Inc" buys 20 NFC cards

1. **Super Admin (You):**
   - Creates organization "TechCorp Inc"
   - Sets max_users = 20, max_cards = 20
   - Creates Admin account: admin@techcorp.com
   - Assigns admin to TechCorp organization

2. **Admin (TechCorp Manager):**
   - Logs in to `/accounts/admin-dashboard/`
   - Creates 20 user accounts (employees)
   - Assigns cards to each employee
   - Customizes organization branding
   - Monitors team analytics

3. **Users (TechCorp Employees):**
   - Each employee logs in
   - Updates their profile, photo, contact info
   - Shares their NFC card at events
   - Views their card analytics

---

## 📊 Current System Status

### ✅ What Works Now (READ-ONLY)
- All three dashboards display correctly
- Users can view data relevant to their role
- User can update their own profile (✅ CRUD complete)
- QR code viewing for admins
- Card export functionality
- Live preview in profile editor

### ❌ What's Missing (CRUD Operations)

#### **Super Admin Missing:**
1. **Admins Management:**
   - ❌ Create new Admin
   - ❌ Edit Admin details
   - ❌ Delete Admin
   - ❌ Change Admin organization

2. **Organizations Management:**
   - ❌ Create new Organization
   - ❌ Edit Organization (name, logo, limits)
   - ❌ Delete Organization
   - ❌ Change subscription tier

3. **Users Management:**
   - ❌ Create User (across any organization)
   - ❌ Edit User
   - ❌ Delete User
   - ❌ Change User organization

#### **Admin Missing:**
1. **Team Members Management:**
   - ❌ Create new User (team member)
   - ❌ Edit User details
   - ❌ Delete/Remove User
   - ❌ Deactivate User
   - ❌ Reset User password

2. **Cards Management:**
   - ❌ Create new Card for user
   - ❌ Edit Card settings
   - ❌ Delete/Deactivate Card
   - ❌ Assign Card to different user

3. **Organization Settings:**
   - ❌ Update organization name
   - ❌ Upload organization logo
   - ❌ Change branding colors

---

## 🎯 Next Steps: Adding CRUD Operations

I will now implement the following:

### Phase 1: Super Admin CRUD (High Priority)
1. ✅ Create Admin
2. ✅ Update Admin
3. ✅ Delete Admin
4. ✅ Create Organization
5. ✅ Update Organization
6. ✅ Delete Organization

### Phase 2: Admin CRUD (High Priority)
1. ✅ Create User (team member)
2. ✅ Update User
3. ✅ Delete User
4. ✅ Create Card for user
5. ✅ Update Card
6. ✅ Delete Card

### Phase 3: Organization Settings (Medium Priority)
1. ✅ Update organization profile
2. ✅ Upload logo
3. ✅ Change branding colors
4. ✅ Manage limits

---

## 📝 Summary

**Super Admin = Platform Owner**
- Manages everything across the entire platform
- Creates and manages Admins and Organizations
- System-wide control

**Admin = Organization Manager/Company Owner**
- Manages their own organization only
- Creates and manages team members (Users)
- Organization-level control

**User = Team Member/Employee**
- Manages only their own profile and card
- Cannot see or manage other users
- Personal-level control

**Organization = Company/Business**
- Groups Users under one Admin
- Has subscription limits (max users, max cards)
- Can have custom branding and settings

---

**STATUS:** Documentation complete. Ready to implement CRUD operations.
