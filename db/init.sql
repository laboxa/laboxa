-- ユーザーテーブルの作成
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS attendance_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(50) NOT NULL,
  type ENUM('checkin', 'checkout'),
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 職場のメンバーを事前登録
INSERT INTO users (name) VALUES
('田中太郎'),
('佐藤花子'),
('鈴木一郎'),
('山田美咲'),
('高橋健太'),
('渡辺真由美'),
('okayu'),
('kazuyaIKEUCHI');

-- サンプルデータを挿入
INSERT INTO attendance_logs (user_name, type, timestamp) VALUES
('田中太郎', 'checkin', '2025-06-10 09:00:00'),
('田中太郎', 'checkout', '2025-06-10 18:00:00'),
('佐藤花子', 'checkin', '2025-06-10 09:15:00'),
('佐藤花子', 'checkout', '2025-06-10 17:45:00'),
('鈴木一郎', 'checkin', '2025-06-10 08:45:00'),
('山田美咲', 'checkin', '2025-06-10 09:30:00'),
('山田美咲', 'checkout', '2025-06-10 18:15:00');