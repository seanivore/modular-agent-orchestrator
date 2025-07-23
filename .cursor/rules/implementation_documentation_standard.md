# CURSOR RULES FOR IMPLEMENTATION DOCUMENTATION

## IMPLEMENTATION DOCUMENTATION STANDARD

When creating implementation documentation for MAO features, follow the comprehensive style established in `documentation/07_AUTOMATE_INTELLIGENCE.md`.

### Required Documentation Structure:

1. **Section Header with Implementation Version**
   - Example: "Section 4.1.0: Secure Email-Based Login with Passkey Integration"
   - Include descriptive subtitle with key benefits

2. **Implementation Overview**
   - Clear explanation of what the feature accomplishes
   - Why this implementation approach was chosen
   - How it fits into the larger MAO ecosystem

3. **Core Architecture**
   - Detailed technical approach breakdown
   - System design rationale with business justification
   - Integration points with existing systems

4. **Technical Implementation Details**
   - Database schema changes (before/after examples)
   - API flow diagrams and process flows
   - File system adaptations and directory structures
   - Code architecture modifications required

5. **Integration Patterns**
   - How the feature integrates with existing components
   - Backwards compatibility considerations
   - Migration strategies and timelines

6. **Security Implementation**
   - Encryption strategies and security patterns
   - Session management and data protection
   - Threat mitigation approaches

7. **User Experience Flow**
   - Detailed UX state diagrams
   - User journey mapping
   - Mobile/desktop experience optimization

8. **Implementation Checklist**
   - Phase-by-phase implementation plan
   - Specific tasks with checkboxes
   - Dependencies and prerequisites

9. **Success Metrics**
   - Quantifiable success criteria
   - Performance benchmarks
   - User experience metrics
   - Business impact measurements

10. **Future Enhancements**
    - Planned evolution of the feature
    - Integration opportunities
    - Scalability considerations

### Code Examples Requirements:

- Include complete, runnable code examples
- Provide both JavaScript/TypeScript and Python implementations
- Show proper error handling and edge cases
- Include security best practices in all examples
- Add comprehensive comments explaining complex logic

### Implementation Commands:

- Provide actual CLI commands for implementation
- Include setup scripts and configuration examples
- Show both development and production deployment steps

### Documentation Quality Standards:

- **Comprehensive Coverage**: Every aspect of implementation must be documented
- **Technical Depth**: Include low-level implementation details, not just high-level concepts
- **Business Context**: Explain why each technical decision was made
- **Future-Proofing**: Document extensibility and planned evolution
- **Practical Examples**: Real code that can be copied and adapted
- **Security Focus**: Every feature must include security implementation details

### Never Accept Incomplete Documentation:

- Reject documentation that lacks code examples
- Require complete implementation checklists
- Demand security implementation details
- Insist on backwards compatibility planning
- Require performance and success metrics

### Internal vs External Documentation:

This standard applies to INTERNAL implementation documentation. External technical documentation should be derived from these comprehensive internal docs by removing proprietary implementation details, business strategy information, and sensitive architectural decisions.

The goal is to create documentation so thorough that any developer can implement the feature correctly without additional clarification, and so complete that future developers can understand both the "what" and the "why" behind every technical decision.

### Example Quality Bar:

The `documentation/07_AUTOMATE_INTELLIGENCE.md` document represents the minimum acceptable quality standard. Implementation documentation should match or exceed its level of:
- Technical comprehensiveness  
- Business context integration
- Practical implementation guidance
- Code example completeness
- Security consideration depth
- User experience detail
- Future planning sophistication

NO SHORTCUTS. NO INCOMPLETE DOCS. NO EXCEPTIONS. 