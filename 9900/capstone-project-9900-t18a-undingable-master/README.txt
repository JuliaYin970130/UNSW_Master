E-commence Recommendation System -- Build a recommendation system for fragrance

Github link: https://github.com/unsw-cse-comp3900-9900-21T3/capstone-project-9900-t18a-undingable.git

<!-- ABOUT THE PROJECT -->

## About The Project

This project will provide an e-commerce website based on a recommendation system, and itsmain product is fragrance. Under the influence of the covid-19, online shopping has become one ofpeople’s main shopping methods.After investigating a large number of existing fragrance websites, it is difficult for us to find awebsite that can recommend perfume according to users’ personal preferences. Especially for thosewho do not have the experience of buying perfume, it is difficult for them to choose the perfume thatsuits their taste accurately.Therefore, in order to enhance the user’s purchase experience and ensure that users can buy thefragrance products they want, our team will provide a perfume online shopping website with arecommendation system.
The project structure is attached above:


```
PROJECT ROOT
│  .gitignore - ignoring files in git
│  README.md - contains information about other files
│  docker-compose.yml
│  
├─ back-end
│   ├─ .classpath
│   ├─ .factorypath
│   ├─ .project
│   ├─ .settings
│   │    ├─ org.eclipse.core.resources.prefs
│   │    ├─ org.eclipse.jdt.apt.core.prefs
│   │    ├─ org.eclipse.jdt.core.prefs
│   │    └─ org.eclipse.m2e.core.prefs
│   ├─ docker
│   │    └─ settings.xml
│   ├─ pom.xml
│   ├─ src
│   │    └─ main
│   │           ├─ java
│   │           └─ resources
│   └─ target
│        ├─ classes
│        │    ├─ application.yaml
│        │    ├─ com
│        │    ├─ generator.properties
│        │    ├─ generatorConfig.xml
│        │    └─ log4j2-spring.xml
│        ├─ generated-sources
│        │    └─ annotations
│        ├─ generated-test-sources
│        │    └─ test-annotations
│        ├─ maven-status
│        │    └─ maven-compiler-plugin
│        └─ test-classes
│
├─ front-end
│   ├─ .env.development.local
│   ├─ .gitignore
│   ├─ README.md
│   ├─ craco.config.js
│   ├─ node_modules
│   ├─ package-lock.json
│   ├─ package.json
│   ├─ public
│   │    ├─ Image
│   │    ├─ api
│   │    ├─ favicon.ico
│   │    ├─ index.html
│   │    ├─ logo192.png
│   │    ├─ logo512.png
│   │    ├─ manifest.json
│   │    └─ robots.txt
│   ├─ run.sh
│   ├─ src
│   │    ├─ App.jsx
│   │    ├─ App.less
│   │    ├─ App.test.js
│   │    ├─ apis
│   │    │    ├─ admin.js
│   │    │    ├─ base.js
│   │    │    ├─ comment.js
│   │    │    ├─ localbase.js
│   │    │    ├─ order.js
│   │    │    ├─ product.js
│   │    │    ├─ shoppingCart.js
│   │    │    └─ user.js
│   │    ├─ components
│   │    │    ├─ Header
│   │    │    ├─ Item
│   │    │    └─ SearchList
│   │    ├─ index.css
│   │    ├─ index.js
│   │    ├─ layouts
│   │    │    └─ DefaultLayout
│   │    ├─ logo.svg
│   │    ├─ pages
│   │    │    ├─ Admin
│   │    │    ├─ AdminManage
│   │    │    ├─ Cart
│   │    │    ├─ Checkout
│   │    │    ├─ Evaluation
│   │    │    ├─ Home
│   │    │    ├─ ItemInfo
│   │    │    ├─ ItemManage
│   │    │    ├─ Login
│   │    │    ├─ Questionaire
│   │    │    ├─ Register
│   │    │    ├─ Search
│   │    │    └─ User
│   │    ├─ setupTests.js
│   │    └─ utils
│   │           └─ index.js
│   └─ working_log.md
└─ Sql
     └─ fragrance_commerce_1108_1916.sql
```

### Built With

- React
- Spring boot
- MySQL
- Docker



## Getting Started

### Prerequisites

Please make sure that your local environment has installed all the required content listed below

#### Back-end

- jdk 8.0

  ```sh
  apt-get install openjdk-8-jdk
  ```

- Maven 3.8.3 - SDK 1.8

#### Front-end

- npm (7.24.0) or yarn (v1.22.15)

  ```sh
  npm install
  # or
  yarn install
  ```

- Ant design (4.17.0 - alpha.9)

  ```sh
  yarn add antd
  ```

- Customise Ant design theme

  ```sh
  yarn add @craco/craco
  yarn add craco-less
  ```

#### Database

- MySQL (Ver 8.0.27)

#### Docker

- Docker CE
- docker-compose(v1)

<!-- USAGE EXAMPLES -->

## Usage

If your environment do not have **docker**, please run the project via following command:

1. Clone the code:

   ```sh
   git clone git@github.com:unsw-cse-comp3900-9900-21T3/capstone-project-9900-t18a-undingable.git my-project
   cd my-project
   ```

2. Import SQL file

   Please find **application.yaml** and **generator.properties** in below path:

   ```sh
   cd /capstone-project-9900-t18a-undingable/Back-end/src/main/resources
   ```

   Please replace 'db' by 'localhost' in url part in those two files.

   And replace '123456' by the mysql root account password in password part in those two files.

   
   SQL file **fragrance_commerce_1108_1916.sql** can be found in /capstone-project-9900-t18a-undingable/Sql

   

3. Run back-end 

   ```sh
   cd /capstone-project-9900-t18a-undingable/Back-end
   mvn spring-boot:run
   ```

4. Run front-end

   ```sh
   cd /capstone-project-9900-t18a-undingable/Front-end/front_end
   npm start
   # or
   yarn start
   ```

5. Open the browser at http://localhost:3000/

6. If terminal shows "Proxy error", please find **package.json** in /capstone-project-9900-t18a-undingable/Front-end/front_end

   Replace "proxy": "http://backend:8080" by "proxy": "http://localhost:8080",

## Usage by docker-compose

Requirements:

- Docker CE
- docker-compose(v1)

start services:

```sh
docker-compose up -d
```

> May wait a few min on first start, because need install dependencies.

restart single service by dev:

```sh
docker-compose restart fronted
docker-compose restart backend
docker-compose restart db
```

import(replace) data by sql file:

```sh
docker exec -i capstone-project-9900-t18a-undingable-db-1  sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < ./Sql/fragrance_commerce_1107_1717.sql
```

If there are any errors, you may need to change some contents in docker-compose.yml 

<!-- LICENSE -->

## License

Distributed under the MIT `LICENSE` .


<!-- CONTACT -->

## Contact

Jiahui Wang - (z5274762@ad.unsw.edu.au) - email

Minxi Xie - (z5245010@ad.unsw.edu.au) - email

Shou Wang - (z5238502@ad.unsw.edu.au) - email

Andy Wu - (z5273525@ad.unsw.edu.au) - email

Jiaqi Yin - (z5239331@ad.unsw.edu.au) - email

Project Link: [https://github.com/unsw-cse-comp3900-9900-21T3/capstone-project-9900-t18a-undingable](https://github.com/unsw-cse-comp3900-9900-21T3/capstone-project-9900-t18a-undingable)

