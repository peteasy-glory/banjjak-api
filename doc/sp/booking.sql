
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
   
	SELECT A.*, B.pet_seq, B.tmp_seq, B.name, B.type, B.pet_type, B.photo, C.idx, C.is_approve FROM 
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
    
call procPartnerPC_Booking_CustomerPetInfo_get(568582);
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
    DECLARE aTmpId VARCHAR(64) DEFAULT '';
    DECLARE aCustomerGradeIdx INT DEFAULT 0;
    DECLARE aShopGradeIdx  INT DEFAULT 0;
    DECLARE aGradeName VARCHAR(64) DEFAULT '';
    DECLARE aGradeOrd  INT DEFAULT 0;
    DECLARE aOwnerMemo TEXT DEFAULT '';
    DECLARE aMemo TEXT DEFAULT '';
    DECLARE aPetMemo TEXT DEFAULT '';
    DECLARE aPetId TEXT DEFAULT '';
    
    SET @beauty_date = '';
    SET @worker = '';
    SET @is_noshow = '';
    SET @noshow_count = 0;
        
     # 회원아이디 가져오기    
    SELECT customer_id, artist_id , cellphone, pet_seq, etc_memo, is_no_show, worker, CONCAT(year,'-',LPAD(month,2,0),'-',LPAD(day,2,0),' ',LPAD(hour,2,0),':',LPAD(minute,2,0)) 
				INTO aCustomerId, aPartnerId, aPhone , aPetId, aMemo, @is_noshow , @worker, @beauty_date
    FROM tb_payment_log 
	WHERE payment_log_seq = dataPaymentCode;

	#가회원인경우 임시 아이디 가져오기
	IF TRIM(aCustomerId) = '' OR aCustomerId IS NULL THEN
		SELECT tmp_seq INTO aTmpId FROM tb_tmp_user
        WHERE cellphone = aPhone AND data_delete = 0;
    END IF;
    
	#노쇼 카운트
	SELECT SUM(is_no_show)INTO @noshow_count FROM tb_payment_log
	WHERE customer_id = IF (LENGTH(TRIM(aCustomerId)) > 0, aCustomerId, aTmpId) AND artist_id=artist_id;
	IF @noshow_count IS NULL THEN
		SET @noshow_count = 0;
    END IF;
    
	#보조연락처 가져오기
 	SELECT GROUP_CONCAT(CONCAT(family_seq,'|',from_cellphone,'|',from_customer_id,'|',from_nickname)) INTO aSubPhone 
    FROM tb_customer_family 
	WHERE to_cellphone = aPhone  AND artist_id = aPartnerId AND is_delete = 0;
   

    
    #등급 가져오기
	SELECT a.idx, a.grade_idx, b.grade_name, b.grade_ord INTO aCustomerGradeIdx, aShopGradeIdx, aGradeName, aGradeOrd
    FROM tb_grade_of_customer a 
		LEFT JOIN tb_grade_of_shop b ON a.grade_idx = b.idx 
    WHERE a.customer_id = IF (LENGTH(TRIM(aCustomerId)) > 0, aCustomerId, aTmpId)  AND b.artist_id = aPartnerId AND a.is_delete = 0 AND b.is_delete = 0;
    
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
           aOwnerMemo AS owner_memo, @noshow_count AS noshow_count, @is_noshow AS is_noshow, @worker AS worker, @beauty_date AS beauty_date,
		#예약 펫 정보
		pet_seq, name, name_for_owner, type, pet_type, gender, weight, photo, CONCAT(year,'-',LPAD(month,2,0),'-',LPAD(day,2,0)) AS birth, neutral, etc,
		beauty_exp, vaccination, dermatosis, heart_trouble, marking, mounting, #미용경험, 예방접종, 피부병, 심장질환, 마킹, 마운팅 
        bite, luxation, CONCAT(dt_eye,dt_nose,dt_mouth,dt_ear,dt_neck,dt_body,dt_leg,dt_tail,dt_genitalia,nothing) as disliked_part
	FROM tb_mypet WHERE pet_seq = aPetId;

END $$ 
DELIMITER ;


call procPartnerPC_Booking_BeforePaymentInfo_get(571239, false, 10);
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
    tb_grade_of_customer
END $$ 
DELIMITER ;

call procPartnerPC_Booking_GradeCustomer_post(0, 3357,'hptop.apple@gmail.com');
select * from tb_grade_of_customer where idx = 22005;
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_GradeCustomer_post $$
CREATE PROCEDURE procPartnerPC_Booking_GradeCustomer_post(
	dataCustomerIdx INT,
    dataGradeIdx INT,
	dataCustomerId VARCHAR(64)
)
BEGIN
	/**
		고객 샵 등급 부여
   */
   	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
	
    IF dataCustomerIdx = 0 THEN
		INSERT INTO tb_grade_of_customer (grade_idx, customer_id) VALUES (dataGradeIdx, dataCustomerId);
    ELSE
		UPDATE tb_grade_of_customer SET grade_idx = dataGradeIdx WHERE idx = dataCustomerIdx;
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

#=================
call procPartnerPC_Booking_PetType_get('cat');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PetType_get $$
CREATE PROCEDURE procPartnerPC_Booking_PetType_get(
	dataType VARCHAR(10) # 0: 강아지, 1: 고양이
)
BEGIN
	/**
	동물 종류 가져오기
   */

	SELECT *
	FROM tb_pet_type
	WHERE type = dataType AND enable_flag=1 ORDER BY name ASC;
   
END $$ 
DELIMITER ;
call procPartnerPC_Booking_PreDataCommon_get('pettester@peteasy.kr');
call procPartnerPC_Booking_PreDataStatic_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PreDataStatic_get $$
CREATE PROCEDURE procPartnerPC_Booking_PreDataStatic_get(
	dataPartner VARCHAR(64)
)
BEGIN
	/**
		예약 접수하기 위한 데이타 가져오기 (동물 크기, 무게별 가격)
   */

	SELECT *, if(second_type = '소형견미용', 1, if(second_type = '중형견미용', 2, if(second_type = '대형견미용', 3, if(second_type = '특수견미용', 4, if(second_type = '기타공통', 5, 9))))) AS sort
    FROM tb_product_dog_static 
    WHERE customer_id = dataPartner
		AND second_type != '기타공통'
	ORDER BY sort ASC, update_time;
END $$ 
DELIMITER ;

call procPartnerPC_Booking_PreDataCommon_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PreDataCommon_get $$
CREATE PROCEDURE procPartnerPC_Booking_PreDataCommon_get(
	dataPartner VARCHAR(64)
)
BEGIN
	/**
		예약 접수하기 위한 데이타 가져오기 (털특징, 털길이 , 추가: 얼굴컷, 다리, 스파, 염색, 기타)
   */

	SELECT * 
	FROM tb_product_dog_common
	WHERE customer_id = dataPartner;
END $$ 
DELIMITER ;

call procPartnerPC_Booking_PreDataWorktime_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PreDataWorktime_get $$
CREATE PROCEDURE procPartnerPC_Booking_PreDataWorktime_get(
	dataPartner VARCHAR(64)
)
BEGIN
	/**
		예약 접수하기 위한 데이타 가져오기 (서비스)
   */

	SELECT * 
	FROM tb_product_dog_worktime
	WHERE is_delete = 2 
		AND artist_id = dataPartner;
END $$ 
DELIMITER ;

call procPartnerPC_Booking_PreDataCommOption_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PreDataCommOption_get $$
CREATE PROCEDURE procPartnerPC_Booking_PreDataCommOption_get(
	dataPartner VARCHAR(64)
)
BEGIN
	/**
		예약 접수하기 위한 데이타 가져오기 (목욕 추가)
   */

	SELECT * 
	FROM tb_product_common_option
	WHERE customer_id = dataPartner;
    
END $$ 
DELIMITER ;

call procPartnerPC_Booking_PreDataCat_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PreDataCat_get $$
CREATE PROCEDURE procPartnerPC_Booking_PreDataCat_get(
	dataPartner VARCHAR(64)
)
BEGIN
	/**
		예약 접수하기 위한 데이타 가져오기 
   */

	SELECT * 
	FROM tb_product_cat
	WHERE customer_id = dataPartner;
    
END $$ 
DELIMITER ;

call procPartnerPC_Booking_PetType_get('dog');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PetType_get $$
CREATE PROCEDURE procPartnerPC_Booking_PetType_get(
	dataAnimal VARCHAR(10)
)
BEGIN
	/**
		예약 접수하기 위한 펫종류 가져오기
   */
	SELECT * 
	FROM tb_pet_type
	WHERE type=dataAnimal AND enable_flag = 1;
    
END $$ 
DELIMITER ;


call procPartnerPC_Booking_WaitingList_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_WaitingList_get $$
CREATE PROCEDURE procPartnerPC_Booking_WaitingList_get(
	dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		예약 승인 대기 리스트
   */
	SELECT b.*, c.pet_seq, c.tmp_seq, c.name, c.type, c.pet_type, c.photo, a.idx, a.is_approve
	FROM tb_grade_reserve_approval_mgr a 
		LEFT JOIN tb_payment_log b ON a.payment_log_seq = b.payment_log_seq 
		LEFT JOIN tb_mypet c ON b.pet_seq = c.pet_seq 
	WHERE a.is_approve = '0'
	AND b.artist_id = dataPartnerId AND b.data_delete = 0
	ORDER BY DATE_FORMAT(CONCAT(b.year,'-',b.month,'-',b.day),'%Y-%m-%d') DESC;
    
END $$ 
DELIMITER ;


call procPartnerPC_Booking_Decision_put(129, 0, 573038);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_Decision_put $$
CREATE PROCEDURE procPartnerPC_Booking_Decision_put(
	dataApproveIdx INT,
	dataDecisionCode INT,
    dataPaymentIdx INT
)
BEGIN
	/**
		예약 승인 대기 확정/취소
   */
  	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    START TRANSACTION;
    
    UPDATE tb_grade_reserve_approval_mgr 
	SET is_approve = dataDecisionCode, mod_date = NOW() 
	WHERE idx = dataApproveIdx;
   
	IF dataDecisionCode = 3 THEN
		UPDATE tb_payment_log 
        SET is_cancel = 1,
            cancel_time = NOW()
		WHERE payment_log_seq = dataPaymentIdx;
	END IF;
    
	IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

call procPartnerPC_Booking_CustomerMemo_get('pettester@peteasy.kr','itseokbeom@gmail.com','','01086331776');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_CustomerMemo_get $$
CREATE PROCEDURE procPartnerPC_Booking_CustomerMemo_get(
	dataPartnerId VARCHAR(64),
    dataCustomerID VARCHAR(64),
    dataTmpSeq VARCHAR(20),
    dataCellphone VARCHAR(20)
)
BEGIN
	/**
		견주 관련 메모
   */
	IF LENGTH(dataCustomerID) > 0 THEN
		SELECT * FROM tb_shop_customer_memo 
		WHERE customer_id = dataCustomerID AND cellphone = dataCellphone AND artist_id = dataPartnerId AND is_delete = 2;
	ELSEIF LENGTH(dataTmpSeq) > 0 THEN
		SELECT * FROM tb_shop_customer_memo 
		WHERE tmp_seq = dataTmpSeq AND cellphone = dataCellphone AND artist_id = dataPartnerId AND is_delete = 2;
	ELSE
		SELECT * FROM tb_shop_customer_memo 
		WHERE cellphone = dataCellphone AND artist_id = dataPartnerId AND is_delete = 2;
    END IF;
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_CustomerMemo_put $$
CREATE PROCEDURE procPartnerPC_Booking_CustomerMemo_put(
	dataIdx INT,
    dataMemo TEXT
)
BEGIN
	/**
		견주 관련 메모 수정
   */
  	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    START TRANSACTION;

    UPDATE tb_shop_customer_memo 
	SET memo = dataMemo
	WHERE scm_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

call procPartnerPC_Booking_PetInfo_get(96565);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PetInfo_get $$
CREATE PROCEDURE procPartnerPC_Booking_PetInfo_get(
	dataPetIdx INT
)
BEGIN
	/**
		견주 펫 정보
   */
	SELECT * FROM tb_mypet 
	WHERE pet_seq = dataPetIdx;
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_PetInfo_put $$
CREATE PROCEDURE procPartnerPC_Booking_PetInfo_put(
	dataIdx INT,
    dataName VARCHAR(50),
    dataType VARCHAR(50),
    dataPetType VARCHAR(20),
    dataYear INT,
    dataMonth INT,
    dataDay INT,
    dataGender VARCHAR(20),
    dataNeutral INT,
    dataWeight VARCHAR(20),
    dataBeautyExp VARCHAR(45),
    dataVaccination VARCHAR(45),
    dataLuxation VARCHAR(45),
    dataBite VARCHAR(45),
    dataDermatosis INT,
    dataHeartTrouble INT,
    dataMarking INT,
    dataMounting INT,
    dataEtc TEXT
)
BEGIN
	/**
		견주 펫 정보 수정
   */
  	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    START TRANSACTION;

    UPDATE tb_mypet 
	SET name=dataName, type=dataType, pet_type=dataPetType, year=dataYear, month=dataMonth, day=dataDay, 
		gender=dataGender,neutral=dataNeutral,weight=dataWeight,beauty_exp=dataBeautyExp,
        vaccination=dataVaccination,luxation=dataLuxation,bite=dataBite,dermatosis=dataDermatosis,
        heart_trouble=dataHeartTrouble,marking=dataMarking,mounting=dataMounting,etc=dataEtc
	WHERE pet_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

call procPartnerPC_Booking_post('pettester@peteasy.kr','부실장','','01912387736',0,'dog','말티즈','펫명',2021, 1, 1,'남아',
                           '1','10.0','1회','1회','없음','안해요','0','0','0','0',2022, 8, 18,9, 0,'session','order','15000','pos-card', 
                           'POS','{}',17,30,'N','1','||||','N','N');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_post $$
CREATE PROCEDURE procPartnerPC_Booking_post(
	dataPartnerID VARCHAR(64),dataWorker VARCHAR(32),
	dataCustomerID VARCHAR(64),dataCellPhone VARCHAR(20),
    dataPetSeq INT,
	dataAnimal VARCHAR(10),dataPetType VARCHAR(32),dataPetName VARCHAR(50),
	dataPetYear INT, dataPetMonth INT, dataPetDay INT,
	dataGender VARCHAR(10), 
	dataNeutral VARCHAR(2),
	dataWeight VARCHAR(10),
	dataBeautyExp VARCHAR(20),
	dataVaccination VARCHAR(20),
	dataLuxation VARCHAR(10),
	dataBite VARCHAR(20),
	dataDermatosis VARCHAR(2),
	dataHeartTrouble VARCHAR(2),
	dataMarking VARCHAR(2),
	dataMounting VARCHAR(2),
  	dataYear INT, dataMonth INT, dataDay INT,
    dataHour INT, dataMin INT,
    dataSessionID VARCHAR(256),
    dataOrderID VARCHAR(256),
    dataLocalPrice VARCHAR(16),
    dataPayType VARCHAR(20),
    dataPayStatus VARCHAR(3),
    dataPayData VARCHAR(4069),
    dataToHour INT,
    dataToMin INT,
    dataUseCouponYN VARCHAR(2),
    dataIsVat VARCHAR(2),
    dataProduct VARCHAR(4096),
    dataReserveYN VARCHAR(2),
    dataADayAgoYN VARCHAR(2)
)
BODY : BEGIN
	/**
		샵  미용 예약하기
   */
	
  	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

    SET @worker_count = 0;
    SET @st = CONCAT(dataYear,lpad(dataMonth,2,0),lpad(dataDay,2,0), lpad(dataHour,2,0), lpad(dataMin,2,0));
	SET @fi = CONCAT(dataYear,lpad(dataMonth,2,0),lpad(dataDay,2,0), lpad(dataToHour,2,0), lpad(dataToMin,2,0));
    
    SELECT COUNT(*) INTO @worker_count 
    FROM tb_payment_log 
    WHERE artist_id = dataPartnerID AND worker = dataWorker
		AND (
			(CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(hour,2,0), lpad(minute,2,0)) <= @st
				AND @st < CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(to_hour,2,0), lpad(to_minute,2,0))) OR
			(CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(hour,2,0), lpad(minute,2,0)) < @fi
				AND @fi <= CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(to_hour,2,0), lpad(to_minute,2,0))) OR
			(CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(hour,2,0), lpad(minute,2,0)) <= @st
				AND @fi <= CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(to_hour,2,0), lpad(to_minute,2,0))) OR 
            (CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(hour,2,0), lpad(minute,2,0)) > @st
				AND @fi > CONCAT(year,lpad(month,2,0),lpad(day,2,0), lpad(to_hour,2,0), lpad(to_minute,2,0))))
        AND is_cancel = 0;
	
    IF @worker_count > 0 THEN
    BEGIN
		SELECT 401 AS err;
		LEAVE BODY;
	END;
    END IF;

	SET @customer_id = dataCustomerID;
	IF LENGTH(@customer_id) < 1 THEN
    BEGIN
		SELECT id INTO @customer_id FROM tb_customer 
		WHERE cellphone = dataCellPhone 
			AND nickname not like 'cellp_%' 
		ORDER BY last_login_time DESC LIMIT 1;

		IF LENGTH(@customer_id) < 1 OR @customer_id IS NULL THEN
        BEGIN
			SELECT CAST(tmp_seq AS CHAR(12)) INTO @customer_id FROM tb_tmp_user WHERE cellphone = dataCellPhone;

      		IF LENGTH(@customer_id) < 1 OR @customer_id IS NULL THEN
            BEGIN
                
                START TRANSACTION;

				INSERT INTO tb_tmp_user SET cellphone = dataCellPhone;
                SET @new_tmp_id = LAST_INSERT_ID();
                
                INSERT INTO tb_mypet 
				SET tmp_seq = @new_tmp_id, customer_id = NULLIF('',''), 
				type = dataAnimal, pet_type = dataPetType, name = dataPetName, 
				year = dataPetYear, month = dataPetMonth, day = dataPetDay, 
				gender = dataGender, neutral = dataNeutral, 
				weight = dataWeight, beauty_exp     = dataBeautyExp, 
				vaccination = dataVaccination, luxation = dataLuxation, bite = dataBite, 
				dermatosis = dataDermatosis, heart_trouble = dataHeartTrouble, 
				marking = dataMarking, mounting = dataMounting;
				SET @new_pet_id = LAST_INSERT_ID();
                
                IF aErr < 0 THEN
                BEGIN
					ROLLBACK;
                    SELECT aErr AS err; 
					LEAVE BODY;
				END;
				ELSE
					COMMIT;
				END IF;
            END;    
			END IF;
        END;    
		END IF;
	END;
    ELSE
    BEGIN
		UPDATE tb_mypet 
        SET type = dataAnimal, pet_type = dataPetType, 
		year = dataPetYear, month = dataPetMonth, day = dataPetDay, 
		gender = dataGender, weight = dataWeight 
		WHERE pet_seq = dataPetSeq;
        SET @new_pet_id = dataPetSeq;
    END;
    END IF;

    START TRANSACTION;
    
    INSERT INTO tb_payment_log
	SET pet_seq= @new_pet_id, session_id = dataSessionID, 
	customer_id = dataCustomerID, artist_id = dataPartnerID, 
	order_id = dataOrderID, local_price = dataLocalPrice, cellphone = dataCellPhone, 
	worker = dataWorker, year = dataYear, month = dataMonth, day = dataDay, pay_type = dataPayType, 
	is_coupon = dataUseCouponYN, hour = dataHour, minute = dataMin, 
	pay_data = dataPayData, to_hour = dataToHour, to_minute = dataToMin, product_type = 'B', approval = '1', 
	is_vat = dataIsVat, product = dataProduct, reserve_yn = dataReserveYN, a_day_ago_yn = dataADayAgoYN, buy_time = NOW();
        
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;

#=====================
 
call procPartnerPC_Booking_Prohibition_get('pettester@peteasy.kr', '20220801', '20220829');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_Prohibition_get $$
CREATE PROCEDURE procPartnerPC_Booking_Prohibition_get(
	dataPartnerID VARCHAR(64),
    dataStDate VARCHAR(13), #yyyymmddHHMMSS
    dataFiDate VARCHAR(13)
)
BEGIN
	/**
		예약 금지 리스트
   */
  	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
	SELECT ph_seq, worker, type, 
		CONCAT( start_year,'-',LPAD(start_month,2,0),'-',LPAD(start_day,2,0),' ',LPAD(start_hour,2,0),':',LPAD(start_minute,2,0)) as st_date,
		CONCAT( end_year,'-',LPAD(end_month,2,0),'-',LPAD(end_day,2,0),' ',LPAD(end_hour,2,0),':',LPAD(end_minute,2,0)) as fi_date, update_time
    FROM tb_private_holiday
    WHERE customer_id = dataPartnerID
        AND DATE_FORMAT( CONCAT( start_year,'-',start_month,'-',start_day,' ',start_hour,':',IFNULL(start_minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) >= DATE_FORMAT( funcYMDHHMMToDash(dataStDate) , '%Y-%m-%d %H:%i' )
        AND DATE_FORMAT( CONCAT( end_year,'-',end_month,'-',end_day,' ',end_hour,':',IFNULL(end_minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) <= DATE_FORMAT( funcYMDHHMMToDash(dataFiDate) , '%Y-%m-%d %H:%i' );
          
END $$ 
DELIMITER ;


select * from tb_private_holiday where customer_id = 'pettester@peteasy.kr' order by update_time desc;
-- call procPartnerPC_Booking_Prohibition_post('pettester@peteasy.kr', 'pettester@peteasy.kr', 'notall', '202208061330', '202208061430');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_Prohibition_post $$
CREATE PROCEDURE procPartnerPC_Booking_Prohibition_post(
	dataPartnerID VARCHAR(64),
    dataWorker VARCHAR(64),
    dataType VARCHAR(32),
    dataStDate VARCHAR(13), #yyyymmddHHMMSS
    dataFiDate VARCHAR(13)
)
BODY: BEGIN
	/**
		예약 금지 설정
   */
  	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
	
    # 현재 일시에 작업 내용이 있는지?
	SELECT COUNT(*) INTO @exist_work  
    FROM tb_payment_log
    WHERE data_delete = 0 AND artist_id = dataPartnerID AND worker = dataWorker
        AND DATE_FORMAT( CONCAT( year,'-',month,'-',day,' ',hour,':',IFNULL(minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) >= DATE_FORMAT( funcYMDHHMMToDash(dataStDate) , '%Y-%m-%d %H:%i' )
        AND DATE_FORMAT( CONCAT( year,'-',month,'-',day,' ',to_hour,':',IFNULL(to_minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) <= DATE_FORMAT( funcYMDHHMMToDash(dataFiDate) , '%Y-%m-%d %H:%i' );

	# 현재 일시가 개인 휴일인지 체크한다.
	SELECT COUNT(*) INTO @exist_holiday
    FROM tb_private_holiday
    WHERE customer_id = dataPartnerID AND worker = dataWorker
        AND DATE_FORMAT( CONCAT( start_year,'-',start_month,'-',start_day,' ',start_hour,':',IFNULL(start_minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) >= DATE_FORMAT( funcYMDHHMMToDash(dataStDate) , '%Y-%m-%d %H:%i' )
        AND DATE_FORMAT( CONCAT( end_year,'-',end_month,'-',end_day,' ',end_hour,':',IFNULL(end_minute,'00'),':00' ), '%Y-%m-%d %H:%i' ) <= DATE_FORMAT( funcYMDHHMMToDash(dataFiDate) , '%Y-%m-%d %H:%i' );
        
    IF @exist_work > 0 THEN
    BEGIN
		SELECT 902 AS err;
		LEAVE BODY;
	END;
    ELSEIF @exist_holiday > 0 THEN
    BEGIN
		SELECT 903 AS err;
		LEAVE BODY;
    END;
    END IF;
    
    START TRANSACTION;

	INSERT INTO tb_private_holiday (customer_id, worker, type, start_year, start_month, start_day, start_hour, start_minute, 
									end_year, end_month, end_day, end_hour, end_minute, update_time) 
	VALUES (dataPartnerID, dataWorker, dataType,
			CAST(SUBSTRING(dataStDate,1,4) AS SIGNED),  CAST(SUBSTRING(dataStDate,5,2) AS SIGNED), CAST(SUBSTRING(dataStDate,7,2) AS SIGNED), 
            CAST(SUBSTRING(dataStDate,9,2) AS SIGNED), CAST(SUBSTRING(dataStDate,11,2) AS SIGNED),
			CAST(SUBSTRING(dataFiDate,1,4) AS SIGNED), CAST(SUBSTRING(dataFiDate,5,2) AS SIGNED),  CAST(SUBSTRING(dataFiDate,7,2) AS SIGNED), 
            CAST(SUBSTRING(dataFiDate,9,2) AS SIGNED), CAST(SUBSTRING(dataFiDate,11,2) AS SIGNED), NOW());

    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;    
END $$ 
DELIMITER ;



call procPartnerPC_Booking_Prohibition_delete(46674);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_Prohibition_delete $$
CREATE PROCEDURE procPartnerPC_Booking_Prohibition_delete(
	dataIdx INT
)
BEGIN
	/**
		예약 금지 설정
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
	
call procPartnerPC_Booking_ShopWorkingTime_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_ShopWorkingTime_get $$
CREATE PROCEDURE procPartnerPC_Booking_ShopWorkingTime_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		샵 오픈/클로즈시간, 주간 근무일
   */
   
	#샵 오픈/클로즈 시간
	SELECT working_start, working_end, rest_public_holiday INTO @shop_open, @shop_close, @is_rest_holiday
    FROM tb_working_schedule 
    WHERE customer_id = dataPartnerID;

	#근무일 
	SELECT is_sunday, is_monday, is_tuesday, is_wednesday, is_thursday, is_friday, is_saturday, week_type
		INTO @sun, @mon, @tue, @wed, @thu, @fri, @sat, @week_type
    FROM tb_regular_holiday 
    WHERE customer_id = dataPartnerID;

	SELECT @shop_open AS shop_open, @shop_close AS shop_close, @is_rest_holiday AS is_rest_holiday, 
		   @sun AS sun, @mon AS mon, @tue AS tue, @wed AS wed, @thu AS thu, @fri AS fri, @sat AS sat, @week_type AS week_type;

END $$ 
DELIMITER ;

call procPartnerPC_Booking_StatutoryHolidays_get(2023, 0);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Booking_StatutoryHolidays_get $$
CREATE PROCEDURE procPartnerPC_Booking_StatutoryHolidays_get(
	dataYear INT,
    dataMonth INT
)
BODY: BEGIN
	/**
		법정공휴일 
   */
   
	IF dataYear < 2000 OR dataMonth > 12 THEN
	BEGIN
        SELECT 904 AS err;
		LEAVE BODY;
    END;
    END IF;
   
	IF dataYear > 0 AND dataMonth > 0 AND dataMonth < 13 THEN
		SELECT * FROM tb_public_holiday WHERE year = dataYear and month = dataMonth ORDER BY year, month, day; 
	ELSE
		SELECT * FROM tb_public_holiday WHERE year = dataYear ORDER BY year, month, day; 
	END IF;
END $$ 
DELIMITER ;





