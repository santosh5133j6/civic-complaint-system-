# Authentication & Dashboard Guide

## 🔐 Authentication System

The application now has a secure authentication system protecting the admin dashboard.

### Default Admin Credentials

- **Username:** `admin`
- **Password:** `admin123`

Alternative account:
- **Username:** `municipal`
- **Password:** `municipal@123`

> ⚠️ **Important:** Change these credentials in production by editing `auth.py`

## 📊 Two Dashboard Types

### 1. Public Dashboard (No Login Required)
**URL:** http://localhost:5000/public-dashboard

**Features:**
- ✅ View all complaints (read-only)
- ✅ Filter by status, priority, category
- ✅ View statistics and charts
- ✅ Click to view full complaint details
- ✅ Show locations on map
- ✅ Auto-refresh every 60 seconds
- ❌ Cannot modify or update complaints

**Who can access:** Anyone - general public

### 2. Admin Dashboard (Login Required)
**URL:** http://localhost:5000/admin

**Features:**
- ✅ All public dashboard features PLUS:
- ✅ Update complaint status
- ✅ Assign to departments
- ✅ Add admin notes
- ✅ Full CRUD operations
- ✅ Advanced analytics

**Who can access:** Only authenticated admin users

## 🔄 Navigation Flow

### For Regular Users:
1. Submit complaint → `/` (home)
2. View all complaints → `/public-dashboard`
3. See complaints on map → `/map`

### For Admins:
1. Login → `/admin/login`
2. Admin dashboard → `/admin` (requires login)
3. Update complaints → Only available in admin dashboard
4. Logout → Click logout button in navbar

## 🛡️ Protected Routes

The following routes require admin authentication:

- `/admin` - Admin dashboard
- `/api/complaints/<id>/update` - Update complaint status

If you try to access these without logging in, you'll be redirected to the login page.

## 🔑 How to Login

1. Navigate to http://localhost:5000/admin
2. If not logged in, you'll be redirected to login page
3. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
4. Click "Login"
5. You'll be redirected to the admin dashboard

## 🚪 How to Logout

Click the "Logout" button in the admin dashboard navbar (top-right)

## 🔒 Security Features

1. **Session-based authentication** - Uses Flask sessions
2. **Password hashing** - Passwords stored as SHA-256 hashes
3. **Login required decorator** - Protects admin routes
4. **Flash messages** - User feedback for login/logout
5. **Redirect handling** - Returns to intended page after login

## 📝 Changing Admin Credentials

Edit `auth.py`:

```python
ADMIN_USERS = {
    'your_username': hash_password('your_password'),
}
```

Or add new admins:

```python
ADMIN_USERS = {
    'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
    'manager': hashlib.sha256('manager@2024'.encode()).hexdigest(),
    'supervisor': hashlib.sha256('super#123'.encode()).hexdigest(),
}
```

## 🌐 URL Structure

| URL | Access Level | Description |
|-----|--------------|-------------|
| `/` | Public | Submit complaint form |
| `/public-dashboard` | Public | View all complaints (read-only) |
| `/map` | Public | Map view of complaints |
| `/admin/login` | Public | Admin login page |
| `/admin` | Admin Only | Admin dashboard with edit capabilities |
| `/admin/logout` | Admin Only | Logout endpoint |

## 💡 Tips

1. **First time users:** Start with the public dashboard to see complaints without logging in
2. **Admins:** Login once and your session persists until you logout or close browser
3. **Testing:** Use demo credentials for testing, change for production
4. **Security:** In production, use environment variables for credentials, not hardcoded values

## 🔧 Troubleshooting

**Problem:** "Access Denied" or redirected to login
- **Solution:** Login with admin credentials

**Problem:** "Invalid username or password"
- **Solution:** Check credentials match those in `auth.py`

**Problem:** Logged in but seeing public dashboard
- **Solution:** Navigate to `/admin` URL, not `/public-dashboard`

**Problem:** Session expired
- **Solution:** Simply login again - sessions persist in browser

## 🎯 Production Recommendations

For production deployment:

1. **Use environment variables** for credentials
2. **Implement proper password hashing** with bcrypt or argon2
3. **Add rate limiting** for login attempts
4. **Use HTTPS** for secure transmission
5. **Implement CSRF protection** 
6. **Add database-backed user management**
7. **Enable two-factor authentication (2FA)**
8. **Set secure session cookie flags**

Example production auth with database:

```python
# Instead of hardcoded dictionary
ADMIN_USERS = UserDB.get_all_admins()  # Load from database
```
