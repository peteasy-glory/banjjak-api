
call procPartnerPC_Booking_BeautyPeroid_get('eaden@peteasy.kr', '2022-07-01', '2022-07-10');
#call procPartnerPC_Booking_BeautyBookingPeroid_get(\'eaden@peteasy.kr\', \'2022-07-02\', \'2022-07-20\')
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_BeautyPeroid_get $$
CREATE PROCEDURE procPartnerPC_Booking_BeautyPeroid_get(
	dataPartnerId VARCHAR(64),
    dataStDate VARCHAR(10), # format yyyy-mm-dd
    dataFiDate VARCHAR(10)  # format yyyy-mm-dd
)
BEGIN
	/**
		미용 예약 현황 기간으로 검색 
   */
   
	SELECT A.*, B.pet_seq, B.tmp_seq, B.name, B.type, B.pet_type, C.is_approve FROM 
	(
		SELECT * FROM gobeautypet.tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId
	) A LEFT JOIN (SELECT * FROM tb_mypet WHERE data_delete = 0) B ON A.pet_seq = B.pet_seq 
    LEFT JOIN (SELECT * FROM tb_grade_reserve_approval_mgr WHERE is_delete = 0) C ON A.payment_log_seq = C.payment_log_seq
	WHERE gobeautypet.funcYMDToDate(A.year, A.month, A.day) >= dataStDate AND
		gobeautypet.funcYMDToDate(A.year, A.month, A.day) < dataFiDate;
END $$ 
DELIMITER ;


call procPartnerPC_Booking_BeautyPeroid_get('eaden@peteasy.kr', '2022-07-01', '2022-07-10');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_BeautyPeroid_get $$
CREATE PROCEDURE procPartnerPC_Booking_BeautyPeroid_get(
	dataPartnerId VARCHAR(64),
    dataStDate VARCHAR(10), # format yyyy-mm-dd
    dataFiDate VARCHAR(10)  # format yyyy-mm-dd
)
BEGIN
	/**
		작업 관리 
   */
   
	SELECT A.*, B.pet_seq, B.tmp_seq, B.name, B.type, B.pet_type, C.is_approve FROM 
	(
		SELECT * FROM gobeautypet.tb_payment_log 
		WHERE data_delete = 0 AND artist_id = dataPartnerId
	) A LEFT JOIN (SELECT * FROM tb_mypet WHERE data_delete = 0) B ON A.pet_seq = B.pet_seq 
    LEFT JOIN (SELECT * FROM tb_grade_reserve_approval_mgr WHERE is_delete = 0) C ON A.payment_log_seq = C.payment_log_seq
	WHERE gobeautypet.funcYMDToDate(A.year, A.month, A.day) >= dataStDate AND
		gobeautypet.funcYMDToDate(A.year, A.month, A.day) < dataFiDate;
END $$ 
DELIMITER ;

 	SELECT GROUP_CONCAT(CONCAT(family_seq,'|',from_cellphone,'|',from_customer_id,'|',from_nickname)) #INTO aSubPhone 
    FROM tb_customer_family 
	WHERE to_cellphone = '01086331776'  AND artist_id = 'pettester@peteasy.kr' AND is_delete = 0;
    
call procPartnerPC_Booking_CustomerPetInfo_get(568668);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_CustomerPetInfo_get $$
CREATE PROCEDURE procPartnerPC_Booking_CustomerPetInfo_get(
	dataPaymentCode INT
)
BEGIN
	/**
		예약자 정보
   */
	DECLARE aCustomerId VARCHAR(64) DEFAULT '';
	DECLARE aPartnerId VARCHAR(64) DEFAULT '';
    DECLARE aPhone VARCHAR(20) DEFAULT '';
    DECLARE aSubPhone VARCHAR(1024) DEFAULT '';
    DECLARE aTmpId VARCHAR(12) DEFAULT '';
    DECLARE aCustomerGradeIdx INT DEFAULT 0;
    DECLARE aShopGradeIdx  INT DEFAULT 0;
    DECLARE aGradeName VARCHAR(64) DEFAULT '';
    DECLARE aGradeOrd  INT DEFAULT 0;
    DECLARE aOwnerMemo TEXT DEFAULT '';
    DECLARE aMemo TEXT DEFAULT '';
    DECLARE aPetMemo TEXT DEFAULT '';
    DECLARE aPetId TEXT DEFAULT '';
        
     # 회원아이디 가져오기    
    SELECT customer_id, artist_id , cellphone, pet_seq, etc_memo INTO aCustomerId, aPartnerId, aPhone , aPetId, aMemo
    FROM tb_payment_log 
	WHERE payment_log_seq = dataPaymentCode;

	#보조연락처 가져오기
 	SELECT GROUP_CONCAT(CONCAT(family_seq,'|',from_cellphone,'|',from_customer_id,'|',from_nickname)) INTO aSubPhone 
    FROM tb_customer_family 
	WHERE to_cellphone = aPhone  AND artist_id = aPartnerId AND is_delete = 0;
   
	#가회원인경우 임시 아이디 가져오기
	IF TRIM(aCustomerId) = '' OR aCustomerId IS NULL THEN
		SELECT tmp_seq INTO aTmpId FROM tb_tmp_user
        WHERE cellphone = aPhone AND data_delete = 0;
    END IF;
    
    #등급 가져오기
	SELECT a.idx, a.grade_idx, b.grade_name, b.grade_ord INTO aCustomerGradeIdx, aShopGradeIdx, aGradeName, aGradeOrd
    FROM tb_grade_of_customer a 
		LEFT JOIN tb_grade_of_shop b ON a.grade_idx = b.idx 
    WHERE a.customer_id = aTmpId AND b.artist_id = aPartnerId AND a.is_delete = 0 AND b.is_delete = 0;
    
    IF LENGTH(aGradeName) < 1 then
		# 등급이 없으면 해당샵 2번째 등급 부여 
		SELECT grade_name , grade_ord INTO aGradeName, aGradeOrd 
        FROM tb_grade_of_shop WHERE artist_id = aPartnerId AND grade_ord = 2 ORDER BY grade_ord ASC;
    END IF;

	# 견주 메모 가져오기
    IF LENGTH(TRIM(aCustomerId)) < 1 THEN
		SELECT memo INTO aOwnerMemo FROM tb_shop_customer_memo 
		WHERE tmp_seq = aTmpId AND cellphone = aPhone AND artist_id = aPartnerId;
	ELSE
		SELECT memo INTO aOwnerMemo FROM tb_shop_customer_memo 
		WHERE customer_id = aCustomerId AND cellphone = aPhone AND artist_id = aPartnerId;
    END IF;

	SELECT aCustomerId AS customer_Id, aTmpId AS tmp_id, aPartnerId AS partner_id, 
		   aPhone AS cell_phone, aSubPhone AS sub_phone, 
           aCustomerGradeIdx AS customer_grade_idx,  aShopGradeIdx AS shop_grade_idx, aGradeName AS grade_name, aGradeOrd AS grade_ord, 
           aOwnerMemo AS owner_memo,
		#예약 펫 정보
		pet_seq, name, name_for_owner, type, pet_type, gender, weight, photo, CONCAT(year,'-',LPAD(month,2,0),'-',LPAD(day,2,0)) AS birth, neutral, etc,
		beauty_exp, vaccination, dermatosis, heart_trouble, marking, mounting #미용경험, 예방접종, 피부병, 심장질환, 마킹, 마운팅 
	FROM tb_mypet WHERE pet_seq = aPetId;

END $$ 
DELIMITER ;

call procPartnerPC_Booking_BeforePaymentInfo_get(518235, True, 10);
call procPartnerPC_Booking_BeforePaymentInfo_get(518235, false, 10);
call procPartnerPC_Booking_BeforePaymentInfo_get(568668, true, 10);
call procPartnerPC_Booking_BeforePaymentInfo_get(568668, false, 10);
            
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_BeforePaymentInfo_get $$
CREATE PROCEDURE procPartnerPC_Booking_BeforePaymentInfo_get(
	dataPaymentCode INT,
    dataIsBeauty BOOL,
    dataGetCount INT
)
BEGIN
	/**
		이전 내용
   */
	DECLARE aPartnerId VARCHAR(64) DEFAULT '';
    DECLARE aDate VARCHAR(20) DEFAULT '';
    DECLARE aPetId INT DEFAULT 0;
    
    SELECT pet_seq, artist_id, CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
							' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) INTO aPetId, aPartnerId, aDate
    FROM tb_payment_log 
    WHERE payment_log_seq = dataPaymentCode;
    
    IF dataIsBeauty = FALSE THEN   
		SELECT *, CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
								' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) AS booking
		FROM tb_payment_log 
		WHERE artist_id = aPartnerId 
			#AND is_no_show = 0 
			#AND is_cancel = 0 
			AND data_delete = 0
			AND approval = 1
			AND etc_memo != ''
			AND pet_seq = aPetId   
			AND CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
								' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) < aDate 
			ORDER BY  CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
								' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) DESC
			LIMIT dataGetCount;
	ELSE
		SELECT *, CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
								' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) AS booking
		FROM tb_payment_log 
		WHERE artist_id = aPartnerId 
			#AND is_no_show = 0 
			#AND is_cancel = 0 
			AND data_delete = 0
			AND approval = 1
			AND pet_seq = aPetId   
			AND CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
								' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) < aDate 
			ORDER BY  CONCAT(year,'-', LPAD(month, 2, 0),'-', LPAD(day, 2, 0), 
								' ', LPAD(hour, 2, 0),':', LPAD(minute, 2, 0)) DESC
			LIMIT dataGetCount;
    END IF;
END $$ 
DELIMITER ;

call procPartnerPC_Booking_NoShow_put(568420, false);
call procPartnerPC_Booking_PaymentInfo_get(568420);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PaymentInfo_get $$
CREATE PROCEDURE procPartnerPC_Booking_PaymentInfo_get(
	dataPaymentIdx INT
)
BEGIN
	/**
		구매건 조회
   */
	SELECT * FROM tb_payment_log WHERE payment_log_seq = dataPaymentIdx;
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_NoShow_put $$
CREATE PROCEDURE procPartnerPC_Booking_NoShow_put(
	dataPaymentIdx INT,
    dataNoShow BOOL 
)
BEGIN
	/**
		노쇼 수정
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
	IF dataNoShow THEN
		UPDATE tb_payment_log SET is_no_show = 1 WHERE payment_log_seq = dataPaymentIdx;
    ELSE
		UPDATE tb_payment_log SET is_no_show = 0 WHERE payment_log_seq = dataPaymentIdx;
    END IF;
    
	IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
	SELECT aErr as err;
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_NoShow_put $$
CREATE PROCEDURE procPartnerPC_Booking_NoShow_put(
	dataPaymentIdx INT,
    dataNoShow BOOL 
)
BEGIN
	/**
		노쇼 수정
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
    
	IF dataNoShow THEN
		UPDATE tb_payment_log SET is_no_show = 1 WHERE payment_log_seq = dataPaymentIdx;
    ELSE
		UPDATE tb_payment_log SET is_no_show = 0 WHERE payment_log_seq = dataPaymentIdx;
    END IF;
    
	IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
	SELECT aErr as err;
END $$ 
DELIMITER ;


--         $que = "SELECT COUNT(*) AS cnt FROM tb_grade_of_customer WHERE customer_id = '{$_POST['id']}' AND grade_idx = '{$_POST['org_grade']}'";
--         //echo $que;
--         $row = sql_fetch_array($que);
--         if($row[0]['cnt']>0) {
--             $que = "UPDATE tb_grade_of_customer SET grade_idx = '{$_POST['grade']}' WHERE customer_id = '{$_POST['id']}' AND grade_idx = '{$_POST['org_grade']}'";
--         } else {
--             //$que = "INSERT INTO tb_grade_of_customer SET grade_idx = '{$_POST['grade']}',  customer_id = '{$_POST['id']}'";
--             $que = "INSERT INTO `tb_grade_of_customer` (`grade_idx`, `customer_id`, `is_delete`) VALUES ('{$_POST['grade']}', '{$_POST['id']}', 0);";
--         } 

call procPartnerPC_Booking_GRADE_SHOP_ID_get('pettester@peteasy.kr');        
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_GRADE_SHOP_ID_get $$
CREATE PROCEDURE procPartnerPC_Booking_GRADE_SHOP_ID_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		샵 등급 조회 (조건: 아이디)
   */
	SELECT * FROM tb_grade_of_shop 
    WHERE is_delete = 0 AND artist_id = dataPartnerId;
    
END $$ 
DELIMITER ;

call procPartnerPC_Booking_GRADE_SHOP_IDX_get(2205);        
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_GRADE_SHOP_IDX_get $$
CREATE PROCEDURE procPartnerPC_Booking_GRADE_SHOP_IDX_get(
	dataGradeIdx INT
)
BEGIN
	/**
		샵 등급 조회 (조건: 인덱스)
   */
	SELECT * FROM tb_grade_of_shop 
    WHERE idx = dataGradeIdx;
    
END $$ 
DELIMITER ;


	SELECT COUNT(*) as aCount , idx as aIdx FROM tb_grade_of_customer
    WHERE is_delete = 0 AND grade_idx = 2203 AND customer_id = 'pettester@peteasy.kr';
    
call procPartnerPC_Booking_GradeCustomer_post(2203,'pettesterr@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_GradeCustomer_post $$
CREATE PROCEDURE procPartnerPC_Booking_GradeCustomer_post(
	dataGradeIdx INT,
	dataCustomerId VARCHAR(64)
)
BEGIN
	/**
		고객 샵 등급 부여
   */
	DECLARE aCount INT DEFAULT 0;
    DECLARE aIdx INT UNSIGNED DEFAULT 0;
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*), idx INTO aCount, aIdx FROM tb_grade_of_customer
    WHERE is_delete = 0 AND grade_idx = dataGradeIdx AND customer_id = dataCustomerId;

	START TRANSACTION;
	
    IF aCount < 1 THEN
		INSERT INTO tb_grade_of_customer (grade_idx, customer_id) VALUES (dataGradeIdx, dataCustomerId);
    ELSE
		UPDATE tb_grade_of_customer SET grade_idx = dataGradeIdx, customer_id = dataCustomerId WHERE idx = aIdx;
    END IF;
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	SELECT aErr as err;
END $$ 
DELIMITER ;

call procPartnerPC_Booking_GradeCustomer_put(2203,'pettesterr@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_GradeCustomer_put $$
CREATE PROCEDURE procPartnerPC_Booking_GradeCustomer_put(
	dataIdx INT UNSIGNED,
	dataGradeIdx INT UNSIGNED
)
BEGIN
	/**
		고객 샵 등급 부여
   */
	DECLARE aCount INT DEFAULT 0;
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SELECT COUNT(*) INTO aCount FROM tb_grade_of_customer WHERE idx = dataIdx;

	
    IF aCount < 1 THEN
		SET aErr = -2;
    ELSE
    BEGIN
		START TRANSACTION;
		UPDATE tb_grade_of_customer SET grade_idx = dataGradeIdx WHERE idx = aIdx;
		IF aErr < 0 THEN
			ROLLBACK;
		ELSE
			COMMIT;
		END IF;
	END;
    END IF;
    
	SELECT aErr as err;
END $$ 
DELIMITER ;