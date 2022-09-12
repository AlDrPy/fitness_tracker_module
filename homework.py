'''Модуль фитнес-трекера. Собирает информацию с датчиков, определяет тип
   тренировки (плавание, бег, спортивная ходьба) и выводит сообщение о 
   её результатах, с расчетом показателей.'''

from typing import Callable



class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance : float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        msg = (f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')
        return (msg.format(self.training_type, self.duration,
                self.distance, self.speed, self.calories))

class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HR: int = 60
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.len_step = Training.LEN_STEP

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.len_step / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, 
                          self.duration,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) 
                * self.weight / Training.M_IN_KM * self.duration * Training.MIN_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                height: float,
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        return ((coeff_calorie_1 * self.weight + (self.get_mean_speed()**2
                // self.height) * coeff_calorie_2 * self.weight) 
                * self.duration * Training.MIN_IN_HR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                length_pool: int,
                count_pool: int,
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.len_step = Swimming.LEN_STEP

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool 
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        return ((self.get_mean_speed() + coeff_calorie_1) 
                * coeff_calorie_2 * self.weight) 


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dic = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking
    }
    return dic[workout_type](*data)

def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)


