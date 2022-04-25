# Istio

## Vocabulary

|Term|Meaning|
|-|-|
|upstream|direction of receiving requests from outside -> POD(proxy -> app) -> and back |
|downstream|direction of sending requests from POD(app -> proxy) -> outside and back|
|inbound|Within POD: proxy container -> app container|
|outbound|Within POD: app container -> proxy container|
|root namespace|Typically `istio-system`, find in `ConfigMap` in `istio-system`|

# mTLS
`PeerAuthentication` selects containers

# References
1. [https://istio.io/latest/docs/reference/glossary/](https://istio.io/latest/docs/reference/glossary/)
2. [https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/intro/terminology](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/intro/terminology)