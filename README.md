# SDTestProject

**Objective:**
This project has two parts. The first part is a system that runs a mysql docker container and stores data from CSV file to a created database. The second part discusses about a database system about how to store image data (with annotations) and retrieve/restore to/from the system.

**Part-1: Data Insert to mysql docker container**

Below are the steps to run the project in your system.

**A. Install Dependencies**

1. Instal Docker
2. Install Python 3
3.  Install sqlalchemy and pymysql
a. pip install  sqlalchemy
b. pip install  pymysql

**B. Project Setup**
1. Clone or download the project
2. In the project root folder, there is a yml file named docker-compose.yml. Open the file and change the path of line 13 to your desired folder path to indicate mounted volume.
3. Go to the project root folder using terminal and run the command: 
docker-compose up
This will download a mysql docker container (for the first run only) and will create a database for storing our data.
4. Create a folder named "china-mobile-user-gemographics" inside root folder of project. Now we need to download our data. Go to https://www.kaggle.com/chinapage/china-mobile-user-gemographics/  and download all the csv files and keep them inside the "china-mobile-user-gemographics" folder you just created.
5. Go to your docker CLI and go to mysql by running this command:
mysql -P 3306 --protocol=tcp -u root -p
6. Now once you are in mysql, run this below command:
GRANT ALL PRIVILEGES ON test_db.* to 'root'@'%';
(the program was unable to insert data because of some permission issues. After giving all preveleges to root, it worked. That's the reason for this command)

**C. Project Run**

	Run database_creator.py (you can use command like "python  database_creator.py" or if you 	are running from spyder editor, you can simply press F5)

**Output**

It takes hours to complete all the insertion of CSV to database. Once it is done, to verify, we can go to docker CLI > mysql (as we did in step-5 of Project Setup). Then we can :
a. run :  "show databases;" (This will show us available databases. Our created one is named "test_db" )
b. run: "use test_db;"
c. run: "show tables;"
d. for each table, run : "select count(*) from TABLE_NAME;" and you will be able to see the number of rows for each table that matches with each of the CSV files.

Below are some sample screenshots of mysql that shows total number of rows inserted:
![Image1](https://github.com/SadiHassan/SDTestProject/tree/master/img/1.png)
![Image2](https://github.com/SadiHassan/SDTestProject/tree/master/img/2.png)

