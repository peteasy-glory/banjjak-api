/*
###################################################################################
#############################         PC 버전 - 로그인         #######################
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
   DECLARE aVal INT DEFAULT 0;
   DECLARE aErr INT DEFAULT 0;
   DECLARE CONTINUE HANDLER FOR SQLEXCEPTION  SET aErr = -1; 
   
	SELECT password, usr_name , nickname, artist_flag , my_shop_flag INTO aPw, aName, aNick, aFlag, aMyShop
    FROM tb_customer
	WHERE enable_flag = 1
		AND id = dataId;
    IF aPw = '' THEN 
	BEGIN
		SET aVal = 1;
		SELECT aErr AS Err, aVal AS Ret, aName AS Name, aMyShop AS isMyShop; #비밀번호가 틀림
        LEAVE BODY;
    END;
    END IF;
    
    IF aFlag = 1 THEN
		SET aVal = 3; # 작업 미용사
		SELECT name INTO aName FROM tb_shop_artist WHERE artist_id = dataId AND del_yn = 'N' LIMIT 1;
    END IF;

	IF (aFlag = 0 AND aMyShop = 0) THEN
	BEGIN
		SET aVal = 2;
		SELECT aErr AS Err, aVal AS Ret, aName AS Name, aMyShop AS isMyShop; #미용사 아님(일반고객)
        LEAVE BODY;
    END;
    END IF;
    
	START TRANSACTION;
    
	UPDATE tb_customer 
    SET last_login_time = NOW(), last_applogin_time=now() 
	WHERE id = dataId AND nickname = aNick;

	IF aErr < 0 THEN
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
	
    SELECT aErr AS Err, aVal AS Ret, aName AS Name, aMyShop AS isMyShop;

END $$ 
DELIMITER ;

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

END $$ 
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_LogOut_get $$
CREATE PROCEDURE procPartnerPC_LogOut_get(
		dataId VARCHAR(64)
)
BEGIN
	/**
		로그아웃 하기
   */


END $$ 
DELIMITER ;

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

END $$ 
DELIMITER ;

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

END $$ 
DELIMITER ;

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

END $$ 
DELIMITER ;
   
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

END $$ 
DELIMITER ;

call procPartnerPC_Login_Ceo_get('tmp_test@peteasy.kr');
DELIMITER $$
DROP PROCEDURE IF EXISTS procPartnerPC_Login_Ceo_get $$
CREATE PROCEDURE procPartnerPC_Login_Ceo_get(
	dataWorkerID VARCHAR(64)
)
BEGIN
	/**
		대표 아이디 찾기. 
  */

	SELECT * FROM gobeautypet.tb_shop_artist
	where artist_id = dataWorkerID
		AND del_yn = 'N';
    
END $$ 
DELIMITER ;

select * from tb_payment_log where buy_time > '2022-05-01' payment_log_seq = 571053;
select * from tb_payment_log where payment_log_seq = 550457;571053

#//////////////////////////////////////////
# /////////////////////////////////////////
#오리|개|반짝펫살롱|중형견미용|목욕|6:25000|브로콜리컷:10000|4:4000|장모_목욕:5000,이중모_목욕:10000|5000|10000|10000
#|||0|3|스파1:6000|스파2:9000|스파3:15000|0|3|기장추가1:5000|기장추가2:10000|기장추가3:15000
#|3|13|1993:놀이구:200:2|1988:상품2:900:2|1992:하네스:600:2|1994:닭고기:800:2|1995:돼지고기:2700:2|1996:소고기:4100:2|2004:사료1:300:2|2003:사료2:400:2|2002:사료3:200:2|2010:털엉킴1:100:2|2009:입질1:1000:2|2007:털엉킴2:200:2|2008:입질10:10000:2|
# /////////////////////////////////////////
#오리|개|반짝펫살롱|중형견미용|부분미용|6:25000|기본얼굴컷:1000|4:4000|이중모_목욕:10000|5000||| //0~11.
#|||0|1|스파2:9000|0|1|기장추가3:15000|0|8|1993:놀이구:200:2|1988:상품2:900:2|1997:오리고기:700:2|1994:닭고기:800:2|2004:사료1:300:2|2003:사료2:400:2|2010:털엉킴1:100:2|2009:입질1:1000:2|
#오리|개|반짝펫살롱|중형견미용|부분미용|6:25000|기본얼굴컷:1000|4:4000|이중모_목욕:10000|5000|10000|10000|
#|||0|3|스파1:6000|스파2:9000|스파3:15000|0|3|기장추가1:5000|기장추가2:10000|기장추가3:15000|0|0|
#글로리|개|반짝펫살롱|소형견미용|부분미용|3:15000|||||||||1|:0|0|0|0|0|0"
/*. 인덱스:쿠폰명:가격
//강아지
0.펫이름|
1.펫 종류(개,고양이)|
2.샵이름|
3.크기(소형견미용,중형견미용 등)|
4.미용상품(부분미용, 목욕, 위생 등)|
5.무게:추가요금(2:6000 => ~2kg이면 6000원)|
6.얼굴컷:추가요금|
7.미용털길이:추가요금|
8.털특징:추가요금(이중모:5000)|
9.발톱의가격(3000)|
10.장화의가격(4000)|
11.방울의가격(5000)|
미확인|
미확인|
14.다리추가서비스 중 선택할 갯수(기존 발톱, 장화, 방울을 선택했다면 0, 샵에 운동화컷, 구두컷 두개 상품이 추가되어있을때 하나를 선택하면 1, 두개 다 선택하면 2, 선택한 것 만큼 바로 뒤에 추가로 운동화컷:1000 추가)|
15.스파선택상품개수|
스파1:1000|
염색선택개수|
브릿지:3000|
기타선택개수|
기타1:3000|
쿠폰구매개수|
쿠폰시퀀스:쿠폰명:가격
제품구매수|
용품시퀀스:제품명:가격:개수(해당 카테고리에서 더 구매했다면 바로 뒤에 추가)|
간식시퀀스:제품명:가격:개수|
사료시퀀스:제품명:가격:개수|
기타제품시퀀스:제품명:가격:개수|

//고양이
고양이|고양이|반짝펫살롱|3:11000||5000|24500|0|1|796:월목욕 소형견 128516;:100000|8|
1993:놀이구:200:1|1988:상품2:900:1|1997:오리고기:700:1|1994:닭고기:800:1|2004:사료1:300:1|2003:사료2:400:1|2010:털엉킴1:100:1|2009:입질1:1000:1|
펫이름 | 펫타입 | 펫샵이름 | 미용 | kg:추가가격 | 장,단모:가격 | 발톱가격 | 단모목욕가격 | 장모목욕가격 | 기타추가개수 | 추가상품 | 제품구매수 | 쿠폰구매수
ex)
가회원|고양이|글로리샵|미용|7.1:10000|단모:45000  |1500     |500     |        |1       |손톱:2000|0|0
-> 7.1kg 단모미용 + 발톱 + 단모목욕 + 추가etc 1개: 손톱
가회원|고양이|글로리샵|미용|7.1:0      |장모:60000  |1500     |          |1000  |2       |손톱:2000|손발톱:2500|0|0|
-> 7.1kg 장모미용 + 발톱 + 장모목욕 + 추가etc 2개 손톱 + 손발톱

*/
