/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80031
 Source Host           : localhost:3306
 Source Schema         : diease

 Target Server Type    : MySQL
 Target Server Version : 80031
 File Encoding         : 65001

 Date: 06/05/2026 10:38:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_record
-- ----------------------------
DROP TABLE IF EXISTS `tb_record`;
CREATE TABLE `tb_record`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键ID',
  `UserId` int NULL DEFAULT NULL COMMENT '用户ID',
  `OriginMapUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '原图路径',
  `HeatmapUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '热力图路径',
  `Confidence` float NULL DEFAULT NULL COMMENT '置信度',
  `DieaseType` int NULL DEFAULT NULL COMMENT '病害索引',
  `DieaseName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '病害名称',
  `CreateTime` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_record
-- ----------------------------
INSERT INTO `tb_record` VALUES (7, 1, '/uploads/origin/origin_c5a6b11d-2e98-4012-b892-176f157ec87f.png', '/uploads/heatmap/heatmap_3131f484-0df7-44cc-9c2a-cc59a4284af7.png', 0.4768, 2, 'Rust', '2026-05-05 22:02:25');

-- ----------------------------
-- Table structure for tb_user
-- ----------------------------
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID（自增主键）',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `IsAdmin` int NOT NULL DEFAULT 0 COMMENT '是否管理员：1-管理员，0-普通用户',
  `IsBanned` int NOT NULL DEFAULT 0 COMMENT '是否被封禁：1-封禁，0-正常',
  `update_time` timestamp NULL DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_phone`(`phone`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_user
-- ----------------------------
INSERT INTO `tb_user` VALUES (1, '13471273310', '123456', 1, 0, '2026-05-06 09:39:00', '2026-05-06 09:39:00');
INSERT INTO `tb_user` VALUES (2, '15977988540', '123456', 0, 0, '2026-05-06 09:39:00', '2026-05-06 09:39:00');
INSERT INTO `tb_user` VALUES (3, '17620363310', '123456', 0, 0, '2026-05-06 09:39:00', '2026-05-06 09:39:00');

SET FOREIGN_KEY_CHECKS = 1;
