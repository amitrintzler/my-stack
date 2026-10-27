# Vault

Secret storage, dynamic credentials, and the single most load-bearing service in most platforms.

**Lock-in class.** Structural. The API and auth methods are specific, and every consumer integrates against them.

## Read only

```bash
vault status                           # seal state, HA, version. works unauthenticated
vault token lookup
vault secrets list -detailed
vault auth list
vault list sys/leases/lookup/          # lease sprawl
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Sealed | 1 | Everything that needs a secret is down or about to be |
| Standby with no active node | 1 | Same, with a longer explanation |
| Root token in use | 2 | It should exist only during break glass, and then be revoked |
| Certificate or token expiring within 14 days | 2 | A scheduled outage nobody scheduled |
| Lease count growing without bound | 3 | A consumer is not renewing correctly, and storage will fill |
| Audit device disabled | 2 | Vault stops serving requests entirely if all audit devices fail, so this is availability, not only compliance |

## Dry run

Policies can be checked with `vault policy read` and tested with a scoped token before rollout. Never test a policy change with a privileged token, since it will appear to work.

## Rollback

Policy and mount changes are reversible by reapplying the previous definition from Git. Revoked leases and rotated roots are not. Unsealing after a bad seal requires the key shares, so confirm who holds them before touching anything, not during.

## Never without approval

Unseal, seal, root token generation, revoking a lease or a token that is in use, disabling an auth method or an audit device, and rotating anything.

Never write a secret value, token or unseal key into any file, ledger, report or commit message, including a partial one. Reference it by path only.

## Failure modes

An expired token in CI presents as a permission error in the application, three layers away from Vault.

Filling storage stops writes, and lease sprawl is the usual cause.

If every audit device fails, Vault blocks requests by design. That surprises people during an incident, at the worst moment.
