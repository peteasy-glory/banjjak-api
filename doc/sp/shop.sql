
-- call procPartnerPC_Shop_Front_get(2023, 0);
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Front_get $$
-- CREATE PROCEDURE procPartnerPC_Shop_Front_get(
-- 	dataPartnerID VARCHAR(64)
-- )
-- BEGIN
-- 	/**
-- 		Shop 대문 사진 관리
--    */
-- 	DECLARE aDone INT DEFAULT FALSE;
-- 	DECLARE aImage VARCHAR(256) DEFAULT '';
-- 	DECLARE aCursor CURSOR FOR
-- 		SELECT image , a
-- 		FROM tb_shop_frontimage 
-- 		WHERE customer_id = dataPartnerID;

-- 	
-- 	SELECT front_image INTO @front_image
-- 	FROM tb_shop 
-- 	WHERE customer_id = dataPartnerID;


-- 	OPEN aCursor;
--     dataLoop: LOOP
-- 		FETCH aCursor INTO aImage;
-- 		
--         IF TRIM(@front_image) = TRIM(aImage) THEN
-- 			
--         END IF;
--         
--         IF aDone THEN
-- 			LEAVE dataLoop;
-- 		END IF;
--     END LOOP;
--     CLOSE aCursor;
--  
-- END $$ 
-- DELIMITER ;

call procPartnerPC_Shop_Front_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Front_get $$
CREATE PROCEDURE procPartnerPC_Shop_Front_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		Shop 대문 사진 조회
   */
   
	SELECT IF(TRIM(A.front_image) = TRIM(B.image), TRUE, FALSE) AS main_image, B.image 
    FROM tb_shop A JOIN tb_shop_frontimage B
		ON A.customer_id = B.customer_id
	WHERE A.customer_id = dataPartnerID;
    
END $$ 
DELIMITER ;

call procPartnerPC_Shop_Front_post('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Front_post $$
CREATE PROCEDURE procPartnerPC_Shop_Front_post(
	dataPartnerID VARCHAR(64),
    dataFilePath VARCHAR(256)
)
BEGIN
	/**
		Shop 대문 사진 추가. 	
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;
	
	INSERT INTO tb_shop_frontimage (customer_id, image) VALUES (dataPartnerID, dataFilePath);
       
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	SELECT aErr as err;
END $$ 
DELIMITER ;

call procPartnerPC_Shop_Front_put('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Front_put $$
CREATE PROCEDURE procPartnerPC_Shop_Front_put(
	dataPartnerID VARCHAR(64),
    dataPath VARCHAR(256)
)
BEGIN
	/**
		Shop 대문 사진 변경
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;

	UPDATE tb_shop SET front_image = TRIM(dataPath) WHERE customer_id = dataPartnerID;
       
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	SELECT aErr as err;
END $$ 
DELIMITER ;

call procPartnerPC_Shop_Front_delete('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Front_delete $$
CREATE PROCEDURE procPartnerPC_Shop_Front_delete(
	dataPartnerID VARCHAR(64),
    dataPath VARCHAR(256)
)
BEGIN
	/**
		Shop 대문 사진 삭제
   */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 

	START TRANSACTION;

	DELETE FROM tb_shop_frontimage WHERE customer_id = dataPartnerID AND image = dataPath;
       
	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	SELECT aErr as err;
END $$ 
DELIMITER ;


call procPartnerPC_Shop_InfoBase_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoBase_get $$
CREATE PROCEDURE procPartnerPC_Shop_InfoBase_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		Shop 기본 정보. 
  */
   
	SELECT shop.name, shop.working_years, shop.photo, shop.self_introduction, shop.career
		INTO @shop_name, @shop_working_years, @shop_photo, @shop_introduction, @shop_carrer
	FROM tb_shop shop, tb_customer customer
		WHERE shop.customer_id = dataPartnerID AND customer.id = dataPartnerID;

	SELECT kakao_channel, SUBSTRING_INDEX(instagram, '/', -1) AS instagram_id, kakao_id INTO @kakao_channel, @instagram_id, @kakao_id
	FROM tb_shop_sns
	WHERE artist_id = dataPartnerID;
    
    SELECT @shop_name AS shop_name, @shop_working_years AS shop_working_years, @shop_photo AS shop_photo, 
		   @shop_introduction AS shop_introduction, @shop_carrer AS shop_carrer, @kakao_channel AS kakao_channel, 
           @instagram_id AS instagram_id, @kakao_id AS kakao_id;

END $$ 
DELIMITER ;

call procPartnerPC_Shop_InfoSalesArea_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoSalesArea_get $$
CREATE PROCEDURE procPartnerPC_Shop_InfoSalesArea_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		Shop 영업 지역 정보. 
  */

	SELECT CONCAT(C.top,' ', C.middle) AS first, GROUP_CONCAT(C.bottom) AS middle
	FROM 
	(
		SELECT * 
		FROM tb_working_region A JOIN tb_region B ON A.region_id = B.id
		WHERE A.customer_id = dataPartnerID
		ORDER BY B.top, B.middle, B.bottom
	) C
	GROUP BY C.middle;

END $$ 
DELIMITER ;

call procPartnerPC_Shop_InfoLicenseAward_get('pettester@peteasy.kr',1);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoLicenseAward_get $$
CREATE PROCEDURE procPartnerPC_Shop_InfoLicenseAward_get(
	dataPartnerID VARCHAR(64),
    dataType INT # 0: 라이센스, 1: 수상경력 
)
BODY: BEGIN
	/**
		Shop 라이센스 , 수상 경력. 
  */

	IF dataType = 0 THEN
    BEGIN
		SELECT photo, name, issue_date, issue_place, update_time FROM tb_license
        WHERE customer_id = dataPartnerID AND enable_flag = 1
        ORDER BY update_time DESC;
		LEAVE BODY;
    END;
    END IF;
    
	SELECT award_seq, photo, name, issue_date, issue_place, update_time FROM tb_award
	WHERE customer_id = dataPartnerID AND enable_flag = 1
    ORDER BY update_time DESC;
    
END $$ 
DELIMITER ;

call procPartnerPC_Shop_InfoLicenseAward_get('pettester@peteasy.kr',1);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_AreaAddr_get $$
CREATE PROCEDURE procPartnerPC_Shop_AreaAddr_get(
	dataFirst VARCHAR(32),
	dataMiddle VARCHAR(32)
)
BEGIN
	/**
		출장지 관리. 
  */

	IF TRIM(dataFirst) = '' AND TRIM(dataMiddle) = '' THEN
    BEGIN
		SELECT DISTINCT( tb_region
		SELECT photo, name, issue_date, issue_place, update_time FROM tb_license
        WHERE customer_id = dataPartnerID AND enable_flag = 1
        ORDER BY update_time DESC;
		LEAVE BODY;
    END;
    END IF;
    
	SELECT award_seq, photo, name, issue_date, issue_place, update_time FROM tb_award
	WHERE customer_id = dataPartnerID AND enable_flag = 1
    ORDER BY update_time DESC;
    
END $$ 
DELIMITER ;

select * from tb_region
WHERE middle = '과천시' and bottom = '갈현동'
WHERE open_flag = 0;

