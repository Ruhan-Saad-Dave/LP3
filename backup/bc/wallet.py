"""
=============================================================================
Assignment: Blockchain Assignment BT2 (Group C)
Title: Key Pair Derivation, Digital Signature Creation & Verification
       (MetaMask Wallet Cryptography)
Course: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
Reference: Lab Manual Pages 128-137
=============================================================================
Demonstrates the fundamental cryptography behind Ethereum & MetaMask wallets:
  1. Cryptographic Private Key Generation (256-bit entropy)
  2. Public Ethereum Address Derivation (secp256k1 Elliptic Curve + Keccak-256)
  3. Message Signing using EIP-191 Standard
  4. Digital Signature Verification & Public Address Recovery
=============================================================================
"""

import sys
import secrets


def demonstrate_wallet_cryptography(custom_message=None):
    """
    Demonstrates Web3 wallet creation, private key generation, digital signature 
    creation, and public key signature verification.
    """
    try:
        from eth_account import Account
        from eth_account.messages import encode_defunct
    except ImportError:
        print("[!] Note: 'eth-account' package not found. Please install via: pip install eth-account")
        return

    print("=" * 75)
    print("   WEB3 WALLET CRYPTOGRAPHY: KEY PAIR & DIGITAL SIGNATURE DEMO")
    print("=" * 75)

    # 1. Generate a secure random 256-bit Private Key (32 bytes hexadecimal)
    raw_private_key = "0x" + secrets.token_hex(32)
    account = Account.from_key(raw_private_key)

    print("\n--- 1. WALLET KEY PAIR GENERATION ---")
    print(f"Private Key (KEEP SECRET!)      : {raw_private_key}")
    print(f"Derived Public Address (Shareable) : {account.address}")
    print("Explanation: The Ethereum address is derived by hashing the elliptic curve")
    print("             public key with Keccak-256 and taking the last 20 bytes.")

    # 2. Define a Message to Sign (e.g., authentication request for dApp login)
    if not custom_message:
        message_text = "Authorize login to Decentralized App at timestamp: 2026-11-01 10:00:00"
    else:
        message_text = custom_message

    print("\n--- 2. MESSAGE SIGNING (EIP-191 STANDARD) ---")
    print(f"Plaintext Message : '{message_text}'")

    # Format message according to EIP-191 standard to prevent transaction replay
    formatted_msg = encode_defunct(text=message_text)

    # Sign the message using the sender's private key
    signed_message = Account.sign_message(formatted_msg, private_key=raw_private_key)
    signature_hex = signed_message.signature.hex()

    print(f"Signature (r, s, v components - 65 bytes):")
    print(f"  Hex: {signature_hex[:50]}...{signature_hex[-20:]}")

    # 3. Verify Signature on Network / Node / Smart Contract
    print("\n--- 3. SIGNATURE VERIFICATION & PUBLIC KEY RECOVERY ---")
    # In Ethereum, ecrecover recovers the public address that created the signature
    recovered_address = Account.recover_message(formatted_msg, signature=signed_message.signature)
    print(f"Original Signer Address   : {account.address}")
    print(f"Recovered Public Address  : {recovered_address}")

    # 4. Check Authentication Validity
    is_valid = (recovered_address.lower() == account.address.lower())
    print("\n--- 4. AUTHENTICATION STATUS ---")
    if is_valid:
        print("  [+] Result: SUCCESS (SIGNATURE VALID & AUTHENTICATED)")
        print("  [+] Proof: The transaction/message was definitively authored by the private key holder.")
    else:
        print("  [-] Result: FAILED (SIGNATURE INVALID / TAMPERED)")

    # 5. Tamper Test Demonstration
    print("\n--- 5. TAMPER-PROOF DEMONSTRATION ---")
    tampered_text = message_text + " [TAMPERED DATA]"
    tampered_msg = encode_defunct(text=tampered_text)
    recovered_tampered = Account.recover_message(tampered_msg, signature=signed_message.signature)
    is_tamper_valid = (recovered_tampered.lower() == account.address.lower())
    print(f"Altered Message           : '{tampered_text}'")
    print(f"Recovered Address on Tamper: {recovered_tampered}")
    print(f"Tamper Verification Match : {is_tamper_valid} -> Tampering rejected!")
    print("=" * 75)


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("Choose Option:")
    print("  1. Run Standard Wallet Cryptography & Signature Verification [Default]")
    print("  2. Sign Custom Message")
    choice = safe_input("Enter choice (1/2) [Default: 1]: ", "1")

    if choice == "2":
        msg = safe_input("Enter message text to sign: ", "Authorize payment of 1.5 ETH to Student Portal")
        demonstrate_wallet_cryptography(custom_message=msg)
    else:
        demonstrate_wallet_cryptography()


if __name__ == "__main__":
    main()
