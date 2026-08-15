#!/usr/bin/env python3
"""
SecureVault — one-time GitHub backlog creation script.

Run via GitHub Actions with GITHUB_TOKEN set, or locally with gh auth login.
Uses the `gh` CLI for all operations.
"""
import subprocess
import json
import sys
import time

REPO = "ahmed-shameel/secure-vault"


def gh(*args, check=True):
    cmd = ["gh"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"WARN: {' '.join(cmd)}\n  stdout: {result.stdout.strip()}\n  stderr: {result.stderr.strip()}")
    return result


def create_label(name, color, description):
    gh("label", "create", name,
       "--repo", REPO,
       "--color", color,
       "--description", description,
       "--force")
    print(f"  label: {name}")


def create_milestone(title, description):
    result = gh("api", "--method", "POST",
                f"/repos/{REPO}/milestones",
                "-f", f"title={title}",
                "-f", f"description={description}",
                "-f", "state=open",
                check=False)
    if result.returncode != 0 and "already_exists" not in result.stderr:
        print(f"  WARN milestone '{title}': {result.stderr.strip()}")
    else:
        print(f"  milestone: {title}")


def milestone_exists(title):
    result = gh("api", f"/repos/{REPO}/milestones",
                "--jq", f'.[] | select(.title=="{title}") | .title')
    return bool(result.stdout.strip())


def create_issue(title, labels, milestone, body):
    result = gh("issue", "create",
                "--repo", REPO,
                "--title", title,
                "--label", labels,
                "--milestone", milestone,
                "--body", body,
                check=False)
    if result.returncode != 0:
        print(f"  WARN issue '{title}': {result.stderr.strip()}")
    else:
        url = result.stdout.strip()
        print(f"  issue: {title} → {url}")
    time.sleep(0.3)


# ─────────────────────────────────────────────────────────────────────────────
# LABELS
# ─────────────────────────────────────────────────────────────────────────────

LABELS = [
    # Type
    ("type:epic",          "8B5CF6", "Epic issue grouping related work"),
    ("type:feature",       "3B82F6", "New feature or functionality"),
    ("type:task",          "6B7280", "Technical task or chore"),
    ("type:security",      "DC2626", "Security-related work"),
    ("type:documentation", "0EA5E9", "Documentation work"),
    ("type:ux",            "EC4899", "UX/UI design work"),
    # Area
    ("area:backend",       "10B981", "Backend / Java / Spring Boot"),
    ("area:frontend",      "F59E0B", "Frontend / Angular / TypeScript"),
    ("area:database",      "8B5CF6", "Database / PostgreSQL / Flyway"),
    ("area:security",      "DC2626", "Security domain"),
    ("area:devops",        "6366F1", "DevOps / CI/CD / Infrastructure"),
    ("area:blockchain",    "F97316", "Blockchain / Testnet"),
    ("area:documentation", "0EA5E9", "Documentation"),
    ("area:ux",            "EC4899", "UX / Design"),
    # Priority
    ("priority:P0",        "DC2626", "Required for MVP – blocks fundamental development"),
    ("priority:P1",        "F59E0B", "Important for MVP"),
    ("priority:P2",        "3B82F6", "Important but can come after MVP"),
    ("priority:P3",        "9CA3AF", "Future / nice-to-have"),
    # Status
    ("status:blocked",     "EF4444", "Blocked by another issue"),
    ("status:ready",       "10B981", "Ready to be worked on"),
    ("status:in-progress", "F59E0B", "Currently being worked on"),
    ("status:review",      "6366F1", "In review"),
]

# ─────────────────────────────────────────────────────────────────────────────
# MILESTONES
# ─────────────────────────────────────────────────────────────────────────────

MILESTONES = [
    ("Foundation",                "Repository setup, architecture, and development environment"),
    ("Authentication & Security", "User auth, MFA, sessions, and security foundation"),
    ("Core Wallets",              "Wallet management, dashboard, and recipients"),
    ("Transactions",              "Transaction domain, send flow, history, and review"),
    ("Security Center",           "Security Center, notifications, and security testing"),
    ("MVP",                       "Complete MVP release with all core features"),
    ("Testnet Integration",       "Blockchain testnet integration and abstraction layer"),
    ("Open Source Release",       "Documentation, contribution guides, and public release"),
]

# ─────────────────────────────────────────────────────────────────────────────
# ISSUES  — (title, labels_csv, milestone_key, body)
# milestone_key must match a MILESTONES title
# ─────────────────────────────────────────────────────────────────────────────

ISSUES = []

# ── EPICS ────────────────────────────────────────────────────────────────────

ISSUES += [

("EPIC 0 — Project Foundation",
 "type:epic,priority:P0,area:documentation",
 "Foundation",
"""## EPIC 0 — Project Foundation

Establish the repository as a serious open-source project with proper structure, documentation, and community files.

### Scope
- Repository structure and configuration files (.gitignore, .editorconfig)
- Core documentation: README, LICENSE, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT
- GitHub templates: issue templates, PR template
- Project documentation directory structure

### Child Issues
- FOUND-001 Initialize repository structure and configuration files
- FOUND-002 Create README.md
- FOUND-003 Create LICENSE file
- FOUND-004 Create CONTRIBUTING.md
- FOUND-005 Create SECURITY.md
- FOUND-006 Create CODE_OF_CONDUCT.md
- FOUND-007 Create GitHub issue templates
- FOUND-008 Create pull request template
"""),

("EPIC 1 — Architecture & Development Environment",
 "type:epic,priority:P0,area:backend,area:devops",
 "Foundation",
"""## EPIC 1 — Architecture & Development Environment

Define the system architecture, module boundaries, and create a working local development environment.

### Scope
- High-level architecture (C4 diagrams) and ADR structure
- Backend module boundaries: auth, users, wallets, transactions, recipients, security, notifications
- Docker Compose local environment with PostgreSQL
- Threat model placeholder

### Child Issues
- ARCH-001 Define high-level system architecture
- ARCH-002 Set up Docker Compose local development environment
- ARCH-003 Create local development documentation
"""),

("EPIC 2 — Backend Foundation",
 "type:epic,priority:P0,area:backend,area:database",
 "Foundation",
"""## EPIC 2 — Backend Foundation

Initialize and configure the Spring Boot application with all foundational infrastructure.

### Scope
- Spring Boot + Maven initialization
- Framework config: Web, JPA, Security, Validation
- PostgreSQL + Flyway
- OpenAPI / Swagger UI
- Exception handling and standardized error responses
- Structured logging and Actuator
- JUnit 5 + Testcontainers foundations

### Child Issues
- BE-001 Initialize Spring Boot application
- BE-002 Configure PostgreSQL and Flyway
- BE-003 Configure exception handling and API error response format
- BE-004 Configure OpenAPI documentation
- BE-005 Configure structured logging
"""),

("EPIC 3 — Authentication & Identity",
 "type:epic,priority:P0,area:backend,area:security",
 "Authentication & Security",
"""## EPIC 3 — Authentication & Identity

Implement the complete user authentication system.

### Scope
- User domain and persistence
- Registration with BCrypt password hashing (cost ≥ 12)
- JWT-based login/logout with refresh tokens
- Session management, expiration, and revocation
- TOTP MFA setup, verification, and recovery codes
- Rate limiting on auth endpoints
- Security events for all auth actions

### Security Requirements
- Passwords never stored in plaintext
- Sensitive user data never exposed in API responses

### Child Issues
- AUTH-001 Implement user domain and persistence
- AUTH-002 Implement user registration
- AUTH-003 Implement login and JWT authentication
- AUTH-004 Implement session management
- AUTH-005 Implement MFA (TOTP)
- AUTH-006 Implement rate limiting for authentication endpoints
"""),

("EPIC 4 — Security Foundation",
 "type:epic,priority:P0,area:security",
 "Authentication & Security",
"""## EPIC 4 — Security Foundation

Establish threat models, security testing strategies, and foundational security controls.

### Scope
- Threat models: authentication, authorization, API, wallets, transactions, sessions, infrastructure
- Security testing strategy (OWASP Top 10 coverage)
- Audit logging and security event model

### Child Issues
- SEC-001 Create threat model — Authentication & Sessions
- SEC-002 Create threat model — API and Authorization
- SEC-003 Create threat model — Wallets and Transactions
- SEC-004 Define security testing strategy
- SEC-005 Implement audit logging
"""),

("EPIC 5 — Angular Frontend Foundation",
 "type:epic,priority:P0,area:frontend",
 "Foundation",
"""## EPIC 5 — Angular Frontend Foundation

Initialize and configure the Angular application with routing, auth state, API client, and error handling.

### Scope
- Angular CLI with TypeScript strict mode, ESLint, Prettier
- Routing with lazy-loaded feature modules
- Environment configuration
- Application shell and navigation
- Authentication state management and JWT interceptor
- HTTP error handling and auth guards
- Global error handling and loading states

### Child Issues
- FE-001 Initialize Angular application
- FE-002 Create application shell, routing, and navigation
- FE-003 Implement authentication state and HTTP client
- FE-004 Implement global error handling and loading states
"""),

("EPIC 6 — UX/UI Design",
 "type:epic,priority:P1,area:ux",
 "Foundation",
"""## EPIC 6 — UX/UI Design

Complete UX/UI design from information architecture through high-fidelity designs, design system, and reusable components.

### Scope
- Information architecture and navigation design
- User flow wireframes for all MVP screens
- Design system: typography, colors, spacing, components
- Responsive behavior definitions
- Accessibility requirements (WCAG 2.1 AA)
- Edge case state designs: loading, empty, error, success, pending

### UX Tickets
UX-001 through UX-020 — see individual issues.
"""),

("EPIC 7 — Dashboard",
 "type:epic,priority:P1,area:backend,area:frontend,area:ux",
 "Core Wallets",
"""## EPIC 7 — Dashboard

Implement the main dashboard showing portfolio overview, wallet summaries, recent transactions, and security status.

### Scope
- Dashboard aggregation API endpoint
- Portfolio, asset, and wallet summaries
- Recent transactions widget
- Security status widget
- Angular dashboard with all states (loading, empty, error)

### Child Issues
- DASH-001 Implement dashboard API endpoint
- DASH-002 Implement Angular dashboard component
"""),

("EPIC 8 — Wallet Management",
 "type:epic,priority:P1,area:backend,area:frontend,area:ux",
 "Core Wallets",
"""## EPIC 8 — Wallet Management

Implement wallet domain with mocked/testnet wallets, wallet list, details, and address display.

**Important:** Initially wallets must be mocked/testnet only. No real-money custody.

### Scope
- Wallet domain, persistence, service, and REST API
- Wallet list and details endpoints
- Angular wallet list and details UI
- Address display with copy and QR code
- Network information display

### Child Issues
- WALLET-001 Implement wallet domain model and persistence
- WALLET-002 Implement wallet service and REST API
- WALLET-003 Implement Angular wallet list and details UI
"""),

("EPIC 9 — Recipients",
 "type:epic,priority:P1,area:backend,area:frontend,area:ux",
 "Transactions",
"""## EPIC 9 — Recipients

Implement saved recipients with CRUD operations, validation, and security considerations around address manipulation.

### Scope
- Recipient domain, persistence, and CRUD API
- Address format validation per asset type
- Security: prevent address manipulation
- Angular recipient management UI

### Child Issues
- RECIP-001 Implement recipient domain, persistence, and API
- RECIP-002 Implement Angular recipients UI
"""),

("EPIC 10 — Transaction Management",
 "type:epic,priority:P1,area:backend,area:frontend,area:ux",
 "Transactions",
"""## EPIC 10 — Transaction Management

Implement the complete transaction domain with lifecycle, send flow, review, MFA authorization, and history.

### Transaction Lifecycle
`REQUESTED → VALIDATING → AWAITING_AUTHORIZATION → AUTHORIZED → PROCESSING → CONFIRMED` (with FAILED and CANCELLED states)

**Important:** No real blockchain broadcasting in MVP. Use mocked processing.

### Child Issues
- TXN-001 Implement transaction domain model and lifecycle
- TXN-002 Implement create transaction and review endpoints
- TXN-003 Implement transaction authorization with MFA
- TXN-004 Implement transaction history and details endpoints
- TXN-005 Implement Angular send flow and transaction UI
"""),

("EPIC 11 — Security Center",
 "type:epic,priority:P1,area:backend,area:frontend,area:ux",
 "Security Center",
"""## EPIC 11 — Security Center

Implement the Security Center with MFA status, sessions, devices, login history, and security alerts.

### Scope
- Security Center API: overview, sessions, devices, activity log
- Session revocation
- Angular Security Center UI

### Child Issues
- SECCTR-001 Implement Security Center API
- SECCTR-002 Implement Angular Security Center UI
"""),

("EPIC 12 — Notifications",
 "type:epic,priority:P1,area:backend,area:frontend",
 "Security Center",
"""## EPIC 12 — Notifications

Implement in-app notifications for security events and transaction updates.

### Notification Types
New login, new device, MFA change, new recipient, transaction authorized, transaction confirmed, suspicious activity

### Child Issues
- NOTIF-001 Implement notification domain and service
- NOTIF-002 Implement notifications API and Angular UI
"""),

("EPIC 13 — Testing & Quality",
 "type:epic,priority:P1,area:backend,area:frontend,area:devops",
 "MVP",
"""## EPIC 13 — Testing & Quality

Establish comprehensive testing strategy and quality tooling across all layers.

### Scope
- Testcontainers integration test infrastructure
- Security test suite (auth, IDOR, injection)
- Static analysis (SpotBugs/find-sec-bugs, Checkstyle)
- OWASP dependency scanning
- Frontend tests

### Child Issues
- TEST-001 Set up Testcontainers integration test infrastructure
- TEST-002 Implement security test suite
- TEST-003 Configure static analysis and dependency scanning
"""),

("EPIC 14 — Blockchain/Testnet Integration",
 "type:epic,priority:P2,area:blockchain",
 "Testnet Integration",
"""## EPIC 14 — Blockchain/Testnet Integration

Implement blockchain abstraction layer and testnet integrations (Ethereum Sepolia, Bitcoin testnet).

**Important:** This epic must NOT block the core MVP. Application must work fully with mocked blockchain services first.

### Child Issues
- CHAIN-001 Define blockchain abstraction interface
- CHAIN-002 Implement Ethereum testnet (Sepolia) integration
"""),

("EPIC 15 — CI/CD & DevSecOps",
 "type:epic,priority:P1,area:devops",
 "MVP",
"""## EPIC 15 — CI/CD & DevSecOps

Implement complete CI/CD pipeline with automated tests, static analysis, and security scanning.

### Pipeline
`Build → Unit Tests → Integration Tests → Static Analysis → Security Scans → Review → Merge`

### Child Issues
- CI-001 Implement GitHub Actions backend CI pipeline
- CI-002 Add security scanning to CI pipeline
- CI-003 Implement frontend CI pipeline
"""),

("EPIC 16 — Open Source & Documentation",
 "type:epic,priority:P1,area:documentation",
 "Open Source Release",
"""## EPIC 16 — Open Source & Documentation

Create comprehensive documentation to make SecureVault a credible, welcoming open-source project.

### Child Issues
- DOCS-001 Write architecture documentation
- DOCS-002 Write API documentation and developer guide
"""),

("EPIC 17 — MVP Release",
 "type:epic,priority:P0,area:devops",
 "MVP",
"""## EPIC 17 — MVP Release

Coordinate and execute the MVP release: end-to-end testing, security review, UX review, and release checklist.

### MVP Feature Set
Authentication + MFA + Sessions + Dashboard + Wallets + Recipients + Transaction History + Mock Send Flow + Transaction Review + Security Center + Security Activity + Notifications + Tests + CI + Security Scanning + Documentation

### Child Issues
- MVP-001 End-to-end testing for MVP
- MVP-002 Security review for MVP
- MVP-003 UX and accessibility review for MVP
- MVP-004 Release checklist and GitHub Release v0.1.0
"""),

("EPIC 18 — Future Production Engineering",
 "type:epic,priority:P3,area:devops,area:backend",
 "Open Source Release",
"""## EPIC 18 — Future Production Engineering

Future architecture improvements for production-grade scalability and observability. Must NOT block MVP.

### Scope
Redis, Kafka, Observability (Micrometer + OpenTelemetry + Grafana), Cloud deployment, High availability, Disaster recovery, Scalability testing, Advanced fraud detection.

### Child Issues
- FUTURE-001 Evaluate Redis for caching and session storage
- FUTURE-002 Evaluate event-driven architecture with Kafka
- FUTURE-003 Observability — metrics, tracing, and dashboards
"""),

]  # end epics

# ── EPIC 0 — Project Foundation ──────────────────────────────────────────────

ISSUES += [

("FOUND-001: Initialize repository structure and configuration files",
 "type:task,area:documentation,priority:P0,status:ready",
 "Foundation",
"""## Description
Set up the foundational repository structure with all essential configuration files.

## Scope
- `.gitignore` for Java/Maven/Node/Angular/IDE files/secrets
- `.editorconfig` for consistent code style (indent, charset, end-of-line)
- `docs/` directory structure
- `backend/` and `frontend/` directory stubs
- Verify repository settings (default branch, topics)

## Acceptance Criteria
- [ ] `.gitignore` covers Java, Maven/Gradle, Node, Angular, IDE files, and secrets
- [ ] `.editorconfig` defines indent style, charset, and end-of-line for all file types
- [ ] Directory structure is documented in README
- [ ] Repository has appropriate GitHub topics set

## Testing Requirements
Manual verification of file presence and content.

## Dependencies
None

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-002: Create README.md",
 "type:documentation,area:documentation,priority:P0,status:ready",
 "Foundation",
"""## Description
Create a comprehensive README that establishes SecureVault as a credible open-source security-first digital asset platform.

## Scope
- Project description and core principle: "Security first. Minimize trust."
- Technology stack overview
- Quick start / local development instructions (placeholder until ARCH-002)
- Architecture overview (placeholder until ARCH-001)
- Contributing and Security policy links
- License badge and CI status badge (placeholder)

## Acceptance Criteria
- [ ] README clearly describes what SecureVault is
- [ ] Core principle is prominently displayed
- [ ] Technology stack is listed
- [ ] Contributing and Security links are present
- [ ] README looks professional for an open-source project

## Testing Requirements
Review for clarity and completeness.

## Dependencies
None

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-003: Create LICENSE file",
 "type:task,area:documentation,priority:P0,status:ready",
 "Foundation",
"""## Description
Add an open-source license to the repository.

## Scope
- Select appropriate license (MIT recommended)
- Add LICENSE file to repository root
- Reference license in README

## Acceptance Criteria
- [ ] LICENSE file exists in repository root
- [ ] License type is stated in README
- [ ] Year and copyright holder are correct

## Testing Requirements
Manual review.

## Dependencies
- FOUND-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-004: Create CONTRIBUTING.md",
 "type:documentation,area:documentation,priority:P1,status:ready",
 "Foundation",
"""## Description
Create contribution guidelines that help external contributors participate in the SecureVault project.

## Scope
- How to report bugs and suggest features
- Development setup prerequisites
- Pull request process and conventions
- Code style requirements
- Commit message conventions (Conventional Commits)
- Review process

## Acceptance Criteria
- [ ] CONTRIBUTING.md covers all required sections
- [ ] Development prerequisites are listed
- [ ] PR process is clearly described
- [ ] Code style expectations are documented
- [ ] Commit convention is specified

## Testing Requirements
Review for completeness.

## Dependencies
- FOUND-002, FOUND-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-005: Create SECURITY.md",
 "type:documentation,area:security,area:documentation,priority:P0,status:ready",
 "Foundation",
"""## Description
Create a security policy documenting responsible vulnerability reporting for SecureVault.

## Scope
- Supported versions
- Vulnerability reporting process (private disclosure)
- Response time commitments
- What NOT to do (public disclosure before fix)
- Security contact / GitHub Security Advisory process

## Acceptance Criteria
- [ ] SECURITY.md exists at repository root
- [ ] Private vulnerability disclosure process is documented
- [ ] Response time expectations are set
- [ ] Security contact / advisory process is referenced

## Testing Requirements
Review for completeness.

## Dependencies
None

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-006: Create CODE_OF_CONDUCT.md",
 "type:documentation,area:documentation,priority:P1,status:ready",
 "Foundation",
"""## Description
Add a Code of Conduct to establish community standards.

## Scope
- Use Contributor Covenant 2.1 as the base
- Customize with project contact information
- Reference in CONTRIBUTING.md

## Acceptance Criteria
- [ ] CODE_OF_CONDUCT.md exists at repository root
- [ ] Uses Contributor Covenant 2.1
- [ ] Contact information is present
- [ ] Referenced from CONTRIBUTING.md

## Testing Requirements
Manual review.

## Dependencies
- FOUND-004

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-007: Create GitHub issue templates",
 "type:task,area:documentation,priority:P1,status:ready",
 "Foundation",
"""## Description
Create GitHub issue templates to ensure consistent, high-quality bug reports and feature requests.

## Scope
- Bug report template: description, steps to reproduce, expected vs actual, environment
- Feature request template: description, motivation, scope, acceptance criteria
- Security vulnerability template — redirect to SECURITY.md
- Blank issue template

## Acceptance Criteria
- [ ] `.github/ISSUE_TEMPLATE/bug_report.yml` exists
- [ ] `.github/ISSUE_TEMPLATE/feature_request.yml` exists
- [ ] Templates include all required fields
- [ ] Security template redirects to responsible disclosure process

## Testing Requirements
Manual verification by creating test issues.

## Dependencies
- FOUND-005

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

("FOUND-008: Create pull request template",
 "type:task,area:documentation,priority:P1,status:ready",
 "Foundation",
"""## Description
Create a pull request template to ensure consistent PR descriptions and review checklists.

## Scope
- PR description sections: What, Why, How, Testing
- Checklist: tests pass, code reviewed, docs updated, security considered
- Link to related issue

## Acceptance Criteria
- [ ] `.github/pull_request_template.md` exists
- [ ] Template includes description, checklist, and issue reference
- [ ] Security consideration checkbox is included

## Testing Requirements
Manual verification.

## Dependencies
- FOUND-004

## Suggested Assignee
Ahmed

## Related Epic
EPIC 0 — Project Foundation
"""),

]

# ── EPIC 1 — Architecture ─────────────────────────────────────────────────────

ISSUES += [

("ARCH-001: Define high-level system architecture",
 "type:task,area:backend,area:frontend,priority:P0,status:ready",
 "Foundation",
"""## Description
Define and document the high-level architecture of SecureVault as a modular monolith with clear domain boundaries.

## Scope
- C4 Level 1 (System Context) and Level 2 (Container) diagrams
- Module boundaries: auth, users, wallets, transactions, recipients, security, notifications
- Frontend/backend communication contract (REST API)
- Database architecture overview
- Transaction lifecycle state diagram
- Security boundary definitions
- `docs/architecture/` directory with ADR structure
- ADR-001: Modular monolith decision

## Acceptance Criteria
- [ ] Architecture diagrams exist in `docs/architecture/`
- [ ] All domain module boundaries are documented
- [ ] Transaction lifecycle states are defined
- [ ] Security boundaries are identified
- [ ] ADR-001 documents the modular monolith decision

## Testing Requirements
Architecture review with team.

## Dependencies
- FOUND-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 1 — Architecture & Development Environment
"""),

("ARCH-002: Set up Docker Compose local development environment",
 "type:task,area:devops,area:backend,priority:P0,status:ready",
 "Foundation",
"""## Description
Create a Docker Compose configuration that enables any developer to run the full stack locally with a single command.

## Scope
- `docker-compose.yml` with PostgreSQL service
- `.env.example` documenting all required environment variables
- Health checks for all services
- Volume mounts for database persistence
- Makefile or startup script with common commands

## Acceptance Criteria
- [ ] `docker-compose up` starts PostgreSQL successfully
- [ ] Database is accessible on configured port
- [ ] `.env.example` documents all required environment variables
- [ ] No secrets are committed to repository
- [ ] Health check confirms PostgreSQL is ready
- [ ] Works on macOS and Linux

## Testing Requirements
Manual: run `docker-compose up` from clean state and verify all services start.

## Dependencies
- FOUND-001, ARCH-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 1 — Architecture & Development Environment
"""),

("ARCH-003: Create local development documentation",
 "type:documentation,area:documentation,area:devops,priority:P0,status:ready",
 "Foundation",
"""## Description
Document how to set up and run SecureVault locally so any new developer can be productive quickly.

## Scope
- Prerequisites (Java version, Node, Docker, etc.)
- Step-by-step setup instructions
- Environment variable guide
- Running backend and frontend
- Running tests
- Common troubleshooting

## Acceptance Criteria
- [ ] `docs/development/local-setup.md` exists
- [ ] A developer following the guide can run the project from scratch
- [ ] All prerequisite versions are specified
- [ ] Troubleshooting section covers common issues

## Testing Requirements
Walk-through by a second person following the guide from scratch.

## Dependencies
- ARCH-002, BE-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 1 — Architecture & Development Environment
"""),

]

# ── EPIC 2 — Backend Foundation ───────────────────────────────────────────────

ISSUES += [

("BE-001: Initialize Spring Boot application",
 "type:task,area:backend,priority:P0,status:ready",
 "Foundation",
"""## Description
Bootstrap the Spring Boot application with the foundational project structure and all required dependencies.

## Scope
- Initialize Spring Boot project with Maven
- Dependencies: Spring Web, Spring Data JPA, Spring Security, Spring Validation, Flyway, PostgreSQL driver, Spring Actuator, Lombok
- Configure application.yml with profiles: dev, test, prod
- Package structure: `com.securevault.*` with domain modules
- Basic health endpoint: `GET /actuator/health`

## Acceptance Criteria
- [ ] Application starts successfully
- [ ] `GET /actuator/health` returns `{"status":"UP"}`
- [ ] `./mvnw package` succeeds
- [ ] Package structure follows defined module boundaries
- [ ] Application profiles (dev, test, prod) are configured
- [ ] No hardcoded secrets in configuration

## Testing Requirements
- Unit test: application context loads
- Integration test: health endpoint returns 200

## Dependencies
- ARCH-001, ARCH-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 2 — Backend Foundation
"""),

("BE-002: Configure PostgreSQL and Flyway",
 "type:task,area:backend,area:database,priority:P0,status:ready",
 "Foundation",
"""## Description
Configure the PostgreSQL database connection and Flyway migration tooling.

## Scope
- Configure Spring Data JPA with PostgreSQL
- Configure HikariCP connection pooling
- Configure Flyway with baseline migration
- Create initial migration: `V1__init_schema.sql`
- Configure Testcontainers for integration tests
- Document database naming conventions

## Acceptance Criteria
- [ ] Application connects to PostgreSQL on startup
- [ ] Flyway runs migrations automatically on startup
- [ ] `V1__init_schema.sql` exists
- [ ] Integration tests use Testcontainers (not H2)
- [ ] Database configuration is environment-variable-driven
- [ ] No database credentials in source code

## Testing Requirements
- Integration test: application context loads with Testcontainers PostgreSQL
- Integration test: Flyway migration runs successfully

## Dependencies
- BE-001, ARCH-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 2 — Backend Foundation
"""),

("BE-003: Configure exception handling and API error response format",
 "type:task,area:backend,priority:P0,status:ready",
 "Foundation",
"""## Description
Establish a consistent, secure error response format for all API errors that does not leak internal implementation details.

## Scope
- Global exception handler (`@RestControllerAdvice`)
- Standard error response DTO: `{timestamp, status, error, message, path}`
- Exception mapping for: validation errors, not found, unauthorized, forbidden, conflict, internal server error
- Stack traces never returned to clients
- Error messages never leak sensitive information

## Acceptance Criteria
- [ ] All API errors return the standard error response format
- [ ] Stack traces are never included in error responses
- [ ] Validation errors return field-level error details
- [ ] 404, 401, 403, 409, 500 are all handled consistently
- [ ] Error messages do not expose internal implementation details

## Testing Requirements
- Unit tests for exception handler
- Integration tests: trigger each error type and verify response format

## Dependencies
- BE-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 2 — Backend Foundation
"""),

("BE-004: Configure OpenAPI documentation",
 "type:task,area:backend,area:documentation,priority:P1,status:ready",
 "Foundation",
"""## Description
Set up Springdoc OpenAPI to automatically generate interactive API documentation.

## Scope
- Add springdoc-openapi dependency
- Configure OpenAPI info (title, description, version, contact, license)
- Swagger UI at `/swagger-ui.html`
- OpenAPI JSON at `/v3/api-docs`
- Security scheme definition
- Disable Swagger UI in production profile

## Acceptance Criteria
- [ ] Swagger UI accessible at `/swagger-ui.html` in dev profile
- [ ] OpenAPI JSON available at `/v3/api-docs`
- [ ] API info is populated
- [ ] Swagger UI disabled in production profile
- [ ] Security scheme is documented

## Testing Requirements
Manual: open Swagger UI and verify endpoints are listed.

## Dependencies
- BE-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 2 — Backend Foundation
"""),

("BE-005: Configure structured logging",
 "type:task,area:backend,priority:P1,status:ready",
 "Foundation",
"""## Description
Configure structured logging with appropriate log levels and security considerations.

## Scope
- Logback with structured JSON output for production
- Human-readable format for development
- Sensitive data (passwords, tokens, keys) never logged
- Request/response logging excluding sensitive headers/bodies
- Correlation IDs for request tracing

## Acceptance Criteria
- [ ] Logs use structured JSON format in production profile
- [ ] Passwords, tokens, and keys are never present in logs
- [ ] HTTP request logging excludes Authorization headers
- [ ] Log levels appropriate (INFO in prod, DEBUG in dev)
- [ ] Correlation IDs included in log output

## Testing Requirements
Review log output for sensitive data leakage.

## Dependencies
- BE-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 2 — Backend Foundation
"""),

]

# ── EPIC 3 — Authentication ───────────────────────────────────────────────────

ISSUES += [

("AUTH-001: Implement user domain and persistence",
 "type:feature,area:backend,area:database,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Create the User domain model with persistence layer for storing user accounts securely.

## Scope
- `User` entity: id (UUID), email, passwordHash, createdAt, updatedAt, enabled, emailVerified, mfaEnabled, mfaSecret (encrypted at rest)
- `UserRepository` (Spring Data JPA)
- Flyway migration: `V2__create_users_table.sql`
- `UserService` with basic CRUD
- DTO classes — `passwordHash` never exposed in responses

## Acceptance Criteria
- [ ] `users` table created by Flyway migration
- [ ] Passwords never stored in plaintext
- [ ] `passwordHash` never included in any API response DTO
- [ ] User entity uses UUID as primary key
- [ ] `createdAt` and `updatedAt` are auto-managed
- [ ] Email addresses stored lowercase and trimmed

## Testing Requirements
- Unit tests: UserService
- Integration tests: UserRepository with Testcontainers

## Dependencies
- BE-001, BE-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 3 — Authentication & Identity
"""),

("AUTH-002: Implement user registration",
 "type:feature,area:backend,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Implement the user registration endpoint with BCrypt password hashing, input validation, and duplicate detection.

## Scope
- `POST /api/v1/auth/register`
- Input: email, password, confirmPassword
- BCrypt password hashing (cost factor >= 12)
- Email uniqueness validation (timing-safe)
- Password strength validation (min 12 chars, mixed case, numbers, symbols)
- Security event: `USER_REGISTERED`
- HTTP responses: 201 Created, 409 Conflict, 422 Validation Error

## Acceptance Criteria
- [ ] Registration succeeds with valid input and returns 201
- [ ] Duplicate email returns 409 without revealing if account exists
- [ ] Weak password returns 422 with clear error
- [ ] Password hashed with BCrypt (cost >= 12)
- [ ] `passwordHash` never returned in response
- [ ] Security event `USER_REGISTERED` recorded

## Testing Requirements
- Unit tests: password validation, email normalization
- Integration tests: register endpoint with valid/invalid inputs
- Security test: no timing oracle on duplicate email

## Dependencies
- AUTH-001, BE-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 3 — Authentication & Identity
"""),

("AUTH-003: Implement login and JWT authentication",
 "type:feature,area:backend,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Implement login endpoint with JWT token issuance and Spring Security configuration.

## Scope
- `POST /api/v1/auth/login`
- Spring Security configuration
- JWT access token (short-lived, e.g. 15 minutes)
- Refresh token (longer-lived, stored in DB)
- `POST /api/v1/auth/refresh`
- JWT validation filter
- `POST /api/v1/auth/logout` (invalidate refresh token)
- Security events: `USER_LOGIN_SUCCESS`, `USER_LOGIN_FAILED`

## Acceptance Criteria
- [ ] Valid credentials return 200 with access_token and refresh_token
- [ ] Invalid credentials return 401 (same message regardless of which field is wrong)
- [ ] Access token expires after configured TTL
- [ ] Refresh token rotation on use
- [ ] Logout invalidates the refresh token
- [ ] Failed login generates security events
- [ ] Tokens use RS256 or HS256 with secure secret

## Testing Requirements
- Unit tests: JWT generation, validation
- Integration tests: login/logout/refresh flows
- Security test: token replay after logout

## Dependencies
- AUTH-001, AUTH-002, BE-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 3 — Authentication & Identity
"""),

("AUTH-004: Implement session management",
 "type:feature,area:backend,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Implement session tracking, expiration, and revocation to support the Security Center.

## Scope
- `Session` entity: id, userId, deviceInfo, ipAddress, userAgent, createdAt, lastActivityAt, expiresAt, revoked
- Flyway migration for sessions table
- Session creation on login
- Session expiration enforcement
- `DELETE /api/v1/sessions/{sessionId}` — revoke session
- `GET /api/v1/sessions` — list active sessions
- Security event on session revocation

## Acceptance Criteria
- [ ] Sessions created and tracked per login
- [ ] Expired sessions are rejected
- [ ] Users can list their active sessions
- [ ] Users can revoke individual sessions
- [ ] Revoked session tokens rejected immediately
- [ ] IP address and user agent stored per session
- [ ] Security event generated on revocation

## Testing Requirements
- Integration tests: session lifecycle
- Security test: revoked session cannot access protected endpoints

## Dependencies
- AUTH-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 3 — Authentication & Identity
"""),

("AUTH-005: Implement MFA (TOTP)",
 "type:feature,area:backend,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Implement TOTP-based multi-factor authentication including setup, verification, and recovery codes.

## Scope
- `POST /api/v1/auth/mfa/setup` — returns TOTP secret and QR code
- `POST /api/v1/auth/mfa/confirm` — verifies first code before enabling
- MFA verification step during login
- Recovery codes: generated on setup, hashed in DB, one-time-use
- `DELETE /api/v1/auth/mfa` — disable MFA (requires current MFA code)
- Security events for all MFA actions
- MFA secret encrypted at rest

## Acceptance Criteria
- [ ] TOTP secret generated per user (not shared)
- [ ] QR code generated for authenticator apps
- [ ] MFA cannot be enabled without verifying the first code
- [ ] Recovery codes work as one-time-use fallback
- [ ] Used recovery codes are invalidated
- [ ] MFA secret is encrypted at rest
- [ ] Security events generated for setup, disable, and use

## Testing Requirements
- Unit tests: TOTP verification logic
- Integration tests: MFA setup and verification flow
- Security test: code replay rejected; used recovery code rejected

## Dependencies
- AUTH-003, AUTH-004

## Suggested Assignee
Ahmed

## Related Epic
EPIC 3 — Authentication & Identity
"""),

("AUTH-006: Implement rate limiting for authentication endpoints",
 "type:security,area:backend,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Implement rate limiting on authentication endpoints to prevent brute-force attacks.

## Scope
- Rate limit `POST /api/v1/auth/login` by IP address and by username
- Rate limit `POST /api/v1/auth/register` by IP address
- Rate limit `POST /api/v1/auth/mfa/verify` by user
- Return 429 Too Many Requests with Retry-After header
- Configurable thresholds via application properties
- Security event on rate limit trigger

## Acceptance Criteria
- [ ] Login endpoint rate-limited per IP (configurable, e.g. 10/minute)
- [ ] Login endpoint rate-limited per email/username
- [ ] Rate limit returns 429 with Retry-After header
- [ ] Thresholds are configurable
- [ ] Rate limit triggers security event

## Testing Requirements
Integration tests: trigger rate limit and verify 429 response.

## Dependencies
- AUTH-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 3 — Authentication & Identity
"""),

]

# ── EPIC 4 — Security Foundation ─────────────────────────────────────────────

ISSUES += [

("SEC-001: Create threat model — Authentication & Sessions",
 "type:security,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Document the threat model for authentication and session management to identify risks and drive security controls.

## Scope
- Identify threat actors and assets
- STRIDE analysis for authentication flow
- Threats: credential brute-force, credential stuffing, session hijacking, token replay, MFA bypass
- Mitigations mapped to each threat
- Output: `docs/security/threat-model-auth.md`

## Acceptance Criteria
- [ ] `docs/security/threat-model-auth.md` exists
- [ ] STRIDE analysis covers login, registration, MFA, and session flows
- [ ] Each identified threat has a documented mitigation
- [ ] Document reviewed by Ahmed and Security contributor

## Testing Requirements
Review meeting or async review.

## Dependencies
- AUTH-001 (understanding of scope)

## Suggested Assignee
Security contributor

## Related Epic
EPIC 4 — Security Foundation
"""),

("SEC-002: Create threat model — API and Authorization",
 "type:security,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Document the threat model for the API layer and authorization to identify bypass and privilege escalation risks.

## Scope
- STRIDE analysis for API endpoints
- Threats: unauthorized access, IDOR, privilege escalation, injection attacks
- Input validation requirements definition
- Authorization model: user can only access their own resources
- Output: `docs/security/threat-model-api.md`

## Acceptance Criteria
- [ ] `docs/security/threat-model-api.md` exists
- [ ] Authorization model is defined
- [ ] IDOR threats identified with mitigations
- [ ] Input validation requirements are defined

## Testing Requirements
Review.

## Dependencies
- ARCH-001

## Suggested Assignee
Security contributor

## Related Epic
EPIC 4 — Security Foundation
"""),

("SEC-003: Create threat model — Wallets and Transactions",
 "type:security,area:security,priority:P1,status:ready",
 "Authentication & Security",
"""## Description
Document threat model for wallet management and transaction processing — the highest-risk domain in SecureVault.

## Scope
- Wallet access controls and authorization threats
- Transaction manipulation threats
- Address spoofing/substitution threats
- Double-spend or replay threats
- Recipient poisoning threats
- Output: `docs/security/threat-model-transactions.md`

## Acceptance Criteria
- [ ] `docs/security/threat-model-transactions.md` exists
- [ ] Transaction manipulation threats are identified
- [ ] Address/recipient tampering threats are documented
- [ ] Mitigations defined for each threat

## Testing Requirements
Review.

## Dependencies
- ARCH-001

## Suggested Assignee
Security contributor

## Related Epic
EPIC 4 — Security Foundation
"""),

("SEC-004: Define security testing strategy",
 "type:security,area:security,priority:P1,status:ready",
 "Authentication & Security",
"""## Description
Define a comprehensive security testing strategy covering authentication, authorization, API security, and OWASP Top 10.

## Scope
- Auth security test cases: brute force, session fixation, token replay
- Authorization test cases: IDOR, privilege escalation
- Input validation test cases: injection, XSS via API
- Rate limiting test cases
- Output: `docs/security/security-testing-strategy.md`

## Acceptance Criteria
- [ ] `docs/security/security-testing-strategy.md` exists
- [ ] Covers OWASP Top 10 relevant items
- [ ] Test cases are specific and actionable
- [ ] Mapped to application features

## Testing Requirements
Review.

## Dependencies
- SEC-001, SEC-002

## Suggested Assignee
Security contributor

## Related Epic
EPIC 4 — Security Foundation
"""),

("SEC-005: Implement audit logging",
 "type:security,area:backend,area:security,priority:P1,status:ready",
 "Authentication & Security",
"""## Description
Implement an audit log that records all security-relevant events for accountability and incident response.

## Scope
- `AuditEvent` entity: id, userId, eventType, ipAddress, userAgent, timestamp, metadata (JSON)
- Flyway migration for `audit_events` table
- `AuditService` for recording events
- Event types: USER_REGISTERED, USER_LOGIN_SUCCESS, USER_LOGIN_FAILED, MFA_ENABLED, MFA_DISABLED, PASSWORD_CHANGED, SESSION_REVOKED, TRANSACTION_AUTHORIZED, etc.
- Read API for Security Center: `GET /api/v1/security/audit-events`
- Audit log is append-only (no update/delete endpoints)

## Acceptance Criteria
- [ ] `audit_events` table created by migration
- [ ] All authentication events are recorded
- [ ] Audit records include timestamp, userId, eventType, IP, userAgent
- [ ] Audit log is append-only
- [ ] Security Center can retrieve audit events for current user

## Testing Requirements
Integration tests: verify events recorded for each auth action.

## Dependencies
- AUTH-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 4 — Security Foundation
"""),

]

# ── EPIC 5 — Angular Frontend Foundation ─────────────────────────────────────

ISSUES += [

("FE-001: Initialize Angular application",
 "type:task,area:frontend,priority:P0,status:ready",
 "Foundation",
"""## Description
Bootstrap the Angular application with TypeScript, routing, and foundational project structure.

## Scope
- Angular CLI project initialization with TypeScript strict mode
- ESLint and Prettier configured
- Project structure: feature modules, shared module, core module
- Angular environments: development, production
- Proxy configuration for local backend API calls
- `frontend/README.md` with setup instructions

## Acceptance Criteria
- [ ] `ng serve` starts without errors
- [ ] TypeScript strict mode is enabled
- [ ] ESLint and Prettier are configured
- [ ] Angular environments are configured
- [ ] API proxy configured for local development
- [ ] `ng build` produces production build without errors

## Testing Requirements
`ng test` passes with default test setup.

## Dependencies
- ARCH-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 5 — Angular Frontend Foundation
"""),

("FE-002: Create application shell, routing, and navigation",
 "type:feature,area:frontend,priority:P0,status:ready",
 "Foundation",
"""## Description
Create the application shell with primary navigation, routing, and lazy-loaded feature modules.

## Scope
- App shell component with navigation sidebar/header
- Routes: /login, /dashboard, /wallets, /transactions, /recipients, /security, /notifications
- Lazy loading for all feature modules
- Auth guard for protected routes
- Default redirect: / to /dashboard (if authenticated) or /login
- Active route highlighting in navigation

## Acceptance Criteria
- [ ] All primary routes are configured
- [ ] Feature modules are lazy-loaded
- [ ] Auth guard redirects unauthenticated users to /login
- [ ] Navigation reflects the active route
- [ ] Browser back/forward navigation works correctly

## Testing Requirements
- Unit tests for auth guard
- Unit tests for routing configuration

## Dependencies
- FE-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 5 — Angular Frontend Foundation
"""),

("FE-003: Implement authentication state and HTTP client",
 "type:feature,area:frontend,area:security,priority:P0,status:ready",
 "Authentication & Security",
"""## Description
Implement authentication state service and HTTP client with token management and error-handling interceptors.

## Scope
- `AuthService`: login, logout, refresh, MFA verification
- Token storage (httpOnly cookie preferred or localStorage with CSRF consideration)
- HTTP interceptor: attach Authorization header
- HTTP interceptor: handle 401 -> refresh token or redirect to login
- HTTP interceptor: global error handling
- `AuthStateService`: current user observable

## Acceptance Criteria
- [ ] Login stores tokens securely
- [ ] HTTP requests include Authorization header automatically
- [ ] 401 response triggers token refresh
- [ ] Token refresh failure redirects to login
- [ ] Auth state is observable
- [ ] Logout clears all stored tokens

## Testing Requirements
- Unit tests for AuthService
- Unit tests for HTTP interceptors

## Dependencies
- FE-002, AUTH-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 5 — Angular Frontend Foundation
"""),

("FE-004: Implement global error handling and loading states",
 "type:feature,area:frontend,priority:P1,status:ready",
 "Foundation",
"""## Description
Implement global error handling and loading state management for consistent UX across all components.

## Scope
- Global error handler service
- Toast/notification service for user-facing errors
- Loading state service (global and per-component)
- Error boundary for unhandled errors
- Network error detection and user-friendly display

## Acceptance Criteria
- [ ] Unhandled API errors show user-friendly message
- [ ] Network errors are detected and shown
- [ ] Loading state is trackable per operation
- [ ] Error messages do not expose technical details

## Testing Requirements
Unit tests for error handler.

## Dependencies
- FE-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 5 — Angular Frontend Foundation
"""),

]

# ── EPIC 6 — UX/UI Design ─────────────────────────────────────────────────────

ISSUES += [

("UX-001: Define information architecture",
 "type:ux,area:ux,priority:P0,status:ready",
 "Foundation",
"""## Objective
Define the information architecture (IA) for SecureVault — the structure, hierarchy, and navigation model that underpins all UX design work.

## Inputs
- UX-Requirements.md (Section 5 — Information Architecture)
- MVP feature list: Dashboard, Wallets, Transactions, Send, Receive, Recipients, Notifications, Security Center

## Deliverables
- Sitemap / IA diagram showing all screens and their relationships
- Primary and secondary navigation structure
- Screen inventory list
- Notes on any proposed changes to initial IA with rationale

## Acceptance Criteria
- [ ] All MVP screens are accounted for in the IA
- [ ] Navigation hierarchy is clear (max 2 levels deep for primary flows)
- [ ] IA is documented in Figma or equivalent tool
- [ ] IA is reviewed and approved before wireframes begin
- [ ] Proposed changes to initial IA are documented with rationale

## Dependencies
None

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-002: Define main navigation",
 "type:ux,area:ux,priority:P0,status:ready",
 "Foundation",
"""## Objective
Design the main navigation pattern — the persistent navigation appearing on all authenticated screens.

## Inputs
- UX-001 (Information Architecture)
- UX-Requirements.md Section 5

## Deliverables
- Navigation component design (sidebar / top nav / bottom nav decision)
- Navigation items with labels and icons
- Active, hover, and collapsed states
- Mobile navigation pattern
- Notification unread badge indicator in navigation

## Acceptance Criteria
- [ ] Navigation design covers all primary sections
- [ ] Active state is clearly indicated
- [ ] Mobile navigation is defined
- [ ] Navigation is consistent with IA from UX-001
- [ ] Keyboard navigation is considered for accessibility

## Dependencies
- UX-001

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-003: Design authentication flow",
 "type:ux,area:ux,priority:P0,status:ready",
 "Authentication & Security",
"""## Objective
Design the complete authentication UX including login, MFA verification, and session timeout handling.

## Inputs
- UX-Requirements.md (Section 6 — Login & Authentication)
- AUTH-003, AUTH-005 (technical auth implementation context)

## Deliverables
- Login screen wireframe/design
- MFA verification screen
- Session timeout/expired state design
- Error states: invalid credentials, invalid MFA, too many attempts, account locked
- Success state: redirect to dashboard
- Logout confirmation

## Acceptance Criteria
- [ ] Login screen design is complete
- [ ] MFA screen design is complete
- [ ] All error states from UX-Requirements Section 6 are designed
- [ ] Design does not reveal whether email or password was incorrect
- [ ] Accessible: form labels, focus states, error announcements

## Dependencies
- UX-001, UX-002

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-004: Design dashboard",
 "type:ux,area:ux,priority:P1,status:ready",
 "Core Wallets",
"""## Objective
Design the main dashboard giving users a clear overview of portfolio, wallets, recent transactions, and security status.

## Inputs
- UX-Requirements.md (Section 7 — Dashboard)
- UX-001 IA, UX-002 Navigation

## Deliverables
- Dashboard wireframe with portfolio, wallet, transactions, and security widgets
- Quick actions (Send, Receive)
- Loading, empty, and error states

## Acceptance Criteria
- [ ] Dashboard answers the 4 key questions from UX-Requirements: how much, what, what happened, do I need to act
- [ ] Security status visible but not intrusive
- [ ] Empty state designed (new user with no wallets)
- [ ] Loading state designed

## Dependencies
- UX-001, UX-002

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-005: Design wallet flow",
 "type:ux,area:ux,priority:P1,status:ready",
 "Core Wallets",
"""## Objective
Design the wallet list view and flow for viewing wallet information.

## Inputs
- UX-Requirements.md (Section 8 — Wallets)
- EPIC 8 wallet feature scope

## Deliverables
- Wallet list screen
- Wallet summary card component
- Navigation to wallet details
- Empty state (no wallets) and loading state

## Acceptance Criteria
- [ ] Wallet list clearly shows asset, balance, and network per wallet
- [ ] Empty state guides user appropriately
- [ ] Design is mobile-responsive
- [ ] Loading state is designed

## Dependencies
- UX-001, UX-004

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-006: Design wallet details",
 "type:ux,area:ux,priority:P1,status:ready",
 "Core Wallets",
"""## Objective
Design the wallet detail screen showing balance, address, network, and recent transactions.

## Inputs
- UX-Requirements.md (Section 8 — Wallets)

## Deliverables
- Wallet detail screen design
- Address display with copy button
- Full address toggle (truncated / full view)
- Network indicator
- Recent transactions list for this wallet
- QR code for receive address

## Acceptance Criteria
- [ ] Wallet address displayed with copy functionality
- [ ] Network clearly labeled to prevent wrong-network sends
- [ ] Full address can be viewed (not just truncated)
- [ ] QR code for receiving is accessible
- [ ] Recent transactions are shown

## Dependencies
- UX-005

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-007: Design receive flow",
 "type:ux,area:ux,priority:P1,status:ready",
 "Transactions",
"""## Objective
Design the Receive flow where users display their wallet address for incoming transfers.

## Inputs
- UX-Requirements.md (Section 8)
- UX-006 wallet details

## Deliverables
- Receive screen with QR code and full address
- Copy address button
- Network warning (send only [ASSET] on [NETWORK])
- Address verification guidance
- Share address option

## Acceptance Criteria
- [ ] QR code is large and scannable
- [ ] Address copyable with single tap
- [ ] Network warning is prominent
- [ ] Design works on mobile

## Dependencies
- UX-006

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-008: Design send flow",
 "type:ux,area:ux,priority:P0,status:ready",
 "Transactions",
"""## Objective
Design the complete send flow — one of the most critical UX flows where mistakes can be irreversible.

## Inputs
- UX-Requirements.md (Section 9 — Send Crypto)
- Transaction lifecycle: REQUESTED -> VALIDATING -> AWAITING_AUTHORIZATION -> AUTHORIZED -> PROCESSING -> CONFIRMED

## Deliverables
- Send flow screens: select asset -> select wallet -> select/enter recipient -> enter amount -> review -> authenticate -> processing -> confirmed/failed
- Error states at each step
- Address input validation feedback
- Amount validation (insufficient funds, min/max)

## Acceptance Criteria
- [ ] All steps from UX-Requirements Section 9 are designed
- [ ] User can always go back to previous step
- [ ] Error states designed at each step
- [ ] Address input gives clear validation feedback
- [ ] Amount input shows available balance

## Dependencies
- UX-005, UX-006, UX-012

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-009: Design transaction review screen",
 "type:ux,area:ux,priority:P0,status:ready",
 "Transactions",
"""## Objective
Design the transaction review screen — the most critical safety screen. Users must verify all details before authorizing.

## Inputs
- UX-Requirements.md (Sections 9.1 Review Screen, 10 Transaction Security)

## Deliverables
- Transaction review screen showing: Asset, From wallet, To recipient + address (full), Amount, Network, Network fee, Total
- Confirm and Cancel actions
- MFA authorization step design
- Clear visual hierarchy emphasizing critical fields

## Acceptance Criteria
- [ ] All fields from UX-Requirements Section 9.1 are shown
- [ ] Recipient address shown in full (not truncated)
- [ ] Network fee and total are prominently displayed
- [ ] Cancel button is clearly accessible
- [ ] MFA authorization step is designed

## Dependencies
- UX-008

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-010: Design transaction history",
 "type:ux,area:ux,priority:P1,status:ready",
 "Transactions",
"""## Objective
Design the transaction history list with filtering, search, and status visualization.

## Inputs
- UX-Requirements.md (Section 12 — Transactions)

## Deliverables
- Transaction list design
- Transaction item: asset, amount (in/out), status, date, recipient/sender
- Filter controls (by asset, status, date range)
- Search, empty state, loading state
- Pagination or infinite scroll

## Acceptance Criteria
- [ ] Transaction list shows key information at a glance
- [ ] Status is visually distinct (pending, confirmed, failed)
- [ ] Filter controls are designed
- [ ] Empty state and loading state are designed

## Dependencies
- UX-004

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-011: Design transaction details",
 "type:ux,area:ux,priority:P1,status:ready",
 "Transactions",
"""## Objective
Design the transaction detail view showing all information about a specific transaction.

## Inputs
- UX-Requirements.md (Section 12 — Transactions)
- Transaction statuses: Pending, Confirmed, Failed, Cancelled

## Deliverables
- Transaction detail screen with all fields: asset, amount, from, to, date/time, network, fee, status, transaction ID
- Status timeline / progress indicator
- Copy transaction ID functionality
- Blockchain explorer link (for testnet)
- All 4 status states designed

## Acceptance Criteria
- [ ] All transaction fields are displayed
- [ ] Transaction status is prominent
- [ ] Status is explained in plain language
- [ ] All 4 status states (Pending, Confirmed, Failed, Cancelled) are designed

## Dependencies
- UX-010

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-012: Design recipients",
 "type:ux,area:ux,priority:P1,status:ready",
 "Transactions",
"""## Objective
Design the recipients management screens — list, add, and delete saved recipients.

## Inputs
- UX-Requirements.md (Section 13 — Recipients)
- EPIC 9 recipient features

## Deliverables
- Recipient list screen
- Add recipient form (name, asset, address, network)
- Address validation feedback
- Delete recipient confirmation dialog
- Empty state
- Recipient card component (name, asset, truncated + copyable address)

## Acceptance Criteria
- [ ] Recipient list clearly shows name, asset, and truncated + copyable address
- [ ] Add recipient form has address validation feedback
- [ ] Delete has a confirmation step
- [ ] New recipient verification flow is designed
- [ ] Empty state is designed

## Dependencies
- UX-001

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-013: Design Security Center",
 "type:ux,area:ux,area:security,priority:P1,status:ready",
 "Security Center",
"""## Objective
Design the Security Center — the central hub for MFA, sessions, devices, and security activity.

## Inputs
- UX-Requirements.md (Section 14 — Security Center)
- EPIC 11 Security Center features

## Deliverables
- Security overview screen (MFA status, active sessions, recent alerts)
- MFA setup and disable flow
- Active sessions list with revoke button
- Devices list
- Login history view
- Security activity feed
- Security alert notification designs

## Acceptance Criteria
- [ ] Security status shown clearly (MFA on/off, suspicious activity)
- [ ] Sessions list shows device, IP, and last activity
- [ ] Individual session revocation is designed
- [ ] Security activity feed is designed
- [ ] Alert states are distinct and actionable

## Dependencies
- UX-002, UX-014, UX-003

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-014: Design notifications",
 "type:ux,area:ux,priority:P1,status:ready",
 "Security Center",
"""## Objective
Design the notifications system UI including the notification list, unread indicator, and different notification types.

## Inputs
- UX-Requirements.md (Section 15 — Notifications)
- Notification types: Information, Success, Warning, Security Alert

## Deliverables
- Notification list screen
- Notification item design for each type (info, success, warning, security alert)
- Unread badge indicator in navigation
- Mark as read / mark all as read interaction
- Empty state

## Acceptance Criteria
- [ ] All 4 notification types are visually distinct
- [ ] Unread indicator is visible in navigation
- [ ] Mark all as read is possible
- [ ] Security alerts are visually prominent
- [ ] Empty state is designed

## Dependencies
- UX-002

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-015: Define responsive behavior",
 "type:ux,area:ux,priority:P1,status:ready",
 "Foundation",
"""## Objective
Define breakpoints and responsive layout behavior for all key screens across desktop, tablet, and mobile.

## Inputs
- UX-Requirements.md (Section 17 — Responsive Design)
- All UX screen designs (UX-003 through UX-014)

## Deliverables
- Breakpoint definitions (mobile, tablet, desktop) with pixel values
- Layout behavior at each breakpoint for primary screens
- Mobile navigation pattern
- Table/list behavior on small screens
- Touch target size guidelines (min 44x44px)

## Acceptance Criteria
- [ ] Breakpoints defined with pixel values
- [ ] Dashboard, wallet, transaction, and security screens have mobile layouts
- [ ] Navigation has a defined mobile pattern
- [ ] Touch targets meet minimum size

## Dependencies
- UX-004 through UX-013

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-016: Define accessibility requirements",
 "type:ux,area:ux,priority:P1,status:ready",
 "Foundation",
"""## Objective
Define accessibility requirements and guidelines for SecureVault (WCAG 2.1 AA minimum).

## Inputs
- UX-Requirements.md (Section 18 — Accessibility)
- WCAG 2.1 AA standard

## Deliverables
- Accessibility requirements document
- Contrast ratio requirements (WCAG AA minimum)
- Keyboard navigation requirements
- Screen reader requirements (ARIA labels)
- Focus state design guidelines
- Form and error message accessibility guidelines

## Acceptance Criteria
- [ ] WCAG 2.1 AA adopted as minimum standard
- [ ] Color contrast ratios are specified
- [ ] Keyboard navigation requirements are documented
- [ ] Color is not the only means of conveying information
- [ ] Document referenced in design system (UX-017)

## Dependencies
None

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-017: Create design system",
 "type:ux,area:ux,priority:P1,status:ready",
 "Foundation",
"""## Objective
Create a consistent design system for SecureVault covering typography, colors, spacing, and UI primitives.

## Inputs
- UX-Requirements.md (Section 19 — Design System)
- UX-016 Accessibility requirements
- Brand attributes: professional, secure, modern, simple

## Deliverables
- Color palette (primary, secondary, semantic: success, warning, error, info)
- Typography scale (headings, body, labels, captions)
- Spacing scale (8px grid)
- Border radius and shadow tokens
- Core component styles: buttons, inputs, cards, badges, status indicators
- Design tokens (exportable to CSS variables)

## Acceptance Criteria
- [ ] Color palette meets WCAG AA contrast requirements
- [ ] Typography scale defined for all text roles
- [ ] Spacing scale follows 8px grid
- [ ] Design system documented in Figma or equivalent
- [ ] Design tokens are defined

## Dependencies
- UX-016

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-018: Create reusable UI components",
 "type:ux,area:ux,priority:P1,status:ready",
 "Foundation",
"""## Objective
Design reusable UI components — the building blocks of the SecureVault interface for Angular implementation.

## Inputs
- UX-017 Design system
- UX-Requirements.md Section 19
- All screen designs (UX-003 through UX-014)

## Deliverables
Component library including: Navigation, Button variants, Input/Form fields, Card, Modal, Toast/Notification, Status badge, Loading spinner, Empty state, Error state, Address display, Amount display, Transaction row, Wallet card.

## Acceptance Criteria
- [ ] All components documented with all states and variants
- [ ] Components use design tokens from UX-017
- [ ] Each component shows all variants (size, color, state)
- [ ] Components named consistently for handoff to Angular implementation

## Dependencies
- UX-017

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-019: Design loading/empty/error/success/pending states",
 "type:ux,area:ux,priority:P1,status:ready",
 "Foundation",
"""## Objective
Design all system states for every major feature area to ensure a complete experience beyond the happy path.

## Inputs
- UX-Requirements.md (Section 16 — States & Edge Cases)
- UX-018 components

## Deliverables
For each major feature area (dashboard, wallets, transactions, recipients, security center, notifications):
- Loading state, empty state, error state, success state, pending state, warning state, security alert state

## Acceptance Criteria
- [ ] All 7 state types from UX-Requirements Section 16 are designed
- [ ] States defined for all major feature areas
- [ ] Loading states use consistent spinner/skeleton pattern
- [ ] Empty states include guidance on next steps
- [ ] Error messages are in plain language

## Dependencies
- UX-017, UX-018

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

("UX-020: Document important UX decisions",
 "type:ux,area:ux,area:documentation,priority:P2,status:ready",
 "Open Source Release",
"""## Objective
Document the rationale behind key UX decisions so future contributors understand the reasoning.

## Inputs
- All UX work (UX-001 through UX-019)
- UX-Requirements.md

## Deliverables
`docs/ux/decisions.md` with key decisions in format: Decision -> Context -> Options considered -> Rationale -> Trade-offs

## Example
Transaction Review shows full recipient address: Truncating was considered but rejected due to address substitution attack risk. Full address display is the safer choice for a security-first product.

## Acceptance Criteria
- [ ] At least 10 key design decisions documented
- [ ] Each decision explains what, why, and trade-offs
- [ ] Covers: navigation pattern, send flow safety, address display, security UX choices
- [ ] Document accessible to future contributors

## Dependencies
- UX-001 through UX-019

## Suggested Assignee
UX contributor

## Related Epic
EPIC 6 — UX/UI Design
"""),

]

# ── EPIC 7 — Dashboard ────────────────────────────────────────────────────────

ISSUES += [

("DASH-001: Implement dashboard API endpoint",
 "type:feature,area:backend,priority:P1,status:ready",
 "Core Wallets",
"""## Description
Implement a dashboard summary endpoint aggregating portfolio overview, wallet summaries, recent transactions, and security status.

## Scope
- `GET /api/v1/dashboard/summary`
- Response: `{ portfolioSummary, walletSummaries[], recentTransactions[], securityStatus }`
- Portfolio summary: total value (mocked), assets summary
- Recent transactions: last 5-10 transactions
- Security status: MFA enabled, active sessions count, last login

## Acceptance Criteria
- [ ] Endpoint requires authentication
- [ ] Returns data only for authenticated user
- [ ] Response matches OpenAPI specification
- [ ] Returns appropriate response when user has no wallets
- [ ] Responds within 500ms under normal load

## Testing Requirements
- Unit tests: service aggregation logic
- Integration tests: endpoint with authenticated user

## Dependencies
- AUTH-003, WALLET-002, TXN-004

## Suggested Assignee
Ahmed

## Related Epic
EPIC 7 — Dashboard
"""),

("DASH-002: Implement Angular dashboard component",
 "type:feature,area:frontend,priority:P1,status:ready",
 "Core Wallets",
"""## Description
Implement the Angular dashboard component displaying portfolio summary, wallet list, recent transactions, and security status.

## Scope
- Dashboard component consuming `GET /api/v1/dashboard/summary`
- Portfolio summary widget
- Wallet cards list
- Recent transactions list
- Security status widget
- Quick action buttons (Send, Receive)
- Loading, empty, and error states (per UX-004 and UX-019)

## Acceptance Criteria
- [ ] Dashboard loads and displays real API data
- [ ] All loading states are implemented
- [ ] Empty state shown for new users
- [ ] Error state handles API failures gracefully
- [ ] Quick actions navigate to correct routes

## Testing Requirements
Unit tests: component with mocked service.

## Dependencies
- FE-003, DASH-001, UX-004, UX-019

## Suggested Assignee
Ahmed

## Related Epic
EPIC 7 — Dashboard
"""),

]

# ── EPIC 8 — Wallet Management ────────────────────────────────────────────────

ISSUES += [

("WALLET-001: Implement wallet domain model and persistence",
 "type:feature,area:backend,area:database,priority:P1,status:ready",
 "Core Wallets",
"""## Description
Implement the Wallet domain entity, repository, and Flyway migration.

## Scope
- `Wallet` entity: id (UUID), userId (FK), name, assetType (BTC/ETH/USDC), network (MAINNET/TESTNET), address, balance (BigDecimal), createdAt, updatedAt
- Flyway migration: `V3__create_wallets_table.sql`
- `WalletRepository` (Spring Data JPA)
- Dev profile seed data: mocked testnet wallets

## Acceptance Criteria
- [ ] `wallets` table created by Flyway migration
- [ ] Wallet associated with a user (FK constraint)
- [ ] Balance stored with sufficient precision (DECIMAL(38,18))
- [ ] Wallet addresses are immutable after creation
- [ ] Dev profile seeds example wallets

## Testing Requirements
Integration tests: WalletRepository with Testcontainers.

## Dependencies
- AUTH-001, BE-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 8 — Wallet Management
"""),

("WALLET-002: Implement wallet service and REST API",
 "type:feature,area:backend,priority:P1,status:ready",
 "Core Wallets",
"""## Description
Implement wallet service with business logic and REST API endpoints.

## Scope
- `WalletService`: getWalletsForUser, getWalletById, validateWalletOwnership
- `GET /api/v1/wallets` — list user's wallets
- `GET /api/v1/wallets/{walletId}` — wallet details
- Authorization: users can only access their own wallets
- Response DTOs with OpenAPI annotations

## Acceptance Criteria
- [ ] List returns only wallets belonging to authenticated user
- [ ] Detail returns 404 if wallet doesn't belong to user
- [ ] Wallet address included in response
- [ ] OpenAPI documentation complete

## Testing Requirements
- Unit tests: WalletService authorization logic
- Integration tests: wallet endpoints with authenticated user

## Dependencies
- WALLET-001, AUTH-003, BE-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 8 — Wallet Management
"""),

("WALLET-003: Implement Angular wallet list and details UI",
 "type:feature,area:frontend,priority:P1,status:ready",
 "Core Wallets",
"""## Description
Implement Angular wallet list and wallet detail views with address display and copy functionality.

## Scope
- Wallet list component with wallet cards
- Wallet detail component
- Address display with copy-to-clipboard and confirmation feedback
- Full address toggle (truncated / full view)
- Network label display
- QR code component for wallet address
- Loading, empty, error states (per UX-005, UX-006, UX-019)

## Acceptance Criteria
- [ ] Wallet list displays all user wallets
- [ ] Copy button copies full address to clipboard with feedback
- [ ] Full address can be revealed from truncated view
- [ ] Network is clearly labeled
- [ ] QR code generated for each wallet address
- [ ] Loading and empty states implemented

## Testing Requirements
Unit tests: address copy functionality.

## Dependencies
- FE-003, WALLET-002, UX-005, UX-006

## Suggested Assignee
Ahmed

## Related Epic
EPIC 8 — Wallet Management
"""),

]

# ── EPIC 9 — Recipients ───────────────────────────────────────────────────────

ISSUES += [

("RECIP-001: Implement recipient domain, persistence, and API",
 "type:feature,area:backend,area:database,priority:P1,status:ready",
 "Transactions",
"""## Description
Implement the Recipient domain with CRUD API endpoints and address validation.

## Scope
- `Recipient` entity: id (UUID), userId (FK), name, assetType, network, address, createdAt, updatedAt
- Flyway migration: `V4__create_recipients_table.sql`
- `GET /api/v1/recipients`, `POST /api/v1/recipients`, `PUT /api/v1/recipients/{id}`, `DELETE /api/v1/recipients/{id}`
- Address format validation per asset type
- Authorization: users can only manage their own recipients

## Acceptance Criteria
- [ ] CRUD endpoints work for authenticated user
- [ ] Users can only access/modify their own recipients
- [ ] Address format validated on create and update
- [ ] Deleting a recipient doesn't affect transaction history
- [ ] Malformed addresses are rejected

## Testing Requirements
- Unit tests: address validation
- Integration tests: CRUD endpoints

## Dependencies
- AUTH-003, BE-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 9 — Recipients
"""),

("RECIP-002: Implement Angular recipients UI",
 "type:feature,area:frontend,priority:P1,status:ready",
 "Transactions",
"""## Description
Implement the Angular recipients management UI with list, add, and delete functionality.

## Scope
- Recipients list component
- Add recipient form with client-side validation
- Delete recipient with confirmation dialog
- Recipient card (name, asset, truncated address, copy button)
- Loading, empty, error states (per UX-012, UX-019)

## Acceptance Criteria
- [ ] Recipients list displays all saved recipients
- [ ] Add form validates address format client-side
- [ ] Delete requires confirmation
- [ ] Address is copyable from list
- [ ] Empty state guides user to add first recipient

## Testing Requirements
Unit tests: form validation.

## Dependencies
- FE-003, RECIP-001, UX-012

## Suggested Assignee
Ahmed

## Related Epic
EPIC 9 — Recipients
"""),

]

# ── EPIC 10 — Transaction Management ──────────────────────────────────────────

ISSUES += [

("TXN-001: Implement transaction domain model and lifecycle",
 "type:feature,area:backend,area:database,priority:P1,status:ready",
 "Transactions",
"""## Description
Implement the core Transaction domain with complete state machine lifecycle.

## Transaction Lifecycle
REQUESTED -> VALIDATING -> AWAITING_AUTHORIZATION -> AUTHORIZED -> PROCESSING -> CONFIRMED (with FAILED and CANCELLED states)

## Scope
- `Transaction` entity: id (UUID), userId (FK), walletId (FK), recipientId (FK nullable), toAddress, assetType, network, amount, fee, status, timestamps
- `TransactionStatus` enum with all states
- Flyway migration: `V5__create_transactions_table.sql`
- `TransactionRepository`
- State machine with enforced transitions
- `transaction_status_history` table for audit trail

## Acceptance Criteria
- [ ] Transaction table created by Flyway migration
- [ ] Status transitions are enforced (invalid transitions throw exception)
- [ ] Amount and fee stored with sufficient precision
- [ ] Status history table records every transition

## Testing Requirements
- Unit tests: state machine transitions
- Integration tests: TransactionRepository

## Dependencies
- WALLET-001, RECIP-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 10 — Transaction Management
"""),

("TXN-002: Implement create transaction and review endpoints",
 "type:feature,area:backend,area:security,priority:P1,status:ready",
 "Transactions",
"""## Description
Implement API endpoints for creating a transaction request and retrieving a review summary.

## Scope
- `POST /api/v1/transactions` — create (REQUESTED -> VALIDATING)
- `GET /api/v1/transactions/{id}/review` — review summary with all fields
- Validation: wallet ownership, sufficient balance (mocked), address format, amount > 0
- Mock fee calculation
- Authorization: transaction owner only

## Acceptance Criteria
- [ ] Transaction creation validates all input
- [ ] Review endpoint returns all required fields (from/to/amount/fee/total/network/asset)
- [ ] Transaction belongs to authenticated user
- [ ] Invalid wallet returns 403
- [ ] Mock fee calculated consistently

## Testing Requirements
- Unit tests: validation, fee calculation
- Integration tests: create and review endpoints

## Dependencies
- TXN-001, AUTH-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 10 — Transaction Management
"""),

("TXN-003: Implement transaction authorization with MFA",
 "type:feature,area:backend,area:security,priority:P0,status:ready",
 "Transactions",
"""## Description
Implement the transaction authorization step requiring MFA verification before a transaction is processed.

## Scope
- `POST /api/v1/transactions/{id}/authorize` — requires MFA code
- Verify MFA code is valid for the user
- Transition: AWAITING_AUTHORIZATION -> AUTHORIZED
- Mock processing: AUTHORIZED -> PROCESSING -> CONFIRMED (with configurable delay)
- Audit event: TRANSACTION_AUTHORIZED
- Notification trigger: transaction authorized and transaction confirmed

## Acceptance Criteria
- [ ] Authorization requires a valid MFA code
- [ ] Invalid MFA code returns 401
- [ ] Transaction transitions through all states correctly
- [ ] Audit event is recorded
- [ ] Notifications triggered for authorized and confirmed states

## Testing Requirements
- Unit tests: authorization logic
- Integration tests: full authorize -> process -> confirm flow

## Dependencies
- TXN-002, AUTH-005, SEC-005

## Suggested Assignee
Ahmed

## Related Epic
EPIC 10 — Transaction Management
"""),

("TXN-004: Implement transaction history and details endpoints",
 "type:feature,area:backend,priority:P1,status:ready",
 "Transactions",
"""## Description
Implement API endpoints for transaction history with filtering and individual transaction details.

## Scope
- `GET /api/v1/transactions` — paginated history with filters (status, asset, date range)
- `GET /api/v1/transactions/{id}` — transaction details
- Page-based pagination
- Authorization: user's own transactions only

## Acceptance Criteria
- [ ] History endpoint returns paginated results
- [ ] Filters work for status, asset type, and date range
- [ ] Details endpoint returns all transaction fields
- [ ] Users can only see their own transactions
- [ ] OpenAPI documentation complete

## Testing Requirements
Integration tests: history and detail endpoints with various filter combinations.

## Dependencies
- TXN-001, AUTH-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 10 — Transaction Management
"""),

("TXN-005: Implement Angular send flow and transaction UI",
 "type:feature,area:frontend,priority:P1,status:ready",
 "Transactions",
"""## Description
Implement the complete Angular transaction UI: multi-step send flow, review, MFA authorization, history, and details.

## Scope
- Multi-step send wizard: select wallet -> select/enter recipient -> enter amount -> review -> MFA -> processing -> result
- Transaction review component with all fields (per UX-009)
- Transaction history list with filters (per UX-010)
- Transaction detail view (per UX-011)
- All states: loading, empty, error, pending, confirmed, failed (per UX-019)

## Acceptance Criteria
- [ ] Multi-step send form wizard works correctly
- [ ] Review screen shows all required fields
- [ ] MFA input required before transaction is submitted
- [ ] Transaction status updates reflected in UI
- [ ] History list supports filtering
- [ ] All error states handled

## Testing Requirements
Unit tests: send flow component state management.

## Dependencies
- FE-003, TXN-002, TXN-003, TXN-004, UX-008, UX-009, UX-010, UX-011

## Suggested Assignee
Ahmed

## Related Epic
EPIC 10 — Transaction Management
"""),

]

# ── EPIC 11 — Security Center ─────────────────────────────────────────────────

ISSUES += [

("SECCTR-001: Implement Security Center API",
 "type:feature,area:backend,area:security,priority:P1,status:ready",
 "Security Center",
"""## Description
Implement Security Center API endpoints for MFA status, active sessions, devices, and security activity.

## Scope
- `GET /api/v1/security/overview` — MFA status, session count, recent alerts
- `GET /api/v1/security/sessions` — active sessions list
- `DELETE /api/v1/security/sessions/{id}` — revoke session
- `GET /api/v1/security/devices` — known devices list
- `GET /api/v1/security/activity` — security audit log (paginated)

## Acceptance Criteria
- [ ] All endpoints require authentication
- [ ] Users can only access their own security data
- [ ] Session revocation is immediate
- [ ] Activity log is paginated
- [ ] Device list shows device name, IP, last seen

## Testing Requirements
Integration tests: all security center endpoints.

## Dependencies
- AUTH-004, AUTH-005, SEC-005

## Suggested Assignee
Ahmed

## Related Epic
EPIC 11 — Security Center
"""),

("SECCTR-002: Implement Angular Security Center UI",
 "type:feature,area:frontend,priority:P1,status:ready",
 "Security Center",
"""## Description
Implement the Angular Security Center UI with MFA management, session management, and security activity views.

## Scope
- Security overview component
- MFA status with enable/disable flow
- Active sessions list with per-session revoke button
- Devices list
- Security activity feed (chronological)
- All states per UX-013 and UX-019

## Acceptance Criteria
- [ ] MFA status displayed with enable/disable option
- [ ] Sessions list shows device, IP, and last activity
- [ ] Session revocation works and removes session from list immediately
- [ ] Security activity feed displays events chronologically
- [ ] All loading and error states handled

## Testing Requirements
Unit tests: session revocation interaction.

## Dependencies
- FE-003, SECCTR-001, UX-013

## Suggested Assignee
Ahmed

## Related Epic
EPIC 11 — Security Center
"""),

]

# ── EPIC 12 — Notifications ───────────────────────────────────────────────────

ISSUES += [

("NOTIF-001: Implement notification domain and service",
 "type:feature,area:backend,priority:P1,status:ready",
 "Security Center",
"""## Description
Implement the notification domain with persistence and service triggered by security and transaction events.

## Scope
- `Notification` entity: id, userId, type, title, body, read, createdAt
- `NotificationType` enum: NEW_LOGIN, NEW_DEVICE, MFA_CHANGED, NEW_RECIPIENT, TRANSACTION_AUTHORIZED, TRANSACTION_CONFIRMED, SUSPICIOUS_ACTIVITY
- Flyway migration: `V6__create_notifications_table.sql`
- `NotificationService`: createNotification, markAsRead, markAllAsRead
- Integration with auth events (login, new device) and transaction events (authorized, confirmed)

## Acceptance Criteria
- [ ] Notifications table created by migration
- [ ] Notifications created for: login, new device, MFA change, transaction authorize, transaction confirm
- [ ] Notifications are per-user
- [ ] Read/unread state is tracked

## Testing Requirements
- Unit tests: NotificationService
- Integration tests: notification creation on events

## Dependencies
- AUTH-003, AUTH-005, TXN-003

## Suggested Assignee
Ahmed

## Related Epic
EPIC 12 — Notifications
"""),

("NOTIF-002: Implement notifications API and Angular UI",
 "type:feature,area:backend,area:frontend,priority:P1,status:ready",
 "Security Center",
"""## Description
Implement notification REST API and Angular notification UI with unread indicator and list.

## Scope
- `GET /api/v1/notifications` — paginated list (filter by read/unread)
- `PUT /api/v1/notifications/{id}/read` — mark single as read
- `PUT /api/v1/notifications/read-all` — mark all as read
- `GET /api/v1/notifications/unread-count` — for badge
- Angular: notifications list page, unread badge in navigation, notification item components (per UX-014)

## Acceptance Criteria
- [ ] API returns user's notifications paginated
- [ ] Unread count endpoint is fast
- [ ] Angular notification list displays all notification types
- [ ] Unread badge updates after reading
- [ ] Security alert notifications are visually distinct

## Testing Requirements
Integration tests: notification API endpoints.

## Dependencies
- NOTIF-001, FE-003, UX-014

## Suggested Assignee
Ahmed

## Related Epic
EPIC 12 — Notifications
"""),

]

# ── EPIC 13 — Testing & Quality ───────────────────────────────────────────────

ISSUES += [

("TEST-001: Set up Testcontainers integration test infrastructure",
 "type:task,area:backend,priority:P0,status:ready",
 "Foundation",
"""## Description
Configure Testcontainers as the integration testing infrastructure for database tests.

## Scope
- Add Testcontainers dependency (PostgreSQL module)
- Create base integration test class with shared PostgreSQL container (container reuse for performance)
- Configure Spring Boot test slices to use Testcontainers
- Configure test profiles
- Document testing patterns

## Acceptance Criteria
- [ ] Integration tests use real PostgreSQL container (not H2)
- [ ] Testcontainers starts automatically for integration tests
- [ ] Tests are isolated (@Transactional or clean state)
- [ ] Container reuse enabled for acceptable test startup time

## Testing Requirements
Verify: existing integration tests pass with Testcontainers.

## Dependencies
- BE-001, BE-002

## Suggested Assignee
Ahmed

## Related Epic
EPIC 13 — Testing & Quality
"""),

("TEST-002: Implement security test suite",
 "type:security,area:security,area:backend,priority:P1,status:ready",
 "Security Center",
"""## Description
Implement automated security tests covering authentication security, authorization enforcement, and input validation.

## Scope
- Authentication security: brute force protection, credential enumeration prevention, token replay
- Authorization / IDOR tests: user cannot access other user's wallets, transactions, sessions, recipients
- Input validation: injection attempts, oversized inputs
- MFA security: code replay rejection, expired code rejection
- Session security: revoked session rejection

## Acceptance Criteria
- [ ] Tests cover all items in SEC-004 security testing strategy
- [ ] IDOR tests verify isolation for wallets, transactions, sessions, recipients
- [ ] Token replay tests verify revoked tokens are rejected
- [ ] Tests are part of CI pipeline

## Testing Requirements
All tests must pass in CI.

## Dependencies
- SEC-004, AUTH-003, AUTH-005, WALLET-002, TXN-002

## Suggested Assignee
Security contributor

## Related Epic
EPIC 13 — Testing & Quality
"""),

("TEST-003: Configure static analysis and dependency scanning",
 "type:task,area:devops,priority:P1,status:ready",
 "MVP",
"""## Description
Configure static analysis tools and dependency vulnerability scanning for the backend.

## Scope
- SpotBugs with find-sec-bugs plugin (security-focused static analysis)
- Checkstyle for code style enforcement
- OWASP Dependency-Check for CVE scanning
- Configure in Maven/Gradle build
- Fail on HIGH/CRITICAL CVEs (configurable threshold)

## Acceptance Criteria
- [ ] SpotBugs runs on every build
- [ ] OWASP Dependency-Check runs and reports CVEs
- [ ] Build fails on HIGH/CRITICAL CVEs
- [ ] Checkstyle configuration matches project code style

## Testing Requirements
Verify tools run in CI.

## Dependencies
- BE-001, CI-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 13 — Testing & Quality
"""),

]

# ── EPIC 15 — CI/CD ───────────────────────────────────────────────────────────

ISSUES += [

("CI-001: Implement GitHub Actions backend CI pipeline",
 "type:task,area:devops,priority:P0,status:ready",
 "Foundation",
"""## Description
Implement the GitHub Actions CI pipeline for the backend, running on every PR and push to main.

## Scope
- `.github/workflows/backend-ci.yml`
- Steps: checkout -> set up Java -> build -> unit tests -> integration tests (Testcontainers) -> static analysis
- Cache Maven/Gradle dependencies
- Test result reporting as GitHub Actions artifacts
- Triggers: push to main, pull_request

## Acceptance Criteria
- [ ] CI runs on every PR and push to main
- [ ] Build, unit tests, and integration tests all run
- [ ] Test results published as artifacts
- [ ] Build cache reduces CI time
- [ ] CI fails if any test fails

## Testing Requirements
Verify CI runs on a test PR.

## Dependencies
- BE-001, TEST-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 15 — CI/CD & DevSecOps
"""),

("CI-002: Add security scanning to CI pipeline",
 "type:security,area:devops,area:security,priority:P1,status:ready",
 "MVP",
"""## Description
Add dependency vulnerability scanning and secret scanning to the CI pipeline.

## Scope
- OWASP Dependency-Check in CI
- Verify GitHub secret scanning is enabled in repository settings
- Trivy or similar for Docker image scanning
- Results published as PR comments or GitHub Security Advisories
- Fail on HIGH/CRITICAL findings (configurable)

## Acceptance Criteria
- [ ] Dependency scanning runs in CI
- [ ] Secret scanning enabled in repository settings
- [ ] Docker image scanning runs on image builds
- [ ] HIGH/CRITICAL findings fail the build
- [ ] Scan results visible in PR checks

## Dependencies
- CI-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 15 — CI/CD & DevSecOps
"""),

("CI-003: Implement frontend CI pipeline",
 "type:task,area:devops,area:frontend,priority:P1,status:ready",
 "Foundation",
"""## Description
Implement the GitHub Actions CI pipeline for the Angular frontend.

## Scope
- `.github/workflows/frontend-ci.yml`
- Steps: checkout -> Node setup -> npm install -> lint -> build -> test
- Cache node_modules
- npm audit for dependency vulnerabilities
- Triggers: push to main, pull_request

## Acceptance Criteria
- [ ] Frontend CI runs on every PR
- [ ] Lint, build, and tests all run
- [ ] `npm audit` runs and reports vulnerabilities
- [ ] Build failure fails CI

## Dependencies
- FE-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 15 — CI/CD & DevSecOps
"""),

]

# ── EPIC 16 — Documentation ───────────────────────────────────────────────────

ISSUES += [

("DOCS-001: Write architecture documentation",
 "type:documentation,area:documentation,priority:P1,status:ready",
 "Open Source Release",
"""## Description
Write comprehensive architecture documentation covering system design, module boundaries, and key decisions.

## Scope
- `docs/architecture/README.md` — architecture overview
- C4 diagrams: System Context, Container, Component
- Module boundary documentation
- Transaction lifecycle state diagram
- Security architecture overview
- ADR index with at least ADR-001 (modular monolith)

## Acceptance Criteria
- [ ] Architecture overview is clear to a new contributor
- [ ] All domain modules are described
- [ ] Transaction lifecycle documented with state diagram
- [ ] ADR-001 (modular monolith decision) exists

## Testing Requirements
Review for clarity.

## Dependencies
- ARCH-001, MVP release features

## Suggested Assignee
Ahmed

## Related Epic
EPIC 16 — Open Source & Documentation
"""),

("DOCS-002: Write API documentation and developer guide",
 "type:documentation,area:documentation,priority:P1,status:ready",
 "Open Source Release",
"""## Description
Ensure the API is fully documented and create a human-readable API guide for contributors.

## Scope
- Verify all endpoints have complete OpenAPI annotations
- `docs/api/README.md` — API overview and authentication guide
- Example requests/responses for key endpoints (auth, wallets, transactions)
- Error response documentation
- API versioning strategy

## Acceptance Criteria
- [ ] All API endpoints documented in OpenAPI
- [ ] Authentication flow documented
- [ ] API guide accessible to new contributors
- [ ] Error codes documented

## Dependencies
All backend endpoint implementations.

## Suggested Assignee
Ahmed

## Related Epic
EPIC 16 — Open Source & Documentation
"""),

]

# ── EPIC 17 — MVP Release ─────────────────────────────────────────────────────

ISSUES += [

("MVP-001: End-to-end testing for MVP",
 "type:task,area:backend,area:frontend,priority:P0,status:ready",
 "MVP",
"""## Description
Perform end-to-end testing of all MVP user flows to verify the complete system works as expected.

## Scope
Complete E2E coverage of: registration -> login -> MFA -> dashboard -> wallet view -> send transaction -> review -> MFA authorize -> confirm -> security center -> notifications -> logout.

Test with mock/testnet data. Document all defects found. Verify all states (loading, empty, error, success).

## Acceptance Criteria
- [ ] All primary MVP user flows complete without errors
- [ ] All defects are documented and prioritized
- [ ] E2E test checklist is signed off

## Testing Requirements
Manual E2E testing checklist. Optionally: Cypress or Playwright automated E2E tests.

## Dependencies
All MVP feature tickets must be complete.

## Suggested Assignee
Ahmed

## Related Epic
EPIC 17 — MVP Release
"""),

("MVP-002: Security review for MVP",
 "type:security,area:security,priority:P0,status:ready",
 "MVP",
"""## Description
Conduct a security review of the complete MVP implementation against threat models and security testing strategy.

## Scope
- Review against SEC-001, SEC-002, SEC-003 threat models
- Execute SEC-004 security test cases
- API security testing (authentication bypass, IDOR, injection)
- Review JWT configuration, password storage, session management
- Document all findings with severity ratings
- Remediation plan for any findings

## Acceptance Criteria
- [ ] All P0 security tests from SEC-004 have been executed
- [ ] No HIGH/CRITICAL unmitigated findings at release
- [ ] All findings documented with severity
- [ ] Remediation plan exists for any remaining findings

## Testing Requirements
Security testing per SEC-004.

## Dependencies
- SEC-001, SEC-002, SEC-003, SEC-004, all MVP features

## Suggested Assignee
Security contributor

## Related Epic
EPIC 17 — MVP Release
"""),

("MVP-003: UX and accessibility review for MVP",
 "type:ux,area:ux,priority:P1,status:ready",
 "MVP",
"""## Description
Conduct a UX review and accessibility audit to verify implementation matches design intent and meets WCAG 2.1 AA.

## Scope
- Compare implementation against all UX designs (UX-003 through UX-019)
- Accessibility audit against UX-016 requirements
- Check all state designs are implemented (loading, empty, error, success)
- Keyboard navigation testing for all primary flows
- Document deviations from design

## Acceptance Criteria
- [ ] All primary screens match design intent
- [ ] WCAG 2.1 AA contrast requirements are met
- [ ] Keyboard navigation works for primary flows
- [ ] All loading/empty/error states are implemented
- [ ] Deviations from design documented and prioritized

## Dependencies
- UX-016, all frontend feature tickets

## Suggested Assignee
UX contributor

## Related Epic
EPIC 17 — MVP Release
"""),

("MVP-004: Release checklist, documentation review, and GitHub Release v0.1.0",
 "type:task,area:documentation,priority:P0,status:ready",
 "MVP",
"""## Description
Complete the MVP release checklist, review all documentation, perform dependency review, and create the v0.1.0 GitHub Release.

## Scope
- Release checklist verification: all features working, tests passing, CI green, security reviewed, UX reviewed, docs complete
- Review README, CONTRIBUTING.md, SECURITY.md accuracy
- Dependency review: licenses (no copyleft conflicts), known CVEs
- Write v0.1.0 release notes (changelog format)
- Create GitHub Release v0.1.0 tagged as `v0.1.0`

## Acceptance Criteria
- [ ] Release checklist complete and signed off
- [ ] README accurately describes the MVP
- [ ] All documentation is accurate and up to date
- [ ] No HIGH/CRITICAL CVEs in dependencies
- [ ] GitHub Release `v0.1.0` created with release notes
- [ ] CI is green on the release tag

## Dependencies
All MVP tickets.

## Suggested Assignee
Ahmed

## Related Epic
EPIC 17 — MVP Release
"""),

]

# ── EPIC 14 — Blockchain ──────────────────────────────────────────────────────

ISSUES += [

("CHAIN-001: Define blockchain abstraction interface",
 "type:task,area:backend,area:blockchain,priority:P2,status:ready",
 "Testnet Integration",
"""## Description
Define the blockchain abstraction interface that decouples the application from any specific blockchain provider.

## Scope
- `BlockchainProvider` interface: getBalance, validateAddress, createTransaction, broadcastTransaction, getTransactionStatus
- `MockBlockchainProvider` (already used in MVP) implementing the interface
- Interface documentation and extension guide
- Design to support multiple providers (Bitcoin, Ethereum)

## Acceptance Criteria
- [ ] Interface defined and documented
- [ ] MockBlockchainProvider implements the interface
- [ ] Application compiles and tests pass with mock provider
- [ ] Interface supports multiple asset types

## Testing Requirements
Existing tests must pass with the abstraction in place.

## Dependencies
- TXN-001 (MVP complete first)

## Suggested Assignee
Ahmed

## Related Epic
EPIC 14 — Blockchain/Testnet Integration
"""),

("CHAIN-002: Implement Ethereum testnet (Sepolia) integration",
 "type:feature,area:backend,area:blockchain,priority:P2,status:ready",
 "Testnet Integration",
"""## Description
Implement a BlockchainProvider for Ethereum Sepolia testnet.

## Scope
- `EthereumTestnetProvider` implementing `BlockchainProvider`
- Balance retrieval via Infura or Alchemy API (key from environment variables)
- Address validation (EIP-55 checksum)
- Transaction creation and broadcasting to Sepolia
- Confirmation monitoring via polling
- No real ETH used — testnet only

## Acceptance Criteria
- [ ] EthereumTestnetProvider implements all interface methods
- [ ] Balance can be retrieved for a Sepolia address
- [ ] Transactions can be broadcast to Sepolia
- [ ] Confirmation status monitored and updates transaction status
- [ ] API key stored securely (environment variable, never committed)

## Testing Requirements
Integration tests against Sepolia testnet (configurable via environment variable).

## Dependencies
- CHAIN-001

## Suggested Assignee
Ahmed

## Related Epic
EPIC 14 — Blockchain/Testnet Integration
"""),

]

# ── EPIC 18 — Future ──────────────────────────────────────────────────────────

ISSUES += [

("FUTURE-001: Evaluate Redis for caching and session storage",
 "type:task,area:backend,priority:P3,status:ready",
 "Open Source Release",
"""## Description
Evaluate and plan Redis for session storage and caching in a post-MVP context.

## Scope
- Identify caching opportunities (dashboard summary, wallet balances)
- Evaluate Redis for session storage vs. current database sessions
- Write ADR documenting the decision and trade-offs

## Acceptance Criteria
- [ ] ADR written for Redis introduction decision
- [ ] Use cases are clearly defined
- [ ] Implementation is NOT started until after MVP is complete

## Dependencies
- MVP release (EPIC 17 complete)

## Suggested Assignee
Ahmed

## Related Epic
EPIC 18 — Future Production Engineering
"""),

("FUTURE-002: Evaluate event-driven architecture with Kafka",
 "type:task,area:backend,priority:P3,status:ready",
 "Open Source Release",
"""## Description
Evaluate Kafka for event-driven architecture in a post-MVP context.

## Scope
- Identify event-driven use cases (blockchain confirmations, notification fanout, audit streaming)
- Evaluate Kafka vs. simpler alternatives (Spring Application Events, scheduled polling)
- Write ADR

## Acceptance Criteria
- [ ] ADR written
- [ ] Use cases defined with justification
- [ ] Implementation NOT started until after MVP

## Dependencies
- MVP release

## Suggested Assignee
Ahmed

## Related Epic
EPIC 18 — Future Production Engineering
"""),

("FUTURE-003: Observability — metrics, tracing, and dashboards",
 "type:task,area:devops,priority:P3,status:ready",
 "Open Source Release",
"""## Description
Plan and implement observability for SecureVault including metrics, distributed tracing, and log aggregation.

## Scope
- Micrometer metrics exported to Prometheus
- Distributed tracing with OpenTelemetry
- Log aggregation setup
- Grafana dashboard for key metrics
- Alerting rules for security events

## Acceptance Criteria
- [ ] Metrics exported to Prometheus
- [ ] Distributed tracing configured
- [ ] Basic Grafana dashboard exists
- [ ] Security event metrics are tracked

## Dependencies
- MVP release

## Suggested Assignee
Ahmed

## Related Epic
EPIC 18 — Future Production Engineering
"""),

]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("SecureVault GitHub Backlog Creation")
    print("=" * 60)

    # 1. Labels
    print("\n[1/4] Creating labels...")
    for name, color, desc in LABELS:
        create_label(name, color, desc)

    # 2. Milestones
    print("\n[2/4] Creating milestones...")
    for title, desc in MILESTONES:
        create_milestone(title, desc)

    # 3. Verify milestones exist
    print("\n[3/4] Verifying milestones...")
    milestone_titles = set()
    for title, _ in MILESTONES:
        if milestone_exists(title):
            milestone_titles.add(title)
            print(f"  milestone: {title}")
        else:
            print(f"  WARN: could not find milestone '{title}'")

    # 4. Create issues
    print(f"\n[4/4] Creating {len(ISSUES)} issues...")
    created = 0
    skipped = 0
    for title, labels, ms_key, body in ISSUES:
        if ms_key not in milestone_titles:
            print(f"  WARN: skipping '{title}' — milestone '{ms_key}' not found")
            skipped += 1
            continue
        create_issue(title, labels, ms_key, body)
        created += 1

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Labels defined:       {len(LABELS)}")
    print(f"Milestones defined:   {len(MILESTONES)}")
    print(f"Issues created:       {created}")
    print(f"Issues skipped:       {skipped}")
    print(f"  - Epics:            19 (EPIC 0-18)")
    print(f"  - UX tickets:       20 (UX-001 to UX-020)")
    print(f"  - Implementation:   ~56 (FOUND, ARCH, BE, AUTH, SEC, FE, DASH, WALLET, RECIP, TXN, SECCTR, NOTIF, TEST, CI, DOCS, MVP, CHAIN, FUTURE)")
    print()
    print("P0 tickets:")
    p0_titles = [t for t, l, m, b in ISSUES if "priority:P0" in l]
    for t in p0_titles:
        print(f"  - {t}")
    print()
    print("Recommended first 10 tickets to execute:")
    first_10 = [
        "ARCH-001: Define high-level system architecture",
        "FOUND-001: Initialize repository structure and configuration files",
        "ARCH-002: Set up Docker Compose local development environment",
        "UX-001: Define information architecture  (parallel)",
        "BE-001: Initialize Spring Boot application",
        "BE-002: Configure PostgreSQL and Flyway",
        "BE-003: Configure exception handling and API error response format",
        "TEST-001: Set up Testcontainers integration test infrastructure",
        "CI-001: Implement GitHub Actions backend CI pipeline",
        "UX-002: Define main navigation  (parallel)",
    ]
    for i, t in enumerate(first_10, 1):
        print(f"  {i:2}. {t}")


if __name__ == "__main__":
    main()
