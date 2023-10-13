# Опис тестового завдання

Використані існтрументи:<br> 
Python 3.11<br> 
Фреймворк: Django та DRF<br> 
СКБД: MySQL<br> 


Реалізовані методи та моделі знаходтся в TestAPI/API<br> 

Дати в базі даних повинні зберігатися в форматі YYYY-MM-DD<br> 

Реалізованні методи:<br> 
user_credits - GET метод з URL-адресою "host/user_credits/<int:user_id>", де <int:user_id> - id клієнта.<br>
Повертає інформацію про всі кредити вказаного клієнта у вигляді JSON.<br>
JSON містить:
- credits - масив кредитів клієнта
	- кожен елемент масиву credits містить:
	- issuance_date - дата видачі кредиту
	- return_date - дата повернення кредиту
	- body - сума виданого кредиту
	- percent - сума нарахованих відсотків
	- close - статус кредиту (true - кредит закрит, false - кредит відкритий)
	- якщо кредит закрит (close=true):
		- payments_sum - сума платежів за кредитом
	- якщо кредит відкритий (close=false):
		- overdue_days - кілкість просрочених днів
		- payments_sum_body - сума платежів за тілом кредиту
		- payments_sum_percent - сума платежів за відстоками кредиту


plans_insert - POST метод з URL-адресою "host/plans_insert"<br>
Отримує csv файл, зчитує з нього дані про плани, додає плани в базу даних, повертає результат успішності/неуспішності додавання в базу даних у вигляді JSON.<br>
Вхідний csv файл в першому рядку повинен містити наступні назви стовпців:
- period - дата плану
- category - назва катекорії плану
- sum - сума плану
В наступних рядка міститься дані планів.<br>
Cтовпці повинні бути розділенні одним символом табуляції.<br>
JSON містить:
- plans - масив результату додавання планів в базу даних
	- Кожен елемент масиву plans містить:
	- period - дата плану
	- category - назва катекорії плану
	- sum - сума плану
	- success - успішність додавання в базу даних (true - план додано в базу даних, false - план не додано в базу даних)
	- message - повідомлення успішності/неуспішності додавання в базу даних


plans_performance - GET метод з URL-адресою "host/plans_performance?date=\<date\>", де \<date\> -  дата, станом на яку відбувається перевірка виконання планів в форматі d.m.Y .<br>
Приймає дату та повертає дані про усі плани, що мают дату меншу за задану, у вигляді JSON.<br>
JSON містить:
- plans - масив планів
	- кожен елемент масиву plans містить:
	- period - місяц плану у вигляді YYYY-MM-DD
	- category - категорія плану
	- sum - сума плану
	- percent - відсоток виконання плану
	- якщо категорія плану "видача":
		- credits_sum - сума виданих кредитів
	- якщо категорія плану "збір":
		- payments_sum - сума платежів


year_performance - GET метод з URL-адресою "host/year_performance?year=\<year\>", де \<year\> - рік за який збирается статистика.<br>
Отримує рік та повертає зведену помісячну інформацію у вигляді JSON.<br>
JSON містить:
- months - масив місяців
	- кожен елемент масиву months містить:
	- period - дата місяцю у вигляді m.Y
	- credits_count - кількість виданих кредитів
	- credits_sum - сума тіл виданих кредитів
	- year_credits_percent - відсоток суми виданих кредитів за місяц відносно суми виданих кредитів за рік
	- payments_count - кілкість платежів
	- payments_sum - сума платежів
	- year_payments_percent - відсоток суми платежів за місяц відносно суми платежів за рік
	- credits_plan_sum - сума плана "видача"
	- credits_percent - відсоток суми виданих кредитів за місяц відносно плану місяця
	- payments_plan_sum - сума плана "збір"
	- payments_percent - відсоток суми платежів за місяц відносно плану місяця<br>
Поля credits_plan_sum, credits_plan_sum, credits_percent, payments_plan_sum, payments_plan_sum, payments_percent можуть бути відсутні якщо в базі даних відсутні відповідні плани.<br>
Поля year_credits_percent, year_payments_percent, credits_percent, payments_percent можуть бути відсутні якщо значеня відносно яких рахуеться відсоток дорівнює 0 (уникнення ділення на 0).	<br>