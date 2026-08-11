# Permissions Model

Jarvis uses capability-based permissions.

## Canonical Capabilities
- READ_SCREEN
- CONTROL_MOUSE
- CONTROL_KEYBOARD
- READ_FILES
- WRITE_FILES
- RUN_COMMAND
- CAMERA
- MICROPHONE
- PHONE_NOTIFICATIONS
- PHONE_MESSAGES
- NETWORK
- AI_PROVIDER
- MEMORY
- DEVICE_CONTROL
- FINANCIAL_ACTION

## Policy
- Sensitive capabilities require explicit authorization.
- Financial capabilities require strongest controls and approval requirements.
- Permission grants/revocations must be auditable.
