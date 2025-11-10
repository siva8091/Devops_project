SELECT client_addr, application_name, count(*) 
FROM pg_stat_activity 
WHERE datname = 'sonarqube'
GROUP BY client_addr, application_name;
