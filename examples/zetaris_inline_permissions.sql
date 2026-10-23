SELECT
  'permission-demo-001' AS id,
  'demo-owner' AS subject,
  'transfer' AS action,
  'daughter-verified' AS recipient_id,
  80000 AS amount_cents,
  TRUE AS verified,
  'ACTIVE' AS status;
