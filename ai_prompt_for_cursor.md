```
Analyze the following JIRA issues for test coverage gaps and generate Robot Framework test cases.

**Input Data**: @source_folder

**Analysis Tasks**:
1. For each JIRA issue, identify what should be tested
2. Determine if existing test coverage is adequate
2.1 if the jira issue is covered by the test case in zfrwbot_218, output the related information
2.2 if the jira issue not covered by the test cases in zfrwbot_218, generate the new test case based on the scheme defined in zfrwbot_218
3. Identify high-risk scenarios that need test coverage
4. Generate Robot Framework test cases for missing coverage

**Output Format**:
Generate a JSON file with this structure:
```json
{
  "analysis_summary": {
    "total_issues": 0,
    "high_priority_gaps": 0,
    "test_cases_generated": 0,
    "analysis_date": "ISO_DATE"
  },
  "coverage_gaps": [
    {
      "issue_key": "ISSUE-123",
      "gap_description": "Missing error handling test",
      "risk_level": "High|Medium|Low",
      "suggested_test": "Test scenario description"
    }
  ],
  "generated_tests": [
    {
      "test_name": "Test Name",
      "issue_keys": ["ISSUE-123"],
      "priority": "High|Medium|Low",
      "robot_code": "*** Test Cases ***\nTest Name\n    [Documentation]    Description\n    # Test implementation"
    }
  ]
}
```

Save the result as `analysis_results_TIMESTAMP.json` in the target_folder.
```

### 2. Security-Focused Analysis

```
Perform security-focused test coverage analysis for the provided JIRA issues.

**Input Data**: [Paste parsed JIRA data here]

**Security Analysis Focus**:
1. **Authentication & Authorization**: Are login, permissions, and access controls tested?
2. **Input Validation**: Are boundary conditions, injection attacks, and malformed input tested?
3. **Data Protection**: Are sensitive data handling and encryption scenarios covered?
4. **Error Handling**: Are security-related error conditions properly tested?
5. **Session Management**: Are session timeout, hijacking, and fixation scenarios tested?

**Output Requirements**:
- Prioritize security-critical test gaps
- Generate Robot Framework tests for authentication/authorization scenarios
- Include negative test cases for security vulnerabilities
- Focus on OWASP Top 10 coverage

Use the standard JSON output format but emphasize security test scenarios.
```

### 3. Performance-Focused Analysis

```
Analyze JIRA issues for performance and scalability test coverage gaps.

**Input Data**: [Paste parsed JIRA data here]

**Performance Analysis Focus**:
1. **Load Testing**: Are normal and peak load scenarios tested?
2. **Stress Testing**: Are system limits and breaking points identified?
3. **Response Time**: Are performance SLAs validated through tests?
4. **Resource Usage**: Are memory, CPU, and database performance monitored?
5. **Scalability**: Are horizontal and vertical scaling scenarios tested?

**Robot Framework Integration**:
- Generate performance test cases using Robot Framework
- Include timing keywords and performance assertions
- Consider integration with performance monitoring tools
- Focus on measurable performance criteria

Output should emphasize performance test scenarios and benchmarks.
```

### 4. API-Focused Analysis

```
Analyze JIRA issues for API test coverage, focusing on REST/GraphQL endpoints.

**Input Data**: [Paste parsed JIRA data here]

**API Testing Focus**:
1. **Endpoint Coverage**: Are all API endpoints tested (GET, POST, PUT, DELETE)?
2. **Request Validation**: Are request parameters, headers, and body validation tested?
3. **Response Validation**: Are response codes, headers, and payload structure tested?
4. **Error Scenarios**: Are 4xx and 5xx error conditions properly tested?
5. **Authentication**: Are API authentication and authorization mechanisms tested?
6. **Rate Limiting**: Are API rate limits and throttling scenarios covered?

**Robot Framework API Tests**:
- Use RequestsLibrary for HTTP testing
- Include JSON schema validation
- Test both happy path and error scenarios
- Validate response times and status codes

Generate comprehensive API test suites based on JIRA issue requirements.
```

### 5. UI/UX-Focused Analysis

```
Perform UI/UX test coverage analysis for web application features described in JIRA issues.

**Input Data**: [Paste parsed JIRA data here]

**UI/UX Analysis Focus**:
1. **User Workflows**: Are complete user journeys tested end-to-end?
2. **Form Validation**: Are input validation and error messages tested?
3. **Navigation**: Are menu, breadcrumb, and routing scenarios covered?
4. **Responsive Design**: Are mobile and tablet layouts tested?
5. **Accessibility**: Are WCAG compliance scenarios included?
6. **Browser Compatibility**: Are cross-browser scenarios tested?

**Robot Framework UI Tests**:
- Use SeleniumLibrary for web testing
- Include page object model patterns
- Test both positive and negative user interactions
- Validate visual elements and user feedback

Focus on user experience quality and accessibility compliance.
```

### 6. Regression-Focused Analysis

```
Analyze JIRA issues to identify critical regression test scenarios.

**Input Data**: [Paste parsed JIRA data here]

**Regression Analysis Focus**:
1. **Core Functionality**: What are the mission-critical features that must always work?
2. **Integration Points**: What system integrations are most likely to break?
3. **Configuration Changes**: What settings or deployment changes could cause issues?
4. **Environment Dependencies**: What external dependencies could cause failures?
5. **Historical Issues**: What types of bugs have occurred before in similar areas?

**Regression Test Strategy**:
- Prioritize tests by business impact and failure probability
- Create smoke test suites for quick validation
- Include database and configuration validation
- Focus on automated execution and fast feedback

Generate regression test suites that can be run automatically on deployments.
```