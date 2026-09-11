# Weather API

A [Flask](https://flask.palletsprojects.com/) weather API with a React (CDN, no build step) frontend. Fetches forecasts from the [Visual Crossing](https://www.visualcrossing.com/weather-api) API, resolves the country from coordinates via [Nominatim](https://nominatim.org/), and caches responses in Redis for 24 hours.

## Features

- `GET /weather?city=<city>&days=<1-15>` — temperature (converted °F → °C), humidity, wind, precipitation, UV index, pressure, visibility and conditions per day
- Redis caching (24h TTL) per `city + date` — falls back transparently to uncached requests if Redis isn't running
- Serves a single-file React frontend at `/`
- Input validation (`days` between 1 and 15) and JSON error responses

## Tech stack

- **Backend:** Flask, Flask-CORS, Redis, Requests, geopy
- **Frontend:** React 18 + Tailwind CSS, loaded from CDN in [`weather-app(AI gen.).html`](<weather-app(AI gen.).html>) — no build step needed

## Requirements

- Python 3.10+
- A [Visual Crossing](https://www.visualcrossing.com/weather-api) API key (free tier: 500 requests/day)
- Redis (optional — the app works without it, just without caching)

## Installation

```bash
git clone https://github.com/skyvva1k3r/weatherAPI.git
cd weatherAPI
pip install flask flask-cors redis requests python-dotenv geopy
```

## Configuration

Create a `.env` file in the project root:

```
API_KEY=your_visual_crossing_api_key
```

## Running

```bash
python main.py
```

Starts on `http://localhost:5000`. Open [`weather-app(AI gen.).html`](<weather-app(AI gen.).html>) in a browser — the backend must be running for it to fetch data.

## API

### `GET /weather`

| Param | Required | Notes |
|---|---|---|
| `city` | yes | city name |
| `days` | no | 1–15, default 7 |

```bash
curl "http://localhost:5000/weather?city=Vienna&days=7"
```

```json
{
  "status": "success",
  "city": "vienna",
  "country": "at",
  "days": 7,
  "data": [
    { "datetime": "2026-09-11", "tempmax": 15.5, "tempmin": 8.3, "conditions": "Partly cloudy", "...": "..." }
  ]
}
```

Errors: `400` invalid params, `404` city not found.

## License

[MIT](LICENSE)

---

# Weather API (Русский)

Погодное API на [Flask](https://flask.palletsprojects.com/) с React-фронтендом (через CDN, без сборки). Прогноз берётся из [Visual Crossing](https://www.visualcrossing.com/weather-api), страна определяется по координатам через [Nominatim](https://nominatim.org/), ответы кэшируются в Redis на 24 часа.

## Возможности

- `GET /weather?city=<город>&days=<1-15>` — температура (конвертация °F → °C), влажность, ветер, осадки, УФ-индекс, давление, видимость и описание погоды по дням
- Кэширование в Redis (TTL 24ч) по ключу `город + дата` — при недоступном Redis приложение прозрачно работает без кэша
- Отдаёт одностраничный React-фронтенд на `/`
- Валидация параметров (`days` от 1 до 15) и JSON-ошибки

## Стек

- **Backend:** Flask, Flask-CORS, Redis, Requests, geopy
- **Frontend:** React 18 + Tailwind CSS, подключаются через CDN в [`weather-app(AI gen.).html`](<weather-app(AI gen.).html>) — сборка не нужна

## Требования

- Python 3.10+
- API-ключ [Visual Crossing](https://www.visualcrossing.com/weather-api) (бесплатный план: 500 запросов/день)
- Redis (опционально — приложение работает и без него, просто без кэша)

## Установка

```bash
git clone https://github.com/skyvva1k3r/weatherAPI.git
cd weatherAPI
pip install flask flask-cors redis requests python-dotenv geopy
```

## Настройка

Создайте файл `.env` в корне проекта:

```
API_KEY=ваш_ключ_visual_crossing
```

## Запуск

```bash
python main.py
```

Стартует на `http://localhost:5000`. Откройте [`weather-app(AI gen.).html`](<weather-app(AI gen.).html>) в браузере — для получения данных backend должен быть запущен.

## Ошибки

`400` — некорректные параметры, `404` — город не найден.

## Лицензия

[MIT](LICENSE)
