# AI Provider Abstraction Specification

Jarvis Core must not be tightly coupled to one AI vendor.

## Conceptual Interface
AIProvider
- OpenAIProvider
- AnthropicProvider
- GoogleProvider
- DeepSeekProvider
- LocalModelProvider
- FutureProvider

## Requirements
- Configurable provider selection/routing policies
- Fallback behavior on provider failure
- Health tracking
- Explicit disclosure when cloud processing is used
