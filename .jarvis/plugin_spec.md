# Plugin Specification

Every plugin/module must declare:
- name
- version
- description
- permissions
- dependencies
- tools
- events
- configuration
- storage
- security requirements

Plugin constraints:
- Isolate failures where practical.
- Avoid forcing Jarvis Core rewrites for new capabilities.
- Enforce capability checks at plugin boundaries.
