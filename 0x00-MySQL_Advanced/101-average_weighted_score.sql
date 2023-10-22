-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

-- Requirements:

-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.


DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS UX,
        (SELECT UX.id, SUM(score * weight) / SUM(weight) AS WX_AVG_SCORE
                FROM users AS UX
                JOIN corrections as CX ON UX.id=CX.user_id
                JOIN projects AS PX ON CX.project_id=PX.id
                GROUP BY UX.id)
        AS UWX
        SET UX.average_score = UWX.WX_AVG_SCORE
        WHERE UX.id=UWX.id;
END$$
DELIMITER ;