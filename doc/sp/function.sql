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

                   
SELECT funcYMDHHMMToDash('202208182213') as t;
DELIMITER $$ 
DROP FUNCTION IF EXISTS funcYMDHHMMToDash$$ 
CREATE FUNCTION funcYMDHHMMToDash (
	dataDate VARCHAR(13)
) RETURNS VARCHAR(18)  #yyyy-mm-dd HH:MM
BEGIN
	RETURN CONCAT(SUBSTRING(dataDate ,1,4),'-',
					SUBSTRING(dataDate ,5,2),'-',
					SUBSTRING(dataDate ,7,2),' ',
					SUBSTRING(dataDate ,9,2),':',
					SUBSTRING(dataDate ,11,2));
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

select funcGradeInfoOfCustomer('pettester@peteasy.kr', 'sally@peteasy.kr');
DELIMITER $$ 
DROP FUNCTION IF EXISTS funcGradeInfoOfCustomer$$ 
CREATE FUNCTION funcGradeInfoOfCustomer (
	dataPartnerId VARCHAR(64),
    dataCustomerId VARCHAR(64)
) RETURNS varchar(64) CHARSET utf8
BEGIN
	SET @grade_name = '';
	SET @grade_ord = 0;
	SELECT A.grade_name, A.grade_ord INTO @grade_name , @grade_ord
    FROM tb_grade_of_shop A JOIN tb_grade_of_customer B
		ON A.idx = B.grade_idx
    WHERE A.artist_id = dataPartnerId AND A.is_delete = 0
			AND B.customer_id = dataCustomerId
	ORDER BY B.idx DESC LIMIT 1;
	IF @grade_ord  < 1 THEN
		RETURN "";
	ELSE
		RETURN CONCAT(@grade_name,'|',@grade_ord);
	END IF;
END $$ 
DELIMITER ;

DELIMITER $$ 
DROP FUNCTION IF EXISTS funcSplitGrade$$ 
CREATE FUNCTION funcSplitGrade (
	dataString VARCHAR(64),
    dataDelimeter VARCHAR(10)
) RETURNS varchar(64) CHARSET utf8
BEGIN
	
    IF dataNum = 1 THEN
		SET @ret = SUBSTRING_INDEX(dataString, dataDelimeter, 1);
	ELSE
		SET @ret = SUBSTRING_INDEX(dataString, dataDelimeter, -1);
    END IF;
    
	IF @grade_ord  < 1 THEN
		RETURN "";
	ELSE
		RETURN CONCAT(@grade_name,'|',@grade_ord);
	END IF;
END $$ 
DELIMITER ;

DELIMITER $$ 
DROP FUNCTION IF EXISTS funcExtractID$$ 
CREATE FUNCTION funcExtractID (
	dataString VARCHAR(64)
) RETURNS varchar(64) CHARSET utf8
BEGIN
	
	SET @new_id = dataString;
	SET @cnt = INSTR(@new_id, '신규등록(');
	
    IF @cnt > 0 THEN
    BEGIN
		SET @new_id = REPLACE(@new_id, '신규등록(', '');
        SET @new_id = SUBSTRING(@new_id, 1, LENGTH(@new_id)-1);
	END;
    END IF;
    IF (@new_id REGEXP ('^[0-9]+$')) THEN 
		RETURN dataString;
    ELSE
		RETURN @new_id;
    END IF;

END $$ 
DELIMITER ;
