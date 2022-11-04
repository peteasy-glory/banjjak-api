call procPartnerPC_Setting_Hotel_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Hotel_get $$
CREATE PROCEDURE procPartnerPC_Setting_Hotel_get(
    dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		호텔 정보 
   */
	SELECT *
	FROM tb_hotel
	WHERE is_delete = 2
		AND artist_id = dataPartnerID;

END $$ 
DELIMITER ;


call procPartnerPC_Setting_Hotel_put('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Hotel_put $$
CREATE PROCEDURE procPartnerPC_Setting_Hotel_put(
    dataIdx INT,
    dataIsPickUp CHAR(1),
    dataIs24Hour CHAR(1),
    dataCheckIn VARCHAR(45),
    dataCheckOut VARCHAR(45),
    dataIsCoupon CHAR(1),
    dataIsFlat CHAR(1),
    dataPetType VARCHAR(10)
)
BEGIN
	/**
		호텔 정보 수정(체크인/체크아웃/쿠폰사용여부
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   

	UPDATE tb_hotel 
    SET is_pickup = dataIsPickUp,  is_24hour = dataIs24Hour,  
		check_in = dataCheckIn,  check_out = dataCheckOut,  
		is_coupon = dataIsCoupon,  is_flat = dataIsFlat,  pet_type = dataPetType,
		update_dt = NOW()
	WHERE h_seq = dataIdx;
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;


call procPartnerPC_Setting_HotelProduct_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_HotelProduct_get $$
CREATE PROCEDURE procPartnerPC_Setting_HotelProduct_get(
    dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		호텔 상품
   */
    
	SELECT * 
	FROM tb_hotel_product
	WHERE is_delete = '2'
		AND artist_id = dataPartnerId
		#AND room_pet_type = 'dog'
	ORDER by room_pet_type ASC, sort ASC;
    
END $$ 
DELIMITER ;

call procPartnerPC_Setting_Photo_get(3915);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Photo_get $$
CREATE PROCEDURE procPartnerPC_Setting_Photo_get(
    dataIdx INT
)
BEGIN
	/**
		사진 가져 오기
   */
	SELECT f_seq, file_name, file_path 
	FROM tb_file
	WHERE is_delete = '1'
		AND f_seq = dataIdx;

END $$ 
DELIMITER ;

call procPartnerPC_Setting_HotelProduct_post(177,'itseokbeom@gmail.com','dog','객실6',1,'2.0','100','200','1','1',10,100,'1','2','객실6 추가','');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_HotelProduct_post $$
CREATE PROCEDURE procPartnerPC_Setting_HotelProduct_post(
    dataIdx INT,
    dataPartnerID VARCHAR(64),
    dataPetType VARCHAR(10),
    dataRoomName VARCHAR(45),
    dataRoomCnt INT,
    dataWeight VARCHAR(45),
    dataNormalPrice VARCHAR(45),
    dataPeakPrice VARCHAR(45),
    dataIsNeutral CHAR(1),
    dataIsNeutralPay CHAR(1),
    dataNeutralPrice INT,
    dataExtraPrice INT,
    dataIsPeak CHAR(1),
    dataIsImage CHAR(1),
    dataComment TEXT,
    dataImage VARCHAR(255)
)
BEGIN
	/**
		호텔 정보 수정(체크인/체크아웃/쿠폰사용여부
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	SET @sort = 1;
	SELECT sort INTO @sort 
	FROM tb_hotel_product
	WHERE is_delete = '2'
		AND artist_id = dataPartnerID
		AND room_pet_type = dataPetType
	ORDER by sort DESC LIMIT 1;

	START TRANSACTION;   

	INSERT INTO tb_hotel_product (
		`h_seq`, `artist_id`, `room_pet_type`, `room_name`, `room_cnt`, 
		`weight`, `normal_price`, `peak_price`, `image`, `sort`, 
		`is_neutral`, `is_neutral_pay`, `neutral_price`, `extra_price`, `is_peak`, 
		`is_image`, `comment`, `reg_dt`
	) VALUES (
		dataIdx, dataPartnerID, dataPetType,dataRoomName, dataRoomCnt, 
        dataWeight, dataNormalPrice, dataPeakPrice, dataImage, @sort, 
		dataIsNeutral, dataIsNeutralPay, dataNeutralPrice, dataExtraPrice, dataIsPeak, 
		dataIsImage, dataComment, NOW()
	);
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;


call procPartnerPC_Setting_HotelProduct_put(401,'6객',2,'2.1','20','200','1','1',5000,10000,'2','1','수정','');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_HotelProduct_put $$
CREATE PROCEDURE procPartnerPC_Setting_HotelProduct_put(
    dataIdx INT,
    dataRoomName VARCHAR(45),
    dataRoomCnt INT,
    dataWeight VARCHAR(45),
    dataNormalPrice VARCHAR(45),
    dataPeakPrice VARCHAR(45),
    dataSort INT,
    dataIsNeutral CHAR(1),
    dataIsNeutralPay CHAR(1),
    dataNeutralPrice INT,
    dataExtraPrice INT,
    dataIsPeak CHAR(1),
    dataIsImage CHAR(1),
    dataComment TEXT,
    dataImage VARCHAR(255)
)
BEGIN
	/**
		호텔 상품 수정
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   

	UPDATE tb_hotel_product 
    SET room_name = dataRoomName,  room_cnt = dataRoomCnt,  weight = dataWeight,  
		normal_price = dataNormalPrice,  peak_price = dataPeakPrice,  sort = dataSort,  
        is_neutral = dataIsNeutral,  is_neutral_pay = dataIsNeutralPay,  neutral_price = dataNeutralPrice,  
        extra_price = dataExtraPrice,  is_peak = dataIsPeak,  is_image = dataIsImage,  comment = dataComment, 
		image = dataImage, update_dt = NOW()
	WHERE hp_seq = dataIdx;
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;

call procPartnerPC_Setting_HotelProduct_delete(401,'6객',2,'2.1','20','200','1','1',5000,10000,'2','1','수정','');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_HotelProduct_delete $$
CREATE PROCEDURE procPartnerPC_Setting_HotelProduct_delete(
    dataIdx INT,
	dataMessage VARCHAR(255)
)
BEGIN
	/**
		호텔 상품 삭제
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   
	
    UPDATE tb_hotel_product SET
		is_delete = '1',
		delete_msg = dataMessage,
		delete_dt = NOW()
	WHERE hp_seq = dataIdx;
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;




call procPartnerPC_Setting_Coupon_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Coupon_get $$
CREATE PROCEDURE procPartnerPC_Setting_Coupon_get(
    dataPartnerID VARCHAR(64),
    dataType CHAR(1)
)
BEGIN
	/**
		호텔 쿠폰 정보 
   */
	SELECT *
	FROM tb_coupon
	WHERE customer_id = dataPartnerID
		AND del_yn = 'N'
		 AND product_type = dataType;

END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Coupon_post $$
CREATE PROCEDURE procPartnerPC_Setting_Coupon_post(
    dataPartnerID VARCHAR(64),
    dataType CHAR(1),
    dataCouponType CHAR(1),
    dataName VARCHAR(250),
    dataGiven INT,
    dataPrice INT
)
BEGIN
	/**
		호텔 쿠폰 추가 
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
 
	START TRANSACTION;   
   
	INSERT INTO tb_coupon (customer_id, product_type, type, name, given, price) 
    VALUES (dataPartnerID, dataType, dataCouponType, dataName, dataGiven, dataPrice);
    
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Coupon_put $$
CREATE PROCEDURE procPartnerPC_Setting_Coupon_put(
    dataIdx INT,
    dataName VARCHAR(250),
    dataGiven INT,
    dataPrice INT
)
BEGIN
	/**
		호텔 쿠폰 수정 
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
  
	START TRANSACTION;   
  
	UPDATE tb_coupon 
    SET name = dataName,  given = dataGiven,  price = dataPrice, del_yn = 'N',update_date = NOW()
	WHERE coupon_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;

#====================== kindergarden ======================
call procPartnerPC_Setting_Kindergarden_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Kindergarden_get $$
CREATE PROCEDURE procPartnerPC_Setting_Kindergarden_get(
    dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		유치원 정보 
   */
	SELECT *
	FROM tb_playroom
	WHERE is_delete = 2
		AND artist_id = dataPartnerID;

END $$ 
DELIMITER ;


call procPartnerPC_Setting_Kindergarden_put('');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_Kindergarden_put $$
CREATE PROCEDURE procPartnerPC_Setting_Kindergarden_put(
    dataIdx INT,
    dataIsPickUp CHAR(1),
    dataIsNeutral CHAR(1),
    dataIsNeutralPay CHAR(1),
    dataNeutralPrice INT,
    dataExtraPrice INT,
    dataIsCoupon CHAR(1),
    dataIsFlat CHAR(1),
    dataIsWeight CHAR(1)
)
BEGIN
	/**
		유치원 정보 수정
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   

	UPDATE tb_playroom 
    SET is_pickup = dataIsPickUp,  is_neutral = dataIsNeutral,  
		is_neutral_pay = dataIsNeutralPay,  neutral_price = dataNeutralPrice,  
        extra_price = dataExtraPrice,
		is_coupon = dataIsCoupon,  is_flat = dataIsFlat,  is_weight = dataIsWeight,
		update_dt = NOW()
	WHERE p_seq = dataIdx;
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;

call procPartnerPC_Setting_PeriodCoupon_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_PeriodCoupon_get $$
CREATE PROCEDURE procPartnerPC_Setting_PeriodCoupon_get(
    dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		유치원 기간 쿠폰 정보 
   */
	SELECT pap_seq,artist_id,name,count,price,sale_price,reg_dt,update_dt
	FROM tb_playroom_allday_pass
	WHERE artist_id = dataPartnerID
		AND is_delete = '2';

END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_PeriodCoupon_post $$
CREATE PROCEDURE procPartnerPC_Setting_PeriodCoupon_post(
    dataPartnerID VARCHAR(64),
    dataName VARCHAR(255),
    dataCount INT,
    dataPrice INT,
    dataSalePrice INT
)
BEGIN
	/**
		유치원 기간 쿠폰 추가 
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   

	INSERT INTO tb_playroom_allday_pass (artist_id, name, count, price, sale_price) 
    VALUES (dataPartnerID, dataName, dataCount, dataPrice, dataSalePrice);
                    
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;


call procPartnerPC_Setting_PeriodCoupon_put(401,'6객',2,'2.1','20','200','1','1',5000,10000,'2','1','수정','');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_PeriodCoupon_put $$
CREATE PROCEDURE procPartnerPC_Setting_PeriodCoupon_put(
    dataIdx INT,
    dataName VARCHAR(255),
    dataCount INT,
    dataPrice INT,
    dataSalePrice INT
)
BEGIN
	/**
		유치원 기간 쿠폰 수정
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   
    
	UPDATE tb_playroom_allday_pass 
    SET name = dataName,  count = dataCount,  price = dataPrice,  sale_price = dataSalePrice, update_dt = NOW()
	WHERE pap_seq = dataIdx;
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_PeriodCoupon_delete $$
CREATE PROCEDURE procPartnerPC_Setting_PeriodCoupon_delete(
    dataIdx INT,
	dataDel CHAR(1),
    dataDelMsg VARCHAR(255)
)
BEGIN
	/**
		유치원 기간쿠폰 삭제
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   
	
	UPDATE tb_playroom_allday_pass SET
		is_delete = dataDel,
		delete_msg = dataDelMsg,
		delete_dt = NOW()
	WHERE pap_seq = dataIdx;
			
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;
					SELECT *
					FROM tb_playroom_allday_pass
					WHERE artist_id = 'itseokbeom@gmail.com'
						AND is_delete = '2'
#================
call procPartnerPC_Setting_KindergardenProduct_get('itseokbeom@gmail.com');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_KindergardenProduct_get $$
CREATE PROCEDURE procPartnerPC_Setting_KindergardenProduct_get(
    dataPartnerId VARCHAR(64)
)
BEGIN
	/**
		유치원 상품 조회
   */
    
	SELECT * 
	FROM tb_playroom_product
	WHERE is_delete = '2'
		AND artist_id = dataPartnerId
	ORDER by sort ASC;
    
END $$ 
DELIMITER ;



    
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_KindergardenProduct_post $$
CREATE PROCEDURE procPartnerPC_Setting_KindergardenProduct_post(
    dataKindergardenIdx INT,
    dataPartnerID VARCHAR(64),
    dataRoom VARCHAR(45),
	dataWeight VARCHAR(45),
    dataNormalPrice VARCHAR(45),
    dataSort INT,
    dataComment TEXT
)
BEGIN
	/**
		유치원 상품 추가 
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   

 	INSERT INTO tb_playroom_product (p_seq, artist_id, room_name, weight, normal_price, sort, tb_playroom_product.comment, reg_dt) 
 	VALUES (dataKindergardenIdx, dataPartnerID, dataRoom, dataWeight, dataNormalPrice, dataSort, dataComment, NOW());

    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;


call procPartnerPC_Setting_KindergardenProduct_put(401,'6객',2,'2.1','20','200','1','1',5000,10000,'2','1','수정','');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_KindergardenProduct_put $$
CREATE PROCEDURE procPartnerPC_Setting_KindergardenProduct_put(
    dataIdx INT,
    dataRoom VARCHAR(45),
    dataWeight VARCHAR(45),
    dataNormalPrice VARCHAR(45),
    dataSort INT,
    dataComment TEXT,
    dataIsDelete CHAR(1)
)
BEGIN
	/**
		유치원 상품 수정
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   

	UPDATE tb_playroom_product SET
		 weight = dataWeight,  normal_price = dataNormalPrice,  sort = dataSort,  comment = dataComment, 
		room_name = dataRoom, is_delete = dataIsDelete, update_dt = NOW()
	WHERE pp_seq = dataIdx;
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;

call procPartnerPC_Setting_KindergardenProduct_delete(401,'6객',2,'2.1','20','200','1','1',5000,10000,'2','1','수정','');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Setting_KindergardenProduct_delete $$
CREATE PROCEDURE procPartnerPC_Setting_KindergardenProduct_delete(
    dataIdx INT,
	dataMessage VARCHAR(255)
)
BEGIN
	/**
		유치원 상품 삭제
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;   
	

	UPDATE tb_playroom_product SET
		is_delete = '1',
		delete_msg = dataMessage,
		delete_dt = NOW()
	WHERE pp_seq = dataIdx;
				
	
    IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
	SELECT aErr AS err;  
END $$ 
DELIMITER ;






