# Sentinel Use Case Library

## 1. IT Metrics Validation

### Problem
Committee-reported metrics may rely on inconsistent denominators, cumulative logic, screenshots, or manually corrected values.

### Sentinel review focus
- numerator and denominator consistency
- reporting-period alignment
- system-of-record lineage
- reviewer approval
- unsupported positive conclusions

### Buyer
IT GRC, CISO office, Internal Audit, 2LOD Risk.

---

## 2. Vendor SOC 2 Reliance Review

### Problem
SOC 2 reports are often collected, but customer-side responsibilities, CUECs, data-flow boundaries, and residual risks are not evaluated deeply.

### Sentinel review focus
- SOC 2 reliance logic
- CUEC applicability
- data handling
- NPI/PII processing
- retention and breach obligations
- internal ownership of complementary controls

### Buyer
TPRM, Procurement Risk, CISO, Compliance.

---

## 3. Privacy Evidence Challenge

### Problem
Teams may claim customer data is protected without showing processing boundaries, retention, access, contractual obligations, or data-flow evidence.

### Sentinel review focus
- data-flow evidence
- processing purpose
- retention logic
- access boundaries
- vendor obligations
- privacy/security control linkage

### Buyer
Privacy Officer, DPO, Legal, TPRM, Security Governance.

---

## 4. SDLC Governance Review

### Problem
Release evidence may show deployment occurred but not prove that required security, risk, change, and approval gates were satisfied.

### Sentinel review focus
- security test evidence
- change record linkage
- approval trail
- exception handling
- production readiness
- release governance

### Buyer
AppSec, DevSecOps, Change Management, Internal Audit.

---

## 5. AI Governance Evidence Review

### Problem
AI use cases may launch without inventorying, tiering, approval evidence, data handling review, monitoring, or incident escalation logic.

### Sentinel review focus
- AI inventory record
- risk/capability classification
- usage restriction
- approval authority
- data handling
- monitoring
- incident escalation

### Buyer
AI Governance, CISO, CIO, Model Risk, Compliance.
