# Woxsenite – Blockchain-Based Student Engagement Reward System

## Overview

Woxsenite is a blockchain-powered student engagement and reward platform designed to encourage participation in academic and extracurricular activities. The system rewards students with digital tokens for activities such as attendance, hackathons, research projects, certifications, sports events, and club activities.

The platform combines Blockchain Technology, Artificial Intelligence, and Web Development to provide a transparent, secure, and automated reward ecosystem for educational institutions.

---

## Problem Statement

Educational institutions often struggle to track and reward student participation fairly and efficiently.

Traditional systems face several challenges:

- Manual verification of certificates and achievements
- Lack of transparency in reward allocation
- Centralized records vulnerable to modification
- Time-consuming administrative processes
- Limited student motivation for extracurricular participation

Woxsenite addresses these challenges through blockchain-based token rewards and AI-assisted certificate verification.

---

## Key Features

### Student Dashboard

Students can:

- View token wallet balance
- Mark daily attendance
- Submit event participation certificates
- View transaction history
- Track earned rewards

### Attendance Reward System

Students submit attendance through the dashboard.

Administrators can:

- Review attendance requests
- Approve submissions
- Automatically reward tokens

### Event Reward System

Students can submit:

- Hackathons
- Research Activities
- Certifications
- Sports Activities
- Club Activities

Each category provides different reward values.

### AI Certificate Verification

The system uses:

- EasyOCR
- RapidFuzz Fuzzy Matching

Workflow:

1. Student uploads certificate
2. OCR extracts text from image
3. Student name is matched against extracted text
4. Confidence score is generated
5. Result is displayed to admin

This reduces manual verification effort.

### Blockchain Token Minting

Upon admin approval:

- Smart contract mints reward tokens
- Tokens are sent to the student's wallet
- Transaction is recorded on blockchain

Benefits:

- Transparency
- Security
- Immutability
- Auditability

### Admin Dashboard

Administrators can:

- Review attendance requests
- Review event submissions
- View AI verification results
- Approve or reject requests
- Trigger blockchain token minting

---

## System Architecture

```text
Student Dashboard
        │
        ▼
Flask Backend
        │
 ┌──────┴──────┐
 ▼             ▼
SQLite      AI Verification
Database    (OCR + Fuzzy Match)
                │
                ▼
         Admin Approval
                │
                ▼
         Solidity Smart Contract
                │
                ▼
        Ganache Blockchain
                │
                ▼
          Token Minting
```

---

## Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Core programming language |
| Flask | Backend web framework |
| HTML | User interface structure |
| CSS | Styling and responsive design |
| JavaScript | Client-side interactions |
| SQLite | Database management |
| Solidity | Smart contract development |
| Ganache | Local blockchain simulation |
| Remix IDE | Smart contract deployment |
| Web3.py | Blockchain interaction from Python |
| EasyOCR | Certificate text extraction |
| OpenCV | Image processing |
| RapidFuzz | Fuzzy string matching |

---

## Database Tables

### Students

Stores:

- Student information
- Wallet addresses
- Token balances

### Attendance

Stores:

- Attendance requests
- Token rewards
- Approval status

### Events

Stores:

- Event submissions
- AI verification results
- Approval status

### Transactions

Stores:

- Reward history
- Token allocation records

### Timetable

Stores:

- Weekly academic schedule

---

## Blockchain Implementation

### Smart Contract Functions

#### Mint Tokens

```solidity
function mint(address wallet, uint amount)
```

Used when:

- Attendance is approved
- Event participation is approved

Tokens are minted directly to the student's wallet.

### Why Blockchain?

Blockchain ensures:

- Immutable records
- Transparent reward allocation
- Secure transaction history
- Trustworthy token distribution

---

## AI Verification Workflow

### Step 1

Student uploads certificate image.

### Step 2

EasyOCR extracts textual content.

Example:

```text
Certificate of Participation

This certifies that
Brinda Reddy

Participated in Hackathon 2026
```

### Step 3

RapidFuzz compares extracted text with the student's name.

### Step 4

Confidence score is generated.

### Step 5

Admin reviews the result.

---

## Project Workflow

### Attendance Flow

```text
Student Marks Attendance
          │
          ▼
Attendance Request Created
          │
          ▼
Admin Approval
          │
          ▼
Smart Contract Mint
          │
          ▼
Tokens Added
```

### Event Flow

```text
Certificate Upload
          │
          ▼
OCR Verification
          │
          ▼
Admin Review
          │
          ▼
Blockchain Mint
          │
          ▼
Transaction Stored
```

---

## Future Enhancements

- Advanced AI-based fraud detection
- QR-based certificate validation
- IPFS certificate storage
- Mobile application support
- Public Ethereum deployment
- Token redemption system
- Campus reward marketplace
- Cafeteria and bookstore integration

---

## Research Contribution

This project demonstrates the integration of:

- Blockchain-based reward systems
- Smart contract token minting
- AI-powered certificate verification
- Educational participation management

The proposed system provides a transparent, secure, and scalable approach for rewarding student engagement in higher education institutions.

