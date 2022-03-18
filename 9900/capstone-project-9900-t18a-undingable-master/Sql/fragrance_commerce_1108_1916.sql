/*
 Navicat Premium Data Transfer

 Source Server         : Centos
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : 192.168.153.128:3306
 Source Schema         : fragrance_commerce

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 08/11/2021 19:16:17
*/

USE fragrance_commerce;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for OrderDetail
-- ----------------------------
DROP TABLE IF EXISTS `OrderDetail`;
CREATE TABLE `OrderDetail`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `orderId` bigint NOT NULL,
  `productId` bigint NOT NULL,
  `price` bigint NULL DEFAULT NULL,
  `quantity` bigint NULL DEFAULT NULL,
  `comment` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `stars` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `productIDFKK`(`productId`) USING BTREE,
  INDEX `orderIdFKKK`(`orderId`) USING BTREE,
  CONSTRAINT `productIDFKK` FOREIGN KEY (`productId`) REFERENCES `Product` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `orderIdFKKK` FOREIGN KEY (`orderId`) REFERENCES `Orders` (`orderId`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of OrderDetail
-- ----------------------------
INSERT INTO `OrderDetail` VALUES (1, 1, 1, 59900, 2, 'The product is so nb!!!!', 5);
INSERT INTO `OrderDetail` VALUES (2, 1, 4, 55550, 1, 'This is a test comment.', 3);
INSERT INTO `OrderDetail` VALUES (3, 4, 2, 50010, 30, 'So bad comment.', 2);
INSERT INTO `OrderDetail` VALUES (4, 11, 1, 14440, 4, '', 0);

-- ----------------------------
-- Table structure for Orders
-- ----------------------------
DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders`  (
  `orderId` bigint NOT NULL AUTO_INCREMENT,
  `userId` bigint NULL DEFAULT NULL,
  `orderTime` datetime NULL DEFAULT NULL,
  `amount` bigint NULL DEFAULT NULL COMMENT 'Total amount of money',
  PRIMARY KEY (`orderId`) USING BTREE,
  INDEX `userIDFKK`(`userId`) USING BTREE,
  CONSTRAINT `userIDFKK` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Orders
-- ----------------------------
INSERT INTO `Orders` VALUES (1, 1, '2021-11-07 15:18:52', 590);
INSERT INTO `Orders` VALUES (4, 2, '2021-11-07 16:30:11', 800);
INSERT INTO `Orders` VALUES (9, 1, '2021-11-08 18:56:30', 3232);
INSERT INTO `Orders` VALUES (10, 1, '2021-11-08 19:00:27', 3232);
INSERT INTO `Orders` VALUES (11, 1, '2021-11-08 19:01:02', 3232);

-- ----------------------------
-- Table structure for Product
-- ----------------------------
DROP TABLE IF EXISTS `Product`;
CREATE TABLE `Product`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `gender` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `brand` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `scent_notes` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `price` bigint NULL DEFAULT NULL,
  `size` bigint NULL DEFAULT NULL,
  `img_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `stock` bigint NULL DEFAULT NULL,
  `description` varchar(1000) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Product
-- ----------------------------
INSERT INTO `Product` VALUES (1, 'Adventus', 'Men', 'Creed', 'Fruity', 34900, 50, '../Image/1.jpg', 100, 'Aventus by Creed is a Chypre Fruity fragrance for men. Aventus was launched in 2010. Aventus was created by Olivier Creed and Erwin Creed. Top notes are Pineapple, Bergamot, Black Currant and Apple; middle notes are Birch, Patchouli, Moroccan Jasmine and Rose; base notes are Musk, oak moss, Ambergris and Vanille.');
INSERT INTO `Product` VALUES (2, 'Bitter Peach', 'Unisex', 'Tom Ford', 'Amber', 47154, 50, '../Image/2.jpg', 100, 'Bitter Peach by Tom Ford is a Amber Vanilla fragrance for women and men. This is a new fragrance. Bitter Peach was launched in 2020. Top notes are Peach, Blood Orange, Cardamom and Heliotrope; middle notes are Rum, Cognac, Davana and Jasmine; base notes are Indonesian Patchouli Leaf, Vanilla, Sandalwood, Tonka Bean, Cashmeran, Benzoin, Styrax, Labdanum and Vetiver.');
INSERT INTO `Product` VALUES (3, 'Coco Mademoiselle', 'Women', 'Chanel', 'Amber', 24818, 100, '../Image/3.jpg', 100, 'Coco Mademoiselle by Chanel is a Amber Floral fragrance for women. Coco Mademoiselle was launched in 2001. The nose behind this fragrance is Jacques Polge. Top notes are Orange, Mandarin Orange, Bergamot and Orange Blossom; middle notes are Turkish Rose, Jasmine, Mimosa and Ylang-Ylang; base notes are Patchouli, White Musk, Vanilla, Vetiver, Tonka Bean and Opoponax. This perfume is the winner of award FiFi Award Best National Advertising Campaign / TV 2008.');
INSERT INTO `Product` VALUES (4, 'Omnia Crystalline', 'Women', 'Bvlgari', 'Floral', 7712, 65, '../Image/4.jpg', 100, 'Omnia Crystalline by Bvlgari is a Floral Aquatic fragrance for women. Omnia Crystalline was launched in 2005. The nose behind this fragrance is Alberto Morillas. Top notes are Bamboo and Pear; middle notes are Lotus, Tea and Cassia; base notes are Musk, Guaiac Wood and Oakmoss.');
INSERT INTO `Product` VALUES (5, 'CK One', 'Unisex', 'Calvin Klein', 'Citrus', 4690, 195, '../Image/5.jpg', 100, 'CK One by Calvin Klein is a Citrus Aromatic fragrance for women and men. CK One was launched in 1994. CK One was created by Alberto Morillas and Harry Fremont. Top notes are Lemon, Green Notes, Bergamot, Pineapple, Mandarin Orange, Cardamom and Papaya; middle notes are Lily-of-the-Valley, Jasmine, Violet, Nutmeg, Rose, Orris Root and Freesia; base notes are Green Accord, Musk, Cedar, Sandalwood, Oakmoss, Green Tea and Amber.');
INSERT INTO `Product` VALUES (6, 'J''adore', 'Women', 'Dior', 'Floral', 24599, 150, '../Image/6.jpg', 100, 'J''adore by Dior is a Floral Fruity fragrance for women. J''adore was launched in 1999. The nose behind this fragrance is Calice Becker. Top notes are Pear, Melon, Magnolia, Peach, Mandarin Orange and Bergamot; middle notes are Jasmine, Lily-of-the-Valley, Tuberose, Freesia, Rose, Orchid, Plum and Violet; base notes are Musk, Vanilla, Blackberry and Cedar. This perfume is the winner of award FiFi Award Best National Advertising Campaign / TV 2007.');
INSERT INTO `Product` VALUES (7, 'Gucci Guilty Absolute', 'Men', 'Gucci', 'Amber', 8547, 50, '../Image/7.jpg', 100, 'Gucci Guilty Absolute by Gucci is a Amber Woody fragrance for men. Gucci Guilty Absolute was launched in 2017. The nose behind this fragrance is Alberto Morillas. Top note is Leather; middle notes are Cypress and Patchouli; base notes are Woody Notes and Vetiver.');
INSERT INTO `Product` VALUES (8, 'Shalimar Eau de Parfum', 'Women', 'Guerlain', 'Amber', 12820, 90, '../Image/8.jpg', 100, 'Shalimar Eau de Parfum by Guerlain is a Amber Spicy fragrance for women. Shalimar Eau de Parfum was launched in 1990. The nose behind this fragrance is Jacques Guerlain. Top notes are Citruses, Bergamot, Lemon, Cedar and Mandarin Orange; middle notes are iris, Patchouli, Vetiver, Jasmine and Rose; base notes are Incense, Vanilla, Leather, Opoponax, Sandalwood, Civet, Tonka Bean and Musk.');
INSERT INTO `Product` VALUES (9, 'Terre d''Hermes', 'Men', 'Hermas', 'Woody', 22336, 200, '../Image/9.jpg', 100, 'Terre d''Hermes by Hermès is a Woody Spicy fragrance for men. Terre d''Hermes was launched in 2006. The nose behind this fragrance is Jean-Claude Ellena. Top notes are Orange and Grapefruit; middle notes are Pepper and Pelargonium; base notes are Vetiver, Cedar, Patchouli and Benzoin. This perfume is the winner of award FiFi Award Fragrance Of The Year Men`s Luxe 2007.');
INSERT INTO `Product` VALUES (10, 'Sauvage', 'Men', 'Dior', 'Fresh', 10292, 100, '../Image/10.jpg', 100, 'Sauvage by Dior is a Aromatic Fougere fragrance for men. Sauvage was launched in 2015. The nose behind this fragrance is Francois Demachy. Top notes are Calabrian bergamot and Pepper; middle notes are Sichuan Pepper, Lavender, Pink Pepper, Vetiver, Patchouli, Geranium and elemi; base notes are Ambroxan, Cedar and Labdanum.');
INSERT INTO `Product` VALUES (11, 'Halfeti', 'Women', 'PENHALIGON''S', 'Woody', 34900, 100, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/b13a849db34e96e1116b56a19b4de8b45dd52d29_720x.jpg?v=1601947680', 100, 'A potion so delightfully intoxicating one falls immediately in love. Warm, strong and reassuring all at once. All respectability forgotten, we have travelled far, as far as Turkey! And here in Halfeti, the red roses appear black so intense is their magic. Top notes: Grapefruit, Bergamot, Green notes, Armoise, Cypress. Heart notes: Cumin, Nutmeg, Violet, Saffron, Rose, Jasmine, Muguet. Base notes: Leather, Oud, Amber, Resins, Tonka, Vanilla, Sandalwood');
INSERT INTO `Product` VALUES (12, 'Amber Aoud Absolue Precieux', 'Men', 'ROJA PARFUMS', 'Woody', 155000, 30, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/298b1fc93e0eb459bcbf3f7f11719e514eb12fb6_720x.jpg?v=1601948568', 100, 'Employing legendary Gum Resins which have been used in perfumery for millennia, Cinnamon, Saffron and Benzoin create a base of unparalleled softness and warmth, where Rose de Mai and Fig dance on top and lend their gentle sweetness. Enveloping fragrance fans in a cloud of olfactive majesty, the popularity of Amber Aoud is not without justification. Top Notes: Bergamot. Heart Notes: Rose de Mai, Jasmin de Grasse, Ylang Ylang, Fig. Base Notes: Cinnamon, Saffron, Patchouli, Oakmoss, Sandalwood, Aoud, Benzoin, Orris, Birch, Ambergris, Musk');
INSERT INTO `Product` VALUES (13, 'Addictive Arts Vision Of A Dream Psychadelic', 'Unisex', 'CLIVE CHRISTIAN', 'Amber', 94900, 75, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/6e29ad81eb87eee83401800ca46c67eeeaa9cef5_720x.jpg?v=1601960243', 100, 'A whirling dream of a perfume, this scent opens with a fresh top note of Kaffir Lime and Armoise, before sliding into the smoky incense accord of Papyrus and Labdanum. Moving through tones of Suede and sweet, spicy Cinnamon, it swirls and settles to a musky base of Sandalwood and Vetiver. 25% Perfume Concentration.');
INSERT INTO `Product` VALUES (14, 'No.1 Masculine', 'Men', 'CLIVE CHRISTIAN', 'Woody', 80900, 50, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/816da02e84d009b2c697abd04e6fa62f56982060_720x.jpg?v=1601963428', 100, 'An Amber that is understated yet distinctive. The base notes of precious 50 year-old Indian sandalwood, powdery musk and vetiver add a rich warmth, enveloping the wearer in a balmy veil of fragrance. Top notes: Sicilian mandarin, pimento, grapefruit, thyme, lime, nutmeg, artemisia, bergamot, cardamom. Heart notes:rose, heliotrope, jasmine, lily of the valley. Base notes: Indian sandalwood, vetiver, musk');
INSERT INTO `Product` VALUES (15, 'Exceptional Extraits Epic Woman 56', 'Women', 'AMOUAGE', 'Floral', 75000, 100, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/ff_36c9f90a-8b55-4041-8d0d-b5cdbcc85470_720x.png?v=1634856752', 100, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/ff_36c9f90a-8b55-4041-8d0d-b5cdbcc85470_720x.png?v=1634856752');
INSERT INTO `Product` VALUES (16, 'Royales Exclusives - White Flowers', 'Women', 'Creed', 'Floral', 67900, 75, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/WhiteFlowers_720x.jpg?v=1632968719', 100, 'A house in the clouds, a spiritual abode away from earth’s cares, an afterlife paradise of flowers, fruit and spices and a vision of a world beyond our own inspired sixth generation master perfumer Olivier Creed to create White Flowers. Serene and composed, White Flowers is a voyage into spirit and dream. White Flowers is an entrée to a new realm where flower petals sigh underfoot and worldly concerns dissolve in a fragrant mist. Top notes: Parma violet leaves, green apple and lemon from Calabria. Heart notes: Italian and Moroccan jasmine, light geranium, Bulgarian rose. Base notes: Musk, Indian sandalwood and narcissus');
INSERT INTO `Product` VALUES (17, 'Rose Incense', 'Women', 'AMOUAGE', 'Floral', 56500, 100, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/f7567e3c479cb115d181a534b90bf036a29910ec_720x.jpg?v=1615951131', 100, 'Rose Incense is distinctively floral and unmistakably woody with unique and contemporary elements, an Eau De Parfum at a concentration of 25% Fragrance oil. With Rose at its heart along with Myrrh and Frankincense at its base, the fragrance evokes a complicated tale of epic proportion. The fresh, clean and citrusy undertones of its top note Elemi, bring the fragrance together with serenity. Top Notes: Elemi, Olibanum (Frankincense) Hyper Absolute, Black Ink Accord. Heart Notes: Damascena Rose Water Essential, Suederal, Frankincense Absolute. Base Notes: Myrrh, Vanilla, Sandalwood, Cedarwood');
INSERT INTO `Product` VALUES (18, 'Not a Perfume', 'Unisex', 'JULIETTE HAS A GUN', 'Woody', 15900, 50, 'https://cdn.shopify.com/s/files/1/0267/4501/2408/products/05d1334ac02385a6b6ecb13cba0bc0f5c7e852d6_720x.jpg?v=1601964060', 100, 'A fragrance made out of a single element called Cetalox. Usually used in perfumery as a base note, it plays here the lead role... Another advantage of this particular composition, is that it is entirely allergen free. The result is minimalist, elegant, pure. Main ingredient: cetalox.');

-- ----------------------------
-- Table structure for ProductCart
-- ----------------------------
DROP TABLE IF EXISTS `ProductCart`;
CREATE TABLE `ProductCart`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cart_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `quantity` bigint NOT NULL,
  `deleteStatus` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cartFK`(`cart_id`) USING BTREE,
  INDEX `productIDFK`(`product_id`) USING BTREE,
  CONSTRAINT `cartFK` FOREIGN KEY (`cart_id`) REFERENCES `ShoppingCart` (`cart_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `productIDFK` FOREIGN KEY (`product_id`) REFERENCES `Product` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ProductCart
-- ----------------------------
INSERT INTO `ProductCart` VALUES (1, 1, 1, 2, 1);
INSERT INTO `ProductCart` VALUES (2, 1, 2, 2, 0);
INSERT INTO `ProductCart` VALUES (3, 5, 2, 5, 0);

-- ----------------------------
-- Table structure for Questionaire
-- ----------------------------
DROP TABLE IF EXISTS `Questionaire`;
CREATE TABLE `Questionaire`  (
  `questionireId` bigint NOT NULL AUTO_INCREMENT,
  `userId` bigint NOT NULL,
  `family` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `forWho` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `lowerPrice` bigint NULL DEFAULT NULL,
  `HigherPrice` bigint NULL DEFAULT NULL,
  `brand` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`questionireId`) USING BTREE,
  INDEX `userFK`(`userId`) USING BTREE,
  CONSTRAINT `userFK` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Questionaire
-- ----------------------------
INSERT INTO `Questionaire` VALUES (1, 1, 'Amber', 'her', 100, 5000, 'Gucci');

-- ----------------------------
-- Table structure for Sale
-- ----------------------------
DROP TABLE IF EXISTS `Sale`;
CREATE TABLE `Sale`  (
  `ProductId` bigint NOT NULL,
  `SaleId` bigint NOT NULL AUTO_INCREMENT,
  `SaleNum` bigint NULL DEFAULT 0,
  PRIMARY KEY (`SaleId`) USING BTREE,
  INDEX `ProductFK`(`ProductId`) USING BTREE,
  CONSTRAINT `ProductFK` FOREIGN KEY (`ProductId`) REFERENCES `Product` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of Sale
-- ----------------------------
INSERT INTO `Sale` VALUES (1, 1, 100);
INSERT INTO `Sale` VALUES (2, 2, 500);
INSERT INTO `Sale` VALUES (3, 3, 1000);
INSERT INTO `Sale` VALUES (4, 4, 3213);
INSERT INTO `Sale` VALUES (5, 5, 13123);
INSERT INTO `Sale` VALUES (6, 6, 765);
INSERT INTO `Sale` VALUES (7, 7, 45555);
INSERT INTO `Sale` VALUES (8, 8, 5000);
INSERT INTO `Sale` VALUES (9, 9, 10000);
INSERT INTO `Sale` VALUES (10, 10, 645);
INSERT INTO `Sale` VALUES (11, 11, 5555);
INSERT INTO `Sale` VALUES (12, 12, 35000);
INSERT INTO `Sale` VALUES (13, 13, 25);
INSERT INTO `Sale` VALUES (14, 14, 555);
INSERT INTO `Sale` VALUES (15, 15, 544);
INSERT INTO `Sale` VALUES (16, 16, 55555);
INSERT INTO `Sale` VALUES (17, 17, 444);
INSERT INTO `Sale` VALUES (18, 18, 33);

-- ----------------------------
-- Table structure for ShoppingCart
-- ----------------------------
DROP TABLE IF EXISTS `ShoppingCart`;
CREATE TABLE `ShoppingCart`  (
  `cart_id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`cart_id`) USING BTREE,
  INDEX `UserCartFK`(`user_id`) USING BTREE,
  CONSTRAINT `UserCartFK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ShoppingCart
-- ----------------------------
INSERT INTO `ShoppingCart` VALUES (1, 1);
INSERT INTO `ShoppingCart` VALUES (5, 2);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `password` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `role` int NULL DEFAULT NULL COMMENT '0:super-admin 1.admin 2user',
  `email` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `User_id_uindex`(`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'super_admin', 'e10adc3949ba59abbe56e057f20f883e', 0, 'super-admin@gmail.com', '+6112345678', 'Sydney NSW 2052, Australia');
INSERT INTO `user` VALUES (2, 'test_admin', 'e10adc3949ba59abbe56e057f20f883e', 1, 'admin@gmail.com', NULL, NULL);
INSERT INTO `user` VALUES (3, 'test', 'e10adc3949ba59abbe56e057f20f883e', 2, NULL, '+8612345678', 'Tiananmen, Beijing');

SET FOREIGN_KEY_CHECKS = 1;
