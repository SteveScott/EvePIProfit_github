SELECT *
FROM pg_stat_activity
WHERE usename = 'lojyjajvpwaaci';

SELECT pg_terminate_backend(pid)
FROM   pg_stat_activity
WHERE  usename = 'lojyjajvpwaaci'
AND    pid <> pg_backend_pid();

