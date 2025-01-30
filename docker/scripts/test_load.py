import requests
import pandas as pd
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

victoria_metrics_url = "http://localhost:8428/api/v1/import"

csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgwB47qVFZcr1Aq--UWxZ6fDi9CGLZm-1i8QoMgfdaHUbV8EqSli3ayPxYYxD8kqfYYHD41uuNxbjZ/pub?gid=1952392108&single=true&output=csv"
logger.info("Загружаем CSV-файл...")
try:
    df = pd.read_csv(csv_url)
    logger.info("CSV-файл успешно загружен")
except Exception as e:
    logger.error(f"Ошибка загрузки CSV: {e}")
    exit(1)

logger.info("Преобразуем timestamp...")
try:
    df['timestamp'] = pd.to_datetime(df['Datetime']).astype(int) // 10**9
    logger.info("Timestamp преобразован")
except Exception as e:
    logger.error(f"Ошибка преобразования timestamp: {e}")
    exit(1)

metrics_columns = ["Temperature", "Humidity", "WindSpeed", "GeneralDiffuseFlows", "DiffuseFlows", "consumption"]
city_zone = "Morocco Zone 1"

metrics_data = []
try:
    for _, row in tqdm(df.iterrows(), total=len(df)):
        for col in metrics_columns:
            metrics_data.append({
                "metric": {"__name__": col, "dataset": "test_data", "city_zone": city_zone},
                "values": [row[col]],
                "timestamps": [row["timestamp"]]
            })
    logger.info("Данные сформированы")
except Exception as e:
    logger.error(f"Ошибка формирования данных: {e}")
    exit(1)

data = str(metrics_data)
logger.info(f"Отправляем данные в VictoriaMetrics ({len(metrics_data)} записей)...")
try:
    response = requests.post(victoria_metrics_url, json=metrics_data)
    if response.status_code == 204:
        logger.info("Данные успешно загружены")
    else:
        logger.error("Ошибка при загрузке данных")
        logger.error(f"Код ответа: {response.status_code}")
        logger.error(f"Заголовки ответа: {response.headers}")
        logger.error(f"Тело ответа: {response.text}")
        logger.error(f"Отправленные данные (первые 500 символов): {data[:500]}")
except requests.RequestException as e:
    logger.error(f"Ошибка запроса: {e}")
