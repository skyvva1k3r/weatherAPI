import React, { useState } from 'react';
import { Cloud, CloudRain, Sun, Wind, Droplets, Eye, Gauge, AlertCircle } from 'lucide-react';

const WeatherApp = () => {
  const [city, setCity] = useState('');
  const [days, setDays] = useState(7);
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Функция для получения иконки погоды
  const getWeatherIcon = (icon) => {
    const iconMap = {
      'clear-day': '☀️',
      'clear-night': '🌙',
      'cloudy': '☁️',
      'partly-cloudy-day': '⛅',
      'partly-cloudy-night': '☁️',
      'rain': '🌧️',
      'snow': '❄️',
      'wind': '💨',
      'fog': '🌫️'
    };
    return iconMap[icon] || '🌤️';
  };

  // Получение данных с бэкенда
  const fetchWeather = async () => {
    if (!city.trim()) {
      setError('Введите название города');
      return;
    }

    setLoading(true);
    setError(null);
    setWeatherData(null);

    try {
      const response = await fetch(
        `http://localhost:5000/weather?city=${encodeURIComponent(city)}&days=${days}`
      );
      
      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Ошибка при получении данных');
        return;
      }

      setWeatherData(data);
    } catch (err) {
      setError('Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен.');
    } finally {
      setLoading(false);
    }
  };

  // Обработчик нажатия Enter
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      fetchWeather();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Заголовок */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-5xl font-bold text-white mb-2">☀️ Прогноз погоды</h1>
          <p className="text-blue-100">Узнайте погоду в любом городе мира</p>
        </div>

        {/* Панель поиска */}
        <div className="bg-white rounded-2xl shadow-2xl p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Город
              </label>
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Например: Vienna, Tokyo, Moscow"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              />
            </div>

            <div className="md:w-40">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Дней
              </label>
              <select
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              >
                {[...Array(15)].map((_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {i + 1}
                  </option>
                ))}
              </select>
            </div>

            <div className="md:self-end">
              <button
                onClick={fetchWeather}
                disabled={loading}
                className="w-full md:w-auto px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition shadow-lg hover:shadow-xl"
              >
                {loading ? 'Загрузка...' : 'Найти'}
              </button>
            </div>
          </div>
        </div>

        {/* Ошибка */}
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6 flex items-start">
            <AlertCircle className="mr-3 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <p className="font-semibold">Ошибка</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Данные о погоде */}
        {weatherData && (
          <div>
            {/* Заголовок с информацией о городе */}
            <div className="bg-white rounded-2xl shadow-2xl p-6 mb-6">
              <h2 className="text-3xl font-bold text-gray-800 capitalize">
                {weatherData.city}
              </h2>
              <p className="text-gray-600">
                Прогноз на {weatherData.days} {weatherData.days === 1 ? 'день' : 'дней'}
              </p>
            </div>

            {/* Карточки прогноза */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {weatherData.data.map((day, index) => (
                <div
                  key={index}
                  className="bg-white rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-shadow"
                >
                  {/* Дата и иконка */}
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <p className="text-sm text-gray-500">
                        {new Date(day.datetime).toLocaleDateString('ru-RU', {
                          weekday: 'short',
                          day: 'numeric',
                          month: 'short'
                        })}
                      </p>
                      <p className="text-xs text-gray-400">{day.datetime}</p>
                    </div>
                    <div className="text-5xl">
                      {getWeatherIcon(day.icon)}
                    </div>
                  </div>

                  {/* Условия */}
                  <p className="text-gray-700 font-medium mb-4">
                    {day.conditions}
                  </p>

                  {/* Температура */}
                  <div className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-4xl font-bold text-gray-800">
                        {day.tempmax}°
                      </span>
                      <span className="text-2xl text-gray-500">
                        {day.tempmin}°
                      </span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <span>Ощущается как {day.feelslike}°</span>
                    </div>
                  </div>

                  {/* Дополнительная информация */}
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div className="flex items-center text-gray-600">
                      <Droplets size={16} className="mr-2 text-blue-500" />
                      <div>
                        <p className="text-xs text-gray-500">Влажность</p>
                        <p className="font-semibold">{day.humidity}%</p>
                      </div>
                    </div>

                    <div className="flex items-center text-gray-600">
                      <Wind size={16} className="mr-2 text-blue-500" />
                      <div>
                        <p className="text-xs text-gray-500">Ветер</p>
                        <p className="font-semibold">{day.windspeed} км/ч</p>
                      </div>
                    </div>

                    <div className="flex items-center text-gray-600">
                      <CloudRain size={16} className="mr-2 text-blue-500" />
                      <div>
                        <p className="text-xs text-gray-500">Осадки</p>
                        <p className="font-semibold">{day.precipprob}%</p>
                      </div>
                    </div>

                    <div className="flex items-center text-gray-600">
                      <Eye size={16} className="mr-2 text-blue-500" />
                      <div>
                        <p className="text-xs text-gray-500">Видимость</p>
                        <p className="font-semibold">{day.visibility} км</p>
                      </div>
                    </div>

                    <div className="flex items-center text-gray-600">
                      <Gauge size={16} className="mr-2 text-blue-500" />
                      <div>
                        <p className="text-xs text-gray-500">Давление</p>
                        <p className="font-semibold">{day.pressure} мб</p>
                      </div>
                    </div>

                    <div className="flex items-center text-gray-600">
                      <Sun size={16} className="mr-2 text-orange-500" />
                      <div>
                        <p className="text-xs text-gray-500">УФ индекс</p>
                        <p className="font-semibold">{day.uvindex}</p>
                      </div>
                    </div>
                  </div>

                  {/* Количество осадков */}
                  {day.precip > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-xs text-gray-600">
                        Осадки: {day.precip} мм
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Пустое состояние */}
        {!weatherData && !loading && !error && (
          <div className="bg-white rounded-2xl shadow-2xl p-12 text-center">
            <div className="text-6xl mb-4">🌍</div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              Начните поиск
            </h3>
            <p className="text-gray-600">
              Введите название города и нажмите "Найти"
            </p>
          </div>
        )}
      </div>

      {/* Футер */}
      <div className="text-center mt-12 pb-8">
        <p className="text-white text-sm">
          Данные предоставлены Visual Crossing Weather API
        </p>
      </div>
    </div>
  );
};

export default WeatherApp;
