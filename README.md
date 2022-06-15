# NTUWS_weighting
## 台大動態民意調查加權程式(限性別、年齡、教育、地區)

### 使用說明
#### 需要套件
1. pandas
2. numpy
3. scipy
4. os

#### 執行前準備
1. 將欲加權之檔案放入與此package相同的資料夾
2. 加權變項須依以下規則編碼(注意大小寫):
    a. 性別: 變數名稱SEX, 值為女:0, 男:1
    b. 年齡: 變數名稱AGE, 值為20-29: 1, 30-39: 2, 40-49: 3, 50-59: 4, 60up: 5
    c. 教育: 變數名稱EDU, 值為小學及以下: 1, 國、初中: 2, 高中、職: 3, 大專: 4, 研究所及以上: 5
    d. 地區: 變數名稱AREA, 值為北北基: 1, 桃竹苗: 2, 中彰投: 3, 雲嘉南: 4, 高屏: 5, 宜花東及離島: 6
3. 修改population.xlsx檔中母體比例(ratio欄位):
    a. sheet SAA: 性別年齡地區分層，ratio欄位為母體比例
    b. sheet SEX, AGE, EDU, AREA同上
4. 加權變項遺漏值請預先coding為-1

### 執行說明
1. 打開main.py
2. 修改rawdata路徑
```
rawdata_path = 檔案路徑
```
3. 事後分層加權執行以下程式碼:
```
### Post-stratification
output_path = 輸出檔案資料夾，預設為此package
output_name = 輸出檔案名稱.csv

df = weighting(df, population_path='population.xlsx').post_stratification()
df.to_csv(os.path.join(output_path, output_name), encoding='utf_8_sig', index=False)
```
4. 多變項反覆加權執行以下程式碼
```
### Raking
output_path = 輸出檔案資料夾，預設為此package
output_name = 輸出檔案名稱.csv

df = weighting(df, population_path='population.xlsx').raking()
df.to_csv(os.path.join(output_path, output_name), encoding='utf_8_sig', index=False)
```