# Debug Assistant

## Overview
Systematic approach to debugging issues in the code.

## Debugging Process

### 1. Understand the Problem
- What is the expected behavior?
- What is the actual behavior?
- When did this start happening?
- Can it be reproduced consistently?

### 2. Gather Information
- Error messages and stack traces
- Relevant log output
- Input data that causes the issue
- Environment details (OS, versions, etc.)

### 3. Isolate the Issue
- Identify the smallest code path that reproduces the bug
- Check recent changes that might have introduced it
- Test with different inputs

### 4. Analyze
- Review the code logic step by step
- Check variable values at key points
- Verify assumptions about data types and values
- Look for common issues:
  - Null/undefined references
  - Off-by-one errors
  - Race conditions
  - Type mismatches

### 5. Fix and Verify
- Implement the fix
- Test the original failing case
- Test related functionality for regressions
- Add tests to prevent recurrence

Please describe the issue you're experiencing, and I'll help debug it systematically.
