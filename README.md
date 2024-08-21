# Verbose-Fishstick Protocol

## Introduction

The **Verbose-Fishstick Protocol** is intentionally flawed protocol 🦠 which designed to track close contacts securely, it uses some privacy and security measures through cryptographic techniques 🔒. Despite its imperfections, this protocol shows a little bit how even imperfect systems can help in public health.

## Protocol Overview

The protocol unfolds through these key steps:

1. **ECC (Elliptic Curve Cryptography)**: Each participant generates a unique identifier using ECC's public key 🔑. <img src="https://github.com/ace-bibabo/verbose-fishstick/blob/main/ECC.png" alt="bibabo" width="100" height="100">



2. **Shamir's Secret Sharing**: The identifier is split into multiple shares using the k-out-of-n Shamir's Secret Sharing scheme. This clever method ensures the ID can only be reconstructed when a minimum number of shares are combined, adding a touch of extra security 🛡️.

3. **Broadcasting Shares via UDP**: These shares are broadcasted over the network using UDP, ensuring efficient and lightweight dissemination 📡.

4. **ID Reconstruction**: Devices gather incoming shares and reconstruct the original ID when they collect the required number of shares. This step ensures that only those in close proximity and for a sufficient duration can obtain the ID, representing true close contact scenarios 🏷️.

5. **Diffie-Hellman Key Exchange for Shared ID**: Once the ID is reconstructed, devices perform a Diffie-Hellman key exchange to derive a shared secret key 🔑. 

6. **Storing IDs in Bloom Filters (BFs)**: IDs are encoded and stored in BFs, which are efficient probabilistic data structures. Each BF holds records for a short period before being periodically sent to a backend server via TCP for cross-referencing with reported cases. The server then responds with exposure status based on these matches 📊.

7. **Reporting Infected Diagnosis**: If a diagnosis is positive, a client can upload its Bloom Filter (BF) to the backend server. This process helps notify other users who may have been exposed, facilitating timely interventions 🚨.

## Potential Attacks

* **Man-in-the-Middle (MiTM)**: An attacker capturing sufficient UDP broadcast shares could broadcast them widely, leading to potential false notifications ⚠️.
