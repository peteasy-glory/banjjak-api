
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
		호텔 정보 수정(체크인/체크아웃/쿠폰사용여부
   */
    DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

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








