-- Temporary fictional permission record. This is NOT a stored source of authority.
-- Run via Guardian's --sql-file option to exercise the real Zetaris HTTP API.
SELECT
  'permission-demo-001' AS id,
  'demo-owner' AS subject,
  'transfer' AS action,
  'daughter-verified' AS recipient_id,
  80000 AS amount_cents,
  TRUE AS verified,
  'ACTIVE' AS status;
