# Basics
| Term | Description |
|------|-------------|
| Connection | Is a transport providing suitable type of service, connection is transient, associated with **one** session |
| Session | Association between client and server. Created by the handshake protocol. Contains security parameters that are shared between **multiple** connections. They are used to avoid **expensive** negotiation of new security parameters for each connection |
| Flight | Chunk of logically grouped data. Exchanged during handshake. Messages from the same flight may be placed in same _Record_ |
| Record | DTLS message fragment that must fit within single IP packet. Contains sequence number and epoch. Conveyed by Record protocol |

# TLS
Protocol directly _above_ layer 4 ISO/OSI. Uses reliable transport **only** (TCP in general).  
Main goal of TLS is to provide secure connection between parties.

Properties:  
* Identity exchange via use of public keys (certificates). They’re used to verify counterparts during initialization of communication. Then the session key (symmetric key) is agreed
* Privacy: data is encrypted via **symmetric** cryptography (key is negotiated during [TLS Handshake Protocol](https://github.com/kiemlicz/util/wiki/SSL#handshake-protocol))
* Reliability, uses integrity checks via secure hash functions

**All** TLS messages are encrypted, even handshake (but with _NULL_ protocol - so they are plain text).
## Description
TLS is composed of two sub-protocols (layers), identified by _Content Type_ field.
 1. TLS Record Protocol (encapsulates handshake protocol)  
 2. TLS Handshake Protocol

Privacy and reliability is ensured by lower layer - _TLS Record Protocol_  
Authentication and encryption algorithm negotiation is ensured by upper layer - _TLS Handshake Protocol_

### Handshake protocol
Designed to authenticate peers with each other using asymmetric cryptography (one way authentication is required, mutual is optional)  
Shared secret negotiation (for latter symmetric cryptography) - in general: session negotiation  

Handshake protocol consists of three sub-protocols:

 1. Handshake Protocol  
  Creates the session (context of whole communication)
  ```
  Client sends ClientHello
  ----------------------->
  
  Server responds with ServerHello
  <-----------------------
  [or server responds with Alert if version or algorithms(ciphers) contained in ClientHello doesn't match with server's]
  <-----------------------
  ```
  There are buggy implementations of server's that close connections without sending any alert messages  
  At this point both sides have established following parameters:  
   * ProtocolVersion
   * SessionID
   * CipherSuite
   * CompressionMethod

  ```
  Server sends its Certificate and ServerKeyExchange
  <-----------------------
  ```
  Optional
  ```
  Server may request client’s certificate (CertificateRequest)
  <-----------------------
  ```
  Optional
  ```
  Server sends ServerHelloDone
  <-----------------------
  ```
  ```
  Client sends its Certificate and ClientKeyExchange 
  ----------------------->
  ```
  ```
  Client sends CertificateVerify 
  ----------------------->
  ```
  Optional, send if the certificate that client has sent “had the signing ability” (all certificates besides ones containing fixed DH parameters). _CertificateVerify_ message contains signature of all sent/received handshake messages so far by the client. Hash and signature used in computation must be the one of those present in supported_signature_algorithms (from _CertificateRequest_). Client creates signature using its private key, server verifies it using client’s public key.
  ```
  Client sends ChangeCipherSpec 
  ----------------------->
  ```
  With cipher it had set as pending. This cipher becomes current (explained in Change Cipher sub-section)
  ```
  Client sends Finished
  ----------------------->
  ```
  Uses new ciphers to send _Finished_
  ```
  Server sends its own ChangeCipherSpec
  <-----------------------
  Server sends Finished message (using new ciphers)
  <-----------------------
  ```

 2. Alert Protocol  
  Indicates failures, associated session identifier must be invalidated. May be used to indicate connection end (via _Alert(close_notify)_).

 3. Change Cipher  
  Receiver of this message must instruct the _Record Layer_ (_Record Protocol_) to immediately copy the read pending state into current state. Sender of this message must immediately instruct the record layer to copy pending write state to current write state.

### Record Protocol
Compression/decompression, division into blocks, reassembly.  
Used by Handshake Protocol.  
Maintains connection state - encryption algorithm, compression algorithm and MAC algorithm.  
Receiving unexpected record type results in _Alert(UnexpectedMessage)_.  
Contains information about compression, MAC and encryption for: 
 - current read/write states 
 - pending read/write states

_Current_ are used for record processing.  
To become current:
 1. the pending is first agreed upon in Handshake Protocol
 2. the change cipher spec message makes it current

# DTLS
TLS over datagram protocols

TLS in its original form cannot be used on top of datagram transport like UDP as:  
 - Decrypting of individual records could be impossible. If record `N` is not received, then integrity check for record `N+1` will fail as relies on previous sequence number
 - Records depend on each other. Cryptographic context is retained between records (as _stream ciphers_ are used).
 - Handshake protocol could fail as requires all messages to be reliably delivered (no messages must be lost during handshake phase) in defined order.

## Mechanisms for fitting TLS into UDP

Message loss protection:
 - Retransmission, if expected other-side message (for handshake phase) doesn't arrive within given time then the message is retransmitted.
 - Stream ciphers are prohibited as they are stateful and loosing packages breaks them (missing record disallows decryption of packets with next sequence number).

Message reordering protection:
 - Each message is assigned explicit sequence number. This way peer can determine if the message it receives is the next message it awaits.
 - Each message is also assigned epoch number. Epoch is incremented with every _ChangeCipherSpec_ message. Usually message from previous epoch can be discarded.

DTLS record must fit in single datagram (in order to avoid IP fragmentation). As e.g. handshake messages are bigger than max record size they can be fragmented in multiple records.

### Summary of TLS handshake changes for DTLS
 1. Stateless cookie exchange
 2. Message loss and reordering handling
 3. Retransmission timers added

## Further considerations
As DTLS can use UDP the client-server relation is changed to more peer-to-peer like. Meaning that it should be possible for both parties to act like client **and** server simultaneously. This is useful feature. DTLS sessions can be long-lived thus e.g. when one side (that acted like server) has lost DTLS state it should be able to establish new one by sending _ClientHello_ immediately after detecting failure

# References
 1. [RFC handshake flow](https://tools.ietf.org/html/rfc5246#section-7.3)
 2. [RFC CertificateVerify details](https://tools.ietf.org/html/rfc4492#section-5.8)
 3. [DTLS RFC](https://tools.ietf.org/html/rfc6347). Mind that this RFC is presented as series of diffs from TLS RFC
 4. [Stream cipher](https://en.wikipedia.org/wiki/Stream_cipher)