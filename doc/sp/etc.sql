

call procPartnerPC_Etc_OneOnOneInquiry_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Etc_OneOnOneInquiry_get $$
CREATE PROCEDURE procPartnerPC_Etc_OneOnOneInquiry_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		1대1 문의하기 조회
   */
	SELECT A.*, B.sub_seq, B.body, B.update_time 
	FROM tb_1vs1_pna A LEFT JOIN tb_1vs1_pna_sub B ON A.id = B.qna_id
	WHERE A.customer_id = dataPartnerID
	ORDER BY A.update_time DESC;
END $$ 
DELIMITER ;

call procPartnerPC_Etc_OneOnOneInquiry_post('pettester@peteasy.kr','eaden@peteasy.kr','오류/장애','','테스트','1.테스트 2.테스트');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Etc_OneOnOneInquiry_post $$
CREATE PROCEDURE procPartnerPC_Etc_OneOnOneInquiry_post(
	dataPartnerID VARCHAR(64),
    dataEmail VARCHAR(64),
    dataMainType VARCHAR(64),
    dataSubType VARCHAR(64),
    dataTitle VARCHAR(256),
    dataBody TEXT
)
BEGIN
	/**
		1대1 문의하기 
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;
    
	SELECT uuid() INTO @uuid;
	INSERT INTO tb_1vs1_pna (id, customer_id, email, title, request_main_type, request_sub_type, body) 
	VALUES (@uuid,dataPartnerID,dataEmail,dataTitle,dataMainType,dataSubType,dataBody);
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

END $$ 
DELIMITER ;


call procPartnerPC_Etc_Notice_get();
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Etc_Notice_get $$
CREATE PROCEDURE procPartnerPC_Etc_Notice_get(
)
BEGIN
	/**
		공지 사항 조회
   */
	SELECT * 
	FROM tb_admin_notice 
	WHERE is_main ='1' AND is_delete = '0' 
	ORDER BY notice_seq DESC;
    
END $$ 
DELIMITER ;


call procPartnerPC_Etc_Resign_put('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Etc_Resign_put $$
CREATE PROCEDURE procPartnerPC_Etc_Resign_put(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		회원 탈퇴하기
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;
    
	UPDATE tb_customer
	SET enable_flag = 0
	WHERE id = dataPartnerID;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

END $$ 
DELIMITER ;

######

call procPartnerPC_Etc_Password_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Etc_Password_get $$
CREATE PROCEDURE procPartnerPC_Etc_Password_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		비밀번호 조회 하기 
   */
	SELECT password
	FROM tb_customer
	WHERE id = 'pettester@peteasy.kr';
    
END $$ 
DELIMITER ;


call procPartnerPC_Etc_Password_put('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Etc_Password_put $$
CREATE PROCEDURE procPartnerPC_Etc_Password_put(
	dataPartnerID VARCHAR(64),
    dataPassword VARCHAR(256)
)
BEGIN
	/**
		회원 탈퇴하기
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;
    
	UPDATE tb_customer
	SET password = dataPassword
	WHERE id = dataPartnerID;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

END $$ 
DELIMITER ;