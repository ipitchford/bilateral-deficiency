# Peer Review Report — Editor-in-Chief Lens

## Manuscript information

- **Title:** *Bilateral Deficiency: A Residual SAT Optimisation Parameter and the Exact Coordinate of Independent Domination on Formula Graphs*
- **Manuscript ID:** internal pre-submission draft
- **Review date:** 8 August 2026
- **Review round:** 1

## Reviewer information

- **Role:** Editor-in-Chief / handling-editor simulation
- **Identity:** theoretical-computer-science editor specializing in structural complexity, reductions, and graph optimization
- **Focus:** journal fit, contribution clarity, editorial completeness, and whether the paper's strongest claims are supported at specialist-journal standard

## Overall assessment

- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision**
- [ ] Reject
- **Confidence:** 4/5

The manuscript defines bilateral deficiency as the minimum clause-minus-variable deficiency of a bipolar residual and proves a size-preserving bijection to independent dominating sets of a canonical formula graph. It then develops separation examples, algebra, width-dependent complexity, a regular-DIM coordinatisation, and a reproducibility artifact. This is an unusually coherent attempt to turn an implicit reduction cost into an explicit optimization object, and the paper is appropriately candid that the arithmetic already appears in Chlebík and Chlebíková. The central results appear substantial enough for a specialist theoretical-computer-science venue if the proofs survive expert checking. The strongest editorial liabilities are not a visible fatal theorem error, but an incomplete priority audit, dependence of the all-integer spectrum on a positive base object that is not stated in the paper, and the absence of an independently checkable lower-bound certificate for that base. Author, archive, funding, and interest fields are also unfinished. I therefore invite a major revision: the mathematical architecture is promising, but the submission must become standalone and archival before journal review.

## Strengths

### S1. Precise claim boundary

Section 2.2 states that the replicated-clause cost is not new and describes the advance as “extraction and extension.” This is editorially strong because it makes the originality claim falsifiable and prevents the paper from claiming priority for the equation \(|D|=k+t|T|-|U|\).

### S2. A contribution larger than a naming exercise

Theorems 2, 4, 5, 6, 7, 9, and 10 collectively give a bijection, algebra, complexity boundary, and graph-family coordinate. Even if one discounts Theorem 1 as a reformulation of the definition, these later results supply several independent tests of whether the new object has mathematical utility.

### S3. Assurance levels are separated honestly

Sections 7.2 and 8 distinguish upper-bound witnesses, execution receipts, structural proofs, and formal proof logs. The supplement repeats that distinction and documents two development failures. This is much more credible than presenting passing code as proof.

### S4. The equipped-family qualification is careful

Section 6 repeatedly says “supplied with” or “equipped with” a specified dominating induced matching. That qualification avoids falsely claiming a canonical representation for arbitrary unlabeled regular graphs.

## Weaknesses

### W1. The positive base of the integer-spectrum theorem is not standalone

**Problem:** Section 6 defines the positive component \(P\) only as “the 15-variable verified component from [1]” and uses \(\beta(P)=1\) to prove that the proper exact \((3,2,2)\) spectrum is all integers. The formula itself and a mathematical lower-bound certificate do not appear in the manuscript.

**Why it matters:** The spectrum theorem is advertised as a complete classification result. A reader should not have to reconstruct a key lemma from a web release and trust an implementation receipt to verify the base value.

**Suggestion:** State \(P\) explicitly in an appendix or compact clause table, give its witness for \(\beta\le1\), and provide either a human-checkable structural lower bound, a checkable proof object, or a precisely scoped computer-assisted theorem with an independently verified checker and archived proof data.

**Severity:** Major.

### W2. Priority positioning is responsible but not yet publication-grade

**Problem:** Section 2.4 explicitly says the search was bounded; the integrity audit names MathSciNet, zbMATH, dissertations, non-English sources, and hypergraph terminology as unsearched or incompletely searched. The closest antecedent lacks a stable page or theorem pinpoint.

**Why it matters:** The title and conclusion ask the community to accept a new parameter. Historical distinctness is not necessary for the proofs, but it is central to the paper's editorial case.

**Suggestion:** Complete a specialist bibliographic audit, add the exact location of the 2008 cost decomposition, and revise the priority paragraph in light of the result. Search independent-domination polynomial work predating the 2018 arXiv citation as well.

**Severity:** Major.

### W3. Submission metadata and archival links are incomplete

**Problem:** The byline, ORCID, CRediT allocation, funding, interests, repository revision, and archival DOI are placeholders (title block and Declarations).

**Why it matters:** These are mandatory for accountable submission, especially for a paper with disclosed AI assistance and a computational base case.

**Suggestion:** Resolve all declarations and deposit an immutable artifact before submission.

**Severity:** Major editorial requirement; not a mathematical defect.

### W4. Some language presents established consequences as more dramatic than they are

**Problem:** Phrases such as “complete solution polynomial” and “complete coordinatisation” are technically qualified, but can initially read as broader than their actual equipped formula-graph domain. Theorem 1 is an exact restatement of the feasible domain rather than a deep structural theorem.

**Why it matters:** A skeptical reader may infer inflation and discount the genuinely nontrivial results.

**Suggestion:** Retain the results but label Theorem 1 as a characterization/proposition, make the domain part of headings, and reserve “complete” for statements whose scope is stated in the same sentence.

**Severity:** Minor.

## Detailed comments

### Title and abstract

The title accurately exposes both the SAT and graph sides but is long. The abstract is admirably specific about the width dichotomy and the claim boundary. It should disclose that the all-integer exact-\((3,2,2)\) spectrum uses a finite computer-verified positive component unless a mathematical certificate is added.

### Introduction

The criteria for parameterhood are useful and the six-use claim is not left as marketing. Consider compressing the repeated assurance disclaimers once the appendix and archive make them concrete.

### Prior art

This section is central and presently good but incomplete. The cost decomposition needs a pinpoint, and the independent-domination polynomial citation should be checked for earlier sources. The manuscript should distinguish “not found” from “absent” exactly as it currently does.

### Mathematical development

The formula-graph bijection is the paper's cleanest core. The algebra and width results make the parameter useful. The regular-DIM result is valuable but must be made standalone at its positive base.

### Reproducibility and declarations

The supplement is unusually transparent. It should be converted from a local directory description into an immutable archive with a versioned manifest. The author placeholders preclude submission as-is.

## Questions for the authors

1. Can the positive exact \((3,2,2)\) base be given a structural lower-bound proof, or will the spectrum theorem be explicitly labeled computer-assisted?
2. What prior-art databases and terminology families will define the final priority audit, and what stopping rule will be reported?
3. Which exact artifact revision and proof/checker objects will be archived and cited by DOI?
4. Is the intended venue primarily SAT/complexity or graph theory, and which half of the contribution should therefore lead the title and abstract?

## Minor issues

- Use one spelling convention consistently for “optimisation/optimization” and “characterisation/characterization.”
- Replace local artifact paths in the final submission with archive-relative paths.
- Add theorem or section pinpoints for technical antecedents wherever possible.

## Dimension scores

| Dimension | Score | Descriptor | Notes |
|---|---:|---|---|
| Originality | 76 | Strong | New explicit object and theory, but close antecedent and incomplete priority audit |
| Methodological rigor | 80 | Strong | Proof architecture and boundary cases are careful; key finite base not standalone |
| Evidence sufficiency | 70 | Adequate | Broad written support, but positive base lower bound remains receipt-dependent |
| Argument coherence | 86 | Strong | Clear claim-to-result progression |
| Writing quality | 82 | Strong | Precise but occasionally overqualified and terminologically expansive |
| Literature integration | 68 | Adequate | Important sources identified; specialist audit incomplete |
| Significance and impact | 76 | Strong | Plausible value across SAT, graph theory, and proof engineering |
| **Weighted average** | **78.1** | **Minor range numerically; Major Revision by linchpin override** | Standalone spectrum proof, priority, and archival requirements control the decision |
