# Database Specialist - SQL Examples

> **Load Trigger**: Schema design, queries, migrations, PostgreSQL

## Schema Design Pattern

```sql
-- Users table with proper constraints
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints for data integrity
    CONSTRAINT email_format CHECK (
      email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    ),
    CONSTRAINT name_not_empty CHECK (
      LENGTH(TRIM(first_name)) > 0 AND LENGTH(TRIM(last_name)) > 0
    )
);

-- Strategic indexes based on query patterns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;
CREATE INDEX idx_users_created_at ON users(created_at);
```

## Auto-Update Timestamp Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## Migration Template

```sql
-- Migration: 001_create_users_table
-- Description: Create initial users table with constraints

-- Up Migration
BEGIN;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

COMMIT;

-- Down Migration (Rollback)
BEGIN;

DROP TABLE IF EXISTS users CASCADE;

COMMIT;
```

## Complex Query with CTE

```sql
-- Find active users with their task counts
WITH user_task_counts AS (
    SELECT
        u.id,
        u.email,
        u.first_name,
        u.last_name,
        COUNT(t.id) as task_count,
        COUNT(t.id) FILTER (WHERE t.status = 'completed') as completed_count
    FROM users u
    LEFT JOIN tasks t ON t.assignee_id = u.id
    WHERE u.is_active = true
    GROUP BY u.id, u.email, u.first_name, u.last_name
)
SELECT
    id,
    email,
    first_name || ' ' || last_name as full_name,
    task_count,
    completed_count,
    CASE
        WHEN task_count > 0
        THEN ROUND(completed_count::numeric / task_count * 100, 2)
        ELSE 0
    END as completion_rate
FROM user_task_counts
ORDER BY completion_rate DESC;
```

## Row-Level Security

```sql
-- Enable RLS on tasks table
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see tasks they own or are assigned to
CREATE POLICY tasks_visibility ON tasks
    FOR SELECT
    USING (
        reporter_id = current_setting('app.current_user_id')::uuid
        OR assignee_id = current_setting('app.current_user_id')::uuid
    );

-- Policy: Users can only update their own tasks
CREATE POLICY tasks_update ON tasks
    FOR UPDATE
    USING (
        reporter_id = current_setting('app.current_user_id')::uuid
    );
```

## Performance Analysis

```sql
-- Analyze slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.*, COUNT(t.id) as task_count
FROM users u
LEFT JOIN tasks t ON t.assignee_id = u.id
WHERE u.is_active = true
GROUP BY u.id
ORDER BY task_count DESC
LIMIT 10;

-- Check index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

## Backup and Restore Commands

```bash
# Backup database
pg_dump -h localhost -U postgres -d mydb -F c -f backup.dump

# Restore database
pg_restore -h localhost -U postgres -d mydb -F c backup.dump

# Export specific table
pg_dump -h localhost -U postgres -d mydb -t users -f users.sql
```
