# Sentinel Evidence Intake Guide

## What v0.9 adds

Sentinel v0.9 adds a simple evidence intake layer.

Supported upload types:

- `.json`
- `.csv`
- `.txt`
- `.md`

## JSON package format

Best format:

```json
{
  "organization": "Sample Bank",
  "industry": "BFSI",
  "evidence_type": "IT Metrics Validation",
  "review_objective": "Validate metric evidence.",
  "items": [
    {
      "title": "Metric Evidence",
      "content": "Evidence text here.",
      "source_system": "System name",
      "owner": "Owner",
      "reporting_period": "Q4"
    }
  ]
}
```

## CSV format

Recommended columns:

```text
title,content,source_system,owner,reporting_period
```

Each row becomes one evidence item.

## Text / Markdown format

The whole file becomes one evidence item.

## Current limitation

This is a beginner-safe browser-side intake parser. It is suitable for MVP demo and structured sample reviews. It is not yet a production document parser for PDFs, Word files, screenshots, or OCR.
