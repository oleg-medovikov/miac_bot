select 'Нет МО прикрепления' as [Тип ошибки], s.[УНРЗ],s.[ФИО],s.[Дата рождения],s.[СНИЛС],s.[Вид лечения],
	s.[Медицинская организация],s.[МО прикрепления], s.[Исход заболевания], s.[Дата исхода заболевания],
	s.[Диагноз],s.[Диагноз установлен],DATEDIFF(day,s.[Дата исхода заболевания],getdate()) as 'Дней в статусе перевода'
	from
(select dbo.get_Gid(idPatient) as 'Gid',* 
	from robo.v_FedReg
	where [Исход заболевания] in ('Перевод пациента в другую МО',
								'Перевод пациента на амбулаторное лечение',
								'Перевод пациента на стационарное лечение')
			and [МО прикрепления] = ''
            and DATEDIFF(day,[Дата исхода заболевания],getdate())  > 7
	) as s