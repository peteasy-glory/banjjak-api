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

UPDATE tb_shop SET is_time_type = '1' WHERE customer_id = 'pettester@peteasy.kr'
call procPartnerPC_Setting_Time_Limit_modify (3333, 'pettester@peteasy.kr', 'pettester1@peteasy.kr', '09:00~10:30');

select * from tb_time_schedule 
where artist_id = 'pettester@peteasy.kr'


select * from tb_time_schedule
where artist_id = 'pettester@peteasy.kr'
;

select * from tb_time_off
where customer_id = 'pettester@peteasy.kr'
;


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

SELECT * FROM tb_time_off
where customer_id = 'pettester@peteasy.kr';

select * From tb_shop
where customer_id = 'pettester@peteasy.kr'
;

select * From tb_artist_list
where artist_id = 'pettester@peteasy.kr'
;

select * from tb_time_schedule
where artist_id = 'pettester@peteasy.kr'
;



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
call procPartnerPC_Setting_BeautyPart_put('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_BeautyPart_put $$
CREATE PROCEDURE procPartnerPC_Setting_BeautyPart_put(
	dataPartnerId VARCHAR(64),
    dataPart CHAR(14),
    dataOne VARCHAR(32
    dataFix1 INT
    dataFix1 INT
    dataFix1 INT
    dataFix1 INT
)
BEGIN
	/**
		미용구분 저장  
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

