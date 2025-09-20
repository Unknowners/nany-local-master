-- Перевірка існування нових таблиць
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('swipes', 'pairs', 'payments', 'chat_threads', 'chat_messages', 'chat_last_reads');
