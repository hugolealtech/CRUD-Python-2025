Use sudo ufw allow 3306

Banco de Dados Maria DB

CREATE DATABASE crud_flask;
CREATE USER 'flask_user'@'%' IDENTIFIED BY 'sua_senha_segura';
GRANT ALL PRIVILEGES ON crud_flask.* TO 'flask_user'@'%';
FLUSH PRIVILEGES;

USE crud_flask;
SELECT * from item
WHERE id = 3
