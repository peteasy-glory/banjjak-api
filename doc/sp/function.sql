SHOW GLOBAL variables like 'log_bin_trust_function_creators';
-- 위 쿼리시 OFF 일 경우 아래 쿼리 실행 콘솔 root에서 실행 로컬에서 에러 나서.  
SET GLOBAL log_bin_trust_function_creators = 1;

DELIMITER $$ 
DROP FUNCTION IF EXISTS funcYMDHHMMToDate$$ 
CREATE FUNCTION funcYMDHHMMToDate (
	dataYear INT,
    dataMonth INT,
    dataDay INT,
    dataHour INT,
    dataMinute INT
) RETURNS VARCHAR(16)  #yyyy-mm-dd HH:MM
BEGIN
	DECLARE aTmp VARCHAR(16)  DEFAULT '';
	SET aTmp = CONCAT(CAST(dataYear AS CHAR(4)), '-', LPAD(CAST(dataMonth AS CHAR(2)),2,'0'), '-', 
				LPAD(CAST(dataDay AS CHAR(2)),2,'0'), ' ', LPAD(CAST(dataHour AS CHAR(2)),2,'0'),':', LPAD(CAST(dataMinute AS CHAR(2)),2,'0'));
	RETURN aTmp;
END $$ 
DELIMITER ;
#select funcYMDToDate(2002, 12, 2);
DELIMITER $$ 
DROP FUNCTION IF EXISTS funcYMDToDate$$ 
CREATE FUNCTION funcYMDToDate (
	dataYear INT,
    dataMonth INT,
    dataDay INT
) RETURNS VARCHAR(16)  #yyyy-mm-dd
BEGIN
	DECLARE aTmp VARCHAR(16)  DEFAULT '';
	SET aTmp = CONCAT(CAST(dataYear AS CHAR(4)), '-', LPAD(CAST(dataMonth AS CHAR(2)),2,'0'), '-', 
				LPAD(CAST(dataDay AS CHAR(2)),2,'0'));
	RETURN aTmp;
END $$ 
DELIMITER ;

DELIMITER ;
#select funcYMToDate(2002, 12);
DELIMITER $$ 
DROP FUNCTION IF EXISTS funcYMDToDate$$ 
CREATE FUNCTION funcYMDToDate (
	dataYear INT,
    dataMonth INT
) RETURNS VARCHAR(16)  #yyyy-mm-dd
BEGIN
	DECLARE aTmp VARCHAR(16)  DEFAULT '';
	SET aTmp = CONCAT(CAST(dataYear AS CHAR(4)), '-', LPAD(CAST(dataMonth AS CHAR(2)),2,'0'), '-', 
				LPAD(CAST(dataDay AS CHAR(2)),2,'0'));
	RETURN aTmp;
END $$ 
DELIMITER ;


