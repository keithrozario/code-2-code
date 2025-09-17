# Functional Specification: MoneyNote API

## 1. Introduction

This document provides a comprehensive functional specification for the MoneyNote API, a self-hosted, open-source bookkeeping application. It details the system's features, user journeys, business rules, and technical architecture.

### 1.1. Purpose of the Document

The purpose of this functional specification is to serve as the definitive guide and single source of truth for the MoneyNote application. It is intended for a wide audience, including developers, quality assurance testers, product managers, and business stakeholders.

This document will:
- **Define Scope:** Clearly articulate the capabilities and limitations of the system.
- **Guide Development:** Provide detailed requirements and user flows to guide the implementation of new features and modifications to existing ones.
- **Ensure Quality:** Establish a clear set of testable requirements for quality assurance and user acceptance testing.
- **Facilitate Communication:** Create a shared understanding of the system's functionality across all teams and stakeholders.
- **Serve as a Reference:** Act as a technical and functional reference for future maintenance, support, and strategic planning.

### 1.2. Goals and Objectives

The primary goal of the MoneyNote application is to empower individuals and small businesses with a private, secure, and comprehensive tool for managing their finances. The system is designed to be self-hostable, ensuring users retain full control and ownership of their sensitive financial data.

The key objectives of the system are:

- **Provide Financial Clarity:** To offer users a clear, consolidated, and accurate overview of their financial health, including their net worth, assets, and liabilities.
- **Enable Detailed Tracking:** To provide robust and intuitive tools for tracking daily incomes, expenses, and transfers with detailed categorization and tagging.
- **Support Diverse Financial Scenarios:** To deliver flexible features that accommodate real-world complexity, including support for managing accounts in multiple currencies and maintaining separate ledgers ("Books") for different financial contexts (e.g., personal vs. business).
- **Ensure Data Integrity and Completeness:** To allow users to attach digital records (e.g., receipts, invoices) to transactions, creating a complete and verifiable financial history.
- **Facilitate Collaboration:** To support multi-user collaboration through a secure group system with role-based access controls, allowing families or small teams to manage finances together.

### 1.3. Scope

The scope of this document covers the core functionalities of the MoneyNote API. The features detailed herein define the boundaries of the current system.

#### In Scope

The following features and capabilities are within the scope of the MoneyNote application:

- **Core Transaction Management:** Full CRUD (Create, Read, Update, Delete) operations for financial transactions, including Expenses, Incomes, Transfers between accounts, and Balance Adjustments.
- **Account Management:** Creation and management of various financial account types, including Checking, Credit, Assets, and Debts.
- **Financial Overview and Reporting:**
    - Calculation and display of Net Worth, Total Assets, and Total Debts.
    - Generation of analytical reports on income and expenses, aggregated by category, tag, and payee.
- **Data Organization:**
    - A hierarchical system for creating and managing categories and tags.
    - Management of a list of payees for transactions.
- **Multi-Book Functionality:** The ability to create and manage multiple, independent financial ledgers ("Books"), each with its own set of categories, tags, payees, and default currency. This includes creating books from templates or by cloning existing ones.
- **Multi-Currency Support:**
    - Assignment of a specific currency to each financial account.
    - Recording of transactions in their original currency, with functionality to store a converted amount in the book's default currency.
    - Consolidation of all financial reports into a single, user-defined default currency.
- **File Attachments:** The ability to upload, attach, view, and delete digital files (e.g., PDFs, images) to transaction records.
- **User and Group Management:** User registration, authentication, and a collaborative "Group" system that allows multiple users to share financial data with defined roles (Owner, Operator, Guest).

#### Out of Scope

The following features and capabilities are considered out of scope for the current version of the MoneyNote application:

- **Automated Budgeting:** The system does not include features for creating spending budgets, setting limits for categories, or tracking performance against a budget.
- **Advanced Investment Tracking:** While asset accounts can be created, the system does not track investment performance, stock portfolios, capital gains, or dividends.
- **Invoicing and Bill Payment:** The application is designed for bookkeeping and does not include functionality to generate or send client invoices, nor does it integrate with services to pay bills directly.
- **Financial Forecasting:** All reporting is based on historical data. The system does not provide tools for forecasting future financial positions or cash flow.
- **Direct Bank Integration:** The system does not automatically import transactions from financial institutions via open banking APIs (e.g., Plaid). All transaction data entry is manual.