SELECT
(
    CASE
        WHEN Age<= 40 THEN 'Genç'
        WHEN Age> 40 AND Age<=55 THEN 'Orta Yaş'
        WHEN Age> 55 AND Age<=75 THEN 'Yaşlı'
        WHEN Age> 75 THEN 'İleri Yaş'        
    END
    
) as 'AgeGroup',
CommuteDistance,
EnglishEducation,
Gender,
HouseOwnerFlag,
MaritalStatus,
NumberCarsOwned,
NumberChildrenAtHome,
EnglishOccupation,
Region,
TotalChildren,
YearlyIncome,
BikeBuyer
FROM t1