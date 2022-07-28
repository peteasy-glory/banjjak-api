/*
###################################################################################
####################                오늘의 메세지.                ####################
###################################################################################
*/
DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayCustomerMessage_get $$
CREATE PROCEDURE procTodayCustomerMessage_get(
		dataCustomerId VARCHAR(64),
        dataTestIdx INT
)
BEGIN
	/**
		고객 오늘의 메시지 조회하기
   */
    DECLARE aPet VARCHAR(64);

	SELECT name INTO aPet FROM tb_mypet 
    WHERE data_delete = 0 
		AND customer_id = dataCustomerId AND (name IS NOT NULL OR name != '')
    ORDER BY pet_seq DESC LIMIT 1;
    
    IF dataTestIdx = 0 THEN
		SELECT aPet, B.idx,  A.msg_idx, B.message, B.icon, B.image, B.link 
		FROM tb_today_mgr A 
			INNER JOIN tb_today_msg B ON A.msg_idx = B.idx 
		WHERE A.is_delete < 1 AND NOW() > A.st_date AND NOW() < A.fi_date 
			AND A.customer_id = dataCustomerId 
		ORDER BY A.ord ASC LIMIT 1;
    ELSE
		SELECT aPet, B.idx,  A.msg_idx, B.message, B.icon, B.image, B.link 
		FROM tb_today_mgr A 
			INNER JOIN tb_today_msg B ON A.msg_idx = B.idx 
		WHERE A.is_delete < 1 AND NOW() > A.st_date AND NOW() < A.fi_date 
			AND A.customer_id = dataCustomerId AND A.msg_idx = dataTestIdx
		ORDER BY A.ord ASC LIMIT 1;
    END IF;
END
;

DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayMessage_get $$
CREATE PROCEDURE procTodayMessage_get(
)
BEGIN
	/**
		오늘의 메시지 전체 조회하기
   */
   
		SELECT id INTO aExistId 
		FROM tb_today_msg 
		WHERE is_delete < 1 
		ORDER BY idx DESC;
END
;

DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayMessage_post $$
CREATE PROCEDURE procTodayMessage_post(
	dataType INT,
    dataMessage VARCHAR(1024),
    dataIcon VARCHAR(256),
    dataImage VARCHAR(256),
    dataLink VARCHAR(256)
)
BEGIN
	/**
		오늘의 메시지 추가하기
   */
	DECLARE aLastId INT DEFAULT 0;
	DECLARE aErr INT DEFAULT '0';
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
	INSERT INTO tb_today_msg (message, type, link, icon, image) 
    VALUES(dataMessage, dataType, dataLink, dataIcon, dataImage);
	SET aLastId = LAST_INSERT_ID();

	IF aErr < 0 THEN
	BEGIN
		ROLLBACK;
		SELECT aErr;
	END;
    ELSE
    BEGIN
		COMMIT;
		SELECT aLastId;
    END;
    END IF;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayMessage_put $$
CREATE PROCEDURE procTodayMessage_put(
	dataIdx INT,
	dataType INT,
    dataMessage VARCHAR(1024),
    dataIcon VARCHAR(256),
    dataImage VARCHAR(256),
    dataLink VARCHAR(256)
)
BEGIN
	/**
		오늘의 메시지 수정하기
   */
	DECLARE aErr INT DEFAULT '0';
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
	UPDATE tb_today_msg 
    SET message=dataMessage, type=dataType, link=dataLink, icon=dataLink, image=dataImage
    WHERE idx = dataIdx;
    
	IF aErr < 0 THEN
	BEGIN
		ROLLBACK;
		SELECT aErr;
	END;
    ELSE
    BEGIN
		COMMIT;
		SELECT dataIdx;
    END;
    END IF;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayCustomerMessage_post $$
CREATE PROCEDURE procTodayCustomerMessage_post(
	dataId VARCHAR(64),
    dataMsgIdx INT,
    dataSt DATETIME,
    dataFi DATETIME
)
BEGIN
	/**
		고객용 오늘의 메시지 추가하기
   */
	DECLARE aLastId INT DEFAULT 0;
	DECLARE aLastOrd INT DEFAULT 9;
	DECLARE aErr INT DEFAULT '0';
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
    /*
    SELECT ord INTO aLastOrd
    FROM tb_today_mgr 
    WHERE customer_id=dataId
		AND is_delete < 1
	ORDER BY ord DESC LIMIT 1;
    
    IF aLastOrd != '' THEN
		SET aLastOrd = aLastOrd + 1;
	ELSE
		SET aLastOrd = 1;
	END IF;
    */

	INSERT INTO tb_today_mgr (customer_id, msg_idx, ord, st_date, fi_date)
    VALUES(dataId, dataMsgIdx, aLastOrd, dataSt, dataFi);
	SET aLastId = LAST_INSERT_ID();
    
	IF aErr < 0 THEN
	BEGIN
		ROLLBACK;
		SELECT aErr;
	END;
    ELSE
    BEGIN
		COMMIT;
		SELECT aLastId;
    END;
    END IF;
END
;
DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayCustomerMessage_put $$
CREATE PROCEDURE procTodayCustomerMessage_put(
	dataIdx INT,
    dataMsgIdx INT,
    dataOrd INT,
    dataSt DATETIME,
    dataFi DATETIME
)
BEGIN
	/**
		고객용 오늘의 메시지 수정하기
   */
	DECLARE aId VARCHAR(128);
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
    SELECT customer_id INTO aId FROM tb_today_mgr WHERE idx = dataIdx;
	UPDATE tb_today_mgr 
    SET ord = 9
    WHERE customer_id = aId;

	UPDATE tb_today_mgr 
    SET msg_idx = dataMsgIdx, ord=dataOrd, st_date=dataSt, fi_date=dataFi
    WHERE idx = dataIdx;

	IF aErr < 0 THEN
	BEGIN
		ROLLBACK;
		SELECT aErr;
	END;
    ELSE
    BEGIN
		COMMIT;
		SELECT dataIdx;
    END;
    END IF;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procTodayCustomerMessage_del $$
CREATE PROCEDURE procTodayCustomerMessage_del(
	dataIdx INT
)
BEGIN
	/**
		고객용 오늘의 메시지 수정하기
   */
	DECLARE aErr INT DEFAULT '0';
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
	UPDATE tb_today_mgr 
    SET is_delete = 1
    WHERE idx = dataIdx;
    
	IF aErr < 0 THEN
	BEGIN
		ROLLBACK;
		SELECT aErr;
	END;
    ELSE
    BEGIN
		COMMIT;
		SELECT dataIdx;
    END;
    END IF;
END
select * from tb_customer where id = 'pettester@peteasy.kr';
call procPartnerPC_LogIn_get('pettester@peteasy.kr', 'fz4dQ1cSrPJlRixIYlofg9lopSam/BmlhhnJFNNKUHs=');
	SELECT password, usr_name , nickname, artist_flag , my_shop_flag #INTO aPw, aName, aNick, aFlag, aMyShop
    FROM tb_customer
	WHERE enable_flag = 1
		AND id = 'pettester@peteasy.kr';
/*
###################################################################################
################################         PC 버전         ###########################
###################################################################################
*/
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_LogIn_get $$
CREATE PROCEDURE procPartnerPC_LogIn_get(
		dataId VARCHAR(64),
        dataPw VARCHAR(64)
)
	/**
		로그인 하기
   */
BODY : BEGIN 
   DECLARE aPw VARCHAR(128) DEFAULT '';
   DECLARE aNick VARCHAR(128) DEFAULT '';
   DECLARE aFlag INT DEFAULT 0;
   DECLARE aName VARCHAR (64) DEFAULT '';
   DECLARE aMyShop INT DEFAULT 0;
   DECLARE aErr INT DEFAULT 0;
   DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
   
	SELECT password, usr_name , nickname, artist_flag , my_shop_flag INTO aPw, aName, aNick, aFlag, aMyShop
    FROM tb_customer
	WHERE enable_flag = 1
		AND id = dataId;
    select aPW;
    IF aPw = '' THEN 
	BEGIN
		SELECT aErr AS Err, 1 AS Ret, aName AS Name, aMyShop AS isMyShop;
        LEAVE BODY;
    END;
    END IF;
    
    IF aFlag = 1 THEN
		SELECT name INTO aName FROM tb_shop_artist WHERE artist_id = dataId AND del_yn = 'N' LIMIT 1;
    END IF;
    
	START TRANSACTION;
    
-- 	UPDATE tb_customer 
--     SET last_login_time = NOW(), last_applogin_time=now() 
-- 	WHERE id = dataId AND nickname = aNick;

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
    SELECT aErr AS Err, 0 AS Ret, aName AS Name, aMyShop AS isMyShop;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Artist_get $$
CREATE PROCEDURE procPartnerPC_Artist_get(
		dataId VARCHAR(64),
        dataNick VARCHAR(64)
)
BEGIN
	/**
		로그인한 종업원 정보 조회 하기
   */
   
		UPDATE tb_customer SET
			last_login_time = NOW(),
			last_applogin_time=now() 
		WHERE id = 'pettester@peteasy.kr'
			AND nickname = 'pet_tester'
			
	SELECT *  
    FROM tb_customer
	WHERE enable_flag = 1 
		AND id = dataId;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_LogOut_get $$
CREATE PROCEDURE procPartnerPC_LogOut_get(
		dataId VARCHAR(64)
)
BEGIN
	/**
		로그아웃 하기
   */

END

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Is_Exist_Id_get $$
CREATE PROCEDURE procPartnerPC_Is_Exist_Id_get(
		dataId VARCHAR(64)
)
BEGIN
	/**
		아이디 중복 체크
   */
	SELECT COUNT(*) 
    FROM tb_customer
	WHERE enable_flag = 1 
		AND id = dataId;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Is_Exist_Phone_get $$
CREATE PROCEDURE procPartnerPC_Is_Exist_Phone_get(
		dataPhone VARCHAR(20)
)
BEGIN
	/**
		전화번호 중복 체크
   */
	SELECT COUNT(*) 
    FROM tb_customer
	WHERE enable_flag = 1 
		AND cellphone = dataPhone;
END

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Join_post $$
CREATE PROCEDURE procPartnerPC_Join_post(
		dataId VARCHAR(64),
        dataPw VARCHAR(128),
        dataNick VARCHAR(64),
        dataPhone VARCHAR(32)
)
BEGIN
	/**
		파트너 회원가입
   */
    DECLARE aLastId INT DEFAULT 0;
	DECLARE aExistId INT DEFAULT 0;
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*) INTO aExistId 
    FROM tb_customer
	WHERE enable_flag = 0 
		AND id = dataId;
    
	IF aExistId > 0 THEN
		SELECT aExistId as ret, -2 as err;
	ELSE
    BEGIN
		START TRANSACTION;
        
        INSERT INTO tb_customer (id, password,nickname,last_login_time,registration_time,push_option, cellphone) 
        VALUES (dataId, dataPw, dataNick, NOW(), NOW(), 1, dataPhone);
		#SET aLastId = LAST_INSERT_ID(); -- NO Autoincrease Index
        UPDATE tb_payment_log SET customer_id = dataId WHERE cellphone = dataPhone AND (customer_id IS NULL OR customer_id = '');
        UPDATE tb_mypet SET customer_id = dataId, tmp_yn = 'N', tmp_seq = NULL WHERE tmp_seq IN (SELECT tmp_seq FROM tb_tmp_user WHERE cellphone = dataPhone);
        UPDATE tb_user_coupon SET customer_id = dataId, tmp_seq = NULL WHERE tmp_seq IN (SELECT tmp_seq FROM tb_tmp_user WHERE cellphone = dataPhone);
        UPDATE tb_coupon_history SET customer_id = dataId, tmp_seq = NULL WHERE tmp_seq IN (SELECT tmp_seq FROM tb_tmp_user WHERE cellphone = dataPhone);
        DELETE FROM tb_tmp_user WHERE tmp_seq IN (SELECT tmp_seq FROM (SELECT tmp_seq FROM tb_tmp_user WHERE cellphone = dataPhone) As Sub);
        IF aErr < 0 THEN
			ROLLBACK;
		ELSE
			COMMIT;
		END IF;
		SELECT aLastId as ret, aErr as err;
    END;
    END IF;
END

   
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Artist_get $$
CREATE PROCEDURE procPartnerPC_Setting_Artist_get(
		dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		파트너 미용사 권한 설정하기
   */
	SELECT artist_seq, artist_id, name 
    FROM tb_shop_artist
	WHERE customer_id = dataPartnerId AND del_yn = 'N' 
    ORDER BY artist_seq DESC;
END

select * from tb_shop_artist
where customer_id='pettester@peteasy.kr'


				SELECT 
					  *
					, GROUP_CONCAT(week ORDER BY week ASC) week_list
					, GROUP_CONCAT(time_start ORDER BY seq ASC) time_start_list
					, GROUP_CONCAT(time_end ORDER BY seq ASC) time_end_list
					, GROUP_CONCAT(seq) as seq_list /*20210607 by migo - 출력순서 조정용*/
				FROM tb_artist_list
				WHERE artist_id = 'eaden@peteasy.kr'
				GROUP BY name
	            ORDER BY sequ_prnt asc, is_main DESC, nicname ASC
                
                
				SELECT * 
				FROM tb_regular_holiday 
				WHERE customer_id = 'eaden@peteasy.kr'
			
            
				SELECT * 
				FROM tb_working_schedule 
				WHERE customer_id = 'eaden@peteasy.kr'
			
            
			
select * from tb_customer where id like 'hptop%';