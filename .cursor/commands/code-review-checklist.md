# Code Review Checklist

When reviewing code, systematically check these areas:

## 1. Correctness
- [ ] Does the code do what it's supposed to do?
- [ ] Are edge cases handled?
- [ ] Are there any obvious bugs?

## 2. Code Quality
- [ ] Is the code readable and well-organized?
- [ ] Are variable and function names descriptive?
- [ ] Is there unnecessary code duplication?
- [ ] Are comments helpful and up-to-date?

## 3. Security
- [ ] Is user input validated and sanitized?
- [ ] Are there any hardcoded secrets?
- [ ] Are SQL queries parameterized?
- [ ] Is authentication/authorization handled correctly?

## 4. Performance
- [ ] Are there any obvious performance issues?
- [ ] Are database queries efficient?
- [ ] Is there unnecessary work in loops?

## 5. Testing
- [ ] Are there adequate tests?
- [ ] Do the tests cover edge cases?
- [ ] Are the tests readable and maintainable?

## 6. Documentation
- [ ] Is the code self-documenting?
- [ ] Are complex algorithms explained?
- [ ] Is the API documented if applicable?

---

**Usage**: Invoke this command with `/code-review-checklist` in Cursor chat to get a structured review of your code.
