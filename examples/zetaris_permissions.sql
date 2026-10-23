-- Run these independently in Zetaris SQL Workspace if supported by your instance.
-- These are ONLY fictional hackathon permissions. No real customers or bank details.
-- Official syntax reference: https://kbase.zetaris.com/knowledge/sql-guide
-- Execute CREATE CONTAINER only once; it will fail if the container already exists.
CREATE SCHEMASTORE CONTAINER ENUVI_DEMO;

-- Next execute:
CREATE SCHEMASTORE VIEW guardian_permissions WITH CONTAINER ENUVI_DEMO AS (
 SELECT 'permission-demo-001' AS id,
        'demo-owner' AS subject,
        'transfer' AS action,
        'daughter-verified' AS recipient_id,
        80000 AS amount_cents,
        TRUE AS verified,
        'ACTIVE' AS status
);

-- Finally test read (should return exactly one synthetic permission):
SELECT id, subject, action, recipient_id, amount_cents,
       verified, status FROM ENUVI_DEMO.guardian_permissions;
