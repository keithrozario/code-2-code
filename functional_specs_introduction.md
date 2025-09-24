# Functional Specification: MoneyNote Application

## 1. Introduction

This document provides a detailed functional specification for the MoneyNote application, an open-source, self-hostable bookkeeping solution. It describes the system's features, capabilities, and the underlying business logic from the perspective of the end-user.

### 1.1. Purpose of the Document

The purpose of this functional specification is to establish a clear and comprehensive understanding of the MoneyNote application's functionality. It serves as a foundational document for various stakeholders:

*   **For Business Analysts and Product Managers**: It formalizes the system's capabilities and user journeys, providing a baseline for future feature development and enhancement.
*   **For Developers**: It acts as an authoritative guide for implementing and maintaining the system, detailing the business rules, data structures, and API functionalities required.
*   **For Quality Assurance Teams**: It provides the basis for creating test plans and test cases to ensure the application meets its intended requirements.
*   **For Project Modernization**: It documents the "as-is" state of the application, which is critical for planning and executing migration and modernization efforts, such as the strategic recommendations outlined in the associated project modernization reports.

This document translates the system's existing behavior, as analyzed from the source code and user journey documents, into a structured set of functional requirements.

### 1.2. Goals and Objectives

The primary goal of the MoneyNote application is to empower users with a private, independent, and comprehensive tool to manage their finances effectively. The system aims to achieve the following high-level objectives:

*   **Provide Financial Clarity**: To offer users a clear and immediate understanding of their financial health by providing a consolidated overview of their assets, liabilities, and net worth.
*   **Enable Detailed Financial Tracking**: To allow for meticulous recording of all financial transactions, including incomes, expenses, and transfers, with robust support for categorization and tagging for detailed analysis.
*   **Support Diverse Financial Structures**: To accommodate various financial scenarios through support for multiple "Books" (ledgers), allowing users to segregate personal, business, or project-based finances.
*   **Handle Global Finances**: To provide seamless support for multiple currencies, enabling users to manage accounts and transactions in different currencies with consistent reporting in a single base currency.
*   **Ensure Data Integrity and Accessibility**: To maintain the integrity of financial records while allowing users to enrich their data with file attachments (e.g., receipts) and export it for external analysis or backup.
*   **Facilitate Collaboration**: To allow multiple users to collaborate on shared financial books within a "Group," with role-based access control.

### 1.3. Scope

This document defines the functional scope of the MoneyNote backend application API.

#### 1.3.1. In Scope

The following features and functionalities are within the scope of this specification:

*   **Financial Overview**: Calculation and presentation of total assets, debts, and net worth.
*   **Transaction Management**: Full CRUD (Create, Read, Update, Delete) operations for financial transactions, including expenses, incomes, transfers, and balance adjustments.
*   **Categorization and Tagging**: Management of hierarchical categories and tags scoped to individual books.
*   **Multi-Book Management**: Creation of books from scratch, from templates, or by copying existing books. Management and isolation of financial data within these books.
*   **Multi-Currency Support**: Management of accounts and transactions in different currencies, including automated exchange rate fetching and manual overrides. All reporting is consolidated into a single base currency.
*   **File Management**: Uploading, attaching, viewing, and deleting files associated with financial transactions.
*   **Data Export**: Exporting a book's complete transaction history to an Excel (`.xlsx`) file.
*   **User and Group Management**: User registration, authentication, and the ability to manage finances collaboratively within groups with role-based access.

#### 1.3.2. Out of Scope

The following items are considered outside the scope of this functional specification document:

*   **Frontend Implementation**: The specific design, user interface (UI), and user experience (UX) of any client application (web or mobile) that consumes the API. This document defines the functional capabilities the API must provide, not how they are presented to the user.
*   **Infrastructure and Deployment**: The underlying infrastructure, server configuration, and specific deployment procedures.
*   **Implementation of Modernization Strategies**: The technical implementation details of migrating the application to cloud-native services (e.g., Google Cloud SQL, Cloud Storage, BigQuery), as recommended in the data layer assessment report. This document defines the functionality to be migrated, not the migration process itself.
*   **Non-Functional Requirements**: Specific performance benchmarks, scalability targets, load testing, and detailed security hardening procedures (e.g., penetration testing).
*   **Third-Party Integrations**: Any integrations with external systems beyond the specified API for fetching currency exchange rates.
