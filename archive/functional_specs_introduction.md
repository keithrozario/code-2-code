# Functional Specification: MoneyNote API

## 1. Introduction

### 1.1 Purpose of the Document

This document provides a detailed functional specification for the MoneyNote API, a comprehensive personal and small business bookkeeping system. Its purpose is to establish a clear and common understanding of the system's features, behaviors, and capabilities among all stakeholders, including developers, quality assurance teams, and project managers. This specification will serve as the definitive guide for the development, testing, and future enhancement of the application, ensuring that the final product aligns with the intended business requirements and user needs.

### 1.2 Goals and Objectives

The primary goal of the MoneyNote system is to provide users with a secure, private, and powerful platform for independent financial management. It empowers users to take full control of their financial data without relying on third-party services.

The key objectives are:

*   **Provide Comprehensive Financial Tracking:** To enable users to meticulously track all financial activities, including incomes, expenses, transfers, and account balance adjustments.
*   **Deliver Actionable Financial Insights:** To offer robust reporting and overview features that give users a clear, consolidated understanding of their financial health, including net worth, asset distribution, and spending patterns.
*   **Support Complex Use Cases:** To provide advanced features such as multi-book accounting for segregating finances (e.g., personal vs. business) and multi-currency support for managing international transactions seamlessly.
*   **Ensure Data Integrity and Privacy:** To build a self-hostable solution that prioritizes user data ownership and provides features for complete and verifiable record-keeping, such as file attachments for transactions.
*   **Facilitate Collaboration:** To allow multiple users to collaborate on shared financial accounts and books through a secure group and role-based access control system.

### 1.3 Scope

This document defines the functional scope of the MoneyNote API backend.

#### 1.3.1 In Scope

The following features and functionalities are within the scope of this specification:

*   **Financial Monitoring:** Calculation and reporting of total assets, debts, and net worth. Visual reporting on the composition of assets and liabilities.
*   **Transaction Management:** Full CRUD (Create, Read, Update, Delete) operations for financial transactions, including expenses, incomes, transfers, and balance adjustments.
*   **Data Classification:** Hierarchical categorization and tagging of transactions for granular analysis.
*   **Multi-Book Accounting:** Creation and management of multiple, independent financial ledgers ("Books"), each with its own set of categories, tags, and payees.
*   **Multi-Currency Support:**
    *   Assignment of specific currencies to financial accounts.
    *   Handling of transactions involving different currencies, including the storage of original and converted amounts.
    *   Consolidated reporting in a single, user-defined default currency.
*   **File Attachments:** Uploading, viewing, and deleting files (e.g., receipts, invoices) associated with specific transactions.
*   **User and Group Management:** User registration, authentication, and the ability to manage collaborative groups with different user roles.

#### 1.3.2 Out of Scope

The following functionalities are considered out of scope for this version of the specification:

*   **Direct Bank Synchronization:** The system does not automatically import transaction data from financial institutions. All data entry is manual.
*   **Automated Budgeting and Forecasting:** The system provides reporting on past activity but does not include features for creating budgets, setting spending goals, or forecasting future financial states.
*   **Investment Portfolio Management:** The system can track the balance of an investment account as a simple asset but does not manage individual stocks, bonds, or performance tracking.
*   **Client Applications:** This document specifies the API backend only. The design and implementation of any web, mobile, or desktop client applications are not covered.
*   **Advanced Tax Preparation:** The system does not generate tax forms or provide features specifically for tax compliance.
