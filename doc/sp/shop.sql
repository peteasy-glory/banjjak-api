
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

	SELECT CONCAT(C.top,' ', C.middle) AS first, GROUP_CONCAT(CONCAT(C.region_id,':', C.bottom)) AS middle
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


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoSalesArea_post $$
CREATE PROCEDURE procPartnerPC_Shop_InfoSalesArea_post(
	dataPartnerID VARCHAR(64),
    dataRegionID INT
)
BODY: BEGIN
	/**
		Shop 영업 지역 정보 삭제. 
  */

	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    SELECT COUNT(*) INTO @count 
    FROM tb_working_region 
    WHERE customer_id=dataPartnerID 
		AND region_id = dataRegionID;

    IF @count > 0 THEN
    BEGIN
		SELECT 0 AS err;   
        LEAVE BODY;
    END;
    END IF;

    START TRANSACTION;

	INSERT INTO tb_working_region (customer_id, region_id, update_time) VALUES(dataPartnerID, dataRegionID, NOW());

    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoSalesArea_delete $$
CREATE PROCEDURE procPartnerPC_Shop_InfoSalesArea_delete(
	dataPartnerID VARCHAR(64),
    dataRegionID INT
)
BEGIN
	/**
		Shop 영업 지역 정보 삭제. 
  */

	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	DELETE FROM tb_working_region WHERE customer_id = dataPartnerID AND region_id = dataRegionID;

    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

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

call procPartnerPC_Shop_InfoLicenseAward_get_post('pettester@peteasy.kr',0,'하하하','공단','2022-01-23','/upload/pettester@peteasy.kr/customer_photo_20220823170517083463.png')
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoLicenseAward_get_post $$
CREATE PROCEDURE procPartnerPC_Shop_InfoLicenseAward_get_post(
	dataPartnerID VARCHAR(64),
    dataType INT, # 0: 라이센스, 1: 수상경력 
    dataName VARCHAR(256),
    dataIssuedBy VARCHAR(256),
    dataPublishedDate VARCHAR(14),
    dataPhoto VARCHAR(256)
)
BODY: BEGIN
	/**
		라이센스/수상경력 추가 . 
  */

	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    

    START TRANSACTION;
	IF dataType < 1 THEN
		INSERT INTO tb_license(customer_id, photo, name, issue_date, issue_place, enable_flag) VALUES (dataPartnerID, dataPhoto, dataName, dataPublishedDate, dataIssuedBy, 1);
	ELSE
		INSERT INTO tb_award(customer_id, photo, name, issue_date, issue_place, enable_flag) VALUES(dataPartnerID, dataPhoto, dataName, dataPublishedDate, dataIssuedBy,1);
    END IF;

    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoLicenseAward_get_delete $$
CREATE PROCEDURE procPartnerPC_Shop_InfoLicenseAward_get_delete(
	dataPartnerID VARCHAR(64),
    dataType INT, # 0: 라이센스, 1: 수상경력 
    dataPhoto VARCHAR(256)
)
BEGIN
	/**
		라이센스/수상 경력 삭제
  */

	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	IF dataType < 1 THEN
		DELETE FROM tb_license WHERE customer_id = dataPartnerID AND photo = dataPhoto;
	ELSE
		DELETE FROM tb_award WHERE customer_id = dataPartnerID AND photo = dataPhoto;
    END IF;

    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   

END $$ 
DELIMITER ;

call procPartnerPC_Shop_AreaAddr_get('서울', '강남구');
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
		SELECT DISTINCT(top) FROM tb_region;
    ELSEIF TRIM(dataFirst) != '' AND TRIM(dataMiddle) = '' THEN
		SELECT DISTINCT(middle) FROM tb_region WHERE top = dataFirst;
	ELSEIF TRIM(dataFirst) != '' AND TRIM(dataMiddle) != '' THEN
		SELECT id, bottom FROM tb_region WHERE top = dataFirst AND middle = dataMiddle;
	ELSE
		SELECT -1 AS err;
    END IF;
    
END $$ 
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Info_put $$
CREATE PROCEDURE procPartnerPC_Shop_Info_put(
	dataPartnerID VARCHAR(64),
	dataWorkingYears INT,
    dataIntroduction VARCHAR(4096),
    dataCareer TEXT,
    dataKakaoChannel VARCHAR(50),
    dataInstagram VARCHAR(50),
    dataKakaoID VARCHAR(50)
)
BEGIN
	/**
		샵 정보 저장. 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	UPDATE tb_shop
	SET working_years = dataWorkingYears,
		self_introduction = dataIntroduction,
		career = dataCareer, update_time = NOW()
	WHERE customer_id = dataPartnerID;
	
	SELECT COUNT(*) INTO @exist_sns FROM tb_shop_sns WHERE artist_id = dataPartnerID;
	
	IF @exist_sns > 0 THEN
	BEGIN
		SET @shop_enable = IF(dataKakaoChannel = '' AND 
								dataInstagram = '' AND 
								dataKakaoID = '', 0, 1);
		UPDATE tb_shop_sns SET
			kakao_channel = dataKakaoChannel,
			instagram = dataInstagram,
			kakao_id = dataKakaoID,
			enable_flag = @shop_enable,
			update_time = NOW()
		WHERE artist_id = dataPartnerID;
	END;
	ELSE
		INSERT INTO tb_shop_sns (artist_id, kakao_channel, instagram, kakao_id, update_time)
		VALUES (dataPartnerID, dataKakaoChannel, dataInstagram, dataKakaoID, NOW());
	END IF;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_InfoPhoto_put $$
CREATE PROCEDURE procPartnerPC_Shop_InfoPhoto_put(
	dataPartnerID VARCHAR(64),
	dataImage VARCHAR(512)
)
BEGIN
	/**
		샵 정보 저장. 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	UPDATE tb_shop 
    SET photo = dataImage 
    WHERE customer_id = dataPartnerID;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;
###############

call procPartnerPC_Shop_Gallery_get('dew@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Gallery_get $$
CREATE PROCEDURE procPartnerPC_Shop_Gallery_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		샵 포트폴리오 조회
  */
	SELECT idx, sort_number, is_tag, image, update_time FROM tb_portfolio 
	WHERE customer_id = dataPartnerID AND enable_flag = 1
	ORDER BY sort_number asc;
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Gallery_post $$
CREATE PROCEDURE procPartnerPC_Shop_Gallery_post(
	dataPartnerID VARChAR(64),
	dataImage VARChAR(256)
)
BEGIN
	/**
		샵 갤러리 추가 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	INSERT INTO tb_portfolio (customer_id, image)
	VALUES (dataPartnerID, dataImage);
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

call procPartnerPC_Shop_Gallery_delete(9608);
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Gallery_delete $$
CREATE PROCEDURE procPartnerPC_Shop_Gallery_delete(
	dataIdx INT
)
BEGIN
	/**
		샵 갤러리 삭제 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	DELETE from tb_portfolio 
    WHERE idx = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

#####################

call procPartnerPC_Shop_Review_get('dew@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Review_get $$
CREATE PROCEDURE procPartnerPC_Shop_Review_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		샵 리뷰 조회
  */

	SELECT A.review_seq, A.payment_log_seq, A.customer_id, A.nickname, 
			A.rating, A.review, A.review_images, A.reg_time, is_blind, 
			A.artist_reply, A.photo, A.reply_time, A.is_artist_blind,
			B.name, B.front_image
	FROM tb_usage_reviews A
	INNER JOIN tb_shop B ON A.artist_id = B.customer_id
	WHERE A.artist_id = dataPartnerID
		AND A.is_delete = 0
	ORDER BY A.reg_time DESC;
    
END $$ 
DELIMITER ;

call procPartnerPC_Shop_Review_put('761','aaaaaaaaaaaaaa')
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Review_put $$
CREATE PROCEDURE procPartnerPC_Shop_Review_put(
	dataIdx INT,
    dataReply TEXT
)
BEGIN
	/**
		샵 리뷰 댓글 추가 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

    UPDATE tb_usage_reviews 
    SET artist_reply = dataReply 
	WHERE review_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Review_delete $$
CREATE PROCEDURE procPartnerPC_Shop_Review_delete(
	dataIdx INT
)
BEGIN
	/**
		샵 리뷰 댓글 삭제 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

    UPDATE tb_usage_reviews 
    SET artist_reply = '' 
	WHERE review_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

call procPartnerPC_Shop_Blog_get('pettester@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Blog_get $$
CREATE PROCEDURE procPartnerPC_Shop_Blog_get(
	dataPartnerID VARCHAR(64)
)
BEGIN
	/**
		샵 blog 조회
  */

	SELECT * FROM tb_blog 
	WHERE customer_id = dataPartnerID AND del_yn = 'N';
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Blog_post $$
CREATE PROCEDURE procPartnerPC_Shop_Blog_post(
	dataPartnerID VARCHAR(64),
    dataLink VARCHAR(200),
    dataTitle VARCHAR(200),
    dataDesc TEXT,
    dataThumb TEXT,
    dataPostDate VARCHAR(20),
    dataBlogger VARCHAR(200)
)
BEGIN
	/**
		샵 리뷰 댓글 추가 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

	INSERT INTO tb_blog(customer_id, link, title, tb_blog.desc, thumbnail, post_date, blogger_name) 
    VALUES(dataPartnerID, dataLink, dataTitle, dataDesc, dataThumb, dataPostDate, dataBlogger);
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Blog_put $$
CREATE PROCEDURE procPartnerPC_Shop_Blog_put(
	dataIdx INT,
    dataLink VARCHAR(200),
    dataTitle VARCHAR(200),
    dataDesc TEXT,
    dataThumb TEXT,
    dataPostDate VARCHAR(20),
    dataBlogger VARCHAR(200)
)
BEGIN
	/**
		샵 리뷰 댓글 추가 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

    UPDATE tb_blog 
    SET del_yn = 'N', link = dataLink, title = dataTitle, tb_blog.desc = dataDesc,
		thumbnail = dataThumb, post_date = dataPostDate, blogger_name = dataBlogger, update_date = CURRENT_TIMESTAMP
	WHERE blog_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;



DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Shop_Blog_delete $$
CREATE PROCEDURE procPartnerPC_Shop_Blog_delete(
	dataIdx INT
)
BEGIN
	/**
		샵 리뷰 댓글 추가 
  */
	DECLARE aErr INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
    
    START TRANSACTION;

    UPDATE tb_blog 
    SET del_yn = 'Y', update_date = CURRENT_TIMESTAMP
	WHERE blog_seq = dataIdx;
    
    IF aErr < 0 THEN
		ROLLBACK;
    ELSE
		COMMIT;
    END IF;
    
    SELECT aErr AS err;   
    
END $$ 
DELIMITER ;