# User Service – CauseHive

This service is part of the [CauseHive](https://github.com/niicommey01/CauseHive) platform, responsible for all user-related operations, including registration, authentication, profile management, and user data security.

---

## Features

- **User Registration:** Create new user accounts with personal details.
- **Authentication:** Secure login/logout for registered users.
- **Profile Management:** Update contact details and donation preferences.
- **Password Recovery:** Reset forgotten passwords through email/contact verification.
- **User Data Security:** All sensitive user data is encrypted.
- **Admin Functions:** Manage (view/edit/deactivate) user accounts.

---

## API Endpoints


### Authentication
- `POST user-service/api/auth/signup/` – Register a new user
- `POST /api/auth/login/` – Login a user
- `POST /api/auth/logout/` – Logout a user
- `POST /api/user/password-reset` – Initiate password recovery

### Profile Management
- `GET /api/auth/profile` – Get current user profile
- `PATCH /api/auth/profile` – Update user profile

---

## Security

- All sensitive data is encrypted in transit and at rest.
- Follows best practices for secure authentication and session management.

---

## Related Services

- [Event/Cause Service](../event_service)
- [Donation Service](../donation_service)
- [Admin Panel Service](../admin_service)

---