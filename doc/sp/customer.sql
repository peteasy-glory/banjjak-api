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
    