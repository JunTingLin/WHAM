# WHAM

> 本專案 Fork 自 [yohanshin/WHAM](https://github.com/yohanshin/WHAM)

從影片自動偵測人體骨架，輸出 SMPL 格式的骨架序列。

## 快速開始

### 1. 下載必要資料

需要先註冊帳號：
- https://smpl.is.tue.mpg.de
- https://smplify.is.tue.mpg.de

```bash
cd WHAM
bash fetch_demo_data.sh
```

### 2. 建立 Docker image

```bash
docker build -f Dockerfile.custom -t wham-pytorch3d .
```

## 使用方式

### 單一影片

```bash
cd WHAM

docker run --gpus all \
  -v $(pwd):/code/ \
  -v /你的影片目錄:/videos \
  --rm wham-pytorch3d \
  bash -c "python demo.py --video /videos/影片.MOV --save_pkl --visualize && python convert_pkl.py /code/output/demo/影片/wham_output.pkl"
```

### 批次處理多個影片

```bash
cd WHAM

for v in IMG_2234 IMG_2235 IMG_2236; do
  echo "Processing $v.MOV ..."
  docker run --gpus all \
    -v $(pwd):/code/ \
    -v /你的影片目錄:/videos \
    --rm wham-pytorch3d \
    bash -c "python demo.py --video /videos/$v.MOV --save_pkl --visualize && python convert_pkl.py /code/output/demo/$v/wham_output.pkl"
done
```

## 參數說明

| 參數 | 說明 |
|------|------|
| `--video` | 輸入影片路徑 |
| `--save_pkl` | 儲存 SMPL 參數為 pkl 檔 |
| `--visualize` | 輸出視覺化影片 |
| `--estimate_local_only` | 只估計相機座標系（跳過 SLAM，適合固定相機）|
| `--calib` | 提供相機內參檔案 |

## 輸出檔案

```
output/demo/影片名稱/
├── wham_output.pkl        # SMPL 參數（Python 3.9）
├── wham_output_py37.pkl   # SMPL 參數（Python 3.7 相容）
├── tracking_results.pth   # 追蹤結果
├── slam_results.pth       # SLAM 結果
└── *.mp4                  # 視覺化影片
```

### wham_output.pkl 內容

| 欄位 | 說明 |
|------|------|
| `pose` | SMPL pose 參數 (72 維)，相機座標系 |
| `pose_world` | SMPL pose 參數，世界座標系 |
| `betas` | SMPL shape 參數（體型）|
| `trans` | 位移（相機座標系）|
| `trans_world` | 位移（世界座標系）|
| `verts` | SMPL mesh 頂點 |
| `frame_ids` | 對應的影格編號 |

## 關於 convert_pkl.py

因為 Docker 環境是 Python 3.9，而 [motion-diffusion-model](https://github.com/JunTingLin/motion-diffusion-model) 使用 Python 3.7，兩者的 pkl 序列化格式不相容。

`convert_pkl.py` 會將 `wham_output.pkl` 轉換為 `wham_output_py37.pkl`（使用 pickle protocol 2），讓 MDM 環境可以正常讀取。
