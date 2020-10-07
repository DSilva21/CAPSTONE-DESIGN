CREATE DEFINER=`root`@`localhost` PROCEDURE `test`()
begin
	DECLARE done INTEGER DEFAULT 0;
    declare test_id int;
    declare test_n varchar(20);
    declare test_F varchar(20);
    declare test_S varchar(20);
    declare openCursor cursor for select * FROM update_list;
    declare continue handler for not found set done =true;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
	BEGIN
	set @query = CONCAT("UPDATE " ,test_n," SET  `",test_S," ` =  `",test_S," `+1 where id= '",test_F,"'");
	prepare get_count from @query;
	execute get_count;
	END;
	open openCursor;
	read_loop:LOOP
	fetch openCursor into test_id,test_n,test_F,test_S;
		IF done THEN
			LEAVE read_loop;	
		END IF;
        set @query = CONCAT("UPDATE " ,test_n," SET 가중치=가중치+1 where id= '",test_F,"'");
        prepare get_count from @query;
        execute get_count;
        set @query = CONCAT("UPDATE " ,test_n," SET ",test_S," = ",test_S,"+1 where id= '",test_F,"'");
        prepare get_count from @query;
        execute get_count;
	end loop read_loop;
	CLOSE openCursor;
    delete from update_list;
    commit;
END