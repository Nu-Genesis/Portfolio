# ISOReady - ISO 27001:2022 Annex A Control Mapping Methodology
**Capstone Project | Cybersecurity Program**

---

## Project Overview

ISOReady is a structured methodology framework developed as a collaborative capstone project by a team of four cybersecurity students. The project was designed to bridge the gap between ISO 27001:2022's Annex A controls and real-world implementation practice - producing a reusable, auditor-ready mapping system applicable to small-to-mid-size organizations operating in cloud-first environments.

The deliverable was a dual-part documentation template that maps every Annex A control across two companion sections: a **Control Entry** (Part A) capturing implementation decisions, clause relevance, and evidence expectations, and a **Methodology Companion** (Part B) providing operational guidance on how to reason through each control's applicability and tier assignment.

---

## Objectives

- Develop a repeatable, defensible methodology for assessing and documenting ISO 27001:2022 Annex A controls
- Apply the framework against a defined reference company profile to simulate practical implementation
- Produce documentation suitable for use in an actual audit preparation context
- Demonstrate team competency in information security governance, risk reasoning, and compliance documentation

---

## Team & Collaboration

This project was completed by a team of four, with responsibilities distributed across control mapping, methodology design, reference company architecture, and documentation quality assurance. Collaborative review cycles ensured consistency of tier assignments and applicability decisions across all controls - a critical requirement given that inconsistent tier reasoning is itself a common ISO audit finding.

Regular team reviews were used to challenge draft decisions against the escalation criteria built into the methodology, replicating the scrutiny an auditor or senior reviewer would apply in practice.

---

## Methodology Design

### Reference Company Profile

All controls were evaluated against a consistent fictional organization with the following characteristics:

- **Size:** 50-200 staff
- **Architecture:** Cloud-first, SaaS-oriented
- **Access Model:** RBAC-governed Identity Provider (IdP)
- **Sector:** Professional services

This profile was deliberately chosen to reflect a realistic and common organizational archetype - one where many controls are split between internal ownership and vendor responsibility.

### Tier Assignment Framework

Each control was assigned one of three tiers reflecting implementation depth required:

| Tier | Label | Depth Required |
|------|-------|----------------|
| Tier 1 | Critical | Full implementation documentation with rationale |
| Tier 2 | Important | High-level summary sufficient |
| Tier 3 | Scoped / Inherited | Scope exclusion or vendor inheritance justification only |

Tier assignment followed a structured five-step decision process evaluating:

1. **Audit Failure Risk** - likelihood of generating a finding in a real ISO 27001 audit
2. **Control Dependencies** - number of downstream controls reliant on this one
3. **Identity Relevance** - whether the control directly governs identity and access management
4. **Reference Company Exposure** - whether the company owns, shares, or inherits the control surface
5. **Tier Assignment** - derived from the above factors using defined escalation logic

### Applicability Decision Framework

Each control was also assessed for applicability:

- **Applicable** - the company fully owns the implementation
- **Partially Applicable** - implementation is split between the company and a vendor
- **Not Applicable (Justified)** - the control does not apply to the company's architecture or service model

A key design principle was that thin or poorly reasoned Not Applicable decisions are themselves a common audit finding. The methodology required specific, auditable justifications for any exclusion.

### Escalation Criteria

The methodology included a formal escalation table specifying conditions under which a tier assignment should be revisited. Triggers included vendor attestation failures, newly discovered control dependencies, architecture changes, and real-world breach events involving the relevant control type. This design reflects the dynamic nature of a live ISMS and was included to make the framework maintainable beyond initial implementation.

---

## Control Entry Structure (Part A)

Each control in the framework was documented using a standardised six-section entry:

1. **Tier Assignment** - assigned tier and rationale
2. **Applicability Decision** - decision and justification
3. **Explanation** - implementation detail scaled to tier depth
4. **Clause Relevance** - mapping to ISO 27001:2022 Clauses 4-10
5. **Evidence Expectation** - specific artifacts an auditor would expect (policy names, log types, review record formats)

The clause relevance section was particularly important - it demonstrates not just what is implemented, but why it matters within the broader ISMS management system context, connecting operational controls to strategic clauses such as leadership (Clause 5), risk assessment (Clause 6), and performance evaluation (Clause 9).

---

## Methodology Companion Structure (Part B)

The companion section was designed to function as a decision-support tool - enabling a practitioner to work through any control independently and arrive at a consistent, defensible outcome. It includes:

- **Plain-language interpretation** of what the control operationally requires
- **Step-by-step tier and applicability decision guidance**
- **Implementation guidance** specific to the reference company profile, including cloud-specific considerations
- **Control linkage mapping** documenting dependency, feed-into, and related relationships with other Annex A controls

The control linkage component was a significant design investment. By explicitly mapping how controls depend on, feed into, or relate to one another, the framework surfaces systemic risks that would otherwise only become visible during a gap assessment - making it a more proactive and resilient planning tool.

---

## Key Skills Demonstrated

- ISO 27001:2022 Annex A interpretation and operational translation
- Risk-tiered control documentation
- Audit-ready evidence specification
- Cloud and SaaS-environment applicability reasoning
- ISMS clause mapping (Clauses 4-10)
- Cross-control dependency analysis
- Collaborative governance documentation in a team environment

---

## Reflections

ISOReady was designed from the outset to be a practical artefact, not an academic exercise. Every structural decision - the tier model, the escalation criteria, the evidence expectations, the control linkage table - was made with an auditor in mind as the end reader. The reference company profile grounded abstract requirements in concrete architecture decisions, and the collaborative review process reinforced the standard itself: that an ISMS is only as strong as the consistency and rigour of its documentation.

---

*Capstone project completed as part of a cybersecurity degree program. Developed collaboratively by a team of four.*
