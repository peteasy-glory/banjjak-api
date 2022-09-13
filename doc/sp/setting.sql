select * from tb_artist_list 
where artist_id = 'pettester@peteasy.kr';
call procPartnerPC_Setting_Artist_Working_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Artist_Working_get $$
CREATE PROCEDURE procPartnerPC_Setting_Artist_Working_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 미용사 근무일시 조회 
   */
	SELECT if(sequ_prnt is NULL,9999, sequ_prnt) as ord, artist_id, name, nicname, if((is_main = ''or is_main = null), 0, is_main) AS is_host
		,is_out AS is_leave, is_view AS is_show
		, GROUP_CONCAT(CONCAT(seq,'|',week,'|', time_start,'|',time_end)) AS work
	FROM tb_artist_list
	WHERE artist_id = dataPartnerId
	GROUP BY name, nicname
	ORDER BY ord ASC, is_main DESC;
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Artist_Working_post $$
CREATE PROCEDURE procPartnerPC_Setting_Artist_Working_post(
	dataPartnerId VARCHAR(64),
    dataName VARCHAR(64),
    dataNick VARCHAR(64),
    
)
BEGIN
	/**
		샵별 미용사 근무일시 추가 
   */
	SELECT if(sequ_prnt=null,9999, sequ_prnt) as ord, artist_id, name, nicname, if((is_main = ''or is_main = null), 0, is_main) AS is_host
		,is_out AS is_leave, is_view AS is_show
		, GROUP_CONCAT(CONCAT(seq,'|',week,'|', time_start,'|',time_end)) AS work
	FROM tb_artist_list
	WHERE artist_id = dataPartnerId
	GROUP BY name, nicname
	ORDER BY sequ_prnt ASC, seq ASC;
END $$ 
DELIMITER ;

select * from tb_artist_list 
where artist_id = 'pettester@peteasy.kr'
;

-- call procPartnerPC_Setting_Artist_Working_get('eaden@peteasy.kr');
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Artist_Working_get $$
-- CREATE PROCEDURE procPartnerPC_Setting_Artist_Working_get(
-- 	dataPartnerId VARCHAR(64)
-- )
-- BEGIN
-- 	/**
-- 		샵별 미용사 근무일시 조회 
--    */
-- 	SELECT * FROM tb_artist_list
-- 	WHERE artist_id = dataPartnerId;	
-- END $$ 
-- DELIMITER ;

-- 	SELECT GROUP_CONCAT(seq) AS seq, name, nicname, GROUP_CONCAT(week)
--     ,  GROUP_CONCAT(CONCAT(time_start, '-',time_end)) AS peroid, GROUP_CONCAT(sequ_prnt)
--     FROM tb_artist_list
-- 	WHERE artist_id = 'eaden@peteasy.kr'
-- 	GROUP BY name, nicname;

call procPartnerPC_Setting_Shop_OpenClose_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Shop_OpenClose_get $$
CREATE PROCEDURE procPartnerPC_Setting_Shop_OpenClose_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 오픈/글로즈 시간
   */
	select * from tb_working_schedule 
	where customer_id = dataPartnerId;
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Shop_OpenClose_modify $$
CREATE PROCEDURE procPartnerPC_Setting_Shop_OpenClose_modify(
    dataPartnerID VARCHAR(64),
    dataOpenTime INT,
    dataCloseTime INT,
    dataIsWorkOnholiday INT
    
)
BEGIN
	/**
		샵별 오픈/글로즈 시간 추가/변경 하기
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*) INTO @row_num 
    FROM tb_working_schedule 
    WHERE customer_id = dataPartnerID;
    
    START TRANSACTION;

    IF @row_num > 0 THEN
    begin
		UPDATE tb_working_schedule
		SET working_start = dataOpenTime, working_end = dataCloseTime, rest_public_holiday = dataIsWorkOnHoliday, update_time = NOW()
		WHERE customer_id = dataPartnerID; 
	end;
    ELSE
    begin
		INSERT INTO tb_working_schedule (customer_id, working_start, working_end, rest_public_holiday, update_time)
        VALUES (dataPartnerID, dataOpenTime, dataCloseTime, dataIsWorkOnHoliday, NOW());
	end;
    END IF;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;
	select * from tb_working_schedule 
	where customer_id = 'pettester@peteasy.kr';
    

call procPartnerPC_Setting_Regular_Holiday_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Regular_Holiday_get $$
CREATE PROCEDURE procPartnerPC_Setting_Regular_Holiday_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵별 정기 휴일 
   */
	select * from tb_regular_holiday 
	where customer_id = dataPartnerId;
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Regular_Holiday_modify $$
CREATE PROCEDURE procPartnerPC_Setting_Regular_Holiday_modify(
	dataPartnerId VARCHAR(64),
    dataWeek VARCHAR(10)
)
BEGIN
	/**
		샵별 정기 휴일 추가/ 수정
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*) INTO @row_num 
    FROM tb_regular_holiday 
    WHERE customer_id = dataPartnerID;
    
    SET @sun = SUBSTRING(dataWeek, 1, 1);
    SET @mon = SUBSTRING(dataWeek, 2, 1);
    SET @tue = SUBSTRING(dataWeek, 3, 1);
    SET @wed = SUBSTRING(dataWeek, 4, 1);
    SET @thu = SUBSTRING(dataWeek, 5, 1);
    SET @fri = SUBSTRING(dataWeek, 6, 1);
    SET @sat = SUBSTRING(dataWeek, 7, 1);
    
    START TRANSACTION;

    IF @row_num > 0 THEN
    begin
		UPDATE tb_regular_holiday
		SET is_sunday = @sun, 
			is_monday = @mon,
			is_tuesday = @tue,
			is_wednesday = @wed,
			is_thursday = @thu,
			is_friday = @fri,
			is_saturday = @sat,
            update_time = NOW()
		WHERE customer_id = dataPartnerID; 
	end;
    ELSE
    begin
		INSERT INTO tb_regular_holiday (customer_id, is_sunday, is_monday, is_tuesday, is_wednesday,is_thursday,is_friday,is_saturday,week_type, update_time)
        VALUES (dataPartnerID, @sun, @mon, @tue,@wed,@thu,@fri,@sat,'1', NOW());
	end;
    END IF;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
END $$ 
DELIMITER ;

select * from tb_regular_holiday where customer_id = 'pettester@peteasy.kr';


call procPartnerPC_Setting_Personal_Vacation_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Personal_Vacation_get $$
CREATE PROCEDURE procPartnerPC_Setting_Personal_Vacation_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		미용사 휴가 설정  
   */
	SELECT worker , GROUP_CONCAT(ph_seq,'|', type, '|',
			CONCAT(start_year,'-', LPAD(start_month,2,0),'-', LPAD(start_day,2,0),' ', LPAD(start_hour,2,0),':', LPAD(start_minute,2,0)), '|',
           CONCAT(end_year,'-', LPAD(end_month,2,0),'-', LPAD(end_day,2,0),' ', LPAD(end_hour,2,0),':', LPAD(end_minute,2,0)), '|', 
           update_time) AS vacation
    FROM tb_private_holiday
    WHERE customer_id = dataPartnerId
    GROUP BY worker;
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Personal_Vacation_post $$
CREATE PROCEDURE procPartnerPC_Setting_Personal_Vacation_post(
	dataPartnerID VARCHAR(64),
    dataWorker VARCHAR(64),
    dataType VARCHAR(20),
    dataStDate VARCHAR(20), 
    dataFiDate VARCHAR(20)
)
BODY: BEGIN
	/**
		미용사 휴가 추가 하기  
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*) INTO @row_num 
    FROM tb_private_holiday 
    WHERE CONCAT(start_year, LPAD(start_month,2,0), LPAD(start_day,2,0), LPAD(start_hour,2,0), LPAD(start_minute,2,0)) = dataStDate
		AND CONCAT(end_year, LPAD(end_month,2,0), LPAD(end_day,2,0), LPAD(end_hour,2,0), LPAD(end_minute,2,0)) = dataFiDate
        AND customer_id = dataPartnerID AND worker = dataWorker;
    IF @row_num > 0 THEN
    BEGIN
		SELECT 401 AS err;
		LEAVE BODY;
    END;
    END IF;
    
    START TRANSACTION;

	INSERT INTO tb_private_holiday
	(customer_id, worker, type, start_year, start_month, start_day, start_hour, start_minute,
								end_year, end_month, end_day, end_hour, end_minute)
	VALUES (dataPartnerID, dataWorker, dataType, 
			CAST(SUBSTRING(dataStDate,1,4) AS SIGNED), CAST(SUBSTRING(dataStDate,5,2) AS SIGNED), CAST(SUBSTRING(dataStDate,7,2) AS SIGNED), 
            CAST(SUBSTRING(dataStDate,9,2) AS SIGNED), CAST(SUBSTRING(dataStDate,11,2) AS SIGNED), 
			CAST(SUBSTRING(dataFiDate,1,4) AS SIGNED), CAST(SUBSTRING(dataFiDate,5,2) AS SIGNED), CAST(SUBSTRING(dataFiDate,7,2) AS SIGNED), 
            CAST(SUBSTRING(dataFiDate,9,2) AS SIGNED), CAST(SUBSTRING(dataFiDate,11,2) AS SIGNED));    
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Personal_Vacation_delete $$
CREATE PROCEDURE procPartnerPC_Setting_Personal_Vacation_delete(
	dataIdx INT
)
BODY: BEGIN
	/**
		미용사 휴가 삭제 하기  
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	
    START TRANSACTION;

	DELETE FROM tb_private_holiday WHERE ph_seq = dataIdx; 
	
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

call procPartnerPC_Setting_Time_Limit_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Time_Limit_get $$
CREATE PROCEDURE procPartnerPC_Setting_Time_Limit_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		타임제 설정 조회   
   */
	SELECT A.*, B.nicname, B.is_main, B.is_out, B.is_view FROM tb_time_schedule A LEFT JOIN 
    (SELECT artist_id, name, nicname, is_main, is_out, is_view FROM  tb_artist_list where artist_id = dataPartnerId GROUP BY name) B 
		ON (A.artist_id = B.artist_id AND A.artist_name = B.name)
    WHERE A.artist_id = dataPartnerId;
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Time_Limit_modify $$
CREATE PROCEDURE procPartnerPC_Setting_Time_Limit_modify(
	dataIdx INT,
	dataPartnerID VARCHAR(64),
    dataName VARCHAR(64),
    dataTime VARCHAR(256)
)
BEGIN
	/**
		타임제 설정 추가/수정   
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

    START TRANSACTION;

    IF dataIdx > 0 THEN
    begin
		UPDATE tb_time_schedule
		SET res_time_off = dataTime, 
			res_time_cnt = '',
			update_date = NOW()
		WHERE no = dataIdx ; 
	end;
    ELSE
    begin
		INSERT INTO tb_time_schedule (artist_id, artist_name, res_time_off, res_time_cnt,reg_date)
        VALUES (dataPartnerID, dataName, dataTime, '', NOW());
	end;
    END IF;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
END $$ 
DELIMITER ;

call procPartnerPC_Setting_BookingChoiceTimeType_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BookingChoiceTimeType_get $$
CREATE PROCEDURE procPartnerPC_Setting_BookingChoiceTimeType_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		예약 스케쥴 운영방식 조회
   */

	SELECT is_time_Type 
    FROM tb_shop
    WHERE customer_id=dataPartnerID;
	
END $$ 
DELIMITER ;

call procPartnerPC_Setting_BookingChoiceTimeType_put('pettester@peteasy.kr', 0);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BookingChoiceTimeType_put $$
CREATE PROCEDURE procPartnerPC_Setting_BookingChoiceTimeType_put(
	dataPartnerID VARCHAR(64),
    dataTimeType INT
)
BEGIN
	/**
		예약 스케쥴 운영방식 설정
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

    START TRANSACTION;

	UPDATE tb_shop 
    SET is_time_type = dataTimeType 
    WHERE customer_id = dataPartnerID;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
END $$ 
DELIMITER ;

call procPartnerPC_Setting_Break_Time_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Break_Time_get $$
CREATE PROCEDURE procPartnerPC_Setting_Break_Time_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		휴게시간 설정 조회   
   */
	SELECT * FROM tb_time_off
    WHERE customer_id = dataPartnerId;
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Break_Time_modify $$
CREATE PROCEDURE procPartnerPC_Setting_Break_Time_modify(
	dataPartnerID VARCHAR(64),
    dataBreakTime VARCHAR(255)
)
BEGIN
	/**
		휴게시간 설정 추가/변경    
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*) INTO @row_num 
    FROM tb_time_off 
    WHERE customer_id = dataPartnerID;
    
    START TRANSACTION;

    IF @row_num > 0 THEN
    begin
		UPDATE tb_time_off
		SET res_time_off = dataBreakTime, update_date = NOW()
		WHERE customer_id = dataPartnerID; 
	end;
    ELSE
    begin
		INSERT INTO tb_time_off (customer_id, res_time_off, res_time_cnt, res_time_off_yn, reg_date, update_date)
        VALUES (dataPartnerID, dataBreakTime, '', 'y', NOW(), NOW());
	end;
    END IF;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;


call procPartnerPC_Setting_Vat_put('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Vat_put $$
CREATE PROCEDURE procPartnerPC_Setting_Vat_put(
	dataPartnerId VARCHAR(64),
    dataIsVat INT
)
BEGIN
	/**
		부가세 설정 변경  
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;
    
	UPDATE tb_shop
	SET is_vat = dataIsVat
	WHERE customer_id = dataPartnerId;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
END $$ 
DELIMITER ;

########################
call procPartnerPC_Setting_BeautyPartDog_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyPartDog_get $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyPartDog_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		강아지 미용구분 조회  
   */
    
    SELECT * FROM tb_product_dog_worktime WHERE artist_id = dataPartnerId AND is_delete = 2;
    
END $$ 
DELIMITER ;

call procPartnerPC_Setting_BeautyPartDog_modify('pettester343333@peteasy.kr', 'update', 'insert');
call procPartnerPC_Setting_BeautyPartDog_modify('eaden@peteasy.kr',"UPDATE tb_product_dog_worktime SET worktime1_disp_yn = 'y', worktime2_disp_yn = 'y', worktime3_disp_yn = 'y', worktime4_disp_yn = 'y', worktime5_disp_yn = 'y', worktime6_disp_yn = 'y', worktime7_disp_yn = 'y', worktime8_disp_yn = 'y', worktime9_disp_yn = 'y', worktime10 = '10', worktime10_title = '미용1', worktime10_disp_yn = 'y', worktime11 = '10', worktime11_title = '미용2', worktime11_disp_yn = 'y', worktime12 = '10', worktime12_title = '미용3', worktime12_disp_yn = 'y', worktime13 = '10', worktime13_title = '미용4 ', worktime13_disp_yn = 'y', worktime14 = '10', worktime14_title = '미용5 ', worktime14_disp_yn = 'y', update_dt = NOW() WHERE artist_id = 'eaden@peteasy.kr'","INSERT INTO tb_product_dog_worktime SET artist_id = 'eaden@peteasy.kr', worktime1_disp_yn = 'y', worktime2_disp_yn = 'y', worktime3_disp_yn = 'y', worktime4_disp_yn = 'y', worktime5_disp_yn = 'y', worktime6_disp_yn = 'y', worktime7_disp_yn = 'y', worktime8_disp_yn = 'y', worktime9_disp_yn = 'y', worktime10 = '10', worktime10_title = '미용1', worktime10_disp_yn = 'y',worktime11 = '10', worktime11_title = '미용2', worktime11_disp_yn = 'y',worktime12 = '10', worktime12_title = '미용3', worktime12_disp_yn = 'y',worktime13 = '10', worktime13_title = '미용4', worktime13_disp_yn = 'y',worktime14 = '10', worktime14_title = '미용5', worktime14_disp_yn = 'y', reg_dt = NOW()");
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyPartDog_modify $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyPartDog_modify(
	dataPartnerId VARCHAR(64),
    dataUpdateQry VARCHAR(4096),
    dataInsertQry VARCHAR(4096)
)
BEGIN
	/**
		강아지 미용구분 저장  
   */
    
    SET @qry = '';
    SET @cnt = 0;

    SELECT COUNT(*) INTO @cnt 
    FROM tb_product_dog_worktime 
    WHERE artist_id = dataPartnerId;
    
    IF @cnt > 0 THEN
		SET @qry = dataUpdateQry;
	ELSE
		SET @qry = dataInsertQry;
	END IF;
    
    call procPartnerPC_QryToExcute(1, @qry);
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyPartDog_delete $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyPartDog_delete(
    dataUpdateQry VARCHAR(4096)
)
BEGIN
	/**
		강아지 미용구분 삭제  
   */
    
    call procPartnerPC_QryToExcute(1, dataUpdateQry);
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_QryToExcute $$
CREATE PROCEDURE procPartnerPC_QryToExcute(
	dataQryType INT, # 0: SELECT, 1: INSERT, UPDATE, DELETE
	dataSQL VARCHAR(4096)
)
BEGIN
	/**
		쿼리 문자열 실행 
        dataQryType INT - 0: SELECT, 1: INSERT, UPDATE, DELETE
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    IF dataQryType = 0 THEN
    BEGIN
		SET @SQL_STR = dataSQL;
		PREPARE stmt FROM @SQL_STR;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;  
    END;
    ELSE
    BEGIN
		START TRANSACTION;
     
		SET @SQL_STR = dataSQL;
		PREPARE stmt FROM @SQL_STR;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;  
		IF aErr < 0 THEN
			ROLLBACK;
		ELSE
			COMMIT;
		END IF;
        
        SELECT aErr AS err;   
    END;
    END IF;
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyAddOptionDog_modify $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyAddOptionDog_modify(
	dataPartnerId VARCHAR(64),
    dataFirstType VARCHAR(10),
    dataSecondType VARCHAR(32),
    dataDirect VARCHAR(64),
    dataUpdateQry VARCHAR(4096),
    dataInsertQry VARCHAR(4096)
)
BEGIN
	/**
		강아지 미용 추가 옵션  
   */
    
    SET @qry = '';
    SET @cnt = 0;
    
    IF dataDirect = '' THEN
		SELECT COUNT(*) INTO @cnt 
		FROM tb_product_dog_static 
		WHERE customer_id = dataPartnerId 
			AND first_type = dataFirstType 
			AND second_type = dataSecondType;    
    ELSE
		SELECT COUNT(*) INTO @cnt 
		FROM tb_product_dog_static 
		WHERE customer_id = dataPartnerId 
			AND first_type = dataFirstType 
			AND second_type = dataSecondType 
			AND direct_title = dataDirect;
	END IF;

    
    IF @cnt > 0 THEN
		SET @qry = dataUpdateQry;
	ELSE
		SET @qry = dataInsertQry;
	END IF;
    
    call procPartnerPC_QryToExcute(1, @qry);
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyAddOptionKind_get $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyAddOptionKind_get(
	dataPartnerID VARCHAR(64),
    dataFirstType VARCHAR(10)
)
BEGIN
	/**
		강아지 미용 추가 옵션 미용 분류 조회( 소형견 미용 , 중형견 미용 등) 
   */
    
	SELECT DISTINCT(IF(second_type='기타공통','추가공통옵션',second_type)) AS second_type
    FROM tb_product_dog_static 
	WHERE customer_id = dataPartnerId AND first_type = dataFirstType;
    
END $$ 
DELIMITER ;
	SELECT *
    FROM tb_product_dog_static 
	WHERE customer_id = 'eaden@peteasy.kr'
		AND first_type =  '개' 
        AND second_type = '소형견미용';


call procPartnerPC_Setting_BeautyAddOption_get('eaden@peteasy.kr', '개','소형견미용');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyAddOption_get $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyAddOption_get(
	dataPartnerID VARCHAR(64),
    dataFirstType VARCHAR(10),
    dataSecondType VARCHAR(32)
)
BEGIN
	/**
		미용 구분 조회 
   */
    
	SELECT *
    FROM tb_product_dog_static 
	WHERE customer_id = dataPartnerID
		AND first_type = dataFirstType 
        AND second_type = dataSecondType;
    
END $$ 
DELIMITER ;


call procPartnerPC_Setting_BeautyPartTimeDog_put('eaden@peteasy.kr', '개','소형견미용');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyPartTimeDog_put $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyPartTimeDog_put(
	dataPartnerID VARCHAR(64),
    dataTime1 INT,
    dataTime2 INT,
    dataTime3 INT,
    dataTime4 INT,
    dataTime5 INT,
    dataTime6 INT,
    dataTime7 INT,
    dataTime8 INT,
    dataTime9 INT,
    dataTime10 INT,
    dataTime11 INT,
    dataTime12 INT,
    dataTime13 INT,
    dataTime14 INT
)
BEGIN
	/**
		미용 구분 조회 
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    UPDATE tb_product_dog_worktime 
    SET worktime1 = CONCAT(dataTime1), worktime2 = CONCAT(dataTime2), worktime3 = CONCAT(dataTime3), 
		worktime4 = CONCAT(dataTime4), worktime5 = CONCAT(dataTime5), worktime6 = CONCAT(dataTime6), 
        worktime7 = CONCAT(dataTime7), worktime8 = CONCAT(dataTime8), worktime9 = CONCAT(dataTime9), 
        worktime10 = CONCAT(dataTime10), worktime11 = CONCAT(dataTime11), worktime12 = CONCAT(dataTime12), 
        worktime13 = CONCAT(dataTime13), worktime14 = CONCAT(dataTime14), update_dt = NOW()  
    WHERE artist_id = dataPartnerID; 
    
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

call procPartnerPC_Setting_Shop_Vat_get('eaden@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Shop_Vat_get $$
CREATE PROCEDURE procPartnerPC_Setting_Shop_Vat_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		부가세 설정
   */
	
    SELECT is_vat 
    FROM tb_shop
	WHERE customer_id = dataPartnerID;
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Shop_Vat_put $$
CREATE PROCEDURE procPartnerPC_Setting_Shop_Vat_put(
	dataPartnerID VARCHAR(64),
    dataVat INT
)
BEGIN
	/**
		부가세 설정
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    UPDATE tb_shop 
    SET is_vat = dataVat 
    WHERE customer_id = dataPartnerID; 
    
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

#==============================
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyAddOptionEtcDog_modify $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyAddOptionEtcDog_modify(
	dataPartnerId VARCHAR(64),
    dataFirstType VARCHAR(10),
    dataSecondType VARCHAR(32),
    dataUpdateQry VARCHAR(4096),
    dataInsertQry VARCHAR(4096)
)
BEGIN
	/**
		강아지 미용 추가 옵션  
   */
    
    SET @qry = '';
    SET @cnt = 0;
    
	SELECT COUNT(*) INTO @cnt 
	FROM tb_product_dog_common 
	WHERE customer_id = dataPartnerId 
		AND first_type = dataFirstType 
		AND second_type = dataSecondType;    

    
    IF @cnt > 0 THEN
		SET @qry = dataUpdateQry;
	ELSE
		SET @qry = dataInsertQry;
	END IF;
    
    call procPartnerPC_QryToExcute(1, @qry);
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyAddOptionEtcDog_delete $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyAddOptionEtcDog_delete(
	dataPartnerId VARCHAR(64),
    dataFirstType VARCHAR(10)  
)
BEGIN
	/**
		강아지 미용 추가 옵션 삭제
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
	DELETE FROM tb_product_dog_common WHERE customer_id = dataPartnerId AND first_type = dataFirstType AND second_type = '추가공통옵션';
	DELETE FROM tb_product_common_option WHERE customer_id = dataPartnerId AND type = '목욕';
	 
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

#=======================
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyCommonOption_delete $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyCommonOption_delete(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		목욕 추가 옵션 삭제
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
	DELETE FROM tb_product_common_option WHERE customer_id = dataPartnerId AND type = '목욕'; 


	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

call procPartnerPC_Setting_BeautyCommonOption_post('eaden@peteasy.kr','오중모','10');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyCommonOption_post $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyCommonOption_post(
	dataPartnerId VARCHAR(64),
    dataBathTitle VARCHAR(64),
    dataBathPrice VARCHAR(12)
)
BEGIN
	/**
		목욕 추가 옵션 추가 
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	INSERT INTO tb_product_common_option 
    SET customer_id = dataPartnerId, type = '목욕', price = dataBathPrice, title = dataBathTitle, reg_date = NOW();

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_Coupon_post $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_Coupon_post(
	dataPartnerId VARCHAR(64),
    dataProductType CHAR(1),
	dataType CHAR(1),
    dataCouponName VARCHAR(32),
    dataGiven VARCHAR(12),
    dataPrice VARCHAR(12)
)
BEGIN
	/**
		쿠폰 추가 
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	INSERT INTO tb_coupon 
	SET customer_id     = dataPartnerId, 
		product_type    = dataProductType, 
		type            = dataType, 
		name            = dataCouponName, 
		given           = dataGiven, 
		price           = dataPrice, 
		reg_date        = NOW();

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_Coupon_put $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_Coupon_put(
	dataIdx INT,
    dataPartnerId VARCHAR(64),
    dataProductType CHAR(1),
	dataType CHAR(1),
    dataCouponName VARCHAR(32),
    dataGiven VARCHAR(12),
    dataPrice VARCHAR(12)
)
BEGIN
	/**
		쿠폰 수정 
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	UPDATE tb_coupon 
	SET customer_id     = dataPartnerId, 
		product_type    = dataProductType, 
		type            = dataType, 
		name            = dataCouponName, 
		given           = dataGiven, 
		price           = dataPrice, 
		update_date     = NOW()  
	WHERE coupon_seq = dataIdx;

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_Coupon_delete $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_Coupon_delete(
	dataIdx INT
)
BEGIN
	/**
		쿠폰 삭제  
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	UPDATE tb_coupon SET del_yn = 'Y'
	WHERE coupon_seq = dataIdx;

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

#======
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_CouponMemo_post $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_CouponMemo_post(
	dataPartnerID VARCHAR(64),
	dataCouponMemo TEXT,
    dataFlatMemo TEXT
)
BEGIN
	/**
		쿠폰 메모 추가 
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	INSERT INTO tb_coupon_memo 
	SET customer_id = dataPartnerID , 
		coupon_memo = dataCouponMemo,
		flat_memo = dataFlatMemo, 
		reg_date = NOW();

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

select * from tb_coupon_memo where customer_id = 'eaden@peteasy.kr';

call procPartnerPC_Setting_Beauty_CouponMemo_put(153,'eadenpeteasy.kreaden@peteasy.kr', 'test', 'test');
	UPDATE tb_coupon_memo 
	SET customer_id = dataPartnerID , 
		coupon_memo = dataCouponMemo,
		flat_memo = dataFlatMemo, 
		update_date = NOW() 
	WHERE coupon_seq = dataIdx;
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_CouponMemo_put $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_CouponMemo_put(
	dataIdx INT,
    dataPartnerId VARCHAR(64),
	dataCouponMemo TEXT,
    dataFlatMemo TEXT
)
BEGIN
	/**
		쿠폰메모 수정 
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	UPDATE tb_coupon_memo 
	SET customer_id = dataPartnerID , 
		coupon_memo = dataCouponMemo,
		flat_memo = dataFlatMemo, 
		update_date = NOW() 
	WHERE memo_seq = dataIdx;

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

#===========
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_StoreGoods_delete $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_StoreGoods_delete(
    dataPartnerId VARCHAR(64),
	dataKind VARCHAR(2)
)
BEGIN
	/**
		매장 상품 해당 종류 삭제
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	DELETE FROM tb_product_dog_etc WHERE customer_id = dataPartnerId AND product_kind = dataKind;

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Beauty_StoreGoods_post $$
CREATE PROCEDURE procPartnerPC_Setting_Beauty_StoreGoods_post(
    dataPartnerId VARCHAR(64),
	dataKind VARCHAR(2),
    dataName VARCHAR(256),
    dataPrice VARCHAR(12)
)
BEGIN
	/**
		매장 상품 해당 종류 삭제 후 추가
   */
    
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	INSERT INTO tb_product_dog_etc 
	SET customer_id    = dataPartnerId, 
		product_kind   = dataKind, 
		name           = dataName, 
		price          = dataPrice, 
		update_time    = NOW();

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
    
END $$ 
DELIMITER ;

