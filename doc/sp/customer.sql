

    SELECT AA.*, IF((LENGTH(BB.customer_id) > 0 ), BB.customer_id, funcTmpUserIndex(AA.cellphone)) AS id, 
    BB.pet_seq, BB.name, BB.year, BB.month, BB.day, BB.hour, BB.minute, BB.product 
    FROM (
		SELECT cellphone, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) AS ymdhm
		FROM tb_payment_log 
		WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr'
		GROUP BY cellphone
	) AA LEFT JOIN  
    (
		SELECT A.*, B.name, B.pet_type, CONCAT(A.year,LPAD(A.month,2,0),LPAD(A.day,2,0),LPAD(A.hour,2,0),LPAD(A.minute,2,0)) AS ymdhm
        FROM tb_payment_log A JOIN tb_mypet B ON A.pet_seq = B.pet_seq  
        WHERE A.data_delete = 0 AND A.artist_id = 'pettester@peteasy.kr'
			AND A.is_cancel = 0 AND A.is_no_show = 0
            
	) BB  ON AA.cellphone = BB.cellphone AND AA.ymdhm = BB.ymdhm

    
    ORDER BY A.cellphone ASC;

	SELECT * 
    FROM tb_tmp_user 
    WHERE cellphone = '01086331776'    
    ;
    SELECT * 
    FROM tb_customer
    WHERE cellphone = '01074856419'    
    ;
    
    select funcGradeOfCustomer('pettester@peteasy.kr', 'hyejin_85@naver.com');
    SELECT A.grade_name INTO @grade_name 
    FROM tb_grade_of_shop A JOIN tb_grade_of_customer B
		ON A.idx = B.grade_idx
    WHERE A.artist_id = 'pettester@peteasy.kr' AND A.is_delete = 0
			AND B.customer_id = 'hyejin_85@naver.com';
    select @grade_name;
    
    select * from tb_grade_of_customer
    where customer_id = 'hyejin_85@naver.com';
    
    select * from tb_grade_of_shop
    where idx in (982,1429,2203);
    
    
    SELECT cellphone, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) AS ymdhm
		FROM tb_payment_log 
		WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr'
		GROUP BY cellphone
    
			AND pl.cellphone != ''
						AND (pl.pet_seq != '' OR pl.pet_seq != '0')
						AND pl.data_delete = '0'
					GROUP BY pl.cellphone
cellphone     ) B ) LIMIT 0, 10000	Error Code: 1248. Every derived table must have its own alias	0.0050 sec

(
	SELECT 'b'AS payment_type, cellphone, MAX(CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0))) AS ymdhm 
	FROM tb_payment_log 
	WHERE artist_id = 'pettester@peteasy.kr'
	GROUP BY cellphone
	UNION 
	SELECT 'k'AS payment_type, cellphone, MAX(CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0))) AS ymdhm 
	FROM tb_playroom_payment_log
	WHERE artist_id = 'pettester@peteasy.kr'
	GROUP BY cellphone
	UNION 
	SELECT 'h'AS payment_type, cellphone, MAX(CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0))) AS ymdhm 
	FROM tb_hotel_payment_log
	WHERE AND artist_id = 'pettester@peteasy.kr'
	GROUP BY cellphone
) A 

SELECT * 
FROM (
	SELECT payment_log_seq, customer_id, pet_seq, cellphone, year, month, day, hour, minute, product
	FROM tb_payment_log
	WHERE is_cancel = 0 AND is_no_show = 0 AND data_delete = 0 AND artist_id = 'pettester@peteasy.kr'
	ORDER BY CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) DESC
) A 
GROUP BY cellphone
    
    GROUP By cellphone
GROUP BY cellphone
;


SELECT cellphone, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) 
FROM tb_payment_log 
WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr' AND
	(cellphone, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)))
IN 
(
	SELECT cellphone, MAX(CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)))
	FROM tb_payment_log 
    WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr'
	GROUP BY cellphone
) 
ORDER BY cellphone asc
;


SELECT * FROM tb_grade_of_shop WHERE artist_id = 'sally@peteasy.kr' ORDER BY grade_ord ASC

;

				SELECT *
				FROM (
					SELECT 
						pl.cellphone, 
						IFNULL(SUM(pl.local_price), '0') AS sum_local_price, 
						IFNULL(SUM(pl.local_price_cash), '0') AS sum_local_price_cash, 
						pl.pet_seq, 
						mp.pet_seq AS mypet_seq,
					    pl.customer_id,
						IFNULL(mp.name, IFNULL(acl.pet_name, SUBSTRING_INDEX(SUBSTRING_INDEX(pl.product,'|',1),'|',-1))) AS pet_name,					   
						(
							SELECT payment_log_seq
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
							ORDER BY update_time DESC
							LIMIT 0 , 1
						) as payment_log_seq,						 
						(
							SELECT update_time
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
							ORDER BY update_time DESC
							LIMIT 0 , 1
						) as update_time2,
						(
							SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(product,'|',4),'|',-1) AS service
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
                                #AND product LIKE '|'
							ORDER BY update_time DESC
							LIMIT 0 , 1
						) as service,
						(
							SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(product,'|',5),'|',-1) AS service2
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
                                #AND product LIKE '|'
							ORDER BY update_time DESC
							LIMIT 0 , 1
						) as service2,
						(
							SELECT is_cancel
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
							ORDER BY update_time DESC
							LIMIT 0 , 1
						) as is_cancel,
						(
							SELECT IFNULL(cancel_time, '')
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
							ORDER BY update_time DESC
							LIMIT 0 , 1
						) as cancel_time,
						(
							SELECT COUNT(*) as cnt
							FROM tb_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
								AND is_cancel = 0
								AND product_type = 'B'
							LIMIT 0 , 1
						) as cnt,
						mp.type,
						mp.pet_type,
						(
							SELECT IFNULL(ba_seq, '') as ba_seq
							FROM tb_beauty_agree
							WHERE artist_id = 'sally@peteasy.kr'
								AND pet_id = pl.pet_seq
								AND doc_type = '0'
							LIMIT 0 , 1
						) as ba_seq,
						'beauty' AS payment_type,
						(
							SELECT reserve
							FROM tb_user_reserve
							WHERE is_delete = '2'
								AND artist_id = 'sally@peteasy.kr'
								AND cellphone = pl.cellphone
							LIMIT 0 , 1
						) as user_reserve
					FROM tb_payment_log AS pl
						LEFT OUTER JOIN tb_artist_customer_list AS acl ON pl.pet_seq = acl.pet_seq
						LEFT OUTER JOIN tb_mypet AS mp ON pl.pet_seq = mp.pet_seq
					WHERE pl.artist_id = 'sally@peteasy.kr'
						AND pl.cellphone != ''
						AND (pl.pet_seq != '' OR pl.pet_seq != '0')
						AND pl.data_delete = '0'
					GROUP BY pl.cellphone
					
					UNION ALL

					SELECT 
						hpl.cellphone, 
						IFNULL(SUM(hpl.add_price_card), '0') AS sum_local_price, 
						IFNULL(SUM(hpl.add_price_cash), '0') AS sum_local_price_cash, 
						hpl.pet_seq,
						mp.pet_seq AS mypet_seq,
						mp.name AS pet_name,
						hpl.customer_id,
						(
							SELECT order_num
							FROM tb_hotel_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = hpl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as payment_log_seq,
						(
							SELECT IFNULL(update_dt, reg_dt)
							FROM tb_hotel_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = hpl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) AS update_time2,
						(
							SELECT concat(room_name,'/',TIMESTAMPDIFF(DAY, check_in_date, check_out_date),'박/~',weight,' Kg') AS service
							FROM tb_hotel_reservation
							WHERE order_num = hpl.order_num
								AND cellphone = hpl.cellphone
							ORDER BY reg_dt desc
							LIMIT 0 , 1
						) AS service,
						(
							SELECT concat(if(extra_price > 0, '시간추가', ''),if(neutral_price > 0, '중성화', ''),if(pickup_price > 0, '픽업', '')) AS service2
							FROM tb_hotel_reservation
							WHERE artist_id = hpl.order_num
								AND cellphone = hpl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as service2,
						(
							SELECT is_delete
							FROM tb_hotel_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = hpl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as is_cancel,
						(
							SELECT IFNULL(delete_dt, '')
							FROM tb_hotel_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = hpl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as cancel_time,	
						(
							SELECT COUNT(*) as cnt
							FROM tb_hotel_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = hpl.cellphone
							LIMIT 0 , 1
						) as cnt,
						mp.type,
						mp.pet_type,
						(
							SELECT IFNULL(ba_seq, '') as ba_seq
							FROM tb_beauty_agree
							WHERE artist_id = 'sally@peteasy.kr'
								AND pet_id = hpl.pet_seq
								AND doc_type = '1'
							LIMIT 0 , 1
						) as ba_seq,
						'hotel' AS payment_type,
						(
							SELECT reserve
							FROM tb_user_reserve
							WHERE is_delete = '2'
								AND artist_id = 'sally@peteasy.kr'
								AND cellphone = hpl.cellphone
							LIMIT 0 , 1
						) as user_reserve
					FROM tb_hotel_payment_log AS hpl
						INNER JOIN tb_mypet AS mp ON hpl.pet_seq = mp.pet_seq
					WHERE hpl.artist_id = 'sally@peteasy.kr'
						AND hpl.cellphone != ''
						AND (hpl.pet_seq != '' OR hpl.pet_seq != '0')
					GROUP BY hpl.cellphone
					
					UNION ALL

					SELECT 
						ppl.cellphone, 
						IFNULL(SUM(ppl.add_price_card), '0') AS sum_local_price, 
						IFNULL(SUM(ppl.add_price_cash), '0') AS sum_local_price_cash, 
						ppl.pet_seq,
						mp.pet_seq AS mypet_seq,
						mp.name AS pet_name,
						ppl.customer_id,
						(
							SELECT order_num
							FROM tb_playroom_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = ppl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as payment_log_seq,
						(
							SELECT IFNULL(update_dt, reg_dt)
							FROM tb_playroom_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = ppl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) AS update_time2,
						(
							SELECT if(service_type = 1, concat(allday_pass_name), if((room_name * count) <> 0, concat((room_name * count),'시간/~',weight,' Kg'), '')) AS service
							FROM tb_playroom_reservation
							WHERE order_num = ppl.order_num
								AND cellphone = ppl.cellphone
							ORDER BY reg_dt desc
							LIMIT 0 , 1
						) AS service,
						(
							SELECT concat(if(extra_price > 0, '시간추가', ''),if(neutral_price > 0, '중성화', ''),if(pickup_price > 0, '픽업', '')) AS service2
							FROM tb_playroom_reservation
							WHERE artist_id = ppl.order_num
								AND cellphone = ppl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as service2,
						(
							SELECT is_delete
							FROM tb_playroom_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = ppl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as is_cancel,
						(
							SELECT IFNULL(delete_dt, '')
							FROM tb_playroom_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = ppl.cellphone
							ORDER BY reg_dt DESC
							LIMIT 0 , 1
						) as cancel_time,	
						(
							SELECT COUNT(*) as cnt
							FROM tb_playroom_payment_log
							WHERE artist_id = 'sally@peteasy.kr'
								AND cellphone = ppl.cellphone
							LIMIT 0 , 1
						) as cnt,
						mp.type,
						mp.pet_type,
						(
							SELECT IFNULL(ba_seq, '') as ba_seq
							FROM tb_beauty_agree
							WHERE artist_id = 'sally@peteasy.kr'
								AND pet_id = ppl.pet_seq
								AND doc_type = '1'
							LIMIT 0 , 1
						) as ba_seq,
						'playroom' AS payment_type,
						(
							SELECT reserve
							FROM tb_user_reserve
							WHERE is_delete = '2'
								AND artist_id = 'sally@peteasy.kr'
								AND cellphone = ppl.cellphone
							LIMIT 0 , 1
						) as user_reserve
					FROM tb_playroom_payment_log AS ppl
						INNER JOIN tb_mypet AS mp ON ppl.pet_seq = mp.pet_seq
					WHERE ppl.artist_id = 'sally@peteasy.kr'
						AND ppl.cellphone != ''
						AND (ppl.pet_seq != '' OR ppl.pet_seq != '0')
					GROUP BY ppl.cellphone
				) AS a
				 ORDER BY a.update_time2 DESC 
			


SELECT * #cellphone#, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) 
FROM tb_payment_log 
WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr' AND
	(cellphone, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)))
IN 
(
	SELECT cellphone, MAX(CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0))) as y  
	FROM tb_payment_log 
    WHERE data_delete = 0 AND artist_id = 'pettester@peteasy.kr'
	GROUP BY cellphone
) 

select *, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) 
from tb_payment_log 
where payment_log_seq = 571055
;
select payment_log_seq, CONCAT(year,LPAD(month,2,0),LPAD(day,2,0),LPAD(hour,2,0),LPAD(minute,2,0)) 
from tb_payment_log 
where cellphone = '01012350000'
	and data_delete = 0 AND artist_id = 'pettester@peteasy.kr'
order by payment_log_seq desc
;

where cellphone = '010581212222'
;
select * from A where (항목, date) in 
(select 항목,max(date) from A group by 항목)


A LEFT JOIN tb_mypet B ON A.pet_sea = B.pet_seq



loof: LOOP
		FETCH cursorPhones
			INTO aPhone;
		IF EOF THEN
			LEAVE loof;
		END IF;
        SELECT COUNT(*) INTO aNoShow
        FROM tb_payment_log 
        WHERE data_delete = 0 AND is_no_show = 1 AND cellphone = aPhone;
        SET aTotalNoShow = CONCAT(aTotalNoShow, '|', aPhone, '|', aNoShow);
        
    END LOOP;
    CLOSE cursorPhones;
    
    
    
        SELECT * 
    FROM 
    (
		SELECT cellphone, customer_id  FROM tb_payment_log 
        WHERE data_delete = 0 AND artist_id = 'sally@peteasy.kr' GROUP BY cellphone, customer_id;
        select * from tb_tmp_user where cellphone='01082320830'
	) A LEFT JOIN 
    (
		SELECT * FROM tb_customer
		WHERE enable_flag = 1 #and cellphone in ('01039091436', '01025180714', '01053906573', '01053906575', '01053906578', '01084599700')
	) B ON A.cellphone = B.cellphone;
    