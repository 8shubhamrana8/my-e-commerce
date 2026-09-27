### My-e-commerce

An eBay-style e-commerce auction platform built with Django, allowing users to create listings, place bids, comment on items, and manage personalized watchlists.

🌟 Key Features
Auction Listing Creation: Users can post new listings with title, detailed description, starting bid, optional image URL, and category classification.

<img width="1917" height="1016" alt="Screenshot 2026-09-27 175222" src="https://github.com/user-attachments/assets/926ee264-9139-473f-92c6-e3419b9d7b30" />

Active Listings Page: Main page showcasing all open, available listings with key details (image, title, current price, date added).

Bidding System:

Interactive bidding validation ensuring bids are higher than the starting price and current highest bid.

<img width="1917" height="1016" alt="Screenshot 2026-09-27 182906" src="https://github.com/user-attachments/assets/7238db8e-014c-449e-b026-df5ed8174193" />

Real-time notifications for winning bids when a listing is closed by its creator


Personalized Watchlist:

<img width="1917" height="1020" alt="Screenshot 2026-09-27 175211" src="https://github.com/user-attachments/assets/e6bdba5c-b9d4-496b-b758-398e6361967e" />

Users can add or remove listings from a private watchlist.

Dedicated Watchlist view displaying tracked items.

Comments & Engagement: Registered users can write and publish comments directly on listing details pages.

<img width="1917" height="1018" alt="Screenshot 2026-09-27 175248" src="https://github.com/user-attachments/assets/630e9135-f719-459a-b51b-e40b5f226f0f" />

Categories Navigation: View listings filtered by specific product categories (e.g., Electronics, Fashion, Home).

Django Admin Panel: Administrative interface to view, edit, and moderate listings, bids, comments, and user profiles.

🛠️ Tech Stack
Backend: Python 3, Django

Frontend: HTML5, CSS3, Bootstrap 4 / 5

Database: SQLite (Django ORM)

Authentication: Django Built-in User Authentication System

💻 Technical Highlights & Data Architecture
Database Schema Design: Modeled relational entities using Django ORM with foreign keys and many-to-many fields connecting User, Listing, Bid, Comment, and Category models.

Form Validation & Error Handling: Custom view logic ensuring legal bid processing, user authentication checks for restricted actions, and edge-case handling for closed auctions.

Modular Template Rendering: Utilized Django template inheritance (base.html), custom tags, and conditional logic to render distinct user states (owner vs. bidder vs. winner).

🚀 Getting Started
Prerequisites
Python 3.x

Django 3.x or 4.x

pip package manager
