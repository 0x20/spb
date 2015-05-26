insert into smarterspacebrain.user (id, firstname, lastname, city, country, member)
          values (1, 'Joris', 'Van Looveren', 'Gent', 'Belgium', true);
insert into smarterspacebrain.user (id, firstname, lastname, city, country, member)
          values (2, 'Jan', 'Vandersmissen', 'Terneuzen', 'Nederland', false);

insert into smarterspacebrain.phonenumbers (user_id, phonenumber, cellphone)
          values (1, '0496456701', true);
insert into smarterspacebrain.phonenumbers (user_id, phonenumber, cellphone)
          values (1, '092345678', false);
insert into smarterspacebrain.phonenumbers (user_id, phonenumber, cellphone)
          values (2, '0456123456', true);

insert into smarterspacebrain.badgenumbers (user_id, badgenumber, own)
          values (1, 'AE:34:FD:65:45', true);

