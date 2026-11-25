# Mobile Equipment Identifier claim audit

This offline static auditor compares documented device identifier claims with Python call patterns. It does not execute inspected code or access the network.

## Usage

```sh
meid-validation-claim-audit audit [repo] --fail-on high --ignore vendor --json --verbose
python3 -m meid_validation_claim_audit audit .
```

The default root is the current directory. The threshold accepts `high` or `medium`; each `--ignore` takes one relative path prefix and may be repeated. The process exits 0 for a pass, 2 for findings at or above the threshold, and 1 for usage or I/O errors. The version option prints the package version.

The root README and Markdown files under a docs directory supply prose; fenced blocks are excluded and inline code is included. Matching ignores case, expands contractions, treats hyphens as spaces, collapses whitespace, and uses exact phrases with word boundaries. Denial spans are removed before positive claims are matched. Production Python files supply evidence; tests are considered separately. Fixtures, docs, examples, and symlinks are excluded from production evidence. Syntax errors provide no evidence.

## Findings

```
documented-meid-validation-claim-false
documented-no-meid-validation-claim-false
```

A positive claim without production evidence is HIGH, or MEDIUM when evidence appears only in tests. A denial contradicted by production evidence is HIGH. A positive claim without any Python files is HIGH, while a denial without Python files passes.

## Differentiation

This audit does not cover the following neighbouring capabilities.
Checking whether input is checked at all is outside this audit.
Checking ISBN-10 or ISBN-13 book number digits is outside this audit.
Checking ISSN serial number digits is outside this audit.
Checking IBAN bank account digits is outside this audit.
Checking universally unique identifier strings is outside this audit.
Checking semantic version strings is outside this audit.
Checking hardware address strings is outside this audit.
Checking bank identifier codes is outside this audit.
Judging schedule strings is outside this audit.
Describing schedule strings in human language is outside this audit.
Running jobs on a schedule is outside this audit.
Checking calendar dates is outside this audit.
Limiting call duration is outside this audit.
Taking card payments is outside this audit.
Extracting card details from documents is outside this audit.
Proving account ownership with a one-time code or confirmation link is outside this audit.
Verifying a password against a stored hash is outside this audit.
Hashing a password for storage is outside this audit.
Generating random passwords is outside this audit.
Password-protecting a PDF is outside this audit.
Sending email is outside this audit.
Sending text messages is outside this audit.
Extracting document data is outside this audit.
Decoding a code from an image is outside this audit.
Checking email addresses for shape or deliverability is outside this audit.
Checking phone numbers for shape or regional validity is outside this audit.
Judging password strength is outside this audit.
Checking JSON against a JSON Schema is outside this audit.
Checking card numbers for shape, Luhn checksum, and brand is outside this audit.
Checking domain names is outside this audit.
Checking web addresses is outside this audit.
Checking numeric network addresses is outside this audit.
Decoding JSON text is outside this audit.
Matching regular expressions is outside this audit.
Splitting web addresses into parts is outside this audit.
Fetching a web address over the network is outside this audit.
Resolving names through DNS is outside this audit.
Encoding account numbers in barcodes is outside this audit.
Extracting account numbers from documents is outside this audit.
Extracting vehicle numbers from registration documents or images is outside this audit.
Splitting vehicle numbers into sections or decoding make, model, and year is outside this audit.
Looking up vehicle history is outside this audit.
Checking hexadecimal colors is outside this audit.
Checking ORCID researcher identifiers is outside this audit.
Checking International Standard Name Identifiers is outside this audit.
Checking and resolving digital object identifiers is outside this audit.
Checking CUSIP national security identifiers is outside this audit.
Checking SEDOL identifiers is outside this audit.
Checking ISIN securities identifiers with their letter-expanded Luhn checksum is outside this audit.
Fetching securities records from market-data services is outside this audit.
Extracting securities identifiers from documents is outside this audit.
Checking 15-digit decimal IMEI identifiers for GSM devices is outside this audit.
Checking older 8-hex-digit Electronic Serial Numbers is outside this audit.
Checking serial numbers in general is outside this audit.
Fetching device records from a registry or carrier is outside this audit.
Extracting device identifiers from documents or photos is outside this audit.
Reading spreadsheets is outside this audit.
Generating spreadsheets is outside this audit.
Reading word-processing documents is outside this audit.
Generating word-processing documents is outside this audit.
Reading presentations is outside this audit.
Generating presentations is outside this audit.
Extracting PDFs is outside this audit.
Generating PDFs is outside this audit.
Merging PDFs is outside this audit.
Splitting PDFs is outside this audit.
Rotating PDFs is outside this audit.
Filling PDF forms is outside this audit.
Watermarking PDFs is outside this audit.
Redacting PDFs is outside this audit.
Compressing PDFs is outside this audit.
Annotating PDFs is outside this audit.
Extracting tables is outside this audit.
Optical character recognition is outside this audit.
Document extraction is outside this audit.
Electronic signatures is outside this audit.
Screen recording is outside this audit.
Video generation is outside this audit.
QR code generation is outside this audit.
Barcode generation is outside this audit.
Barcode scanning is outside this audit.
Audio mixing is outside this audit.
Audio generation is outside this audit.
Audio editing is outside this audit.
Source separation is outside this audit.
Speech recognition is outside this audit.
Text-to-speech is outside this audit.
Noise suppression is outside this audit.
Music generation is outside this audit.
Music transcription is outside this audit.

## Limitations

```
validate meid
```

The bare phrase above can describe a manual runbook step instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid validation
```

The bare phrase above can describe a roadmap feature instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid validator
```

The bare phrase above can describe a hosted web page rather than local code instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid check
```

The bare phrase above can describe a field-presence lint rule instead of implemented functionality, so the finding may be a false positive and needs human review.

```
check meid
```

The bare phrase above can describe a manual runbook step instead of implemented functionality, so the finding may be a false positive and needs human review.

```
verify meid
```

The bare phrase above can describe a visual comparison with a handset instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid code validation
```

The bare phrase above can describe a field-presence check instead of implemented functionality, so the finding may be a false positive and needs human review.

```
valid meid
```

The bare phrase above can describe an example input instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid is valid
```

The bare phrase above can describe example output text instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid is invalid
```

The bare phrase above can describe example error text instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid validity
```

The bare phrase above can describe a configuration flag or column name instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid format validation
```

The bare phrase above can describe a format description instead of implemented functionality, so the finding may be a false positive and needs human review.

```
validate meid number
```

The bare phrase above can describe a shape-only number check instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid number validation
```

The bare phrase above can describe a specification section instead of implemented functionality, so the finding may be a false positive and needs human review.

```
validate meid code
```

The bare phrase above can describe a manual runbook step instead of implemented functionality, so the finding may be a false positive and needs human review.

```
check meid code
```

The bare phrase above can describe a manual runbook step instead of implemented functionality, so the finding may be a false positive and needs human review.

```
validate meid hex
```

The bare phrase above can describe a manual runbook step instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid decimal validation
```

The bare phrase above can describe a specification section instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid number check
```

The bare phrase above can describe an enrolment checklist item instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid validation
```

The bare phrase above can describe a result produced by an external platform instead of implemented functionality, so the finding may be a false positive and needs human review.

```
meid
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

```
meid number
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

```
validate identifier
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

```
check digit
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

```
luhn
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

```
manufacturer code
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

```
serial number
```

The bare phrase above alone does not establish this capability and is excluded from the lists.

Static patterns do not establish semantic correctness.

Dead code counts as evidence.

Alias chains the tracer cannot follow are missed.

Each evidence route must appear in one module.

Local definitions shadow matching routes even when they wrap a real call.

A call on an unknown object may be missed even when that object provides a real operation.

A bare library import is not evidence.

A subprocess invoking an external checker is not evidence.

A roadmap claim is still treated as a claim.

A changelog claim is still treated as a claim.

A TODO claim is still treated as a claim.

Denials outside the exact list are not recognised.

Claims outside the root README and docs directories are not read.

The library accepts a 14-digit hexadecimal form without a check digit.

The library accepts an 18-digit decimal form without a check digit.

The library routes all-decimal input to IMEI validation, so a valid IMEI passes that route.

The library performs no manufacturer-code registry check.

A compact operation only transforms its input and is not evidence.

A format operation only formats its input and is not evidence.

A check-digit calculation alone is not evidence.

A binary conversion alone is not evidence.

A pseudo-ESN conversion alone is not evidence.

A Luhn checksum alone is not evidence.

An IMEI operation alone is not evidence.

An ESN operation alone is not evidence.

A device lookup alone is not evidence.

A length check alone is not evidence.

A manufacturer-code membership check alone is not evidence.

A regular expression match alone is not evidence.

A generic input check alone is not evidence.

An email address check alone is not evidence.

A phone number check alone is not evidence.

A web address check alone is not evidence.

A numeric address check alone is not evidence.

A domain check alone is not evidence.

An ISBN check alone is not evidence.

An ISSN check alone is not evidence.

An IBAN check alone is not evidence.

An ISIN check alone is not evidence.
