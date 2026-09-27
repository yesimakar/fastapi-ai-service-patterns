# Provider Boundary

Routes should not call model SDKs directly. They should call service-layer abstractions that manage validation, retries, fallbacks, and diagnostics.
