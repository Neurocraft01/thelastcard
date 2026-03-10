# 🔐 ADMIN ROLES - SIMPLIFIED SYSTEM

**This project uses a simple 3-tier role system:**

1. **Super Admin** - Platform owner with full control
2. **Admin** - User manager who can manage users and cards
3. **User** - Regular platform user

**NOTE:** Organizations have been REMOVED. This is now a simple flat structure with no grouping.

---

## 👤 Role Hierarchy

### 1. SUPER ADMIN (Platform Owner)

**Access Level:** Complete system control - manages all admins, users, and settings

**Dashboard Features:**
- Dashboard: System overview (total users, admins, cards)
- View all Admins
- View all Users  
- View all Cards
- Platform-wide analytics
- System settings

**Permissions:**

✅ **SUPER_ADMIN Can:**
- CREATE new Admin accounts
- UPDATE Admin details (email, name, active status)
- DELETE Admin accounts
- VIEW all admins across platform
- VIEW all users and cards
- VIEW system-wide analytics
- MANAGE global platform settings
- SUSPEND/ACTIVATE Admins

❌ **SUPER_ADMIN Cannot:**
- Directly manage regular users (that's Admin's job)
- Directly manage cards (that's Admin's job)

---

### 2. ADMIN (User Manager)

**Access Level:** Full control over regular users and their cards

**Dashboard Features:**
- Dashboard: Platform overview (users, cards, analytics)
- View all users (USER role)
- Create/Edit/Delete users
- View all cards
- Manage cards for users
- Reset user passwords
- Export cards for printing
- System analytics
- Admin settings

**Pages Accessible:**
- Admin Dashboard (`/accounts/admin-dashboard/`)
- Users Management (`/accounts/admin-dashboard/users/`)
- Cards Management (`/accounts/admin-dashboard/cards/`)
- User Detail pages
- Card Detail pages  
- Analytics
- Settings

✅ **ADMIN Can:**
- CREATE new User accounts
- UPDATE User details (name, email, status)
- DELETE Users
- RESET User passwords
- VIEW all users on platform
- CREATE cards for users
- UPDATE card settings
- DELETE cards
- VIEW card analytics
- EXPORT cards for printing
- MANAGE user profiles
- VIEW system analytics

❌ **ADMIN Cannot:**
- Create/Edit/Delete other Admins
- Create/Edit/Delete Super Admins
- Access Super Admin dashboard
- Change platform settings
- View Super Admin analytics

---

### 3. USER (Regular Member)

**Access Level:** Personal profile and card only

**Dashboard Features:**
- Dashboard: Personal overview
- Edit own profile
- View own card
- Order physical cards
- View own analytics

**Permissions:**

✅ **USER Can:**
- EDIT own profile
- VIEW own card
- ORDER physical NFC cards
- VIEW own analytics
- UPDATE own settings
- SHARE own profile

❌ **USER Cannot:**
- View other users' profiles (admin pages)
- Create/Edit other users
- Access Admin dashboard
- Access Super Admin dashboard
- Manage cards for others

---

## 🚀 How It Works

### Simplified Flow:

```
SUPER ADMIN (Platform Owner)
    │
    ├── Creates/Manages → ADMIN accounts
    │
    └── Views system-wide data

ADMIN (User Manager)
    │
    ├── Creates/Manages → USER accounts
    │
    ├── Creates/Manages → Cards for users
    │
    └── Views all platform users & cards

USER (Regular Member)
    │
    └── Manages own profile & views own data
```

### Example Scenario:

1. **Super Admin (You)**:
   - Creates admin account "admin@example.com"
   - Assigns ADMIN role
   - Admin can now login

2. **Admin**:
   - Logs in to Admin Dashboard
   - Creates user "john@example.com" with USER role
   - Creates NFC card for John
   - Can view/edit John's data

3. **User (John)**:
   - Logs in to User Dashboard
   - Edits his profile
   - Views his card
   - Orders physical card
   - Cannot see other users

---

## 🎯 What Changed from Original System?

### ❌ REMOVED:
- Organization model and grouping
- Organization limits (max_users, max_cards)
- Organization branding/settings
- Organization admin assignment
- Organization-scoped access
- Complex multi-tenant logic

### ✅ NOW:
- Simple flat structure
- Admins manage ALL users (not just organization)
- No user/card limits
- Direct role-based access
- Easier to understand and use

---

## 📋 Common Scenarios

### Super Admin Creating an Admin:
1. Login as Super Admin
2. Go to `/accounts/superadmin/admins/`
3. Click "Create Admin"
4. Enter: email, username, first name, last name
5. Default password: `Admin@123`
6. Admin can now login and manage users

### Admin Creating a User:
1. Login as Admin
2. Go to `/accounts/admin-dashboard/users/`
3. Click "Add User" (button needs UI)
4. Enter: email, username, first name, last name
5. Default password: `User@123`
6. User can now login

### User Editing Profile:
1. Login as User
2. Go to Dashboard
3. Click "Edit Profile"
4. Update information
5. Click "Save"

---

## 🔐 Security & Access Control

### Permission Mixins:
- `SuperAdminRequiredMixin` - Only Super Admin access
- `AdminRequiredMixin` - Admin OR Super Admin access
- `UserRequiredMixin` - Any authenticated user

### No Cross-Role Access:
- Users cannot access Admin pages
- Admins cannot access Super Admin pages
- Unauthorized access returns 403 Forbidden

---

## 📝 Summary

| Feature | Super Admin | Admin | User |
|---------|------------|-------|------|
| Create/Edit/Delete Admins | ✅ | ❌ | ❌ |
| Create/Edit/Delete Users | ❌ | ✅ | ❌ |
| Manage All Cards | ❌ | ✅ | ❌ |
| View All Users | ✅ | ✅ | ❌ |
| Platform Analytics | ✅ | ✅ | ❌ |
| Edit Own Profile | ✅ | ✅ | ✅ |
| Own Analytics | ✅ | ✅ | ✅ |

**SIMPLE. NO ORGANIZATIONS. JUST 3 ROLES. EASY TO USE.**

---

*Last Updated: February 4, 2026*
*See: SIMPLIFIED_ADMIN_SYSTEM.md for implementation details*
