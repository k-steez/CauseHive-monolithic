# CauseHive
Integral components for the CauseHive Donation App.


# Overview of CauseHive’s Requirements
CauseHive is a web application designed to connect donors with a wide range of charitable
events and causes. The platform enables users to easily register, browse and search for events
or causes, and make secure donations using various payment methods. Users can manage
their profiles, track their donation history, and receive confirmations and receipts for every
contribution. The app also allows donors to submit testimonials about their experiences and
view feedback from others.
Administrators and organizers have access to a dedicated panel where they can create and
manage events or causes, oversee user accounts, monitor all donations, and generate detailed
reports on donation activity and event performance. Security is a core focus, with robust data
encryption and secure payment processing in place to protect user information.
Overall, CauseHive streamlines the donation process, making it simple for individuals to support
meaningful causes, while providing organizers with the tools they need to effectively manage
and promote their fundraising efforts.
# 1. User Management
● User Registration: Users can create accounts with personal details to donate,
track donations, and manage profiles.
● User Login/Logout: Registered users can log in and out securely.
● Profile Management: Users can update their profile with new information, such
as contact details and donation preferences.
● Password Recovery: Users can reset their passwords using email or contact
verification.
# 2. Event & Cause Catalog
● Event/Cause Listing: List of active donation events and causes with descriptions
and goals.
● Event/Cause Details: View details about each event or cause, including organizer,
target amount, progress, and updates.
● Search and Filter: Users can search for events/causes by name, organizer, or
category, and filter by location, goal, or status.
● Category Management: Causes and events are organized into categories (e.g.,
health, education, disaster relief).
# 3. Making Donations
● Add to Donation Cart: Users can select one or more causes/events to donate to
in a single session.
● View Donation Cart: Users can review selected causes/events and intended
donation amounts.
● Update Donation Cart: Users can change donation amounts or remove
causes/events before proceeding.
● Save for Later: Users can bookmark causes/events to donate to at a later time.
# 4. Donation Process
● Donor Information: Users can enter or confirm their contact and payment
information.
● Payment Options: Support for various payment methods (credit/debit card, bank
transfer, mobile money, etc.).
● Donation Summary: Display selected causes, donation amounts, transaction
fees, and total amount.
● Donation Confirmation: Send confirmation via email or SMS, including a receipt
and summary.
# 5. Donation Management
● Donation Tracking: Users can track the status of their donations and see
progress updates from organizers.
● Donation History: Users can view a history of all their past donations with details
and receipts.
● Donation Cancellation/Refunds: Users can request cancellation or refunds
according to policy (if applicable).
# 6. Reviews and Testimonials
● Submit Testimonial: Donors can submit testimonials about their giving
experience or the impact of their donations.
● View Testimonials: Users can read testimonials and feedback from other donors.
# 7. Admin Panel
● Event/Cause Management: Admins/organizers can add, edit, and delete
events/causes.
● User Account Management: Admins can manage user accounts.
● Donation Oversight: Admins can view, verify, and manage all donations.
● Reporting: Generate reports on donation volumes, user activity, and event/cause
performance.
# 8. Security
● Data Encryption: Sensitive data (personal and payment info) is encrypted.
● Secure Payment Processing: Secure gateways are used for all financial
transactions.
Use Case Diagram (Description)
User:
● Access donor support.
● Provide feedback/testimonials.
● Browse and view events/causes.
● View event/cause details.
● View donation/payment history.
● Make donations to events/causes.
● Manage profile via login system.
Administrator/Organizer:
● Manage users (view, edit, deactivate).
● Manage donations (view, track, update, refund).
● Manage events/causes (edit details, add, delete).
● Generate reports (donation volumes, user activity, event/cause performance).
# User Stories
User Registration and Authentication
# 1. Donor Registration:
As a visitor, I want to create an account so I can donate and track my giving
history.
# 2. User Login:
As a registered donor, I want to log in to access my account and donation history.
# 3. Password Recovery:
As a user, I want to recover my password if I forget it.
Event/Cause Browsing and Search
# 4. Browse Events/Causes:
As a donor, I want to browse events and causes by category or location.
# 5. Search Events/Causes:
As a donor, I want to search for specific events or causes by name or organizer.
# 6. Event/Cause Details:
As a donor, I want to view detailed information about an event or cause before
donating.
Donation Cart and Checkout
# 7. Add to Donation Cart:
As a donor, I want to select multiple causes/events and specify donation
amounts.
# 8. View Donation Cart:
As a donor, I want to review my selected donations before confirming.
# 9. Remove from Donation Cart:
As a donor, I want to remove or adjust causes/events in my donation cart.
# 10. Checkout/Donate:
As a donor, I want to complete my donation(s) securely.
Payment and Donation Management
# 11. Payment Processing:
As a donor, I want to pay using various methods.
# 12. Donation Confirmation:
As a donor, I want to receive a confirmation and receipt.
# 13. Donation Tracking:
As a donor, I want to track the status and impact of my donations.
Account Management
# 14. View Donation History:
As a donor, I want to view all my past donations.
# 15. Update Account Information:
As a donor, I want to update my personal and payment details.
Admin/Organizer Functionality
# 16. Add New Event/Cause:
As an admin/organizer, I want to add new events or causes.
# 17. Manage Donations:
As an admin/organizer, I want to view, verify, and update donation statuses.
# 18. User Management:
As an admin, I want to manage donor accounts.
# Pre- and Post-Conditions (Examples)
Donor Registration:
● Pre: Visitor accesses registration page and provides valid info.
● Post: Account created, user logged in or redirected, confirmation sent.
# Make a Donation:
● Pre: User is logged in, has selected causes/events, and entered payment details.
● Post: Donation processed, confirmation sent, donation appears in user’s history.
# Add New Event/Cause (Admin):
● Pre: Admin is logged in and accesses event management.
● Post: New event/cause is listed and available for donations.
# Non-Functional Requirements
● Performance: Website loads quickly and supports many users.
● Reliability: Platform is available for donations at all times.
● Security: All sensitive data is encrypted; secure payment processing.
● Usability: Clean, responsive design; easy navigation for donors and organizers.
# Glossary
● User Registration: Creating a donor account.
● Event/Cause Listing: Displaying active donation opportunities.
● Donation Cart: Temporary holding area for selected donations.
● Donation Confirmation: Notification of successful donation.
● Donation Tracking: Monitoring status and impact of donations.
● Admin Panel: Backend interface for managing users, events, and donations.
