-- 000002_create_messages.down.sql
DROP INDEX IF EXISTS idx_messages_room_time;
DROP INDEX IF EXISTS idx_messages_room_id;
DROP TABLE IF EXISTS messages;
