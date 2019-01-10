/*
 Navicat MySQL Data Transfer

 Source Server         : InterfaceTest
 Source Server Type    : MySQL
 Source Server Version : 80012
 Source Host           : localhost:3306
 Source Schema         : interface_autotester

 Target Server Type    : MySQL
 Target Server Version : 80012
 File Encoding         : 65001

 Date: 29/11/2018 17:54:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for interface_api
-- ----------------------------
DROP TABLE IF EXISTS `interface_api`;
CREATE TABLE `interface_api`  (
  `api_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增长主键',
  `api_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '接口的名字',
  `file_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '接口对应的测试脚本名字',
  `r_url` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '请求接口的URL',
  `r_method` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '接口请求方式',
  `p_type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '传参方式',
  `rely_db` tinyint(4) NULL DEFAULT 0 COMMENT '是否依赖数据库',
  `status` tinyint(4) NULL DEFAULT 0,
  `ctime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`api_id`) USING BTREE,
  UNIQUE INDEX `api_name`(`api_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of interface_api
-- ----------------------------
INSERT INTO `interface_api` VALUES (1, '用户注册', 'user_registration', 'http://39.106.41.11:8080/register/', 'post', 'data', 1, 1, '2018-11-29 15:39:44');
INSERT INTO `interface_api` VALUES (2, '用户登录', 'users_login', 'http://39.106.41.11:8080/login/', 'post', 'data', 1, 1, '2018-11-29 15:39:44');
INSERT INTO `interface_api` VALUES (3, '查询博文', 'get_blog', 'http://39.106.41.11:8080/getBlogContent/', 'get', 'url', 0, 1, '2018-11-29 16:55:16');

-- ----------------------------
-- Table structure for interface_data_store
-- ----------------------------
DROP TABLE IF EXISTS `interface_data_store`;
CREATE TABLE `interface_data_store`  (
  `api_id` int(11) NOT NULL COMMENT '对应interface_api的api_id',
  `case_id` int(11) NOT NULL COMMENT '对应interface_test_case里面的id',
  `data_store` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '存储的依赖数据',
  `ctime` datetime(0) NULL DEFAULT NULL,
  INDEX `api_id`(`api_id`, `case_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of interface_data_store
-- ----------------------------
INSERT INTO `interface_data_store` VALUES (1, 1, '{\"username\":\"srwcx01\",\"password\":\"d85fb67e312ed3a589951720a6f3b079\"}', '2018-11-29 17:40:00');
INSERT INTO `interface_data_store` VALUES (2, 2, '{\'token\': u\'e2b2d93dfca68c45b9e396ac028adb24\', u\'userid\': 55066}', '2018-11-29 17:41:05');

-- ----------------------------
-- Table structure for interface_test_case
-- ----------------------------
DROP TABLE IF EXISTS `interface_test_case`;
CREATE TABLE `interface_test_case`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增长主键',
  `api_id` int(11) NOT NULL COMMENT '对应interface_api的api_id',
  `r_data` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '请求接口时传的参数',
  `rely_data` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用例依赖的数据',
  `res_code` int(11) NULL DEFAULT NULL COMMENT '接口期望响应code',
  `res_data` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接口响应body',
  `data_store` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '依赖数据存储',
  `check_point` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接口响应校验依据数据',
  `status` tinyint(4) NULL DEFAULT 0 COMMENT '用例执行状态，0不执行，1执行',
  `ctime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `api_id`(`api_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of interface_test_case
-- ----------------------------
INSERT INTO `interface_test_case` VALUES (1, 1, '{\"username\":\"srsdcx01\",\"password\":\"wcx123wac1\",\"email\":\"wcx@qq.com\"}', '', 200, NULL, '{\"request\":[\"username\",\"password\"],\"response\":[\"code\"]}', '{\"code\":\"00\"}', 1, '2018-11-29 15:39:44');
INSERT INTO `interface_test_case` VALUES (2, 2, '{\'username\': \'wcx\', \'password\': \'wcx123wac\'}', '{\"1->1\":[\"username\",\"password\"]}', 200, NULL, '{\"response\":[\"userid\", \"token\"]}', '{\"code\": \"00\",\"username\":{\"R\":\"[a-zA-Z]+\"}}', 1, '2018-11-29 15:39:44');
INSERT INTO `interface_test_case` VALUES (3, 3, '1', NULL, 200, NULL, NULL, NULL, 0, NULL);
INSERT INTO `interface_test_case` VALUES (4, 1, '{\"username\":\"srwcx2201\",\"password\":\"wcx123wac1\",\"email\":\"wcx@qq.com\"}', NULL, NULL, NULL, NULL, NULL, 0, NULL);

SET FOREIGN_KEY_CHECKS = 1;
