# Database Connection Troubleshooting Runbook

## Purpose

Provide investigation guidance for application incidents involving database connectivity.

## Connection Pool Exhaustion

Common indicators include:

- Database connection acquisition timeouts
- Connection pool exhaustion errors
- Increased application latency
- Increased HTTP 5xx responses
- Failed database-dependent requests

## Investigation

Check:

1. Database connection pool configuration.
2. Connection acquisition timeout.
3. Connection error rate before and after recent deployments.
4. Application logs for connection acquisition failures.
5. Distributed traces for failed database spans.
6. Recent configuration or deployment changes.
7. Historical incidents with similar symptoms.

## Remediation

Potential remediation may include restoring an approved connection-pool configuration or rolling back a configuration change.

Production remediation requires human approval.

## Verification

After an approved remediation:

- Confirm database connection errors return to baseline.
- Confirm HTTP 500 rate returns to baseline.
- Confirm application latency returns to normal.
- Verify successful database spans in distributed traces.