# QuizKn0ck

## 起動方法
1. リポジトリをクローンする
```bash
git clone https://github.com/tochiman/Quizsalad.git
```
2. 環境変数の設定
- frontフォルダの中(.env)
```env
NEXTAUTH_URL='http://localhost:3000'
NEXTAUTH_SECRET='<ランダムな値>'
API_FRONT='http://localhost:8080'
API_BACK='http://api:8080'
```
- dbフォルダの中(.env_sql)
```env
MYSQL_DATABASE=Quizsalad
MYSQL_USER=<好きなもの>
MYSQL_PASSWORD=<好きなもの>
MYSQL_ROOT_PASSWORD=<好きなもの>
```
3. frontコンテナのセットアップ(初回起動のみ実行)
```bash
docker compose run --rm front sh -c "yarn install"
```
4. コンテナの起動
```bash
docker compose up -d
```
