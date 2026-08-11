# Security Policy (Initial)

Security principles:
- Least privilege
- Explicit authorization
- Secure credential handling
- Input/output validation
- Auditability for sensitive operations
- Safe plugin boundaries

Mandatory controls:
- No API keys/secrets in source code.
- Permission checks before device, file, network, financial, or automation actions.
- Logging for security-relevant events.
- Recovery/safe mode pathways for critical failures.
